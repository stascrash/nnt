'''
Created on 5 Mar 2014

@author: stanislav.poritskiy
'''
import datetime
from collections import namedtuple
import os


class NoteWriter(object):
	def __init__(self, notes_file):
		self.week_range = self.get_week_range((datetime.datetime.today()))
		self.today_date = datetime.date.today().strftime("%A")
		self.notes_file = notes_file

	def write_entry(self, raw_entry):
		with open(self.notes_file, "a+") as text_file:
			file_content = text_file.readlines()
			text_file.write(self.format_entry(raw_entry, file_content))
		text_file.close()

	def format_entry(self, raw_entry, file_content):
		post = ''
		message = '\t+ {0} \n'.format(raw_entry)
		if self.is_current_week(file_content):
			if self.is_today(file_content):
				post += message
			else:
				post += "{0} - \n".format(self.today_date)
				post += message
		else:
			post += self.create_header()
			post += "{0} - \n".format(self.today_date)
			post += message
		return post

	def is_today(self, file_content):
		today = "{0} -".format(self.today_date)
		for line in file_content:
			print line
			if str(today) == str(line.rstrip()):
				return True
		return False

	def is_current_week(self, file_content):
		clue = 'Week of: {0}, {1}'.format(self.week_range[0], self.week_range[1])
		for line in file_content:
			if str(clue) == str(line.rstrip()):
				return True
		return False

	def create_header(self):
		header = ''
		header += '\n'
		header += 'Week of: {0}, {1}'.format(self.week_range[0], self.week_range[1])
		header += '\n'
		return header

	def get_week_range(self, day):
		week_range = namedtuple('week_range', ['start', 'end'])
		current_week_day = day.weekday()
		to_beginning_of_week = datetime.timedelta(days=current_week_day)
		beginning_of_week = day - to_beginning_of_week
		to_end_of_week = datetime.timedelta(days=7 - current_week_day)
		end_of_week = day + to_end_of_week
		return (beginning_of_week.strftime("%B %d, %Y"), end_of_week.strftime("%B %d, %Y"))

	@staticmethod
	def handle_message(message):
		writer = NoteWriter("h:/notes.txt")
		writer.write_entry(message)

	@staticmethod
	def show_notes():
		os.system('start ' + 'h:/notes.txt')


