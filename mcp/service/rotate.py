import datetime
import os
import shutil

import fooster.cron

import mcp.config

import mcp.model.server

scheduler = None

def rotate_log(prefix, filename):
    if os.path.getsize(filename) > mcp.config.maxlogsize*1024:
        shutil.copy(prefix + '/' + filename, prefix + '/log/' + datetime.strftime('%Y-%m-%d_%H-%M') + '.' + filename)
        with open(filename, 'w') as file:
            pass

def rotate():
    for entry in mcp.model.server.items():
        rotate_log(mcp.config.prefix + '/' + entry.server, 'server.log')
        rotate_log(mcp.config.prefix + '/' + entry.server, 'error.log')
        rotate_log(mcp.config.prefix + '/' + entry.server, 'script-error.log')

def start():
    global scheduler

    scheduler = fooster.cron.Scheduler()
    scheduler.add(fooster.cron.Job(rotate, minute=0))
    scheduler.start()

def stop():
    global scheduler

    scheduler.stop()
    scheduler = None
