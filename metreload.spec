# -*- mode: python -*-
from metreload.spec import a, pyz, options, exe_options


exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          **options, **exe_options)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               **options)
