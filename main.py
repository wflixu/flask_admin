import os
import sys
import builtins

if 'PGADMIN_SERVER_MODE' in os.environ:
    if os.environ['PGADMIN_SERVER_MODE'] == 'OFF':
        builtins.SERVER_MODE = False
    else:
        builtins.SERVER_MODE = True
else:
    builtins.SERVER_MODE = None

print("--------", builtins.SERVER_MODE)


import config
