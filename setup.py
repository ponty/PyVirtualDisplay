import versioneer
from distutils.core import setup
import os.path
import sys


NAME = 'pyvirtualdisplay'
URL = 'https://github.com/ponty/PyVirtualDisplay'
DESCRIPTION = 'python wrapper for Xvfb, Xephyr and Xvnc'
PACKAGES = [NAME,
            NAME + '.examples',
            ]

versioneer.versionfile_source = NAME + '/_version.py'
versioneer.versionfile_build = versioneer.versionfile_source
versioneer.tag_prefix = ''
versioneer.parentdir_prefix = NAME + '-'

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

classifiers = [
    # Get more strings from
    # http://www.python.org/pypi?%3Aaction=list_classifiers
    "License :: OSI Approved :: BSD License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
]

install_requires = open("requirements.txt").read().split('\n')

setup(
    name=NAME,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description=DESCRIPTION,
    long_description=open('README.rst', 'r').read(),
    classifiers=classifiers,
    keywords='Xvfb Xephyr X wrapper',
    author='ponty',
    # author_email='',
    url=URL,
    license='BSD',
    packages=PACKAGES,
    install_requires=install_requires,
    **extra
)
