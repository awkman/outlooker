from datetime import date
from datetime import timedelta

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from outlooker import Outlooker
from day import Day


class MainUI(QtWidgets.QMainWindow):

	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		screen = QtWidgets.QApplication.desktop().screenGeometry()
		self.setGeometry(screen.width() - 100, 100, 50, 400)
		self.menuBar().hide()
		self.centralWidget = QtWidgets.QWidget()
		self.setCentralWidget(self.centralWidget)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

	def mouseMoveEvent(self, event):
		self.move(event.pos())
		
	def set_layout_mode(self, mode):
		if mode == 'v':
			self.layout = QtWidgets.QVBoxLayout()
		elif mode == 'h':
			self.layout = QtWidgets.QHBoxLayout()

		self.centralWidget.setLayout(self.layout)

	def set_display_mode(self, mode):
		if mode == 'week':
			self.show_week()

	def show_week(self):
		for i in range(0, 6):
			tmp_date = date.today() + timedelta(days=i)
			apmts = Outlooker.get_events_start_from(tmp_date)
			day = Day(self, tmp_date, apmts)
			day.update_label()
			self.centralWidget.layout().addWidget(day)
