import os
import sys

input('This will upload a new version of Brian2 to PyPI, press return to continue ')
# upload to pypi
os.chdir('../../..')
os.system('%s setup.py sdist --formats=gztar --with-cython --fail-on-error' % sys.executable)