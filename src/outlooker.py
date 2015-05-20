import win32com.client
from datetime import date


class Outlooker:
	
	app = win32com.client.Dispatch('Outlook.Application')
	ns = app.Session

	@classmethod
	def get_folder(cls):
		return cls.ns.GetDefaultFolder(28)

	@classmethod
	def get_events_start_from(cls, start):
		folder = cls.get_folder()
		restrict = "[StartDate] = '" + start.strftime('%m/%d/%Y') + "'"
		return folder.Items.Restrict(restrict)

	@classmethod
	def del_event_by_entry_id(cls, id):
		apmt = cls.ns.GetItemFromID(id)
		apmt.Delete()

	@classmethod
	def save_event(cls, subject, day, desc):
		apmt = cls.app.CreateItem(3)
		apmt.Subject = subject
		apmt.Body = desc
		apmt.StartDate = day
		apmt.Save()
