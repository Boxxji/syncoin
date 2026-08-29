#!/usr/bin/env python3
"""
SynCoin Desktop Packager — Build standalone releases for macOS & Windows
Generates downloadable binary distributions (.app / .exe)
"""
import os
import platform
import subprocess
import sys

def build():
    sys_name = platform.system()
    print(f"📦 Packaging SynCoin Desktop App for {sys_name}...")
    
    cmd = [
        sys.executable, "-m", "pip", "install", "pyinstaller", "--quiet"
    ]
    subprocess.run(cmd)

    dist_name = "SynCoin-Desktop-Mac" if sys_name == "Darwin" else "SynCoin-Desktop-Windows"
    build_cmd = [
        "pyinstaller",
        "--name", dist_name,
        "--onefile",
        "--windowed",
        "--clean",
        "desktop_app.py"
    ]
    print(f"🚀 Running PyInstaller: {' '.join(build_cmd)}")
    res = subprocess.run(build_cmd, cwd=os.path.dirname(__file__))
    if res.returncode == 0:
        print(f"✅ Standalone binary successfully generated in desktop/dist/{dist_name} !")
    else:
        print(f"❌ Packaging failed with return code {res.returncode}")

if __name__ == "__main__":
    build()
