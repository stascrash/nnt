'''
Created on 5 Mar 2014

@author: stanislav.poritskiy
'''

import os
import sys
from ui import Ui_Dialog
from writeLog import NoteWriter
from PyQt5.QtWidgets import QDialog, QApplication, QListWidgetItem
from PyQt5.QtCore import QObject, pyqtSignal, QThread, Qt
import datetime
import json
import nnt_logger
import logging
nnt_logger.setup_logging()
LOGGER = logging.getLogger("nnt")

NNT_COMMAND_SEPARATOR = ":"
NNT_COMMANDS = {"@q": "quit_cmd",
				"@show": "show_cmd",
				"@setoutput": "set_output_file_cmd",
				"_@makenote": "message_cmd"}


class NoteController(Ui_Dialog, QDialog):
	"""Main controller of NNT. It handles communication between user and
	user command-line keys. NNT-Controller instantiates handlers and
	performs calls on them. """

	def __init__(self):
		super(NoteController, self).__init__()
		self.setupUi(self)
		self.mouse_left_click = False
		self.current_x = 0
		self.current_y = 0

		self.set_style()
		self.setModal(True)
		self.setWindowFlags(Qt.FramelessWindowHint)

		# self.noteListWidget.setHidden(True)
		self.user_input = None
		self.writer = NoteModel()
		self.connect_signals()



	def set_style(self):
		with open("darkorange.stylesheet", "r") as fp:
			self.setStyleSheet(fp.read())

	def mouseMoveEvent(self, event):
		super(NoteController, self).mouseMoveEvent(event)
		if self.mouse_left_click:
			self.move(event.globalPos().x() - self.current_x, event.globalPos().y() - self.current_y)

	def mousePressEvent(self, event):
		super(NoteController, self).mousePressEvent(event)
		if event.button() == Qt.LeftButton:
			self.mouse_left_click = True
			self.current_x = event.pos().x()
			self.current_y = event.pos().y()

	def mouseReleaseEvent(self, event):
		super(NoteController, self).mouseReleaseEvent(event)
		self.mouse_left_click = False

	def connect_signals(self):
		self.noteLineEdit.returnPressed.connect(self.on_enter_pressed)
		self.noteListWidget.currentItemChanged.connect(self.on_note_changed)
		self.writer.commands.quit_sgl.connect(self.on_quit)
		self.writer.commands.make_note_sgl.connect(self.on_make_note)
		self.writer.commands.show_note_sgl.connect(self.on_show_note)

	def on_note_changed(self, current, previous):
		if current:
			LOGGER.debug("Current: {}".format(current.text()))
		if previous:
			LOGGER.debug("Previous: {}".format(previous.text()))

	def on_enter_pressed(self):
		"""When user enters a message and hit's enter. """
		self.user_input = self.noteLineEdit.text()
		self.writer.check_input(self.user_input)
		self.noteLineEdit.setText("")

	def on_quit(self):
		self.accept()

	def on_make_note(self, message):
		self.writer.make_note(message)
		self.update_note_widget(message)

	def on_show_note(self):
		self.noteListWidget.setHidden(False)

	def update_note_widget(self, message):
		time_str = message.date.strftime("%y/%m/%d")
		item = QListWidgetItem()
		item.setText(" | ".join([time_str, message.preview_message]))
		item.setData(Qt.UserRole, message)
		self.noteListWidget.addItem(item)


class NoteMessage(object):
	"""Simple container to register Message Types."""
	__days__ = {0: "Sunday",
				1: "Monday",
				2: "Tuesday",
				3: "Wednesday",
				4: "Thursday",
				5: "Friday",
				6: "Saturday"}

	def __init__(self, user_input):
		self.date = datetime.datetime.now()
		self.message = self._format_user_input(user_input)
		self.preview_message = self.trim_message()

	def trim_message(self):
		if len(self.message) > 27:
			return self.message[:26] + "..."
		else:
			return self.message

	def _format_user_input(self, user_input):
		"""Do string cleanup/strips, break into max-char-lenght.
		all format-settings are read from separate JSON"""
		# TODO: Formatting needs to be implemented. Currently this is pass-through
		formatted_user_input = user_input
		return formatted_user_input


	def __call__(self, *args, **kwargs):
		return self.message

	def __hash__(self):
		return hash(self.message)


class NoteModel(QObject):
	"""This is an NNT engine. If it recognizes that input is a key-word command
	it then emits a signal to controller to select appropriate action."""

	@property
	def notes(self):
		return self.writer.get_notes()

	def __init__(self):
		super(NoteModel, self).__init__()
		self.settings_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "settings.json"))
		self.config = self._load_config()

		self.commands = NoteCommands()
		self.writer = NoteWriter(self.config)

	def check_input(self, usr_input):
		if self.is_command(usr_input):
			self.execute_command(usr_input)
		else:
			self.execute_command(NNT_COMMAND_SEPARATOR.join(["_@makenote", usr_input]))

	def is_command(self, usr_input):
		try:
			arg_name = usr_input.split(NNT_COMMAND_SEPARATOR, 1)[0]
		except ValueError:
			arg_name = usr_input
		return arg_name in NNT_COMMANDS

	def execute_command(self, command_args):
		command, args = self._get_command_args(command_args)
		self.commands.run(command, args)

	def _get_command_args(self, command_args):
		if ":" in command_args:
			try:
				command, args = command_args.split(NNT_COMMAND_SEPARATOR, 1)
			except ValueError:
				args = None
				command = command_args
		else:
			args = None
			command = command_args
		return command, args

	def _load_config(self):
		LOGGER.debug("Loading settings file: {}".format(self.settings_file))
		with open(self.settings_file, "r") as fb:
			return json.load(fb)

	def make_note(self, message):
		self.writer.write_entry(message)


class NoteCommands(QObject):
	"""This class provides base functionality of NNT."""
	quit_sgl = pyqtSignal()
	make_note_sgl = pyqtSignal("PyQt_PyObject")
	show_note_sgl = pyqtSignal()

	def __init__(self):
		super(NoteCommands, self).__init__()

	def run(self, command, args):
		try:
			command = NNT_COMMANDS.get(command)
		except KeyError:
			LOGGER.error("\"{}\" command is not recognized by NNT\nCheck your spelling.".format(command))

		if hasattr(self, command) and callable(getattr(self, command)):
			callable_command = getattr(self, command)
			callable_command(args)
		else:
			LOGGER.error("\"{}\" cannot be executed.".format(command))

	def show_cmd(self, *args):
		self.show_note_sgl.emit()

	def quit_cmd(self, *args):
		self.quit_sgl.emit()

	def message_cmd(self, user_input):
		self.make_note_sgl.emit(NoteMessage(user_input))

	def set_output_file_cmd(self, *args):
		arg = args[0].strip()
		notes_file = os.path.normpath(arg)
		self.config["out_file"] = notes_file
		with open(self.settings_file, "w") as fb:
			json.dump(self.config, fb)
		self._load_config()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	d = NoteController()
	d.show()
	sys.exit(app.exec_())
