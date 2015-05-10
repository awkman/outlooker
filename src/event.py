import win32com.client

class Event:

	def __init__(self):
		None
	
	def set_start_datetime(self, datetime):
		self.start_datetime = datetime

	def set_end_datetime(self, datetime):
		self.start_datetime = datetime

	def set_subject(self, subject):
		self.subject = subject

	def set_desc(self, desc):
		self.desc = desc 
	
	def set_complete(self, complete):
		self.complete = complete
	
	def update_subject(self, subject):
		self.subject = subject
		self.src.Subject = subject
		self.src.Save()
	
	def update_desc(self, desc):
		self.desc = desc
		self.src.Body = desc
		self.src.Save()

	def update_complete(self, complete):
		self.complete = complete
		self.src.Complete = complete
		self.src.Save()

	def set_source(self, src):
		self.src = src
