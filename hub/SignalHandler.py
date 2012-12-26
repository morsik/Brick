class SignalHandler():
	def __init__(self):
		self.handlers = {}
	
	def connect(self, signal_name, function_handler):
		if signal_name in self.handlers:
			print("Handler %s already exists!" % (signal_name))
			return False
		self.handlers[signal_name] = function_handler
		return True
	
	def disconnect(self, signal_name):
		if signal_name in self.handlers:
			self.handlers.remove(signal_name)
			return True
		else:
			print("Handler %s doesn't exists!" % (signal_name))
			return False
	
	def emit(self, signal_name, *args):
		if signal_name in self.handlers:
			self.handlers[signal_name](*args)
			return True
		else:
			print("Handler %s doesn't exists!" % (signal_name))
			return False

signals = SignalHandler()
