import sys

sys.path.append(os.path.dirname(__file__) + '/cron.py')
sys.path.append(os.path.dirname(__file__) + '/db.py')
sys.path.append(os.path.dirname(__file__) + '/web.py')

import cron, db, web

sys.path.remove(os.path.dirname(__file__) + '/cron.py')
sys.path.remove(os.path.dirname(__file__) + '/db.py')
sys.path.remove(os.path.dirname(__file__) + '/web.py')

__all__ = ['cron', 'db', 'web']
