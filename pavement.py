# -*- Import: -*-
from paver.easy import *
from paver.setuputils import setup
from setuptools import find_packages

try:
    # Optional tasks, only needed for development
    # -*- Optional import: -*-
    import paver.doctools
    import paver.virtual
    import paver.misctasks
    ALL_TASKS_LOADED = True
except ImportError, e:
    info("some tasks could not not be imported.")
    debug(str(e))
    ALL_TASKS_LOADED = False

NAME = 'PyVirtualDisplay'
PACKAGE = 'pyvirtualdisplay'
URL = 'https://github.com/ponty/pyvirtualdisplay'
DESCRIPTION = 'python wrapper for Xvfb and Xephyr'

__version__ = None
py = path('.') / PACKAGE / '__init__.py'
for line in open(py).readlines():
    if '__version__' in line:
        exec line
        break
assert __version__    
version = __version__

classifiers = [
    # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    "License :: OSI Approved :: BSD License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    ]

install_requires = [
    # -*- Install requires: -*-
    'setuptools',
    'path.py',
    'EasyProcess',
    ]

entry_points = """
    # -*- Entry points: -*-
    """

# compatible with distutils of python 2.3+ or later
setup(
    name=NAME,
    version=version,
    description=DESCRIPTION,
    long_description=open('README.rst', 'r').read(),
    classifiers=classifiers,
    keywords='Xvfb Xephyr X wrapper',
    author='ponty',
    #author_email='zy@gmail.com',
    url=URL,
    license='BSD',
    packages=find_packages(exclude=['bootstrap', 'pavement', ]),
    include_package_data=True,
    test_suite='nose.collector',
    zip_safe=False,
    install_requires=install_requires,
    entry_points=entry_points,
    )

options(
    # -*- Paver options: -*-
    minilib=Bunch(
        extra_files=[
            # -*- Minilib extra files: -*-
            ]
        ),
    sphinx=Bunch(
        docroot='docs',
        builddir="_build",
        sourcedir=""
        ),
    virtualenv=Bunch(
        packages_to_install=[
            # -*- Virtualenv packages to install: -*-
            "nose",
            "Sphinx>=0.6b1",
            "pkginfo",
            "virtualenv"],
        dest_dir='./virtual-env/',
        install_paver=True,
        script_name='bootstrap.py',
        paver_command_line=None
        ),
    )

options.setup.package_data = paver.setuputils.find_package_data(
    PACKAGE, package=PACKAGE, only_in_packages=False)

if ALL_TASKS_LOADED:
    @task
    @needs('generate_setup', 'minilib', 'setuptools.command.sdist')
    def sdist():
        """Overrides sdist to make sure that our setup.py is generated."""

@task
def pychecker():
    sh('pychecker --stdlib --only --limit 100 {package}/ '.format(package=PACKAGE))

@task
def findimports():
    '''list external imports'''
    sh('findimports {package} |grep -v ":"|grep -v {package}|sort|uniq'.format(package=PACKAGE))

@task
def pyflakes():
    sh('pyflakes {package}'.format(package=PACKAGE))

@task
def nose():
    sh('nosetests --with-xunit --verbose')

@task
def sloccount():
    sh('sloccount --wide --details {package} tests > sloccount.sc'.format(package=PACKAGE))

@task
def clean():
    root=path(__file__).dirname().abspath()
    ls=[]
    dls=[]
    ls+=root.walkfiles('*.pyc')
    ls+=root.walkfiles('*.html')
    ls+=root.walkfiles('*.zip')
    ls+=root.walkfiles('*.css')
    ls+=root.walkfiles('*.png')
    ls+=root.walkfiles('*.doctree')
    ls+=root.walkfiles('*.pickle')

    dls+=[root / 'dist']
    dls+=root.listdir('*.egg-info')

    for x in ls:
        x.remove()
    for x in dls:
        x.rmtree()

@task
@needs('sloccount', 'html', 'sdist', 'nose')
def hudson():
    pass


