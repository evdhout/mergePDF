#!python3

import PyInstaller.__main__


PyInstaller.__main__.run([
    'mergePDF.py',
    '--onefile',
    '--windowed'
])
