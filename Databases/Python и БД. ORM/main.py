import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
import configparser
from completion import load_data_from_json
from models import create_tables
from requests_handler import get_purchase_facts_by_publisher as purchases

config = configparser.ConfigParser()
config.read('settings.ini', encoding='utf-8')

host = config['database'].get('host') or input("Введите host базы данных: ")
port = config['database'].get('port') or input("Введите port базы данных: ")
user = config['database'].get('user') or input("Введите имя пользователя базы данных: ")
password = config['database'].get('password') or input("Введите пароль базы данных: ")
dbname = config['database'].get('dbname') or input("Введите название базы данных: ")
json_file_path = config['database'].get('json_file_path') or input("Введите путь json файла: ")

DNS = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
engine = sq.create_engine(DNS)

# Создание таблиц
create_tables(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Загрузка данных из JSON файла
load_data_from_json(session, json_file_path)

# Получение входных данных от пользователя
publisher_identifier = input("Введите имя или идентификатор издателя: ")

# Получение фактов о покупке книг по данному издателю
purchases(session, publisher_identifier)

# Закрываем сессию
session.close()
