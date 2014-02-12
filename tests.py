import logging
import os
import sys
import unittest

path = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
sys.path.append(path)

from ext.helpers import fix_path; fix_path()

from core.tests import *
from ext.tests import *
from lib.tests import *


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.WARN)
    unittest.main(verbosity=2)
