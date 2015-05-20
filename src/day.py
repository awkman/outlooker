from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from day_detail import DayDetail
from table_model import TableModel
from event import Event


class Day(QtWidgets.QDockWidget):

	def __init__(self, parent, date, apmts):
		QtWidgets.QDockWidget.__init__(self, parent)
		self.label = QtWidgets.QLabel()
		self.setWidget(self.label)
		self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
		self.label.linkActivated.connect(self.label_activated_handler)

		self.set_events(apmts)
		self.set_date(date)

	def get_finished_count(self):
		cnt = 0
		for event in self.events:
			if event.complete:
				cnt = cnt + 1
		return cnt

	def set_events(self, apmts):
		self.events = []
		for apmt in apmts:
			event = Event(apmt)
			self.events.append(event)

	def update_label(self):
		finished = str(self.get_finished_count())
		total = str(len(self.events))
		self.label.setText(finished + '/' + '<a href="#total_' + total + '">'
						   + total + '</a>')
		self.label_font = QtGui.QFont("Consolas", 20, QtGui.QFont.Bold)
		self.label.setFont(self.label_font)

	def label_activated_handler(self, text):
		self.table = DayDetail(self)
		self.table_model = TableModel(self.events)
		self.table.setModel(self.table_model)
		self.table.table_view.horizontalHeader().hideSection(3)
		self.table_model.itemChanged.connect(self.table_item_changed_handler)

		self.table.show()

	def set_date(self, date):
		self.date = date
		self.setWindowTitle(self.date.strftime('%m/%d'))
		self.label_font = QtGui.QFont("Consolas", 10, QtGui.QFont.Bold)
		self.setFont(self.label_font)
	
	def table_item_changed_handler(self, item):
		event = self.events[item.row()]
		if item.column() == 0:
			event.update_subject(item.data(0))
		elif item.column() == 1:
			event.update_desc(item.data(0))
		elif item.column() == 2:
			event.update_desc(item.data(0))
