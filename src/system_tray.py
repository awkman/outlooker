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

	def exit_action(self):
		QtWidgets.QApplication.quit()
	
	def show_action(self):
		self.main_ui.show()

	def hide_action(self):
		self.main_ui.hide()

	def config_action(self):
		if not self.config: 
			self.config_init()
		self.config.show()

	def config_init(self):
		None

	def init_menu_action(self):
		self.showAction = self.menu.addAction('Show')
		self.showAction.triggered.connect(self.show_action)

		self.hideAction = self.menu.addAction('Hide')
		self.hideAction.triggered.connect(self.hide_action)

		self.configAction = self.menu.addAction('Config')
		self.configAction.triggered.connect(self.config_action)

		self.exitAction = self.menu.addAction('Exit')
		self.exitAction.triggered.connect(self.exit_action)

	
class MainUI(QtWidgets.QMainWindow):

	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.menuBar().hide()
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
		self.outlooker = Outlooker()

	def setDisplayMode(self, mode):

		if mode == 'week':
			self.show_week()

	def show_week(self):
		for i in range(0, 6):
			apmts = self.outlooker.get_events_start_from(date.today() + timedelta(days=i))
			total = len(apmts)
			finished = 0
			for apmt in apmts:
				if apmt.Complete:
					finished = finished + 1
					
			day = Day()
			day.set_label(str(finished) + '/' + str(total))
			self.addDockWidget(QtCore.Qt.TopDockWidgetArea, day)

class Day(QtWidgets.QDockWidget):

	def __init__(self):
		QtWidgets.QDockWidget.__init__(self)

	def set_label(self, label):
		self.label = QtWidgets.QLabel(label)
		self.setWidget(self.label)


def main():

	config = configparser.ConfigParser()
	config.read('../config/config.ini')

	app = QtWidgets.QApplication(sys.argv)

	w = QtWidgets.QWidget()
	trayIcon = SystemTrayIcon(QtGui.QIcon("..\pics\icon.png"), w)
	main_ui = MainUI()
	main_ui.setWindowOpacity(float(config['Main']['opacity']))

	main_ui.setDisplayMode(config['Main']['display_mode'])

	trayIcon.set_main_ui(main_ui)

	trayIcon.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
