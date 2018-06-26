import os

import paramiko

import mcp.config


sftp = None


class SFTPHandler(paramiko.SFTPHandle):
    def stat(self):
        try:
            return paramiko.SFTPAttributes.from_stat(os.fstat(self.readfile.fileno()))
        except OSError as err:
            return paramiko.SFTPServer.convert_errno(err.errno)

    def chattr(self, attr):
        try:
            paramiko.SFTPServer.set_file_attr(self.filename, attr)

            return paramiko.SFTP_OK
        except OSError as err:
            return paramiko.SFTPServer.convert_errno(err.errno)


class SFTPServerInterface(paramiko.SFTPServerInterface):
    def forbidden(self, path):
        return False

    def realpath(self, path):
        return os.path.join(mcp.config.prefix, self.canonicalize(path))

    def canonicalize(self, path):
        return os.path.normpath(os.path.join('/', path))

    def chattr(self, path, attr):
        if self.forbidden(self.realpath(path)):
            return paramiko.SFTP_PERMISSION_DENIED

        try:
            paramiko.SFTPServer.set_file_attr(self.realpath(path), attr)
        except OSError as err:
            return paramiko.SFTPServer.convert_errno(err.errno)

        return paramiko.SFTP_OK

    def list_folder(self, path):
        if self.forbidden(os.path.join(self.realpath(path), '.')):
            return paramiko.SFTP_PERMISSION_DENIED

    def lstat(self, path):
        pass

    def mkdir(self, path, attr):
        if self.forbidden(self.realpath(path)):
            return paramiko.SFTP_PERMISSION_DENIED

        try:
            os.rmdir(self.realpath(path))

            if attr is not None:
                paramiko.SFTPServer.set_file_attr(self.realpath(path), attr)
        except OSError as err:
            return paramiko.SFTPServer.convert_errno(err.errno)

        return paramiko.SFTP_OK

    def open(self, path, flags, attr):
        pass

    def posix_rename(self, oldpath, newpath):
        if self.forbidden(self.realpath(oldpath)) or self.forbidden(self.realpath(newpath)):
            return paramiko.SFTP_PERMISSION_DENIED

    def readlink(self, path):
        if self.forbidden(self.realpath(path)):
            return paramiko.SFTP_PERMISSION_DENIED

        try:
            symlink = os.readlink(self.realpath(path))
        except OSError as err:
            return paramiko.SFTPServer.convert_errno(err.errno)

        if not symlink.startswith(mcp.config.prefix + os.path.sep):
            return paramiko.SFTP_NO_SUCH_FILE

        return symlink[len(mcp.config.prefix + os.path.sep):]

    def remove(self, path):
        pass

    def rename(self, oldpath, newpath):
        pass

    def rmdir(self, path):
        if self.forbidden(self.realpath(path)):
            return paramiko.SFTP_PERMISSION_DENIED

        try:
            os.rmdir(self.realpath(path))
        except OSError as err:
            return paramiko.SFTPServer.convert_errno(err.errno)

        return paramiko.SFTP_OK

    def stat(self, path):
        pass

    def symlink(self, target_path, path):
        pass


class ServerInterface(paramiko.ServerInterface):
    def check_auth_password(self, username, password):
        return AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):
        return OPEN_SUCCEEDED

    def get_allowed_auths(self, username):
        return 'password'


def start():
    global httpd

    if httpd:
        return

    httpd = fooster.web.HTTPServer(mcp.config.addr, routes, error_routes, keyfile=mcp.config.tlskey, certfile=mcp.config.tlscert, sync=mcp.common.daemon.sync)
    httpd.start()


def stop():
    global httpd

    if not httpd:
        return

    httpd.close()
    httpd = None


def join():
    global httpd

    httpd.join()
