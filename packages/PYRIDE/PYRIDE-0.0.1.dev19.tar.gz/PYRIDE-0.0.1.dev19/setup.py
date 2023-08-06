
from setuptools import setup

NAME = 'PYRIDE'
AUTHOR = 'Nicholas C. Pandolfi'
AUTHOR_EMAIL = 'npandolfi@wpi.edu'
URL = 'https://github.com/nickpandolfi/'   #   TODO   Change URL !!!
LICENSE = 'MIT'


# A cross-platform, embeddable IDE for python flavored RegEx
SHORT_DESCRIPTION = "PYRIDE: A Cross-Platform RegEx IDE"
INSTALL_REQUIRES = ['requests']



BASE_VERSION = '0.0.1' # Change the version number here
with open('dev-count.txt') as version_file:
   append, dev_line = version_file.readlines()[0:2]
   append_text = append.split(':')[1][:-1]
   do_append = eval(append_text)
   dev_number = eval(dev_line.split(':')[1])

if do_append:
   VERSION = BASE_VERSION + f'.dev{dev_number}'
   with open('dev-count.txt', 'w+') as new_version_file:
      append_line = f'Append:{append_text}\n'
      new_dev_num = dev_number + 1
      dev_num_line = f'Version:{new_dev_num}'
      new_version_file.write(append_line + dev_num_line)
else:
   VERSION = BASE_VERSION
print(VERSION)



try:
    LONG_DESCRIPTION = open('README.txt').read()
except FileNotFoundError:
    LONG_DESCRIPTION = SHORT_DESCRIPTION


PACKAGES = ['pyride']

PACKAGE_DATA = {'pyride': ['test/*']}        #        TODO  TODO  TODO  TODO

ENTRY_POINTS = {'console_scripts': ['pyride = pyride.__main__:main']}

PLATFORMS = ['Windows', 'MacOS', 'POSIX', 'Unix']

KEYWORDS = ['Regular Expression', 'RegEx', 'regex', 're', 'Python', 'Python 3',
            'user-friendly', 'command-line', 'script', 'ide', 'IDE',
            'Integrated Development Environment', 'api', 'parser', 'highlight', '']

CLASSIFIERS = ['Development Status :: 3 - Alpha',
               'Environment :: Console',
               'Topic :: Software Development',
               'Topic :: Software Development :: Build Tools',
               'Topic :: Desktop Environment :: File Managers',
               'Intended Audience :: Developers',
               'Intended Audience :: Science/Research',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Programming Language :: Python :: 3.8',
               'License :: OSI Approved :: MIT License']

setup(name=NAME,
      version=VERSION,
      install_requires=INSTALL_REQUIRES,
      description=SHORT_DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      packages=PACKAGES,
      zip_safe=False,
      entry_points=ENTRY_POINTS,
      platforms=PLATFORMS,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      license=LICENSE,
      keywords=KEYWORDS,
      classifiers=CLASSIFIERS)
