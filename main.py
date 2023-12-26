import os

os.environ['PGADMIN_SERVER_MODE'] = 'OFF'
os.environ['PGADMIN_INT_KEY'] = '6217b349-4000-433e-a008-e1dacfdd7a8b'
os.environ['PGADMIN_INT_PORT'] = '5050'

import sys
import builtins


builtins.SERVER_MODE = True


import config
import setup


print(config.APP_NAME)
