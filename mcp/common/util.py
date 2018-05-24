import os
import os.path
import shutil

def copy_contents(src, dst):
    for entry in os.listdir(src):
        entry = src + '/' + entry
        if os.path.isdir(entry):
            copy_contents(entry, dst + '/' + entry)
        else:
            shutil.copy2(entry, dst + '/' + entry)

def chown_contents(path, uid, gid):
    for entry in os.listdir(path):
        entry = path + '/' + entry
        if os.path.isdir(entry):
            chown_contents(entry, uid, gid)
        else:
            os.chown(entry, uid, gid)
