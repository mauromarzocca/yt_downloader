import os
import subprocess
import sys
import core

def build():
    # Install requirements
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    print(f"Building YouTube Downloader v{core.VERSION} for {sys.platform}...")

    # Data separator for PyInstaller (Windows uses ;, Unix uses :)
    sep = ";" if sys.platform == "win32" else ":"

    # Define common args for both builds
    # We use pyinstaller directly with arguments instead of spec file generation to keep it simple,
    # BUT we need to inject the Info.plist content for macOS versioning.
    # The clean way is to generate a spec, modify it, and build from it.

    # However, PyInstaller allows passing a .spec file directly.
    # Let's write the spec file content dynamically to handle the version string.

    # macOS Info.plist configuration
    info_plist = {
        'CFBundleName': 'YouTubeDownloader',
        'CFBundleDisplayName': 'YouTubeDownloader',
        'CFBundleGetInfoString': "YouTube Downloader",
        'CFBundleIdentifier': "com.youtubedownloader.app",
        'CFBundleVersion': core.VERSION,
        'CFBundleShortVersionString': core.VERSION,
        'NSHumanReadableCopyright': "Un programma di Mauro Marzocca",
    }

    # We will generate the spec file content for GUI
    spec_content_gui = f"""
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('icon.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='YouTubeDownloader',
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
    icon='icon.png',
)

# macOS Bundle configuration
app = BUNDLE(
    exe,
    name='YouTubeDownloader.app',
    icon='icon.png',
    bundle_identifier='com.youtubedownloader.app',
    info_plist={info_plist}
)
"""

    # Write GUI Spec
    with open("YouTubeDownloader.spec", "w") as f:
        f.write(spec_content_gui)

    print("Building GUI from spec...")
    subprocess.check_call(["pyinstaller", "--clean", "YouTubeDownloader.spec"])

    # ---------------------------------------------------------
    # CLI Build (simpler, usually no need for Bundle/Info.plist on macOS console apps in same way)
    # We will just run the command for CLI as before, or generate a spec if needed.
    # A simple command is enough for CLI.

    print("Building CLI...")
    cmd_cli = [
        "pyinstaller",
        "--name=YouTubeDownloader-CLI",
        "--onefile",
        "--console",
        "--clean",
        f"--add-data=icon.png{sep}.",
        "cli_entry.py"
    ]
    subprocess.check_call(cmd_cli)

    print(f"Build complete. Artifacts in 'dist/' folder.")

if __name__ == "__main__":
    build()
