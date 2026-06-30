# -*- coding: utf-8 -*-
import os
import platform
from pypdf import PdfReader, PdfWriter

from src.Crypt import decrypt
from src.Boxes import show_box
from src.Connection import Connection


db = Connection()


class ReportController:
    def gen_contract(self, index):
        try:
            path = f'{os.path.expanduser('~')}/Documentos/CONTRATOS_DE_VOLUNTARIOS'
            template = f'{os.path.dirname(os.path.abspath('__main__'))}/assets/contract/contrato.pdf'

            if platform.system() == 'Windows':
                path = path.replace(
                    '/',
                    '\\'
                ).replace(
                    'Documentos',
                    'Documents'
                )

            conn = db.create_connection()
            cursor = conn.cursor()
            result = cursor.execute(f'SELECT * FROM voluntaries WHERE id = {index}').fetchone()

            reader = PdfReader(template)
            writer = PdfWriter()

            writer.clone_reader_document_root(reader)

            writer.update_page_form_field_values(
                writer.pages[0],
                {
                    'nome': result[3],
                    'cpf': decrypt(result[15])
                },
            )

            os.makedirs(path, exist_ok=True)
            writer.write(f'{path}/Contrato_de_' + result[3].replace(' ','_') + '.pdf')

            show_box('SUCESSO', 'Contrato de voluntariado gerado com sucesso!')

        except Exception as e:
            show_box('ERRO', e)

        finally:
            db.close_connection()

