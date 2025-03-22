import configparser
import random
import requests
import logging
import interactions

from contextlib import contextmanager

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.functions import func

from models import engine, Word
from telebot import types, TeleBot, StateMemoryStorage
from telebot.handler_backends import State, StatesGroup

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='bot.log',
    filemode='a'
)
logger = logging.getLogger(__name__)

def load_settings(get_setting):
    """Загрузка настроек из файла."""
    settings_file = 'settings.ini'
    config = configparser.ConfigParser()
    config.read(settings_file)
    state_storage = StateMemoryStorage()
    settings = []


    if get_setting == 'get_bot':
        TOKEN_BOT = config['TOKENS'].get('TOKEN_BOT') or input("Введите token: ")
        return TeleBot(TOKEN_BOT, state_storage=state_storage)
    elif get_setting == 'get_setting':
        settings.append(config['TOKENS'].get('HOST_YANDEX_DISK'))
        settings.append(config['TOKENS'].get('YANDEX_TOKEN'))
        return settings
    else:
        return None


class Command:
    """Класс для определения текстов кнопок команд."""
    ADD_WORD = "Добавить слово ➕"
    DELETE_WORD = "Удалить слово🔙"
    NEXT = "Дальше ⏭"
    ADD_DIST = "Добавить из словаря"
    ADD_SELF = "Добавить свое слово"
    CONTINUE = "Продолжить"
    ABORT = "Закончить"


class MyStates(StatesGroup):
    """Класс для определения состояний бота."""
    target_word = State()      # Состояние для ввода целевого слова
    translate_word = State()   # Состояние для перевода слова
    another_words = State()    # Состояние для работы с другими словами
    nickname_input = {}        # Глобальное состояние для отслеживания nickname пользователей


class MessageHandler:
    def __init__(self):
        self.known_users = interactions.get_all_users()
        self.user_steps = {}
        self.bot = load_settings('get_bot')
        self.buttons = []
        self.words = []
        self.add_word_data = {}
        self.progress = 0
        self.session = None

        if not self.bot:
            logger.error("Настройка bot не получена.")
            return

        logger.info("Бот запущен!")
        self.start_polling()

    @staticmethod
    def get_text_commands():
        """Получение текстов для команд."""
        return {
            'start': "Привет 👋 Давай попрактикуемся в английском языке."
                     " Тренировки можешь проходить в удобном для себя темпе. "
                     "Причём у тебя есть возможность использовать тренажёр "
                     "как конструктор и собирать свою собственную базу для обучения. "
                     "Для этого воспользуйся инструментами Добавить слово➕ "
                     "или Удалить слово🔙. Ну что, начнём ⬇️",
            'help': "Я знаю команды: "
                    "/start, /stop, /cards, /create_folder",
            'create_folder': "Для создания папки на Яндекс диске."
        }

    @contextmanager
    def session_scope(self):
        """Контекстный менеджер для управления сессией базы данных."""
        session = sessionmaker(bind=engine)()
        self.session = session
        try:
            yield session
            session.commit()
        except Exception as e:
            logger.error(f"Ошибка в сессии базы данных: {e}")
            session.rollback()
            raise e
        finally:
            session.close()

    def send_create_folder(self, message):
        """Обработка команды '/create_folder' для создания папки на Яндекс.Диске."""
        logger.info(f"Пользователь {message.from_user.id} вызвал команду /create_folder.")

        self.bot.send_message(message.chat.id, "Введите название папки, которую хотите создать на Яндекс.Диске:")
        self.bot.register_next_step_handler(message, self.create_folder)

    def create_folder(self, message):
        """Создание папки на disk.yandex."""
        folder_name = message.text
        logger.info(f"Пользователь {message.from_user.id} запросил создание папки: {folder_name}")

        HOST_YANDEX_DISK, YANDEX_TOKEN = load_settings('get_setting')

        if not HOST_YANDEX_DISK or not YANDEX_TOKEN:
            logger.error("Не удалось загрузить настройки для disk.yandex.")
            self.bot.reply_to(message, "Ошибка: не удалось загрузить настройки для disk.yandex.")
            return

        headers = {'Authorization': 'OAuth %s' % YANDEX_TOKEN}
        request_url = HOST_YANDEX_DISK + '/v1/disk/resources?path=%s' % folder_name
        response = requests.put(url=request_url, headers=headers)

        if response.status_code == 201:
            logger.info(f"Папка {folder_name} успешно создана на disk.yandex.")
            self.bot.reply_to(message, "Я создал папку %s" % folder_name)
        elif response.status_code == 409:
            logger.warning(f"Папка {folder_name} уже существует на disk.yandex.")
            self.bot.reply_to(message, f"Папка '{folder_name}' уже существует на disk.yandex.")
        else:
            logger.error(f"Ошибка при создании папки {folder_name}: {response.text}")
            self.bot.reply_to(message, f"Ошибка при создании папки: {response.text}")

    def close_session(self):
        """Метод для завершения сессии базы данных при остановке бота."""
        if self.session:
            self.session.close()
            logger.info("Сессия успешно закрыта.")

    def start_polling(self):
        """Запуск бота на получение сообщений."""

        @self.bot.message_handler(commands=['start',
                                            'help',
                                            'cards',
                                            'next',
                                            'stop',
                                            'create_folder',
                                            'add_word',
                                            'delete_word'
                                            'continue',
                                            'abort'])
        def handle_commands(message):
            """Обработка команд."""
            command = message.text.split()[0]
            logger.info(f"Пользователь {message.from_user.id} вызвал команду: {command}")

            if command == '/start':
                self.send_salutation(message)
            elif command == '/help':
                self.send_help(message)
            elif command == '/cards':
                self.create_cards(message)
            elif command == '/next':
                self.create_cards(message)
            elif command == '/stop':
                self.stop_bot(message)
            elif command == '/create_folder':
                self.send_create_folder(message)
            elif command == '/add_word':
                self.prep_new_word(message)
            elif command == '/delete_word':
                self.enter_delete_word(message)
            elif command == '/continue':
                self.create_cards(message)
            elif command == '/abort':
                self.stop_bot(message)
            else:
                logger.warning(f"Неизвестная команда: {command}")
                self.bot.reply_to(message, "Неизвестная команда. Используйте /help для списка команд.")

        @self.bot.message_handler(func=lambda message: message.text == Command.NEXT)
        def clicking_next(message):
            """Начинает процедуру добавления слова"""
            chat_id = message.chat.id
            logger.info(f"Пользователь {chat_id} вызвал команду: next")
            self.run_command_next(message)

        @self.bot.message_handler(func=lambda message: message.text == Command.CONTINUE)
        def clicking_continue(message):
            """Продолжает изучение слов"""
            chat_id = message.chat.id
            logger.info(f"Пользователь {chat_id} вызвал команду: continue")
            self.create_cards(message)

        @self.bot.message_handler(func=lambda message: message.text == Command.ABORT)
        def clicking_abort(message):
            """Заканчивает обучение"""
            chat_id = message.chat.id
            logger.info(f"Пользователь {chat_id} вызвал команду: abort")
            self.stop_bot(message)

        @self.bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
        def add_word(message):
            """Начинает процедуру добавления слова"""
            chat_id = message.chat.id
            logger.info(f"Пользователь {chat_id} вызвал команду: add_word")
            self.prep_new_word(message)

        @self.bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
        def delete_word(message):
            """Начинает процедуру удаления слова"""
            chat_id = message.chat.id
            logger.info(f"Пользователь {chat_id} вызвал команду: delete_word")
            delete_word = self.bot.send_message(chat_id, "Введите удаляемое слово на английском")
            self.bot.register_next_step_handler(delete_word, self.enter_delete_word)

        @self.bot.message_handler(func=lambda message: message.text == Command.ADD_DIST)
        def adding_word_from_database(message):
            """Добавляет новое слово из базы данных в словарь пользователя."""
            chat_id = message.chat.id
            logger.info(f"Пользователь {chat_id} вызвал команду: adding_word_from_database")
            result, text = interactions.add_random_word_for_user(str(chat_id))
            if result is True:
                self.bot.send_message(chat_id, f"Слово {str(text)} добавлено в ваш словарь.")
            else:
                self.bot.send_message(chat_id, text)

            self.create_cards(message)

        @self.bot.message_handler(func=lambda message: message.text == Command.ADD_SELF)
        def add_your_own_word(message):
            """Начинает добавление нового слова пользователя."""
            chat_id = message.chat.id
            logger.info(f"Пользователь {chat_id} вызвал команду: add_your_own_word")
            self.enter_english_word(message)

        @self.bot.message_handler(func=lambda message: True, content_types=['text'])
        def handle_text(message):
            """Обработка текстовых сообщений (слов для изучения)."""
            logger.info(f"Пользователь {message.from_user.id} ввел текст: {message.text}")

            with self.bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                target_word = data.get('target_word')

            if target_word and message.text == target_word:
                logger.info(f"Пользователь {message.from_user.id} правильно угадал слово: {target_word}")
                self.process_correct_word(message)
            else:
                logger.info(f"Пользователь {message.from_user.id} ввел неправильный ответ.")
                self.bot.send_message(message.chat.id, "Неверно. Попробуйте еще раз.")

        logger.info("Бот начал polling.")
        self.bot.polling()

    def process_correct_word(self, message):
        """Обработка правильного слова."""
        self.progress_words()
        self.bot.send_message(message.chat.id, "Отлично!")
        self.create_cards(message)

    def question_of_continuation(self, message):
        """Выбор продолжения."""
        logger.info(f"Пользователь {message.chat.id} начал question_of_continuation.")

        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

        self.buttons = []
        self.buttons.extend([
            types.KeyboardButton(Command.CONTINUE),
            types.KeyboardButton(Command.ABORT)
        ])

        markup.add(*self.buttons)

        question = "Ну что, продолжим?"
        self.bot.send_message(message.chat.id, question, reply_markup=markup)

    def send_salutation(self, message):
        """Отправляет приветствие пользователю на основе chat.id."""
        cid = str(message.chat.id)
        nickname = self.get_nickname_by_id(cid)
        if not nickname:
            logger.info('send_salutation - start if')
            self.bot.send_message(cid, "Незнакомец, давай знакомиться")
            self.request_nickname(message)  # Передаем сообщение в метод
        else:
            logger.info('send_salutation - start else')
            self.bot.send_message(cid, f"Давай {nickname} изучать английский...")
            self.create_cards(message)

    def send_help(self, message):
        """Обработка команды '/help'."""
        start_text = self.get_text_commands()['help']
        self.bot.reply_to(message, start_text)

    def stop_bot(self, message):
        """Обработка команды '/stop'."""
        self.bot.reply_to(message, "Бот останавливается, до свидания!")
        self.close_session()  # Закрываем сессию (если есть)
        self.bot.stop_polling()  # Останавливаем бота

    def run_command_next(self, message):
        self.progress_words()
        self.create_cards(message)

    def progress_words(self):
        """Увеличивает прогресс изучения слов"""
        if self.progress < len(self.words) - 1:
            self.progress += 1
        else:
            self.progress = 0

    def get_nickname_by_id(self, user_id):
        """Проверка наличия user_id в словаре known_users и возвращение соответствующего nickname."""
        return self.known_users.get(user_id, None)

    def request_nickname(self, message):
        """Запрашивает у пользователя псевдоним."""
        logger.info('request_nickname')
        msg = self.bot.reply_to(message, "Введите никнейм пользователя:")  # Исправлено на message
        self.bot.register_next_step_handler(msg, self.add_new_user)

    def is_nickname_known(self, nickname_to_check):
        """Проверяет, существует ли nickname в словаре known_users."""
        return nickname_to_check in self.known_users.values()

    def add_new_user(self, message):
        """Добавляет нового пользователя в базу данных."""
        logger.info(f"Добавление нового пользователя: {message.from_user.id}")
        new_nickname = message.text
        new_id = str(message.chat.id)

        if self.is_nickname_known(new_nickname):
            logger.warning(f"Никнейм {new_nickname} уже занят.")
            self.bot.reply_to(message, f"Этот nickname {new_nickname} уже занят")
            self.request_nickname(message)
        else:
            item = {"chat_id": new_id, "nickname": new_nickname}
            interactions.add_new_user(item)
            self.known_users = interactions.get_all_users()
            logger.info(f"Пользователь {new_nickname} успешно добавлен.")
            self.bot.reply_to(message, f"Пользователь {new_nickname} добавлен")
            self.words = interactions.get_first_five_words(new_id)
            self.send_salutation(message)

    def enter_delete_word(self, delete_word):
        """Удаляет слово на английском"""
        logger.info(f"enter_delete_word удаляемое слово {delete_word.text} на английском")
        chat_id = delete_word.chat.id
        result = interactions.remove_word_for_user(delete_word.text, str(chat_id))
        if result is True:
            self.bot.reply_to(delete_word, "Слово успешно удалено из вашего словаря.")
            logger.info(f"Слово {delete_word} успешно удалено из словаря")
            self.question_of_continuation(delete_word)
        elif isinstance(result, str):
            self.bot.reply_to(delete_word, result)
            self.question_of_continuation(delete_word)
        else:
            self.bot.reply_to(delete_word, "Что-то пошло не так, но мы уже работаем над этим.")
            self.question_of_continuation(delete_word)

    def prep_new_word(self, message):
        """Выбор способа добавления слова."""
        logger.info(f"Пользователь {message.chat.id} начал выбор способа добавления слова prep_new_word.")

        markup = types.ReplyKeyboardMarkup(row_width=1)

        self.buttons = []
        self.buttons.extend([
            types.KeyboardButton(Command.ADD_DIST),
            types.KeyboardButton(Command.ADD_SELF)
        ])

        markup.add(*self.buttons)

        question = "Выбери способ добавления слова"
        self.bot.send_message(message.chat.id, question, reply_markup=markup)

    def enter_english_word(self, message):
        """Запрашивает слово на английском"""
        logger.info("enter_english_word Запрашивает слово на английском")
        self.buttons = []
        markup = types.ReplyKeyboardMarkup(row_width=1)
        markup.add(*self.buttons)
        chat_id = message.chat.id
        enter_word = self.bot.send_message(chat_id, "Введите слово на английском")

        self.bot.register_next_step_handler(enter_word, self.enter_russian_word)

    def enter_russian_word(self, message):
        """Запрашивает слово на русском"""
        logger.info("enter_russian_word Запрашивает слово на русском")
        chat_id = message.chat.id
        self.add_word_data['english'] = message.text
        logger.info(f"Пользователь {message.chat.id} ввел слово {message.text}")
        enter_word = self.bot.send_message(chat_id, "Введите перевод слова на русском")
        self.bot.register_next_step_handler(enter_word, self.add_users_word_to_database)

    def add_users_word_to_database(self, message):
        """Добавляет новое слово в базу данных и в словарь пользователя."""
        chat_id = message.chat.id
        self.add_word_data['russian'] = message.text
        self.add_word_data['chat_id'] = chat_id
        self.add_word_data['subsections'] = 14
        print(self.add_word_data['english'], self.add_word_data['russian'])

        russian = str(self.add_word_data.get('russian', '')).strip().lower()
        english = str(self.add_word_data.get('english', '')).strip().lower()

        if (russian == "добавить из словаря" or
                english == "добавить из словаря" or
                russian == "добавить свое слово" or
                english == "добавить свое слово"):
            self.bot.send_message(chat_id, f"Нельзя добавить {self.add_word_data['english']}")
            self.enter_english_word(message)
            return

        logger.info('add_users_word_to_database')
        logger.info(f"Пользователь {chat_id} ввел слово {message.text}")
        word_data = self.add_word_data.copy()

        result = interactions.add_word_for_user(word_data)
        if result is True:
            logger.info(f"Слово {self.add_word_data['english']} успешно добавлено.")
            self.bot.reply_to(message, f"Слово {self.add_word_data['english']} успешно добавлено.")
            self.create_cards(message)
        elif isinstance(result, str):
            logger.warning(result)
            self.bot.reply_to(message, result)
            self.create_cards(message)
        else:
            self.bot.reply_to(message, "Что-то пошло не так, но мы уже работаем над этим.")
            self.create_cards(message)

    def check_words_availability(self):
        """Проверяет, есть ли слова для изучения, и корректирует progress."""
        if not self.words:
            logger.warning("Список слов для изучения пуст.")
            return False

        if self.progress >= len(self.words) or self.progress < 0:
            logger.warning(f"Некорректное значение progress: {self.progress}. Сбрасываем progress в 0.")
            self.progress = 0

        return True

    def get_current_word(self):
        """Возвращает текущее слово и его перевод."""
        current_word = self.words[self.progress]
        english = current_word.get('english', '')
        russian = current_word.get('russian', '')

        if not english or not russian:
            logger.error(f"Текущее слово не содержит английского или русского перевода: {current_word}")
            return None, None

        return english, russian

    def generate_random_words(self, target_word, count=3):
        """Генерирует список случайных слов для выбора."""
        try:
            random_words = self.get_random_words(target_word, count)
            if not random_words:
                logger.warning("Не удалось получить случайные слова для выбора.")
                random_words = []

            return random_words
        except Exception as e:
            logger.error(f"Ошибка при генерации случайных слов: {e}")
            return []

    def create_keyboard(self, words, target_word):
        """Создает клавиатуру с кнопками для выбора перевода."""
        full_words = words.copy()
        full_words.append(target_word)
        random.shuffle(full_words)

        markup = types.ReplyKeyboardMarkup(row_width=2)
        buttons = [types.KeyboardButton(word) for word in full_words]
        buttons.extend([
            types.KeyboardButton(Command.ADD_WORD),
            types.KeyboardButton(Command.DELETE_WORD),
            types.KeyboardButton(Command.NEXT)
        ])
        markup.add(*buttons)

        return markup

    def send_card_message(self, message, russian, markup, english, random_words):
        """Отправляет сообщение с карточкой и устанавливает состояние."""
        greeting = f"Выбери перевод слова:\n🇷🇺 {russian}"
        self.bot.send_message(message.chat.id, greeting, reply_markup=markup)

        # Устанавливаем состояние для текущего слова
        self.bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)

        # Сохраняем данные в состоянии
        with self.bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['target_word'] = english
            data['translate_word'] = russian
            data['other_words'] = random_words

        logger.info(f"Карточка для слова '{english}' успешно создана.")

    def create_cards(self, message):
        """Создание карточек для изучения слов."""
        logger.info(f"Создание карточек для пользователя {message.from_user.id}")
        self.words = interactions.get_words_by_user_id(str(message.chat.id))

        if not self.check_words_availability():
            self.bot.send_message(message.chat.id, "Список слов пуст. Добавьте слова для изучения.")
            return

        english, russian = self.get_current_word()
        if not english or not russian:
            self.bot.send_message(message.chat.id, "Ошибка: слово не содержит перевода.")
            return

        random_words = self.generate_random_words(english)
        if not random_words:
            self.bot.send_message(message.chat.id, "Ошибка: не удалось получить случайные слова.")
            return

        markup = self.create_keyboard(random_words, english)

        self.send_card_message(message, russian, markup, english, random_words)

    def get_random_words(self, target_word, count=3):
        """Получает случайные слова из таблицы words, исключая target_word."""
        with (self.session_scope() as session):
            try:
                random_words = session.query(Word).filter(Word.english != target_word).order_by(func.random()
                                                                                            ).limit(count).all()

                if not random_words:
                    logger.warning("В таблице нет слов, кроме указанного.")
                    return []

                return [word.english for word in random_words]

            except SQLAlchemyError as e:
                logger.error(f"Ошибка при получении случайных слов: {e}")
                return []


if __name__ == '__main__':
    MessageHandler()