import configparser
import psycopg2
import re

class Database:
    def __init__(self, settings_file='settings.ini'):
        self.settings_file = settings_file
        self.conn = None
        self.load_settings()

    def load_settings(self):
        """Загрузка настроек из файла."""
        config = configparser.ConfigParser()
        config.read(self.settings_file, encoding='utf-8')

        self.database = config['Connection'].get('database') or input("Введите название базы данных: ")
        self.user = config['Connection'].get('user') or input("Введите имя пользователя базы данных: ")
        self.password = config['Connection'].get('password') or input("Введите пароль базы данных: ")

    def connect(self):
        """Соединение с базой данных."""
        try:
            self.conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")

    def close(self):
        """Закрытие соединения с базой данных."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def structure_database(self):
        """Создание структуры данных."""
        self.connect()

        try:
            with self.conn.cursor() as cur:
                # Удаление таблиц, если они существуют
                cur.execute('''
                    DROP TABLE IF EXISTS phones;
                    DROP TABLE IF EXISTS clients;
                ''')

                # Создание таблиц
                cur.execute('''
                     CREATE TABLE IF NOT EXISTS clients (
                        client_id SERIAL PRIMARY KEY,
                        first_name VARCHAR(40) NOT NULL,
                        last_name VARCHAR(40) NOT NULL,
                        email VARCHAR(100) NOT NULL UNIQUE
                    );
                ''')

                cur.execute('''
                    CREATE TABLE IF NOT EXISTS phones (
                        phone_id SERIAL PRIMARY KEY,
                        client_id INT NOT NULL REFERENCES clients(client_id) ON DELETE CASCADE,
                        phone VARCHAR(14) NOT NULL
                    );
                ''')

                self.conn.commit()
                print("Структура базы данных успешно создана.")
        except Exception as e:
            print(f"Произошла ошибка при работе с базой данных: {e}")
        finally:
            self.close()

    def create(self):
        self.structure_database()

    def add_new_client(self, first_name, last_name, email):
        """Добавление нового клиента."""
        self.connect()

        try:
            with self.conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO clients (first_name, last_name, email)
                    VALUES (%s, %s, %s) RETURNING client_id
                ''', (first_name, last_name, email))

                client_id = cur.fetchone()[0]
                self.conn.commit()
                return client_id
        except Exception as e:
            print(f"Произошла ошибка при добавлении нового клиента: {e}")
            return None
        finally:
            self.close()

    def add_phone(self, client_id, phone):
        """Добавление телефона созданного клиента."""
        self.connect()

        try:
            with self.conn.cursor() as cur:
                cur.execute('''
                        INSERT INTO phones (client_id, phone)
                        VALUES (%s, %s)
                    ''', (client_id, phone))
                self.conn.commit()
        except Exception as e:
            print(f"Произошла ошибка при добавлении телефона: {e}")
        finally:
            self.close()

    def add_new_entry(self):
        """Ввод данных клиента и телефонов."""
        first_name = input("Введите имя клиента: ")
        last_name = input("Введите фамилию клиента: ")
        email = input("Введите email клиента: ")

        # Добавление нового клиента и получение его ID
        client_id = self.add_new_client(first_name, last_name, email)

        if client_id is None:
            print("Не удалось добавить клиента.")
            return

        self.input_number_phone(client_id)

        print("Клиент и телефоны успешно добавлены.")

    def input_number_phone(self, client_id=None):
        if client_id is None:
            client_id = self.find_client_by_name()

        if client_id is None:
            print("Не удалось найти клиента.")
            return

        while True:
            phone = input("Введите номер телефона клиента (или нажмите Enter, чтобы завершить): ")
            if not phone:
                break

            # Преобразуем номер телефона
            cleaned_phone = self.clean_phone_number(phone)
            if cleaned_phone:
                self.add_phone(client_id, cleaned_phone)
                print(f"Добавлен номер: {cleaned_phone}")
            else:
                print("Введите корректный номер телефона.")

    def clean_phone_number(self, phone):
        """Очистка номера телефона, чтобы сохранить только цифры."""
        cleaned = re.sub(r'\D', '', phone)

        # Проверяем, что номер является валидным
        if cleaned.startswith('7') or cleaned.startswith('8'):
            return '7' + cleaned[1:]

        return cleaned

    def update(self, client_id, first_name=None, last_name=None, email=None):
        """Изменение данных о клиенте."""
        result = False
        self.connect()

        try:
            with self.conn.cursor() as cur:
                if first_name:
                    cur.execute('''
                        UPDATE clients SET first_name = %s WHERE client_id = %s
                    ''', (first_name, client_id))

                if last_name:
                    cur.execute('''
                        UPDATE clients SET last_name = %s WHERE client_id = %s
                    ''', (last_name, client_id))

                if email:
                    cur.execute('''
                        UPDATE clients SET email = %s WHERE client_id = %s
                    ''', (email, client_id))

                self.conn.commit()
                result = True
        except Exception as e:
            print(f"Произошла ошибка при изменении данных о клиенте: {e}")
        finally:
            self.close()

        return result

    def change_information_client(self, client_id=None):
        """Подготовка к изменению данных о клиенте."""
        if client_id is None:
            client_id = self.find_client_by_name()

        if client_id is None:
            print("Не удалось найти клиента.")
            return

        new_first_name = input("Введите новое имя клиента (или нажмите Enter, чтобы пропустить): ")
        new_last_name = input("Введите новую фамилию клиента (или нажмите Enter, чтобы пропустить): ")
        new_email = input("Введите новый email клиента (или нажмите Enter, чтобы пропустить): ")

        if not new_first_name and not new_last_name and not new_email:
            print("Изменения не произведены")
            return

        result = self.update(client_id, new_first_name if new_first_name else None,
                             new_last_name if new_last_name else None,
                             new_email if new_email else None)

        if result:
            print("Изменения успешно произведены")
        else:
            print("Произошла ошибка при обновлении информации о клиенте.")

    def delete_phone(self, client_id=None):
        """Удалить телефон для существующего клиента."""
        if client_id is None:
            client_id = self.find_client_by_name()

        if client_id is None:
            print("Не удалось найти клиента.")
            return

        phones = self.find_all_phone_client(client_id)

        if not phones:
            print("Нет телефонов для данного клиента.")
            return

        print("Номера телефонов клиента:")
        for phone_id, phone_number in phones:
            print(f"ID: {phone_id}, Номер: {phone_number}")

        phone_id = input("Введите удаляемый id телефона (или нажмите Enter, чтобы ввести номер): ")
        phone = input("Введите удаляемый номер телефона (или нажмите Enter, чтобы продолжить): ")

        if not phone_id and not phone:
            print("Произошла ошибка: не был введен ни номер, ни id телефона")
            return

        if phone_id and not self.check_id_existence(phones, int(phone_id)):
                print("Не удалось найти телефон с указанным id.")
                return

        self.connect()

        try:
            with self.conn.cursor() as cur:
                if phone_id:
                    cur.execute('DELETE FROM phones WHERE phone_id = %s', (phone_id,))
                    print(f"Телефон с id {phone_id} успешно удален.")
                elif phone:
                    cur.execute('DELETE FROM phones WHERE phone = %s', (phone,))
                    print(f"Телефон {phone} успешно удален.")
                self.conn.commit()
        except Exception as e:
            print(f"Произошла ошибка при удалении телефона: {e}")
        finally:
            self.close()

    def check_id_existence(self, phones, phone_id):
        """Проверить id на существование."""
        return any(id == phone_id for id, _ in phones)

    def find_all_phone_client(self, client_id):
        """Найти все телефоны клиента."""
        self.connect()

        try:
            with self.conn.cursor() as cur:
                cur.execute('SELECT phone_id, phone FROM phones WHERE client_id = %s', (client_id,))
                return cur.fetchall()
        except Exception as e:
            print(f"Произошла ошибка при поиске клиента: {e}")
            return []
        finally:
            self.close()

    def delete(self, client_id=None):
        """Удалить существующего клиента."""
        if client_id is None:
            client_id = self.find_client_by_name()

        if client_id is None:
            print("Не удалось найти клиента.")
            return

        warning = input(f"Данные с id {client_id}, введите \"ДА\" для подтверждения: ")
        if warning != "ДА":
            print("Операция отменена, введено не \"ДА\"")
            return

        self.connect()

        try:
            with self.conn.cursor() as cur:
                # Удаление телефонов клиента
                cur.execute('DELETE FROM phones WHERE client_id = %s', (client_id,))
                deleted_count = cur.rowcount
                self.conn.commit()

                if deleted_count > 0:
                    print(f"Успешно удалено {deleted_count} телефонов клиента с id {client_id}.")
                else:
                    print(f"Нет телефонов для удаления для клиента с id {client_id}.")

                # Удаление клиента
                cur.execute('DELETE FROM clients WHERE client_id = %s', (client_id,))
                deleted_client_count = cur.rowcount
                self.conn.commit()

                if deleted_client_count > 0:
                    print(f"Успешно удален клиент с id {client_id}.")
                else:
                    print(f"Клиент с id {client_id} не найден.")
        except Exception as e:
            print(f"Произошла ошибка при удалении клиента: {e}")
        finally:
            self.close()

    def find(self, query):
        """Найти клиента по его данным: имени, фамилии, email или телефону."""
        self.connect()

        try:
            with self.conn.cursor() as cur:
                cur.execute('''
                        SELECT * FROM clients WHERE first_name LIKE %s OR last_name LIKE %s OR email LIKE %s
                    ''', ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
                clients = cur.fetchall()

                if clients:
                    phones = self.find_all_phone_client(clients[0][0])
                else:
                    cur.execute('''
                            SELECT * FROM phones WHERE phone LIKE %s
                        ''', ('%' + query + '%',))
                    phones = cur.fetchall()
        except Exception as e:
            print(f"Произошла ошибка при поиске клиента: {e}")
            clients, phones = [], []  # Возвращаем пустые списки при ошибке
        finally:
            self.close()
        return clients, phones

    def find_client_by_name(self):
        """Поиск клиента по имени и фамилии."""
        first_name = input("Введите имя искомого клиента: ")
        last_name = input("Введите фамилию искомого клиента: ")

        self.connect()

        try:
            with self.conn.cursor() as cur:
                cur.execute('''
                        SELECT client_id FROM clients WHERE first_name = %s AND last_name = %s
                    ''', (first_name, last_name))
                result = cur.fetchone()  # Получаем одну запись

                return result[0] if result else None
        except Exception as e:
            print(f"Произошла ошибка при поиске клиента: {e}")
            return None
        finally:
            self.close()


if __name__ == "__main__":
    clients = Database()
    # Создание структуры базы данных.
    # clients.create()

    # Добавление клиента.
    # clients.add_new_entry()

    # Добавление телефона для существующего клиента.
    # Введите номер id клиента или оставьте без изменений.
    # client_id = None
    # clients.input_number_phone(client_id)

    # Изменение данных о клиенте.
    # Введите номер id клиента или оставьте без изменений.
    # client_id = None
    # clients.change_information_client(client_id)

    # Удаление телефона для существующего клиента.
    # Введите номер id клиента или оставьте без изменений.
    # client_id = None
    # clients.delete_phone(client_id)

    # Удаление существующего клиента.
    # Введите номер id клиента или оставьте без изменений.
    # client_id = None
    # clients.delete(client_id)
	
	# Найти клиента по его данным: имени, фамилии, email или телефону.
    # clients, phones = clients.find('Петр')

    # print("Клиент: ", clients)
    # print("Телефон: ", phones)
