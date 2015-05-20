import configparser
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from main_ui import MainUI
from system_tray import SystemTray


def main():

	config = configparser.ConfigParser()
	config.read('../config/config.ini')

	app = QtWidgets.QApplication(sys.argv)
	#with open(config['Main']['skin_path']) as f:
	#	app.setStyleSheet(f.read())

	tray_icon_widget = QtWidgets.QWidget()
	tray_icon = SystemTray(QtGui.QIcon("..\pics\icon.png"), tray_icon_widget)

	main_ui = MainUI()
	main_ui.set_layout_mode(config['Main']['layout'])
	main_ui.setWindowOpacity(float(config['Main']['opacity']))
	main_ui.set_display_mode(config['Main']['display_mode'])

	tray_icon.set_main_ui(main_ui)
	tray_icon.show()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
