"""
Specifications for PyInstaller
"""

from subprocess import check_output
from warnings import warn

from PyInstaller.building.build_main import Analysis, PYZ
from PyInstaller.utils.hooks import copy_metadata

from . import __version__ as version


BLOCK_CIPHER = None
UPX = True
BASENAME = 'metreload'

name_with_version = '{}-{}'.format(BASENAME, version)

# Do analysis
a = Analysis(['metreload/cli.py'],
             pathex=[],
             binaries=[],
             datas=copy_metadata('pydap'),
             hiddenimports=['pandas._libs.tslibs.np_datetime',
                            'pandas._libs.skiplist'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=BLOCK_CIPHER)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=BLOCK_CIPHER)

options = dict(strip=False,
               upx=True)

exe_options = dict(name=BASENAME,
                   debug=False,
                   console=True)
