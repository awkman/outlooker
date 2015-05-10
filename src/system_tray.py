import sys
from datetime import date
from datetime import timedelta
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import configparser

from outlooker import Outlooker


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

	def __init__(self, icon, parent=None):
		QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)

		self.menu = QtWidgets.QMenu(parent)
		self.init_menu_action()
		self.setContextMenu(self.menu)
	
	def set_main_ui(self, w):
		self.main_ui = w

	def exit_action_handler(self):
		QtWidgets.QApplication.quit()
	
	def show_toggle_action_handler(self):
		if self.main_ui.isVisible():
			self.main_ui.hide()
			self.show_toogle_action.setText('Show')
		else:
			self.main_ui.show()
			self.show_toogle_action.setText('Hide')

	def config_action_handler(self):
		self.config.show()

	def init_menu_action(self):
		self.show_toogle_action = self.menu.addAction('Show')
		self.show_toogle_action.triggered.connect(self.show_toggle_action_handler)

		self.config_action = self.menu.addAction('Config')
		self.config_action.triggered.connect(self.config_action_handler)

		self.exit_action = self.menu.addAction('Exit')
		self.exit_action.triggered.connect(self.exit_action_handler)

	
class MainUI(QtWidgets.QMainWindow):

	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.menuBar().hide()
		self.centralWidget = QtWidgets.QWidget()
		self.setCentralWidget(self.centralWidget)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.outlooker = Outlooker()

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
			apmts = self.outlooker.get_events_start_from(tmp_date)
			total = len(apmts)
			finished = 0
			for apmt in apmts:
				if apmt.Complete:
					finished = finished + 1
					
			day = Day()
			day.set_date(tmp_date.strftime("%m/%d/%Y"))
			day.set_label(str(finished) + '/' + str(total))
			self.centralWidget.layout().addWidget(day)


class Day(QtWidgets.QDockWidget):

	def __init__(self):
		QtWidgets.QDockWidget.__init__(self)

	def set_label(self, label):
		self.label = QtWidgets.QLabel(label)
		self.setWidget(self.label)
	
	def set_date(self, date):
		self.setWindowTitle(date)


def main():

	config = configparser.ConfigParser()
	config.read('../config/config.ini')

	app = QtWidgets.QApplication(sys.argv)

	tray_icon_widget = QtWidgets.QWidget()
	tray_icon = SystemTrayIcon(QtGui.QIcon("..\pics\icon.png"), tray_icon_widget)

	main_ui = MainUI()
	main_ui.set_layout_mode(config['Main']['layout'])
	main_ui.setWindowOpacity(float(config['Main']['opacity']))
	main_ui.set_display_mode(config['Main']['display_mode'])

	tray_icon.set_main_ui(main_ui)
	tray_icon.show()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
