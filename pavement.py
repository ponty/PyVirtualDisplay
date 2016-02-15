from path import Path
from paver.doctools import cog, html
from paver.easy import options
from paver.options import Bunch
from paver.setuputils import setup


IMPORTS=[cog, html, setup]
    
options(
    cog=Bunch(
        basedir='.',
        pattern='README.rst',
        includedir='pyvirtualdisplay',
        beginspec='#--',
        endspec='--#',
        endoutput='#-#',
    )
)


# get info from setup.py
setup_py = ''.join(
    [x for x in Path('setup.py').lines() if 'setuptools' not in x])
exec(setup_py)