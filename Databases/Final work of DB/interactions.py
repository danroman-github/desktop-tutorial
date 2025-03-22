import random
from filling import create_session
from models import User, UserWord, Word, Сompleted

def get_all_users():
    """Получение всех пользователей и их ID из базы данных."""
    session = create_session()
    known_users = {}

    try:
        # Запрос всех пользователей
        users = session.query(User).all()

        # Формирование словаря из списка пользователей
        for user in users:
            known_users[user.chat_id] = user.nickname

    except Exception as e:
        print(f"Ошибка при получении пользователей: {e}")

    finally:
        session.close()

    return known_users

def add_words_for_user(chat_id, words):
    """Добавление списка слов для определенного пользователя по его ID."""
    session = create_session()
    try:
        # Проверяем, существует ли пользователь
        user = session.query(User).filter(User.id == chat_id).first()
        if not user:
            raise ValueError(f"Пользователь с ID {chat_id} не найден.")

        # Добавляем слова в базу данных
        for word_text in words:
            # Проверяем существует ли слово
            word = session.query(Word).filter(Word.word_text == word_text).first()
            if not word:
                # Если слово не существует, создаем новое
                word = Word(word_text=word_text)
                session.add(word)

            # Создаем связь между пользователем и словом
            user_word = UserWord(id_users=chat_id, id_words=word.id)
            session.add(user_word)

        # Сохраняем изменения
        session.commit()
    except Exception as e:
        session.rollback()  # Откат в случае ошибки
        raise e
    finally:
        session.close()

def get_words_by_user_id(chat_id):
    """Получение списка слов для определенного пользователя по его ID."""
    user_id = str(chat_id)
    session = create_session()
    try:
        # Находим связь пользователя и его слов
        user = session.query(User).filter(User.chat_id == chat_id).first()

        if user is None:
            return []  # Если пользователь не найден, возвращаем пустой список

        user_words = session.query(UserWord).filter(UserWord.id_users == user.id).all()

        # Получаем список слов на основе связей
        words = []
        for user_word in user_words:
            word = session.query(Word).filter(Word.id == user_word.id_words).first()
            if word:
                words.append({'russian': word.russian, 'english': word.english})

        return words
    finally:
        session.close()

def add_initial_words_user(session, words, user):
    """Добавление связей начальных слов с пользователем."""
    for word in words:
        user_word = UserWord(id_users=user.id, id_words=word.id)

        session.add(user_word)
        session.commit()

def get_first_five_words(chat_id):
    """Получение первых 5 слов из базы данных."""
    session = create_session()
    try:
        # Выполнение запроса для получения первых 5 слов
        words = session.query(Word).limit(5).all()

        # Получаем id пользователя
        user = session.query(User).filter_by(chat_id=chat_id).first()
        add_initial_words_user(session, words, user)
        return words
    finally:
        session.close()

def add_new_user(item):
    """Добавление нового пользователя в базу данных."""
    session = create_session()
    if 'nickname' in item:
        # Получаем максимальное значение id из таблицы users
        max_id = session.query(User).order_by(User.id.desc()).first()
        print(max_id.id)
        new_id = (max_id.id + 1) if max_id else 1  # если max_id None, устанавливаем id на 1

        user = User(id=new_id, chat_id=item['chat_id'], nickname=item['nickname'])
        session.add(user)

        try:
            session.commit()  # Попытка сохранить новые данные в базе данных
            print(f"Пользователь добавлен: {user.nickname} (ID: {user.id})")
            return user  # Возвращаем объект пользователя, если добавление прошло успешно
        except Exception as e:
            session.rollback()  # Откат транзакции в случае ошибки
            print(f"Ошибка при добавлении пользователя: {str(e)}")  # Логирование ошибки
            return None  # Возвращаем None, если произошла ошибка
    else:
        print(f"Пропущен элемент users из-за отсутствия 'nickname': {item}")
        return None  # Возвращаем None, если отсутствует 'nickname'

def add_word_for_user(word_data):
    """Добавление нового слова и связь с пользователем."""
    print('interactions.add_word_for_user')
    session = create_session()
    chat_id = str(word_data['chat_id'])
    russian = word_data['russian']
    english = word_data['english']
    subsections = word_data['subsections']

    # Проверка существования слова
    existing_word = session.query(Word).filter_by(english=english, russian=russian).first()

    if existing_word is None:
        # Создание нового объекта Word
        new_word = Word(english=english, russian=russian, id_subsections=subsections)
        session.add(new_word)

        # Фиксация изменений для получения id нового слова
        session.commit()

        # Получаем id пользователя
        user = session.query(User).filter_by(chat_id=chat_id).first()
        if user is not None:
            print(f"Добавляем связь между пользователем и словом. id пользователя: {user.id}")
            # Создание связи между пользователем и новым словом
            user_word = UserWord(id_users=user.id, id_words=new_word.id)
            session.add(user_word)
            session.commit()
            print("Связь успешно добавлена.")
            return True
        else:
            error = f"Пользователь с chat_id {chat_id} не найден."
            # Откат изменений, если пользователь не найден
            session.rollback()
            return error
    else:
        error = f"Слово '{english}' уже существует в базе данных."
        return error

def remove_word_for_user(english: str, chat_id: str):
    """Удаление связи user_word между пользователем и словом, а также добавление записи в таблицу completed."""
    # print('interactions.remove_word_for_user')
    session = create_session()

    try:
        # Находим id пользователя по chat_id
        user = session.query(User).filter_by(chat_id=chat_id).first()
        if not user:
            error = f"Пользователь с chat_id {chat_id} не найден."
            return error

        # Находим id слова по english
        word = session.query(Word).filter_by(english=english).first()
        if not word:
            error = f"Слово '{english}' не найдено."
            return error

        # Находим и удаляем запись из users_words
        user_word = session.query(UserWord).filter_by(id_users=user.id, id_words=word.id).first()
        if not user_word:
            error = f"Связь между пользователем {user.nickname} и словом '{english}' не найдена."
            return error

        # Создаем запись для таблицы completed
        completed_entry = Сompleted(id_users=user.id, id_words=word.id)

        session.delete(user_word)
        session.add(completed_entry)
        session.commit()
        print(f"Связь между пользователем {user.nickname} и словом '{english}' успешно удалена.")
        return True

    except Exception as e:
        error = f"Произошла ошибка при удалении записи: {e}"
        session.rollback()  # Откатываем изменения в случае ошибки
        return error

    finally:
        session.close()  # Закрываем сессию

def add_random_word_for_user(chat_id):
    """Добавляет связь user_word со случайным словом из таблицы words,
        если это слово отсутствует в таблице completed."""
    print('interactions.add_random_word_for_user')
    session = create_session()

    try:
        # Получаем пользователя по chat_id
        user = session.query(User).filter_by(chat_id=chat_id).first()
        if user is None:
            error = [False, f"Пользователь с chat_id {chat_id} не найден."]
            return error

        # Получаем все слова, которые отсутствуют в таблице completed
        completed_word_ids = {entry.id_words for entry in session.query(Сompleted).filter_by(id_users=user.id).all()}
        available_words = session.query(Word).filter(~Word.id.in_(completed_word_ids)).all()

        if not available_words:
            error = [False, "Нет доступных слов для добавления."]
            return error

        # Выбор случайного слова
        random_word = random.choice(available_words)

        # Проверка, существует ли уже связь между пользователем и словом
        existing_link = session.query(UserWord).filter_by(id_users=user.id, id_words=random_word.id).first()
        if existing_link:
            error = [False, f"Связь между пользователем {user.nickname} и словом {random_word.english} уже существует."]
            return error

        # Создание связи между пользователем и словом
        user_word_link = UserWord(id_users=user.id, id_words=random_word.id)
        session.add(user_word_link)  # Добавляем запись в users_words
        session.commit()  # Фиксируем изменения
        print(f"Слово {random_word.english} успешно добавлено для {user.nickname}.")
        success = [True, random_word.english]
        return success

    except Exception as e:
        error = [False, f"Произошла ошибка при добавлении слова: {e}"]
        return error
        session.rollback()  # Откатить изменения при ошибке
    finally:
        session.close()  # Закрытие сессии

if __name__ == '__main__':
    words = get_words_by_user_id('5107777284')
    print(words)

