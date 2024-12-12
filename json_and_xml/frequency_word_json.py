import json

# Функция получения данных
def open_news(open_file):

    with open(open_file, encoding='utf-8') as f:
        return json.load(f)


# Функция составления списка слов
def fetch_words(news_list):
    words = []

    for line in news_list:
        text = line['description']
        word_list = text.lower().split()

        for word in word_list:

            if len(word) > 6:
                words.append(word)

    return words


# Функция подсчета частоты слов
def count_words(words):
    counts_word = {}

    for word in words:

        if word in counts_word:
            counts_word[word] += 1
        else:
            counts_word[word] = 1

    return counts_word


news_data = open_news('newsafr.json')
news_list = news_data['rss']['channel']['items']
words = fetch_words(news_list)
counts_word = count_words(words)
top_10 = sorted(counts_word.items(), key=lambda x: x[1], reverse=True)[:10]

print('Топ 10 самых часто встречающихся в новостях слов,\n'
      'в файле newsafr.json, длиннее 6 символов:')
for word, count in top_10:
    print(f'{word} - {count}')
