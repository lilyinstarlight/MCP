import fooster.cron

import mcp.model.source

scheduler = None

def update():
    for source in mcp.model.source.items():
        mcp.model.source.update(source.name)

def start():
    global scheduler

    scheduler = fooster.cron.Scheduler()
    scheduler.add(fooster.cron.Job(update, minute=0))
    scheduler.start()

def stop():
    global scheduler

    scheduler.stop()
    scheduler = None
