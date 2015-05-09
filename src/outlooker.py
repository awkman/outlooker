import win32com.client
from datetime import date


class Outlooker:
	
	def __init__(self):
		
		self.o = win32com.client.Dispatch('Outlook.Application')
	
	def add_event_item(self, title, content, start, end):
		apmt = self.o.CreateItem(1)
		apmt.Subject = title
		apmt.Start = start.strftime('%m/%d/%Y')
		apmt.End = end.startftime('%m/%d/%Y')
		ampt.Save()
	
	def del_event(self, index):
		self.o.items(index).Delete()

	def update_event(self, index):
		apmt = self.o.Items(index)
		apmt.Subject = title
		apmt.Start = start.strftime('%m/%d/%Y')
		apmt.End = end.startftime('%m/%d/%Y')
		ampt.Save()

	def get_events(self, start, end):
		#ns = self.o.GetNamespace('MAPI')
		ns = self.o.Session
		folder = ns.GetDefaultFolder(28)
		restrict = "[StartDate] >= '" + start.strftime('%m/%d/%Y') + \
				   "' AND [DueDate] <= '" + end.strftime('%m/%d/%Y') + \
				   "'"
		apmts = folder.Items.Restrict(restrict)

		return apmts
	
	def get_events_start_from(self, start):
		#ns = self.o.GetNamespace('MAPI')
		ns = self.o.Session
		folder = ns.GetDefaultFolder(28)
		restrict = "[StartDate] = '" + start.strftime('%m/%d/%Y') + "'"
		apmts = folder.Items.Restrict(restrict)

		return apmts
