# -*- coding: utf-8 -*-
from PyQt6 import QtWidgets

from src.Boxes import show_box
from controller.RegisterController import RegisterController

controller = RegisterController()
controller.create()


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
        if password != window.txt_confirm.text().strip():
            show_box('ERRO', 'As senhas não coincidem.')

        else:
            verification = controller.select(user)

            if verification:
                show_box(
                    'ERRO',
                    '''Já existe um usuário com este nome.
                    \nPor favor, escolha outro nome.'''
                )

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
