# -*- mode: python -*-
from metreload.spec import a, pyz, options, exe_options

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          **options,
          **exe_options)

