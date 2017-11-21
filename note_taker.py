'''
Created on 5 Mar 2014

@author: stanislav.poritskiy
'''
try:  # Python 2/3 support
	import Tkinter as TK
except ImportError as e:
	import tkinter as TK

import threading
import json
import os
from writeLog import NoteWriter
# from PyQt5.QtWidgets import QDialog, QWidget

class NoteUI(threading.Thread):
	def __init__(self):
		super(NoteUI, self).__init__()
		self.tk = None
		self.var = None
		self.entry = None
		self.frame = None
		self.user_input = None
		self.config = None
		self.settings_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "settings.json"))
		self.start()

	def force_quit(self, *args):
		self.tk.quit()

	def run(self):
		self._load_config()
		self.tk = TK.Tk()
		self.tk.title("NNT: Nice Note Taker!")
		self.tk.protocol("WM_DELETE_WINDOW", self.force_quit)
		self.tk.overrideredirect(0)
		self.tk.lift()
		self.tk.focus_get()
		self.build_entry_widget()
		self.tk.mainloop()

	def _load_config(self):
		with open(self.settings_file, "r") as fb:
			self.config = json.load(fb)
			NoteWriter.config = self.config

	def build_entry_widget(self):
		self.var = TK.StringVar()
		self.frame = TK.Frame(self.tk)
		self.frame.pack()
		self.entry = TK.Entry(self.frame, width=50, textvariable=self.var)
		self.entry.bind('<Return>', self.send_to_writer)
		self.entry.pack()

	def send_to_writer(self, event):
		user_input = str(self.var.get())
		if not self.is_command(user_input):
			NoteWriter.handle_message(user_input)
			self.var.set("")
		self.var.set("")

	def is_command(self, arg):
		try:
			arg_name, value = arg.split(":", 1)
		except ValueError:
			value = None
			arg_name = arg

		args = ["@q", "@show", "@set_output"]
		functions = {"@q": self.force_quit,
		             "@show": NoteWriter.show_notes,
		             "@set_output": self.set_output_file}
		if arg_name in args:
			functions[arg_name](value)
			return True
		return False

	def set_output_file(self, *args):
		arg = args[0].strip()
		notes_file = os.path.normpath(arg)
		self.config["out_file"] = notes_file
		with open(self.settings_file, "w") as fb:
			json.dump(self.config, fb)
		self._load_config()


if __name__ == '__main__':
	note = NoteUI()
