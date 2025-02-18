# pyinstaller.spec

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['app.py'],
             pathex=['.'],
             binaries=[],
             datas=[('survive/survive.json', 'survive'),
                    ('survive/cover.jpg', 'survive'),
                    ('survive/1.jpg', 'survive'),
                    ('templates/cover.html', 'templates'),
                    ('templates/index.html', 'templates'),
                    ('static/main.css', 'static')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
           cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='my_flask_app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='my_flask_app')