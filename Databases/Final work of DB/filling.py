import os
import json
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from models import Base, engine, User, Word, Subsection, UserWord, get_config

def database_exists(engine):
    """Проверка существования базы данных."""
    try:
        with engine.connect() as conn:
            return True
    except Exception as e:
        print(f"Ошибка при проверке базы данных: {e}")
        return False

def create_session():
    """Создание и возврат новой сессии."""
    Session = sessionmaker(bind=engine)
    return Session()

def add_user(session, item):
    """Добавление пользователя в базу данных."""
    if 'nickname' in item:
        user = User(id=item['id'], chat_id=item['chat_id'], nickname=item['nickname'])
        session.add(user)
    else:
        print(f"Пропущен элемент users из-за отсутствия 'nickname': {item}")

def add_subsection(session, item):
    """Добавление подраздела в базу данных."""
    if 'name' in item:
        subsection = Subsection(id=item['id'], name=item['name'])
        session.add(subsection)
    else:
        print(f"Пропущен элемент subsections из-за отсутствия 'name': {item}")

def add_word(session, item):
    """Добавление слова в базу данных."""
    if all(key in item for key in ['id', 'english', 'russian', 'id_subsections']):
        word = Word(
            id=item['id'],
            english=item['english'],
            russian=item['russian'],
            id_subsections=item['id_subsections']
        )
        session.add(word)
    else:
        print(f"Пропущен элемент words из-за отсутствия обязательных полей: {item}")

def add_user_word(session, item):
    """Добавление связи между пользователем и словом в базу данных."""
    if all(key in item for key in ['id_users', 'id_words']):
        user_word = UserWord(
            id_users=item['id_users'],
            id_words=item['id_words']
        )
        session.add(user_word)
    else:
        print(f"Пропущен элемент users_words из-за отсутствия обязательных полей: {item}")


def reset_sequence(session):
    """Сброс секвенции автоинкремента для таблицы words."""
    try:
        # SQL запрос для сброса секвенции
        reset_query = text("""
            SELECT setval(pg_get_serial_sequence('users', 'id'), coalesce(max(id), 0) + 1, false) 
            FROM users;
            SELECT setval(pg_get_serial_sequence('subsections', 'id'), coalesce(max(id), 0) + 1, false) 
            FROM subsections;
            SELECT setval(pg_get_serial_sequence('words', 'id'), coalesce(max(id), 0) + 1, false) 
            FROM words;
            SELECT setval(pg_get_serial_sequence('users_words', 'id'), coalesce(max(id), 0) + 1, false) 
            FROM users_words;
        """)

        # Выполнить SQL запрос
        session.execute(reset_query)
        session.commit()  # Зафиксировать изменения

        print("Секвенция успешно сброшена.")
    except Exception as e:
        print(f"Произошла ошибка при сбросе секвенции: {e}")
        session.rollback()  # Откатить изменения в случае ошибки

def insert_data(session, json_file_path):
    """Загрузка данных из JSON файла в базу данных."""
    if not os.path.isfile(json_file_path):
        print(f"Файл {json_file_path} не найден.")
        return

    with open(json_file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Ошибка при загрузке JSON: {e}")
            return

    for item in data:
        if item['table'] == 'users':
            add_user(session, item)
        elif item['table'] == 'subsections':
            add_subsection(session, item)
        elif item['table'] == 'words':
            add_word(session, item)
        elif item['table'] == 'users_words':
            add_user_word(session, item)

    session.commit()

if __name__ == '__main__':
    # Удаление и создание всех таблиц
    Base.metadata.drop_all(engine)  # Не забудьте раскомментировать, если нужно удалять таблицы
    Base.metadata.create_all(engine)

    # Получаем путь к файлу JSON из конфигурации
    json_file_path = get_config()

    # Проверка существования базы данных и вставка данных
    session = create_session()

    with create_session() as session:
        if database_exists(engine):
            insert_data(session, json_file_path)
            reset_sequence(session)
        else:
            print("База данных не доступна.")
