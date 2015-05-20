from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from event import Event


class SystemTray(QtWidgets.QSystemTrayIcon):

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
