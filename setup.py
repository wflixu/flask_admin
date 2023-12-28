
"""Perform the initial setup of the application, by creating the auth
and settings database."""

import argparse
import os
import sys

# We need to include the root directory in sys.path to ensure that we can
# find everything we need when running in the standalone runtime.
root = os.path.dirname(os.path.realpath(__file__))
if sys.path[0] != root:
    sys.path.insert(0, root)


import builtins
import config


