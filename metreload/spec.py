###############################################################################
# Copyright (C) 2018–2019  The Spine Project Authors
#
# This file is part of MetReload
#
# MetReLoad is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
###############################################################################

"""
Specifications for PyInstaller
"""

from PyInstaller.building.build_main import Analysis, PYZ
from PyInstaller.utils.hooks import copy_metadata, collect_data_files

from . import __version__ as version


BLOCK_CIPHER = None
UPX = True
BASENAME = 'metreload'

name_with_version = '{}-{}'.format(BASENAME, version)  # pylint: disable=C0103

# Do analysis
a = Analysis(['metreload/cli.py'],
             pathex=[],
             binaries=[],
             datas=copy_metadata('pydap')\
                   + collect_data_files('distributed')\
                   + collect_data_files('dask')\
                   + [('docs/_build/html', 'documentation')],
             hiddenimports=['pandas._libs.tslibs.np_datetime',
                            'pandas._libs.skiplist',
                            'pydap.responses.das',
                            'pydap.responses.html',
                            'pydap.responses.ascii',
                            'pydap.responses.version'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=BLOCK_CIPHER)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=BLOCK_CIPHER)

options = dict(strip=False,
               upx=UPX)

exe_options = dict(name=BASENAME,
                   debug=False,
                   console=True)
