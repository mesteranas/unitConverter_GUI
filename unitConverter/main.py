import sys
from custome_errors import *
sys.excepthook = my_excepthook
import update
import gui
import guiTools
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
language.init_translation()
conversions = {
    'Length': {
        'Meters to Feet': lambda x: x * 3.28084,
        'Feet to Meters': lambda x: x / 3.28084
    },
    'Weight': {
        'Kilograms to Pounds': lambda x: x * 2.20462,
        'Pounds to Kilograms': lambda x: x / 2.20462
    },
    'Temperature': {
        'Celsius to Fahrenheit': lambda x: (x * 9/5) + 32,
        'Fahrenheit to Celsius': lambda x: (x - 32) * 5/9
    }
}

class main (qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(app.name + _("version : ") + str(app.version))
        layout=qt.QVBoxLayout()
        self.unit_type_combo = qt.QComboBox()
        self.unit_type_combo.addItems(conversions.keys())
        self.unit_type_combo.currentIndexChanged.connect(self.update_conversion_options)
        
        self.conversion_combo = qt.QComboBox()
        self.update_conversion_options()  # Initialize with first unit type
        
        self.value_input = qt.QLineEdit()
        self.value_input.setPlaceholderText('Enter value')
        
        self.result_label = qt.QLabel('Result: ')
        
        self.convert_button = guiTools.QPushButton('Convert')
        self.convert_button.clicked.connect(self.convert_units)
        
        layout.addWidget(self.unit_type_combo)
        layout.addWidget(self.conversion_combo)
        layout.addWidget(self.value_input)
        layout.addWidget(self.convert_button)
        layout.addWidget(self.result_label) 
        self.setting=guiTools.QPushButton(_("settings"))
        self.setting.clicked.connect(lambda: settings(self).exec())
        layout.addWidget(self.setting)
        w=qt.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

        mb=self.menuBar()
        help=mb.addMenu(_("help"))
        helpFile=qt1.QAction(_("help file"),self)
        help.addAction(helpFile)
        helpFile.triggered.connect(lambda:guiTools.HelpFile())
        helpFile.setShortcut("f1")
        cus=help.addMenu(_("contact us"))
        telegram=qt1.QAction("telegram",self)
        cus.addAction(telegram)
        telegram.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/mesteranasm"))
        telegramc=qt1.QAction(_("telegram channel"),self)
        cus.addAction(telegramc)
        telegramc.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/tprogrammers"))
        githup=qt1.QAction(_("Github"),self)
        cus.addAction(githup)
        githup.triggered.connect(lambda: guiTools.OpenLink(self,"https://Github.com/mesteranas"))
        X=qt1.QAction(_("x"),self)
        cus.addAction(X)
        X.triggered.connect(lambda:guiTools.OpenLink(self,"https://x.com/mesteranasm"))
        email=qt1.QAction(_("email"),self)
        cus.addAction(email)
        email.triggered.connect(lambda: guiTools.sendEmail("anasformohammed@gmail.com","project_type=GUI app={} version={}".format(app.name,app.version),""))
        Github_project=qt1.QAction(_("visite project on Github"),self)
        help.addAction(Github_project)
        Github_project.triggered.connect(lambda:guiTools.OpenLink(self,"https://Github.com/mesteranas/{}".format(settings_handler.appName)))
        Checkupdate=qt1.QAction(_("check for update"),self)
        help.addAction(Checkupdate)
        Checkupdate.triggered.connect(lambda:update.check(self))
        licence=qt1.QAction(_("license"),self)
        help.addAction(licence)
        licence.triggered.connect(lambda: Licence(self))
        donate=qt1.QAction(_("donate"),self)
        help.addAction(donate)
        donate.triggered.connect(lambda:guiTools.OpenLink(self,"https://www.paypal.me/AMohammed231"))
        about=qt1.QAction(_("about"),self)
        help.addAction(about)
        about.triggered.connect(lambda:qt.QMessageBox.information(self,_("about"),_("{} version: {} description: {} developer: {}").format(app.name,str(app.version),app.description,app.creater)))
        self.setMenuBar(mb)
        if settings_handler.get("update","autoCheck")=="True":
            update.check(self,message=False)
    def closeEvent(self, event):
        if settings_handler.get("g","exitDialog")=="True":
            m=guiTools.ExitApp(self)
            m.exec()
            if m:
                event.ignore()
        else:
            self.close()
    def update_conversion_options(self):
        unit_type = self.unit_type_combo.currentText()
        self.conversion_combo.clear()
        self.conversion_combo.addItems(conversions[unit_type].keys())
    def convert_units(self):
        try:
            unit_type = self.unit_type_combo.currentText()
            conversion = self.conversion_combo.currentText()
            value = float(self.value_input.text())
            result = conversions[unit_type][conversion](value)
            self.result_label.setText(f"Result: {str(result)}")
        except ValueError:
            self.result_label.setText("Please enter a valid number.")
App=qt.QApplication([])
w=main()
w.show()
App.setStyle('fusion')
App.exec()