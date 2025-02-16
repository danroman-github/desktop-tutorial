import os
import json


def open_news(file_name):
    """Функция получения данных"""
    if not os.path.exists(file_name):
        print(f"Файл {file_name} не найден. Пропускаем.")
        return

    with open(file_name, encoding='utf-8') as f:
        return json.load(f)


def fetch_words(news_list):
    """Функция составления списка слов"""
    words = []

    for line in news_list:
        text = line['description']
        word_list = text.split()

        for word in word_list:
            if len(word) > 6:
                words.append(word)
    return words


def count_words(words):
    """Функция подсчета частоты слов"""
    counts_word = {}

    for word in words:
        if word in counts_word:
            counts_word[word] += 1
        else:
            counts_word[word] = 1
    return counts_word


file_name = 'newsafr.json'
news_data = open_news(file_name)
news_list = news_data['rss']['channel']['items']
words = fetch_words(news_list)
counts_word = count_words(words)
top_10 = sorted(counts_word.items(), key=lambda x: x[1], reverse=True)[:10]

print(f'Топ 10 самых часто встречающихся в новостях слов,\nв файле {file_name}, длиннее 6 символов:')
for word, count in top_10:
    print(f'{word} - {count}')
