import sys
from datetime import date
from datetime import timedelta
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import configparser

from outlooker import Outlooker
from event import Event
from table_model import TableModel

def convert_outlook_events_to_native_events(apmts):
	events = []
	for apmt in apmts:
		event = Event()
		event.set_source(apmt)
		event.set_start_datetime(apmt.StartDate)
		event.set_end_datetime(apmt.DueDate)
		event.set_subject(apmt.Subject)
		event.set_desc(apmt.Body)
		event.set_complete(apmt.Complete)
		events.append(event)
	return events
	

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
			day = Day()
			day.set_events(apmts)
			day.set_date(tmp_date)
			day.update_label()
			self.centralWidget.layout().addWidget(day)


class Day(QtWidgets.QDockWidget):

	def __init__(self):
		QtWidgets.QDockWidget.__init__(self)
		self.label = QtWidgets.QLabel()
		self.setWidget(self.label)
		self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
		#self.label.setOpenExternalLinks(True)
		self.label.linkActivated.connect(self.label_activated_handler)

	def get_finished_count(self):
		cnt = 0
		for event in self.events:
			if event.complete:
				cnt = cnt + 1
		return cnt

	def set_events(self, apmts):
		self.events = convert_outlook_events_to_native_events(apmts)

	def update_label(self):
		finished = str(self.get_finished_count())
		total = str(len(self.events))
		self.label.setText(finished + '/' + '<a href="#total_' + total + '">'
						   + total + '</a>')

	def label_activated_handler(self, text):
		self.table = QtWidgets.QTableView()
		self.table_model = TableModel(self.events)
		self.table.setModel(self.table_model)
		self.table_model.itemChanged.connect(self.table_item_changed_handler)

		self.table.show()

	def set_date(self, date):
		self.date = date
		self.setWindowTitle(self.date.strftime('%m/%d/%Y'))
	
	def table_item_changed_handler(self, item):
		event = self.events[item.row()]
		if item.column() == 0:
			event.update_subject(item.data(0))
		elif item.column() == 1:
			event.update_desc(item.data(0))
		elif item.column() == 2:
			event.update_desc(item.data(0))

	

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
