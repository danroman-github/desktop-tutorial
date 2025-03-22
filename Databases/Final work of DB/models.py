import sqlalchemy as sq
from configparser import ConfigParser
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

config = ConfigParser()
config.read('settings.ini', encoding='utf-8')

host = config['DATABASE'].get( 'host') or input("Введите host базы данных: ")
port = config['DATABASE'].get('port') or input("Введите port базы данных: ")
user = config['DATABASE'].get('user') or input("Введите имя пользователя базы данных: ")
password = config['DATABASE'].get('password') or input("Введите пароль базы данных: ")
dbname = config['DATABASE'].get('dbname') or input("Введите название базы данных: ")
json_file_path = config['DATABASE'].get('json_file_path') or input("Введите путь json файла: ")

DNS = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
engine = sq.create_engine(DNS)


class User(Base):
    """Класс пользователь."""

    __tablename__ = "users"

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    chat_id = sq.Column(sq.String(length=20), unique=True)
    nickname = sq.Column(sq.String(length=40), unique=True)

    users_words = relationship("UserWord", back_populates="users")
    completed_words = relationship("Сompleted", back_populates="users")


class Subsection(Base):
    """Класс подраздел."""

    __tablename__ = "subsections"

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    name = sq.Column(sq.String(length=40), unique=True)

    words = relationship("Word", back_populates="subsection", cascade='all, delete')


class Word(Base):
    """Класс слово."""

    __tablename__ = "words"

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    english = sq.Column(sq.String(length=40), nullable=False)
    russian = sq.Column(sq.String(length=40), nullable=False)
    id_subsections = sq.Column(sq.Integer, sq.ForeignKey("subsections.id"), nullable=False)

    subsection = relationship("Subsection", back_populates="words")
    users_words = relationship("UserWord", back_populates="words")
    completed = relationship("Сompleted", back_populates="words")


class UserWord(Base):
    """Класс пользователь-слово."""

    __tablename__ = "users_words"

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    id_users = sq.Column(sq.Integer, sq.ForeignKey("users.id"), nullable=False)
    id_words = sq.Column(sq.Integer, sq.ForeignKey("words.id"), nullable=False)

    users = relationship("User", back_populates="users_words")
    words = relationship("Word", back_populates="users_words")


class Сompleted(Base):
    """Класс пройденные слова."""

    __tablename__ = "completed"

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    id_users = sq.Column(sq.Integer, sq.ForeignKey("users.id"), nullable=False)
    id_words = sq.Column(sq.Integer, sq.ForeignKey("words.id"), nullable=False)

    users = relationship("User", back_populates="completed_words", cascade='all, delete')
    words = relationship("Word", back_populates="completed", cascade='all, delete')


def get_config():
    """Возвращает параметры конфигурации."""
    return json_file_path

if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
