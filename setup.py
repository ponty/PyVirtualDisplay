import os.path

from setuptools import setup

NAME = "pyvirtualdisplay"

# get __version__
__version__ = None
exec(open(os.path.join(NAME, "about.py")).read())
VERSION = __version__

PYPI_NAME = "PyVirtualDisplay"
URL = "https://github.com/ponty/pyvirtualdisplay"
DESCRIPTION = "python wrapper for Xvfb, Xephyr and Xvnc"
LONG_DESCRIPTION = """pyvirtualdisplay is a python wrapper for Xvfb, Xephyr and Xvnc

Documentation: https://github.com/ponty/pyvirtualdisplay/tree/"""
LONG_DESCRIPTION += VERSION
PACKAGES = [
    NAME,
    NAME + ".examples",
]


classifiers = [
    # Get more strings from
    # http://www.python.org/pypi?%3Aaction=list_classifiers
    "License :: OSI Approved :: BSD License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
]

install_requires = ["EasyProcess"]

setup(
    name=PYPI_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    classifiers=classifiers,
    keywords="Xvfb Xephyr X wrapper",
    author="ponty",
    # author_email='',
    url=URL,
    license="BSD",
    packages=PACKAGES,
    #     include_package_data=True,
    #     zip_safe=False,
    install_requires=install_requires,
    # **extra
)
