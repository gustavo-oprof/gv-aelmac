# -*- coding: utf-8 -*-
from src.Crypt import *
from src.Boxes import show_box
from src.Connection import Connection

db = Connection()


class AppController:
    def create(self):
        try:
            create_table_string = '''
                CREATE TABLE IF NOT EXISTS voluntaries (
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
                )
            '''

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
            encrypted_data = cursor.execute(f'SELECT * FROM voluntaries WHERE id = {index}').fetchone()
            data = []
            i = 0
            
            while i < len(encrypted_data):
                if i < 4:
                    data.append(encrypted_data[i])
                else:
                    data.append(decrypt(encrypted_data[i]))

                i += 1

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
                '{crypt(model.father)}',
                '{crypt(model.mother)}',
                '{crypt(model.address)}',
                '{crypt(model.number)}',
                '{crypt(model.complement)}',
                '{crypt(model.neighbourhood)}',
                '{crypt(model.city)}',
                '{crypt(model.state)}',
                '{crypt(model.postal_code)}',
                '{crypt(model.home_phone)}',
                '{crypt(model.mobile_phone)}',
                '{crypt(model.cpf)}',
                '{crypt(model.home_town)}',
                '{crypt(model.home_state)}',
                '{crypt(model.birth_date)}',
                '{crypt(model.civil_state)}',
                '{crypt(model.gender)}',
                '{crypt(model.scholarship)}',
                '{crypt(model.email)}',
                '{crypt(model.course)}',
                '{crypt(model.company_name)}',
                '{crypt(model.ocupation)}',
                '{crypt(model.company_time)}',
                '{crypt(model.company_address)}',
                '{crypt(model.company_neighbourhood)}',
                '{crypt(model.company_number)}',
                '{crypt(model.company_city)}',
                '{crypt(model.company_state)}',
                '{crypt(model.company_postal_code)}',
                '{crypt(model.company_phone)}'
            )'''

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
            nome_do_pai = '{crypt(model.father)}',
            nome_da_mae = '{crypt(model.mother)}',
            endereco = '{crypt(model.address)}',
            numero = '{crypt(model.number)}',
            complemento = '{crypt(model.complement)}',
            bairro = '{crypt(model.neighbourhood)}',
            cidade = '{crypt(model.city)}',
            estado = '{crypt(model.state)}',
            cep = '{crypt(model.postal_code)}',
            telefone_residencial = '{crypt(model.home_phone)}',
            telefone_celular = '{crypt(model.mobile_phone)}',
            cpf = '{crypt(model.cpf)}',
            cidade_natal = '{crypt(model.home_town)}',
            estado_natal = '{crypt(model.home_state)}',
            data_de_nascimento = '{crypt(model.birth_date)}',
            estado_civil = '{crypt(model.civil_state)}',
            genero = '{crypt(model.gender)}',
            escolaridade = '{crypt(model.scholarship)}',
            email = '{crypt(model.email)}',
            cursando = '{crypt(model.course)}',
            empresa = '{crypt(model.company_name)}',
            ocupacao = '{crypt(model.ocupation)}',
            tempo_de_empresa = '{crypt(model.company_time)}',
            endereco_empresa = '{crypt(model.company_address)}',
            bairro_empresa = '{crypt(model.company_neighbourhood)}',
            numero_empresa = '{crypt(model.company_number)}',
            cidade_empresa = '{crypt(model.company_city)}',
            estado_empresa = '{crypt(model.company_state)}',
            cep_empresa = '{crypt(model.company_postal_code)}',
            telefone_empresa = '{crypt(model.company_phone)}'
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
            
            return cursor.execute('SELECT COUNT(*) FROM voluntaries').fetchone()[0]

        except Exception as e:
            show_box('ERRO', e)

        finally:
            db.close_connection()

    def delete(self, index):
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            cursor.execute(f'DELETE FROM voluntaries WHERE id = {index}')

            cursor.execute(f'UPDATE voluntaries SET id = id - 1 WHERE id > {index}')

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
                f"SELECT id, nome FROM voluntaries WHERE nome LIKE '%{(word)}%'"
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
