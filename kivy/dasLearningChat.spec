# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=collect_data_files('kivy') + # add all paths which are required
    [
        ('data', 'data'),
        ('kv_files', 'kv_files'),
        ('main_layout.kv', '.')
    ],
    hiddenimports=[
        "kivymd.uix.screenmanager",
        "kivymd.uix.textfield",
        "kivymd.uix.button",
        "kivymd.uix.label",
        "kivymd.uix.screen",
        "kivymd.uix.boxlayout",
        "kivymd.uix.scrollview",
        "kivy.metrics",
        "kivymd.icon_definitions",
        "kivymd.uix.dropdownitem",
        "kivy.uix.widget",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='OllamaAiChat',
    icon='data/images/favicon.ico',
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
