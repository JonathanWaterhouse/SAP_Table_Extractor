__author__ = 'U104675'
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
#build_exe_options = {"packages": ["PyQt5.QtNetwork","PyQt5.QtWebKit","PyQt5.QtPrintSupport"]}
packages = []
include_files = []

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name='SAPDownload',
      version='0.95',
      description='SAP Table Downloader',
	  options = {"build_exe": { 'packages' : packages, 'include_files': include_files}},
      executables = [Executable("SAPTableExtractorGUI.py", base=base)]
      )