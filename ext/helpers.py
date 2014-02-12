import os
import sys


def fix_path():
    libpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'lib')
    if libpath not in sys.path and os.path.exists(libpath):
        sys.path.append(libpath)
