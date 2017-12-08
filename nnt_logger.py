import os
import json
import logging.config


class NoteHandler(logging.Handler):
	def __init__(self, **kwargs):
		# print(kwargs)
		super(NoteHandler, self).__init__()

	def emit(self, record):
		log_entry = self.format(record)
		print(log_entry)



class NoteFormatter(logging.Formatter):
	def __init__(self, *args):
		super(NoteFormatter, self).__init__()
		# print(*args)

	def format(self, record):
		super(NoteFormatter, self).format(record)


def setup_logging(
		default_path='log_cfg.json',
		default_level=logging.INFO,
		env_key='LOG_CFG'):
	"""Setup logging configuration"""
	path = default_path
	value = os.getenv(env_key, None)
	if value:
		path = value
	if os.path.exists(path):
		with open(path, 'rt') as f:
			config = json.load(f)
		logging.config.dictConfig(config)
	else:
		logging.basicConfig(level=default_level)


if __name__ == '__main__':
	setup_logging()
	L2 = logging.getLogger("nnt.notes")
	L2.debug("test here")

