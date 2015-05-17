from PyQt5 import QtGui

from event import Event

class TableModel(QtGui.QStandardItemModel):
	
	def __init__(self, events):
		QtGui.QStandardItemModel.__init__(self)
		self.events = events
		self.set_header()
		self.init_data()
	
	def set_header(self):
		self.setHorizontalHeaderItem(0, QtGui.QStandardItem('Subject'))
		self.setHorizontalHeaderItem(1, QtGui.QStandardItem('Description'))
		self.setHorizontalHeaderItem(2, QtGui.QStandardItem('Complete'))
		self.setHorizontalHeaderItem(3, QtGui.QStandardItem('EntryID'))
	
	def init_data(self):
		row = 0
		for event in self.events:
			self.setItem(row, event)
			row = row + 1

	def setItem(self, row, event):
		super(TableModel, self).setItem(row, 0, QtGui.QStandardItem(event.subject))
		super(TableModel, self).setItem(row, 1, QtGui.QStandardItem(event.desc))
		super(TableModel, self).setItem(row, 2, QtGui.QStandardItem(event.complete))
		super(TableModel, self).setItem(row, 3, QtGui.QStandardItem(event.entry_id))
	
