# -*- coding: utf-8 -*-
from src.Crypt import hash_query
from src.Boxes import show_box
from src.Connection import Connection


db = Connection()


class LoginController():
    def create(self):
        try:
            create_table_string = '''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT NOT NULL PRIMARY KEY,
                user TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                level TEXT NOT NULL,
                status TEXT
            )'''

            conn = db.create_connection()
            cursor = conn.cursor()
            cursor.execute(create_table_string)
        except Exception as e:
            show_box('ERRO', e)

        finally:
            db.close_connection()


    def insert(self, user, password, level):
        try:
            user_id = hash_query(user)
            password = hash_query(password)

            conn = db.create_connection()
            cursor = conn.cursor()

            cursor.execute(
                f'''INSERT INTO users VALUES (
                    '{user_id}',
                    '{user}',
                    '{password}',
                    '{level}',
                    'OFF'
                )'''
            )
            conn.commit()

            show_box('SUCESSO', 'Usuário criado com sucesso!')

        except Exception as e:
            show_box('ERRO', e)

        finally:
            db.close_connection()


    def login(self, username, password):
        try:
            id = hash_query(username)
            password = hash_query(password)

            conn = db.create_connection()
            cursor = conn.cursor()
            user_data = cursor.execute(f'SELECT user, password FROM users WHERE id = \'{id}\'').fetchone()

            if user_data is None:
                return 'USER NOT FOUND'
                
            if password != user_data[1]:
                return 'WRONG PASSWORD'
            else:
                cursor.execute(f'UPDATE users SET status = \'ON\' WHERE id = \'{id}\'')
                conn.commit()
                return 'OK'
                
        except Exception as e:
            show_box('ERRO', e)


        finally:
            db.close_connection()

    def get_access_level(self):
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            level = cursor.execute('SELECT level FROM users WHERE status = \'ON\'').fetchone()[0]

            return level

        except Exception as e:
            show_box('ERRO', e)

        finally:
            db.close_connection()

    def reset_status(self):
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET status = \'OFF\'')
            conn.commit()          
                
        except Exception as e:
            show_box('ERRO', e)

        finally:
            db.close_connection()