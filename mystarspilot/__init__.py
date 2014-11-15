"""
MyStarsPilot - a CLI tool to search your starred Github repositories.
"""
__author__ = 'wolfg1969'
__version__ = '0.0.1'
__licence__ = 'MIT'

import sys
from .core import main


if __name__ == '__main__':
    sys.exit(main())