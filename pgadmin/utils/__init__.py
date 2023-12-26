
import os
import sys

IS_WIN = (os.name == 'nt')

def env(name):
    if name in os.environ:
        return os.environ[name]
    return None

def fs_short_path(_path):
    return _path
