# -*- coding: utf-8 -*-
from PyQt6 import QtWidgets

from src.Boxes import show_box
from controller.LoginController import LoginController

controller = LoginController()


def create(window):
    this_window = QtWidgets.QApplication.activeWindow()

    user = window.txt_user.text().strip()
    password = window.txt_password.text().strip()
    level = window.cmb_level.currentText()

    if len(password) < 8:
        show_box(
            'ERRO',
            '''A senha digitada é muito pequena.
            \nDigite uma senha com ao menos 8 caracteres.'''
        )

    else:
        if window.txt_password.text().strip() != window.txt_confirm.text().strip():
            show_box('ERRO', 'As senhas não coincidem.')

        else:
            controller.insert(user, password, level)

            choice = show_box(
                'SELEÇÃO',
                'Deseja retornar para a tela de login?'
            )

            if choice == 'yes':
                from view.LoginWindow import Ui_MainWindow
                this_window.close()

                window.Login = QtWidgets.QMainWindow()
                window.ui = Ui_MainWindow()
                window.ui.setupUi(window.Login)
                window.Login.show()
