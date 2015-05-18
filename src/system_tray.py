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
		screen = QtWidgets.QApplication.desktop().screenGeometry()
		self.setGeometry(screen.width() - 100, 100, 50, 400)
		self.menuBar().hide()
		self.centralWidget = QtWidgets.QWidget()
		self.setCentralWidget(self.centralWidget)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.outlooker = Outlooker()

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
			apmts = self.outlooker.get_events_start_from(tmp_date)
			day = Day(self, tmp_date, apmts)
			day.update_label()
			self.centralWidget.layout().addWidget(day)
	

class DayDetail(QtWidgets.QFrame):

	def __init__(self, parent):
		QtWidgets.QFrame.__init__(self)
		self.parent = parent

		self.layout = QtWidgets.QVBoxLayout()

		self.group = QtWidgets.QGroupBox()
		self.box_layout = QtWidgets.QHBoxLayout()
		self.add_button = QtWidgets.QPushButton()
		self.del_button = QtWidgets.QPushButton()
		self.add_button.setText("Add")
		self.del_button.setText("Del")
		self.box_layout.addWidget(self.add_button)
		self.box_layout.addWidget(self.del_button)
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
		self.subject_text = QtWidgets.QLineEdit()
		desc_label = QtWidgets.QLabel('Description')
		self.desc_text = QtWidgets.QLineEdit()
		date_label = QtWidgets.QLabel('Date')
		self.date_text = QtWidgets.QLineEdit()
		self.date_text.setText(date.today().strftime("%m/%d/%Y"))
		#self.date_text.textChanged.connect(self.date_select_handler)
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
		pass

	def date_select_handler(self):
		pass
		#self.calendar = QtWidgets.QCalendarWidget()
		#self.calendar.show()
		#self.calendar.clicked.connect(self.fill_date_handler)
	
	def fill_date_handler(self, date):
		pass

	def show(self):
		parent_point = self.parent.mapToGlobal(QtCore.QPoint(self.parent.x(), self.parent.y()))
		self.setGeometry(parent_point.x() - self.width(),
						 parent_point.y(), self.width(),
						 self.height())
		super(DayDetail, self).show()

	def setModel(self, model):
		self.table_view.setModel(model)


class Day(QtWidgets.QDockWidget):

	def __init__(self, parent, date, apmts):
		QtWidgets.QDockWidget.__init__(self, parent)
		self.label = QtWidgets.QLabel()
		self.setWidget(self.label)
		self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
		#self.label.setOpenExternalLinks(True)
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
		#self.table = QtWidgets.QTableView()
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

	
def main():

	config = configparser.ConfigParser()
	config.read('../config/config.ini')

	app = QtWidgets.QApplication(sys.argv)
	#with open(config['Main']['skin_path']) as f:
	#	app.setStyleSheet(f.read())

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
