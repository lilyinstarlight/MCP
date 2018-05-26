import os
import os.path
import shutil

def copy_contents(src, dst):
    os.makedirs(dst, exist_ok=True)

    for entry in os.listdir(src):
        full = src + '/' + entry
        if os.path.isdir(full):
            copy_contents(full, dst + '/' + entry)
        else:
            shutil.copy2(full, dst + '/' + entry)

def chown_contents(path, uid, gid):
    for entry in os.listdir(path):
        full = path + '/' + entry
        if os.path.isdir(full):
            chown_contents(full, uid, gid)
        else:
            os.chown(full, uid, gid)
