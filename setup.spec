# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['setup.py'],
    pathex=[],
    binaries=[],
    datas=[('menu.py', '.'), ('main.py', '.'), ('harta1.txt', '.'), ('harta2.txt', '.'), ('harta3.txt', '.'), ('harta4.txt', '.'), ('harta5.txt', '.'), ('player.jpg', '.'), ('bot.jpg', '.'), ('_psycopg.pyd', 'psycopg2')],
    hiddenimports=['psycopg2', 'psycopg2'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='setup',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
