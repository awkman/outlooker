import win32com.client

class Event:

	def __init__(self, apmt):
		self.set_source(apmt)
		self.set_start_datetime(apmt.StartDate)
		self.set_end_datetime(apmt.DueDate)
		self.set_subject(apmt.Subject)
		self.set_desc(apmt.Body)
		self.set_complete(apmt.Complete)
		self.set_entry_id(apmt.EntryID)
	
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
	
	def set_entry_id(self, id):
		self.entry_id = id

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
