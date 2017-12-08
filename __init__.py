import sys
import subprocess
import os.path as path
sys.path.append(path.dirname(__file__))

from fman import ApplicationCommand, show_alert

import note_taker

class Note(ApplicationCommand):
	def __call__(self, *args, **kwargs):

		nnt = note_taker.NoteController()
		nnt.exec_()
		# sys_py_exe = r"C:\Python35-32\python.exe"
		# program_file = path.abspath(path.join(path.dirname(__file__), "note_taker.py"))
		# p = subprocess.run([sys_py_exe, program_file], shell=True)
		# exit_code = p.check_returncode()
		# if exit_code != 0:
		# 	show_alert("Something went wrong with NoteTaker. Exit Code: {}".format(exit_code))
