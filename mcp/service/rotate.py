import datetime
import os
import shutil

import fooster.cron

import mcp.config

import mcp.service.manager

scheduler = None

def rotate_log(prefix, filename):
    if os.path.getsize(filename) > mcp.config.maxlogsize*1024:
        shutil.copy(prefix + '/' + filename, prefix + '/log/' + datetime.strftime('%Y-%m-%d_%H-%M') + '.' + filename)
        with open(filename, 'w') as file:
            pass

def rotate():
    for server in mcp.service.manager.server_list:
        rotate_log(server.prefix, 'server.log')
        rotate_log(server.prefix, 'error.log')
        rotate_log(server.prefix, 'script-error.log')

def start():
    global scheduler

    scheduler = fooster.cron.Scheduler()
    scheduler.add(fooster.cron.Job(rotate, minute=0))
    scheduler.start()

def stop():
    global scheduler

    scheduler.stop()
    scheduler = None
