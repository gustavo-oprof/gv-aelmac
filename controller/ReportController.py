# -*- coding: utf-8 -*-
import os
import pandas
import platform
from pypdf import PdfReader, PdfWriter

from src.Boxes import show_box
from src.Connection import Connection


db = Connection()


class ReportController:
    def gen_contract(self, index):
        try:
            path = f'{os.path.expanduser('~')}/Documentos/CONTRATOS_DE_VOLUNTARIOS'

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
            result = cursor.execute(
                f'SELECT * FROM voluntaries WHERE id = {index}').fetchone()

            reader = PdfReader(
                f'{os.path.dirname(os.path.abspath('__main__'))}/assets/contract/contrato.pdf')
            writer = PdfWriter()

            writer.clone_reader_document_root(reader)

            writer.update_page_form_field_values(
                writer.pages[0],
                {
                    'nome': result[3],
                    'cpf': result[15]
                },
            )

            os.makedirs(path, exist_ok=True)
            writer.write(f'{path}/Contrato_de_' + result[3] + '.pdf')

            show_box('SUCESSO', 'Contrato de voluntariado gerado com sucesso!')

        except Exception as e:
            show_box('ERRO', e)

        finally:
            db.close_connection()

    def gen_xlsx(self):
        try:
            select_string = 'SELECT * FROM voluntaries'

            conn = db.create_connection()
            data_frame = pandas.read_sql_query(select_string, conn)

            path = f'{os.path.expanduser('~')}/Documentos/PLANILHA_DE_VOLUNTARIOS.xlsx'
            if platform.system() != 'Linux':
                path = path.replace(
                    '/',
                    '\\'
                ).replace(
                    'Documentos',
                    'Documents'
                )

            data_frame.to_excel(path, index=False)

            show_box(
                'SUCESSO',
                'Planilha de voluntários gerada na pasta de documentos.'
            )

        except Exception as e:
            show_box('ERRO', e)

        finally:
            db.close_connection()
