import os
import os.path
import re
import shutil
import subprocess

def copy_contents(src, dst):
    os.makedirs(dst, exist_ok=True)

    for entry in os.listdir(src):
        full = os.path.join(src, entry)
        if os.path.isdir(full):
            copy_contents(full, os.path.join(dst, entry))
        else:
            shutil.copy2(full, os.path.join(dst, entry))

def chown_contents(path, uid, gid):
    for entry in os.listdir(path):
        full = os.path.join(path, entry)
        if os.path.isdir(full):
            chown_contents(full, uid, gid)
        else:
            os.chown(full, uid, gid)

def copy_libs(exe, dst):
    os.makedirs(dst, exist_ok=True)

    libraries = {}
    for line in subprocess.check_output(['ldd', exe]).splitlines():
        match = re.match('\t(.*) => (.*) \(0x|\t(.*) \(0x', line.decode())
        if match:
            if match.group(1) and match.group(2):
                libraries[match.group(1)] = match.group(2)
            elif match.group(3):
                libraries[os.path.basename(match.group(3))] = match.group(3)

    for library, path in libraries.items():
        shutil.copy2(path, os.path.join(dst, library))
