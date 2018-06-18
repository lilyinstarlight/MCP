import datetime
import os
import os.path
import shutil

import fooster.cron

import mcp.config

import mcp.model.server

scheduler = None

def rotate_log(prefix, filename):
    if os.path.getsize(os.path.join(prefix, filename)) > mcp.config.maxlogsize*1024:
        shutil.copy(os.path.join(prefix, filename), os.path.join(prefix, 'log', datetime.datetime.now().strftime('%Y-%m-%d_%H-%M') + '.' + filename))
        with open(os.path.join(prefix, filename), 'w') as file:
            pass

def rotate():
    for entry in mcp.model.server.items():
        rotate_log(os.path.join(mcp.config.prefix, entry.server), 'server.log')
        rotate_log(os.path.join(mcp.config.prefix, entry.server), 'error.log')
        rotate_log(os.path.join(mcp.config.prefix, entry.server), 'script-error.log')

def start():
    global scheduler

    if scheduler:
        return

    scheduler = fooster.cron.Scheduler()
    scheduler.add(fooster.cron.Job(rotate, minute=0))
    scheduler.start()

def stop():
    global scheduler

    if not scheduler:
        return

    scheduler.stop()
    scheduler = None
