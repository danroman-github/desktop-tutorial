import configparser
import requests
import os
import json
from tqdm import tqdm
from datetime import datetime


class Courseword():
    yandex_url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, settings_file = 'settings.ini'):
        self.settings_file = settings_file
        self.vk_token = None
        self.vk_user_id = None
        self.yandex_token = None
        self.vk_api_version = '5.199'
        self.default_count = 5
        self.disk_folder = 'VK_photos'
        self.load_settings()

    def load_settings(self):
        """Загрузка настроек из файла."""
        config = configparser.ConfigParser()
        config.read(self.settings_file)

        self.vk_token = config['Tokens'].get('vk_token') or input("Введите токен VK: ")
        self.vk_user_id = config['Tokens'].get('vk_user_id') or input("Введите ID пользователя VK: ")
        self.yandex_token = config['Tokens'].get('yandex_token') or input("Введите токен Яндекс.Диска: ")

    def get_photos(self, album_id='profile'):
        """Функция получения фотографий из ВК."""
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': self.vk_user_id,
            'count': self.default_count,
            'album_id': album_id,
            'photo_sizes': 1,
            'extended': 1,
            'access_token': self.vk_token,
            'v': self.vk_api_version
        }
        response = requests.get(url, params=params)
        response.raise_for_status()

        # Проверяем, что правильный формат ответа
        data = response.json()
        if 'response' in data and isinstance(data['response'], dict):
            return data['response'].get('items', [])
        else:
            print("Ошибка получения данных из VK:", data)
            return []

    def get_album_info(self, album_id):
        """Получение информации об альбоме по его ID."""
        url = 'https://api.vk.com/method/photos.getAlbums'
        params = {
            'owner_id': self.vk_user_id,
            'access_token': self.vk_token,
            'v': self.vk_api_version
        }
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        if 'response' in data and isinstance(data['response'], dict):
            albums = data['response']['items']
            for album in albums:
                if album['id'] == int(album_id):
                    return album['title']
        return None

    def _build_headers(self):
        """Создание заголовков для запросов к Яндекс диску."""
        return {'Authorization': f'OAuth {self.yandex_token}'}

    def create_yandex_disk_folder(self, folder_name):
        """Функция создание папки на Яндекс диске"""
        headers = self._build_headers()
        params = {'path': folder_name}
        response = requests.put(self.yandex_url, params=params, headers=headers)

        if response.status_code == 201:
            print(f"Папка '{folder_name}' успешно создана на Яндекс диске.")
        elif response.status_code == 409:
            print(f"Папка '{folder_name}' уже существует на Яндекс диске.")
        elif response.status_code == 401:
            print("Ошибка авторизации. Проверьте токен Яндекс диска.")
        else:
            print(f"Ошибка при создании папки: {response.status_code}. {response.text}")

    def get_yandex_disk(self, file_name, file_path):
        """Функция загрузки фотографий на Яндекс диске."""
        if not os.path.exists(file_path):
            print(f"Ошибка: Файл '{file_path}' не найден.")
            return

        url = f'{self.yandex_url}/upload'
        headers = self._build_headers()
        params = {
            'path': f'{self.disk_folder}/{file_name}',
            'overwrite': 'true'
        }

        # Получение URL для загрузки файла
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            url_upload = response.json()['href']

            # Загрузка файла
            with open(file_path, 'rb') as f:
                upload_response  = requests.put(url_upload, files={'file': f})

                # Загрузка файла
                if upload_response.status_code == 201:
                    print(f"Файл '{file_name}' успешно загружен на Яндекс диск.")
                else:
                    print("Ошибка при загрузке файла"
                          f"'{file_name}': {upload_response.status_code}. {upload_response.text}")
        elif response.status_code == 409:
            print(f"Ошибка: Директория '{self.disk_folder}' не существует на Яндекс диск.")
        elif response.status_code == 401:
            print("Ошибка авторизации. Проверьте токен Яндекс диска.")
        else:
            print(f"Ошибка при получении URL для загрузки файла: {response.status_code}. {response.text}")

    def get_unique_file_name(self, like_count, date, existing_files):
        """Формирование имени файла на основе количества лайков и даты загрузки."""
        date_str = datetime.fromtimestamp(date).strftime('%Y%m%d')
        base_file_name  = f'{like_count}'

        # Проверяем, если есть конфликт по лайкам, добавляем дату к имени
        if f'{base_file_name}.jpg'  in existing_files:
            file_name = f'{base_file_name}_{date_str}'

            # Проверяем, есть ли конфликт после добавления даты, добавляем время к имени
            if f'{file_name}.jpg' in existing_files:
                time_str = datetime.fromtimestamp(date).strftime('%H%M%S')
                file_name += f'_{time_str}'

            return f'{file_name}.jpg'

        # Возвращаем полное имя файла с расширением
        return f'{base_file_name}.jpg'

    def process_photos(self, photos):
        """Обработка и загрузка фотографий на Яндекс диск."""
        photos_info = []
        existing_files = set()

        for photo in tqdm(photos):
            like_count = photo['likes']['count']
            upload_date = photo['date']
            file_name = self.get_unique_file_name(like_count, upload_date, existing_files)
            existing_files.add(file_name)

            max_size_photo = max(photo['sizes'], key=lambda x: x['width'] * x['height'])
            photo_url = max_size_photo['url']
            file_response = requests.get(photo_url)

            file_path = f'./{file_name}'
            with open(file_path, 'wb') as f:
                f.write(file_response.content)

            self.get_yandex_disk(file_name, file_path)
            photos_info.append({'file_name': file_name, 'size': max_size_photo['type']})
            os.remove(file_path)

        with open('photos_info.json', 'w') as json_file:
            json.dump(photos_info, json_file, indent=4)

        print("Копирование завершено успешно")

    def run(self):
        """Основной метод для начала резервного копирования."""
        album_id = input("Введите ID альбома (по умолчанию 'profile'): ") or 'profile'

        # Получаем название альбома по ID, если введен альбом не 'profile'
        album_title = self.get_album_info(album_id)
        if album_title:
            self.disk_folder = album_title
        else:
            self.disk_folder = album_id

        self.create_yandex_disk_folder(self.disk_folder)
        photos = self.get_photos(album_id)


        if not photos:
            print("Нет доступных фотографий для резервного копирования.")
            return

        # Сортировка фотографий по максимальному размеру
        sorted_photos = sorted(
            photos,
            key=lambda x: max(size['width'] * size['height'] for size in x['sizes']),
            reverse=True
        )[:self.default_count]

        self.process_photos(sorted_photos)


if __name__ == '__main__':
    courseword = Courseword()
    courseword.run()
