# -*- coding: utf-8 -*-
import os
import platform
from shutil import copyfile
from PyQt6 import QtGui, QtWidgets

from src.Boxes import show_box
from model.AppModel import AppModel
from controller.AppController import AppController
from controller.ReportController import ReportController
from controller.LoginController import LoginController


app_controller = AppController()
login_controller = LoginController()
report_controller = ReportController()
model = AppModel()
app_controller.create()


def role_control(window):
    level = login_controller.get_access_level()

    if level == 'COMUM' or level == None:
        window.btn_add.setVisible(False)
        window.btn_edit.setVisible(False)
        window.btn_save.setVisible(False)
        window.btn_cancel.setVisible(False)
        window.btn_delete.setVisible(False)

    elif level == 'GERENTE':
        window.btn_delete.setVisible(False)


def load_window(window):
    registers = app_controller.get_total()

    if registers < 1:
        window.txt_index.setMinimum(0)
        window.txt_index.setMaximum(0)
        handle_navigation(window, False)
        window.tab_voluntary.setEnabled(False)
        window.tab_company.setEnabled(False)
        window.btn_delete.setEnabled(False)
        window.btn_print.setEnabled(False)
        window.btn_edit.setEnabled(False)
    else:
        window.txt_index.setValue(1)
        window.txt_index.setMinimum(1)
        window.txt_index.setMaximum(registers)
        handle_fields(window, 'fill')
        handle_navigation(window, True)


def validate_fields(model):
    for key, value in model.__dict__.items():
        if value:
            match key:
                case '_mobile_phone':
                    minimum_length = 15
                case '_cpf':
                    minimum_length = 14
                case '_birth_date':
                    minimum_length = 10
                case _:
                    minimum_length = 1

            if len(value) < minimum_length:
                return False

    return True


def handle_navigation(window, status, mode):
    if status:
        window.tab_voluntary.setEnabled(False)
        window.tab_company.setEnabled(False)
        window.btn_search.setEnabled(True)
        window.txt_search.setReadOnly(False)
        window.txt_index.setReadOnly(False)
    else:
        window.tab_voluntary.setEnabled(True)
        window.tab_company.setEnabled(True)
        window.btn_search.setEnabled(False)
        window.txt_search.setReadOnly(True)
        window.txt_index.setReadOnly(True)

    if mode == 'writing':
        window.btn_add.setEnabled(False)
        window.btn_edit.setEnabled(False)
        window.btn_delete.setEnabled(False)
        window.btn_print.setEnabled(False)
        window.btn_cancel.setEnabled(True)
        window.btn_save.setEnabled(True)

        window.txt_name.setFocus()
    else:
        window.btn_add.setEnabled(True)
        window.btn_edit.setEnabled(True)
        window.btn_delete.setEnabled(True)
        window.btn_print.setEnabled(True)
        window.btn_cancel.setEnabled(False)
        window.btn_save.setEnabled(False)


def handle_fields(window, action):
    if action == 'empty' or window.txt_index.value() == 0:
        main_window = window.pic_box.window()

        window.pic_box.clear()
        window.lbl_register.setText('')

        for field in main_window.findChildren(QtWidgets.QLineEdit):
            field.setText('')

    else:
        if window.txt_index.value() != 0:
            response = app_controller.select(window.txt_index.value())

            path = f'assets/pictures/{response[1]}.jpg'
            if platform.system() == 'Windows':
                path = path.replace('/', '\\')

            try:
                if os.path.exists(path):
                    image = QtGui.QPixmap(path)
                    window.pic_box.setPixmap(image)
            except:
                pass

            window.lbl_register.setText('Registrado em:\n' + response[2])
            window.txt_name.setText(response[3])
            window.txt_father.setText(response[4])
            window.txt_mother.setText(response[5])
            window.txt_address.setText(response[6])
            window.txt_number.setText(response[7])
            window.txt_complement.setText(response[8])
            window.txt_neighbourhood.setText(response[9])
            window.txt_city.setText(response[10])
            window.cmb_state.setCurrentText(response[11])
            window.txt_postal_code.setText(response[12])
            window.txt_home_phone.setText(response[13])
            window.txt_mobile_phone.setText(response[14])
            window.txt_cpf.setText(response[15])
            window.txt_home_town.setText(response[16])
            window.cmb_home_state.setCurrentText(response[17])
            window.txt_birth_date.setText(response[18])
            window.cmb_civil_state.setCurrentText(response[19])
            window.cmb_gender.setCurrentText(response[20])
            window.txt_scholarship.setText(response[21])
            window.txt_email.setText(response[22])
            window.cmb_course.setCurrentText(response[23])
            window.txt_company_name.setText(response[24])
            window.txt_company_time.setText(response[25])
            window.txt_ocupation.setText(response[26])
            window.txt_company_address.setText(response[27])
            window.txt_company_neighbourhood.setText(response[28])
            window.txt_company_number.setText(response[29])
            window.txt_company_city.setText(response[30])
            window.cmb_company_state.setCurrentText(response[31])
            window.txt_company_postal_code.setText(response[32])
            window.txt_company_phone.setText(response[33])


def btn_add_clicked(window):
    handle_navigation(window, False, 'writing')
    handle_fields(window, 'empty')
    window.status = 'adding'


def btn_edit_clicked(window):
    handle_navigation(window, False, 'writing')
    window.status = 'editing'


def btn_cancel_clicked(window):
    handle_navigation(window, True, 'reading')
    window.status = None

    try:
        handle_fields(window, 'fill')

    except:
        handle_fields(window, 'empty')


def btn_save_clicked(window):
    import random
    import string
    import datetime

    date = datetime.datetime.now().strftime('%d/%m/%Y')
    model.unique_id = ''.join(
        random.choices(
            string.ascii_lowercase + string.digits, k=16
        )
    )

    model.name = window.txt_name.text().strip().upper()
    model.father = window.txt_father.text()
    model.mother = window.txt_mother.text()
    model.address = window.txt_address.text()
    model.number = window.txt_number.text()
    model.complement = window.txt_complement.text()
    model.neighbourhood = window.txt_neighbourhood.text()
    model.city = window.txt_city.text()
    model.state = window.cmb_state.currentText()
    model.postal_code = window.txt_postal_code.text()
    model.home_phone = window.txt_home_phone.text()
    model.mobile_phone = window.txt_mobile_phone.text()
    model.cpf = window.txt_cpf.text()
    model.home_town = window.txt_home_town.text()
    model.home_state = window.cmb_home_state.currentText()
    model.birth_date = window.txt_birth_date.text()
    model.civil_state = window.cmb_civil_state.currentText()
    model.gender = window.cmb_gender.currentText()
    model.scholarship = window.txt_scholarship.text()
    model.email = window.txt_email.text()
    model.course = window.cmb_course.currentText()
    model.company_name = window.txt_company_name.text()
    model.company_time = window.txt_company_time.text()
    model.ocupation = window.txt_ocupation.text()
    model.company_address = window.txt_company_address.text()
    model.company_neighbourhood = window.txt_company_neighbourhood.text()
    model.company_number = window.txt_company_number.text()
    model.company_city = window.txt_company_city.text()
    model.company_state = window.cmb_company_state.currentText()
    model.company_postal_code = window.txt_company_postal_code.text()
    model.company_phone = window.txt_company_phone.text()

    if not validate_fields(model):
        show_box(
            'ATENÇÃO',
            '''Alguns campos não foram preenchidos corretamente.\nPreencha-os e tente novamente.'''
        )
    else:
        choice = show_box('SELEÇÃO', 'Deseja salvar as alterações?')

        if choice == 'yes':
            if window.status == 'adding':
                new_total = app_controller.insert(model, date)
                window.txt_index.setMaximum(new_total)
                window.txt_index.setMinimum(1)

            elif window.status == 'editing':
                app_controller.update(model, window.txt_index.value())

            choice = show_box(
                'SELEÇÃO',
                'Deseja adicionar uma foto desse voluntário?'
            )

            if choice == 'yes':
                import platform
                import os

                dialog = QtWidgets.QFileDialog()
                file = dialog.getOpenFileName(
                    dialog,
                    'Selecionar imagem',
                    os.path.expanduser('~'),
                    'Arquivos de imagem (*.jpeg *.jpg *.png)'
                )

                if file[0] != '':
                    path = './assets/pictures' if platform.system() == 'Linux' else '.\\assets\\pictures'
                    os.makedirs(path, exist_ok=True)

                    copyfile(
                        file[0],
                        f'{path}/{model.unique_id}.jpg'
                    )

                    image = QtGui.QPixmap(f'{path}/{model.unique_id}.jpg')
                    window.pic_box.setPixmap(image)

                    show_box(
                        'ADICIONAR FOTO',
                        f'Imagem adicionada para o voluntário <{model.name}>!'
                    )

            btn_cancel_clicked(window)


def btn_delete_clicked(window):
    choice = show_box(
        'SELEÇÃO',
        f'Deseja excluir o registro de <{window.txt_name.text()}>?'
    )

    if choice == 'yes':
        app_controller.delete(window.txt_index.value())

        load_window(window)
        handle_fields(window, 'fill')


def btn_search_clicked(window):
    if window.txt_search.text().strip() == '':
        report_controller.gen_xlsx()

    else:
        app_controller.id_search(window.txt_search.text().strip().upper())


def btn_print_clicked(window):
    try:
        report_controller.gen_contract(window.txt_index.value())
    except Exception as e:
        show_box('ERRO', e)
