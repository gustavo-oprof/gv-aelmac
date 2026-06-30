# -*- coding: utf-8 -*-
from PyQt6 import QtWidgets

from src.Boxes import show_box
from controller.LoginController import LoginController

controller = LoginController()
controller.create()
controller.reset_status()

def create(window):
    from view.RegisterWindow import Ui_MainWindow

    QtWidgets.QApplication.activeWindow().close()

    window.Register = QtWidgets.QMainWindow()
    window.ui = Ui_MainWindow()
    window.ui.setupUi(window.Register)
    window.Register.show()


def login(window):
    this_window = QtWidgets.QApplication.activeWindow()

    user = window.txt_user.text().strip()
    password = window.txt_password.text().strip()
    
    response = controller.login(user, password)

    if response == 'USER NOT FOUND':
        show_box('ERRO', 'O usuário informado não existe.')
    elif response == 'WRONG PASSWORD':
        show_box('ERRO', 'Senha incorreta para o usuário informado')
    else:
        from view.AppWindow import Ui_MainWindow
        this_window.close()

        window.App = QtWidgets.QMainWindow()
        window.ui = Ui_MainWindow()
        window.ui.setupUi(window.App)
        window.App.show()
