import Tkinter as TK
import threading
from writeLog import NoteWriter


class NoteUI(threading.Thread):
	def __init__(self):
		super(NoteUI, self).__init__()
		self.tk = None
		self.var = None
		self.entry = None
		self.frame = None
		self.user_input = None
		self.start()

	def force_quit(self):
		self.tk.quit()

	def run(self):
		self.tk = TK.Tk()
		self.tk.title("NNT: Nice Note Taker!")
		self.tk.protocol("WM_DELETE_WINDOW", self.force_quit)
		self.tk.overrideredirect(0)
		self.tk.lift()
		self.tk.focus_get()
		self.build_entry_widget()
		self.tk.mainloop()

	def build_entry_widget(self):
		self.var = TK.StringVar()
		self.frame = TK.Frame(self.tk)
		self.frame.pack()
		self.entry = TK.Entry(self.frame, width=50, textvariable=self.var)
		self.entry.bind('<Return>', self.send_to_writer)
		self.entry.pack()

	def send_to_writer(self, event):
		user_input = str(self.var.get())
		if not self.check_for_args(user_input):
			NoteWriter.handle_message(user_input)
			self.var.set("")
		self.var.set("")

	def check_for_args(self, arg):
		args = ["@q", "@show"]
		functions = {"@q": self.force_quit, "@show": NoteWriter.show_notes}
		if arg in args:
			functions[arg]()
			return True
		return False


if __name__ == '__main__':
	ui = NoteUI()



