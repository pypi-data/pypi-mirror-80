
"""
A script to automatically push to PyPI (both test and real)

USAGE REQUIRES: pip, wheel, twine
"""

import subprocess
import os
import shutil
import time

'''

ARCHIVE

args1 = [
        'python', 'setup.py', 'sdist',
        '--formats=gztar', 'bdist_wheel', 'bdist_wininst',
        'check', 'upload', '-r', result
        ]

'''

# DO WE WANT TO PUSH TO PYPI OR PULL FROM PYPI
push_or_pull = input("Push or pull from pypi? (push/pull): ")
while push_or_pull not in ('push', 'pull'):
    push_or_pull = input("Incorrect response! Must either be 'pull' or 'push'\nTry again: ")

# DO WE WANT TO PUSH/PULL WITH TESTPYPI OR THE REGULAR PYPI
response = input("To the test, or real pypi? (test/real): ")
while response not in ('test', 'real'):
    response = input("Incorrect response! Must either be 'test' or 'real'\nTry again: ")

if push_or_pull == 'push':

    if response == 'test':
        repository = 'https://test.pypi.org/legacy/'
    else:
        repository = 'https://upload.pypi.org/legacy/'
    
    twine_call = ['twine', 'upload', '--repository-url', repository, 'dist/*']

    # BUILD THE DISTRIBUTION ARTIFACTS
    subprocess.call(['python', 'setup.py', 'sdist', 'bdist_wheel', 'check'])

    # HAVE TWINE UPLOAD BINARIES TO SPECIFIED REPOSITORY INDEX
    subprocess.call(twine_call)
    
    # CLEANUP
    shutil.rmtree('pyride.egg-info')
    shutil.rmtree('build')
    shutil.rmtree('dist')
    if os.path.exists('pyride/pyride.egg-info'):
        os.chdir('pyride')
        shutil.rmtree('pyride.egg-info')

else:
    
    if response == 'test':
        repository = 'https://test.pypi.org/simple/'
    else:
        repository = 'https://pypi.python.org/pypi'
        #repository = 'https://upload.pypi.org/legacy/'

    subprocess.call(['pip', 'uninstall', 'pyride'])
    subprocess.call(['pip', 'install', '--no-cache-dir', '--upgrade', '-i', repository, 'pyride'])

    time.sleep(10)

    subprocess.call(['pip', 'uninstall', 'pyride'])
    subprocess.call(['pip', 'install', '--no-cache-dir', '--upgrade', '-i', repository, 'pyride'])

input()

