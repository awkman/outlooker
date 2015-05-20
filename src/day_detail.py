from datetime import date

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from outlooker import Outlooker


class DayDetail(QtWidgets.QFrame):

	def __init__(self, parent):
		QtWidgets.QFrame.__init__(self)
		self.parent = parent

		self.layout = QtWidgets.QVBoxLayout()

		self.add_button = QtWidgets.QPushButton()
		self.del_button = QtWidgets.QPushButton()
		self.add_button.setText("Add")
		self.del_button.setText("Del")
		self.box_layout = QtWidgets.QHBoxLayout()
		self.box_layout.addWidget(self.add_button)
		self.box_layout.addWidget(self.del_button)
		self.group = QtWidgets.QGroupBox()
		self.group.setLayout(self.box_layout)
		self.layout.addWidget(self.group)

		self.table_view = QtWidgets.QTableView()
		self.table_view.verticalHeader().hide()
		self.layout.addWidget(self.table_view)

		self.setLayout(self.layout)

		self.add_button.clicked.connect(self.add_handler)
		self.del_button.clicked.connect(self.del_handler)
	
	def del_handler(self):
		selected_indexes = self.table_view.selectedIndexes()
		for index in selected_indexes:
			entry_id_index = self.table_view.model().index(index.row(), 3)
			entry_id = self.table_view.model().data(entry_id_index)
			Outlooker.del_event_by_entry_id(entry_id)

	def add_handler(self):
		self.add_frame = QtWidgets.QFrame()

		subject_label = QtWidgets.QLabel('Subject')
		desc_label = QtWidgets.QLabel('Description')
		date_label = QtWidgets.QLabel('Date')
		self.subject_text = QtWidgets.QLineEdit()
		self.desc_text = QtWidgets.QLineEdit()
		self.date_text = QtWidgets.QLineEdit()
		self.date_text.setText(date.today().strftime("%m/%d/%Y"))
		self.save_button = QtWidgets.QPushButton('Save')
		self.save_button.clicked.connect(self.save_handler)

		self.add_frame_layout = QtWidgets.QGridLayout()
		self.add_frame_layout.addWidget(date_label, 1, 1)
		self.add_frame_layout.addWidget(self.date_text, 1, 2)
		self.add_frame_layout.addWidget(subject_label, 2, 1)
		self.add_frame_layout.addWidget(self.subject_text, 2, 2)
		self.add_frame_layout.addWidget(desc_label, 3, 1)
		self.add_frame_layout.addWidget(self.desc_text, 4, 1)
		self.add_frame_layout.addWidget(self.save_button, 5, 1)
		self.add_frame.setLayout(self.add_frame_layout)

		self.add_frame.show()

	def save_handler(self):
		Outlooker.save_event(self.subject_text.text(), self.date_text.text(),
							 self.desc_text.text())

	def show(self):
		parent_point = self.parent.mapToGlobal(QtCore.QPoint(self.parent.x(), self.parent.y()))
		self.setGeometry(parent_point.x() - self.width(),
						 parent_point.y(), self.width(),
						 self.height())
		super(DayDetail, self).show()

	def setModel(self, model):
		self.table_view.setModel(model)
