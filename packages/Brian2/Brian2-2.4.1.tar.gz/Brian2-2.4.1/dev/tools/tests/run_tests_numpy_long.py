'''
Run all the numpy tests (including tests that take a long time) using pytest.
Exits with error code 1 if a test failed.
'''
import sys

import brian2

if not brian2.test('numpy', long_tests=True):  # If the test fails, exit with a non-zero error code
    sys.exit(1)
