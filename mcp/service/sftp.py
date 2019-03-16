import multiprocessing
import os
import os.path
import re
import select
import socket

import paramiko

import mcp.config
import mcp.error

import mcp.model.server
import mcp.model.user


# inspired by https://github.com/rspivak/sftpserver/blob/master/src/sftpserver/stub_sftp.py
class SFTPHandle(paramiko.SFTPHandle):
    def stat(self):
        try:
            return paramiko.SFTPAttributes.from_stat(os.fstat(self.readfile.fileno()))
        except OSError as err:
            return paramiko.SFTPServer.convert_errno(err.errno)

    def chattr(self, attr):
        try:
            paramiko.SFTPServer.set_file_attr(self.filename, attr)
        except OSError as err:
            return paramiko.SFTPServer.convert_errno(err.errno)

        return paramiko.SFTP_OK


class SFTPServerInterface(paramiko.SFTPServerInterface):
    def __init__(self, server, *args, **kwargs):
        self.user = server.user

        super().__init__(server, *args, **kwargs)

    def forbidden(self, path, modify=False):
        if path == os.path.join(mcp.config.prefix, ''):
            return modify

        match = re.match('^' + os.path.join(mcp.config.prefix, '') + '(?P<server>' + mcp.model.server.servers_allowed + ')(?:$|/)', path)
        if not match:
            return True

        server = match.group('server')

        if modify and (path == os.path.join(mcp.config.prefix, server) or path == os.path.join(mcp.config.prefix, server, '')):
            return True

        if self.user.admin:
            return False

        return server not in self.user.servers

    def realpath(self, path, readlink=False):
        rpath = os.path.join(mcp.config.prefix, self.canonicalize(path)[1:])

        if readlink:
            while os.path.islink(rpath):
                rpath = os.path.join(mcp.config.prefix, self.canonicalize(os.path.join(os.path.dirname(path), os.readlink(rpath)))[1:])

        return rpath

    def chattr(self, path, attr):
        if self.forbidden(self.realpath(path), True):
            return paramiko.SFTP_PERMISSION_DENIED

        try:
            paramiko.SFTPServer.set_file_attr(self.realpath(path), attr)
        except OSError as err:
            return paramiko.SFTPServer.convert_errno(err.errno)

        return paramiko.SFTP_OK

    def list_folder(self, path):
        if self.forbidden(self.realpath(path, True)):
            return paramiko.SFTP_PERMISSION_DENIED

        try:
            rpath = self.realpath(path, True)

            folder = []

            files = os.listdir(rpath)
            for filename in files:
                if rpath != os.path.join(mcp.config.prefix, '') or self.user.admin or filename in self.user.servers:
                    attr = paramiko.SFTPAttributes.from_stat(os.lstat(os.path.join(rpath, filename)))
                    attr.filename = filename
                    folder.append(attr)

            return folder
        except OSError as err:
            return paramiko.SFTPServer.convert_errno(err.errno)

    def lstat(self, path):
        if self.forbidden(self.realpath(path)):
            return paramiko.SFTP_PERMISSION_DENIED

        try:
            return paramiko.SFTPAttributes.from_stat(os.lstat(self.realpath(path)))
        except OSError as err:
            return paramiko.SFTPServer.convert_errno(err.errno)

    def mkdir(self, path, attr):
        if self.forbidden(self.realpath(path), True):
            return paramiko.SFTP_PERMISSION_DENIED

        try:
            os.mkdir(self.realpath(path))

            if attr is not None:
                paramiko.SFTPServer.set_file_attr(self.realpath(path), attr)
        except OSError as err:
            return paramiko.SFTPServer.convert_errno(err.errno)

        return paramiko.SFTP_OK

    def open(self, path, flags, attr):
        if self.forbidden(self.realpath(path, True), True):
            return paramiko.SFTP_PERMISSION_DENIED

        rpath = self.realpath(path)
        rflags = flags
        rattr = attr

        try:
            binary_flag = getattr(os, 'O_BINARY',  0)
            rflags |= binary_flag

            mode = getattr(attr, 'st_mode', None)

            fd = os.open(rpath, rflags, mode if mode is not None else 0o666)
        except OSError as err:
            return paramiko.SFTPServer.convert_errno(err.errno)

        if flags & os.O_CREAT and rattr is not None:
            rattr._flags &= ~rattr.FLAG_PERMISSIONS

            paramiko.SFTPServer.set_file_attr(rpath, rattr)

        if flags & os.O_WRONLY:
            if flags & os.O_APPEND:
                fstr = 'ab'
            else:
                fstr = 'wb'
        elif flags & os.O_RDWR:
            if flags & os.O_APPEND:
                fstr = 'a+b'
            else:

                fstr = 'r+b'
        else:
            fstr = 'rb'

        try:
            f = os.fdopen(fd, fstr)
        except OSError as err:
            return paramiko.SFTPServer.convert_errno(err.errno)

        fobj = SFTPHandle(rflags)
        fobj.filename = rpath
        fobj.readfile = f
        fobj.writefile = f

        return fobj

    def posix_rename(self, oldpath, newpath):
        if self.forbidden(self.realpath(oldpath), True) or self.forbidden(self.realpath(newpath), True):
            return paramiko.SFTP_PERMISSION_DENIED

        try:
            os.rename(self.realpath(oldpath), self.realpath(newpath))
        except OSError as err:
            return paramiko.SFTPServer.convert_errno(err.errno)

        return paramiko.SFTP_OK

    def readlink(self, path):
        if self.forbidden(self.realpath(path)):
            return paramiko.SFTP_PERMISSION_DENIED

        try:
            symlink = os.readlink(self.realpath(path))
        except OSError as err:
            return paramiko.SFTPServer.convert_errno(err.errno)

        if not symlink.startswith(mcp.config.prefix + os.sep):
            return paramiko.SFTP_NO_SUCH_FILE

        return symlink[len(mcp.config.prefix + os.sep):]

    def remove(self, path):
        if self.forbidden(self.realpath(path), True):
            return paramiko.SFTP_PERMISSION_DENIED

        try:
            os.remove(self.realpath(path))
        except OSError as err:
            return paramiko.SFTPServer.convert_errno(err.errno)

        return paramiko.SFTP_OK

    def rename(self, oldpath, newpath):
        if self.forbidden(self.realpath(oldpath), True) or self.forbidden(self.realpath(newpath), True):
            return paramiko.SFTP_PERMISSION_DENIED

        try:
            os.replace(self.realpath(oldpath), self.realpath(newpath))
        except OSError as err:
            return paramiko.SFTPServer.convert_errno(err.errno)

        return paramiko.SFTP_OK

    def rmdir(self, path):
        if self.forbidden(self.realpath(path), True):
            return paramiko.SFTP_PERMISSION_DENIED

        try:
            os.rmdir(self.realpath(path))
        except OSError as err:
            return paramiko.SFTPServer.convert_errno(err.errno)

        return paramiko.SFTP_OK

    def stat(self, path):
        if self.forbidden(self.realpath(path, True)):
            return paramiko.SFTP_PERMISSION_DENIED

        try:
            return paramiko.SFTPAttributes.from_stat(os.stat(self.realpath(path, True)))
        except OSError as err:
            return paramiko.SFTPServer.convert_errno(err.errno)

    def symlink(self, target_path, path):
        if self.forbidden(self.realpath(path), True):
            return paramiko.SFTP_PERMISSION_DENIED

        rpath = self.realpath(path)

        if len(target_path) > 0 and target_path[0] == '/':
            rtpath = self.realpath(target_path)
        else:
            rtpath = os.path.normpath(target_path)

        try:
            os.symlink(rtpath, rpath)
        except OSError as err:
            return paramiko.SFTPServer.convert_errno(err.errno)

        return paramiko.SFTP_OK


class ServerInterface(paramiko.ServerInterface):
    def check_auth_password(self, username, password):
        try:
            self.user = mcp.model.user.check_user(username, password)
            return paramiko.AUTH_SUCCESSFUL
        except mcp.error.NoUserError:
            return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED

        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def get_allowed_auths(self, username):
        return 'password'


def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    sock.bind(mcp.config.sftpaddr)
    sock.listen()

    while running.value:
        read, _, _ = select.select([sock], [], [], mcp.config.poll_interval)

        if read:
            conn, addr = sock.accept()

            host_key = paramiko.RSAKey.from_private_key_file(mcp.config.sftpkey)

            transport = paramiko.Transport(conn)
            transport.add_server_key(host_key)
            transport.set_subsystem_handler('sftp', paramiko.SFTPServer, SFTPServerInterface)

            server = ServerInterface()
            transport.start_server(server=server)

            channel = transport.accept()


running = multiprocessing.Value('b', False)
process = None


def start():
    global process

    if process:
        return

    running.value = True
    process = multiprocessing.Process(target=run, name='mcp-sftp')
    process.start()

def stop():
    global running, process

    if not process:
        return

    running.value = False
    process.join()
    process = None
