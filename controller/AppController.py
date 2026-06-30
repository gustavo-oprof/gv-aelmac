# -*- coding: utf-8 -*-
from src.Boxes import show_box
from src.Connection import Connection

db = Connection()


class AppController:
    def create(self):
        try:
            create_table_string = '''CREATE TABLE IF NOT EXISTS voluntaries (
                id INTEGER PRIMARY KEY NOT NULL,
                codigo_unico TEXT UNIQUE NOT NULL,
                registrado TEXT NOT NULL,
                nome TEXT NOT NULL,
                nome_do_pai TEXT NOT NULL,
                nome_da_mae TEXT NOT NULL,
                endereco TEXT NOT NULL,
                numero TEXT NOT NULL,
                complemento TEXT,
                bairro TEXT NOT NULL,
                cidade TEXT NOT NULL,
                estado TEXT NOT NULL,
                cep TEXT NOT NULL,
                telefone_residencial TEXT,
                telefone_celular TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                cidade_natal TEXT,
                estado_natal TEXT,
                data_de_nascimento TEXT NOT NULL,
                estado_civil TEXT,
                genero TEXT,
                escolaridade TEXT,
                email TEXT UNIQUE,
                cursando TEXT,
                empresa TEXT,
                ocupacao TEXT,
                tempo_de_empresa TEXT,
                endereco_empresa TEXT,
                bairro_empresa TEXT,
                numero_empresa TEXT,
                cidade_empresa TEXT,
                estado_empresa TEXT,
                cep_empresa TEXT,
                telefone_empresa TEXT
            )'''

            conn = db.create_connection()
            cursor = conn.cursor()
            cursor.execute(create_table_string)
        except Exception as e:            
            show_box('ERRO', e)

        finally:
            db.close_connection()

    def select(self, index):
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            data = cursor.execute(f'SELECT * FROM voluntaries WHERE id = {index}').fetchone()

            return data

        except Exception as e:
            show_box('ERRO', e)

        finally:
            db.close_connection()

    def insert(self, model, date):
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            voluntary_id = cursor.execute(
                'SELECT COUNT(*) FROM voluntaries'
            ).fetchone()[0] + 1

            insert_string = f'''INSERT INTO voluntaries VALUES(
            {voluntary_id},
            '{model.unique_id}',
            '{date}',
            '{model.name}',
            '{model.father}',
            '{model.mother}',
            '{model.address}',
            '{model.number}',
            '{model.complement}',
            '{model.neighbourhood}',
            '{model.city}',
            '{model.state}',
            '{model.postal_code}',
            '{model.home_phone}',
            '{model.mobile_phone}',
            '{model.cpf}',
            '{model.home_town}',
            '{model.home_state}',
            '{model.birth_date}',
            '{model.civil_state}',
            '{model.gender}',
            '{model.scholarship}',
            '{model.email}',
            '{model.course}',
            '{model.company_name}',
            '{model.ocupation}',
            '{model.company_time}',
            '{model.company_address}',
            '{model.company_neighbourhood}',
            '{model.company_number}',
            '{model.company_city}',
            '{model.company_state}',
            '{model.company_postal_code}',
            '{model.company_phone}')'''

            cursor.execute(insert_string)
            conn.commit()

            show_box(
                'SUCESSO',
                'Registro de voluntário criado com sucesso!'
            )

            return voluntary_id

        except Exception as e:
            show_box('ERRO', e)

        finally:
            db.close_connection()

    def update(self, model, index):
        try:
            conn = db.create_connection()
            cursor = conn.cursor()

            update_string = f'''UPDATE voluntaries SET             
            nome = '{model.name}',
            nome_do_pai = '{model.father}',
            nome_da_mae = '{model.mother}',
            endereco = '{model.address}',
            numero = '{model.number}',
            complemento = '{model.complement}',
            bairro = '{model.neighbourhood}',
            cidade = '{model.city}',
            estado = '{model.state}',
            cep = '{model.postal_code}',
            telefone_residencial = '{model.home_phone}',
            telefone_celular = '{model.mobile_phone}',
            cpf = '{model.cpf}',
            cidade_natal = '{model.home_town}',
            estado_natal = '{model.home_state}',
            data_de_nascimento = '{model.birth_date}',
            estado_civil = '{model.civil_state}',
            genero = '{model.gender}',
            escolaridade = '{model.scholarship}',
            email = '{model.email}',
            cursando = '{model.course}',
            empresa = '{model.company_name}',
            ocupacao = '{model.ocupation}',
            tempo_de_empresa = '{model.company_time}',
            endereco_empresa = '{model.company_address}',
            bairro_empresa = '{model.company_neighbourhood}',
            numero_empresa = '{model.company_number}',
            cidade_empresa = '{model.company_city}',
            estado_empresa = '{model.company_state}',
            cep_empresa = '{model.company_postal_code}',
            telefone_empresa = '{model.company_phone}'
            WHERE id = {index}'''

            cursor.execute(update_string)
            conn.commit()

            show_box(
                'SUCESSO',
                'Registro de voluntário editado com sucesso!'
            )

        except Exception as e:
            show_box('ERRO', e)

        finally:
            db.close_connection()

    def get_total(self):
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            total = cursor.execute(
                'SELECT COUNT(*) FROM voluntaries'
            ).fetchone()[0]

            return total

        except Exception as e:
            show_box('ERRO', e)

        finally:
            db.close_connection()

    def delete(self, index):
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            cursor.execute(f'DELETE FROM voluntaries WHERE id = {index}')

            cursor.execute(
                f'UPDATE voluntaries SET id = id - 1 WHERE id > {index}')

            conn.commit()

            show_box('SUCESSO', 'Registro deletado com sucesso!')

        except Exception as e:
            show_box('ERRO', e)

        finally:
            db.close_connection()

    def id_search(self, word):
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            result = cursor.execute(
                f"SELECT id, nome FROM voluntaries WHERE nome LIKE '%{word}%'"
            ).fetchall()

            if result == []:
                show_box(
                    'ATENÇÃO',
                    'Não foram encontrados resultados com o termo utilizado.'
                )

            else:
                message = ''

                for row in result:
                    for column in row:
                        message += str(column)
                        message += ' - '

                    message = message[:-3]
                    message += '\n\n'

                show_box('PESQUISA', message)

        except Exception as e:
            show_box('ERRO', e)

        finally:
            db.close_connection()
