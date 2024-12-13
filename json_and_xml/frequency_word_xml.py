import xml.etree.ElementTree as ET


def fetch_words(news_list):
    """Функция составления списка слов"""
    words = []

    for line in news_list:
        if hasattr(line, 'find'):
            description_element = line.find('description')
            if description_element is not None and description_element.text:
                text = description_element.text
                word_list = text.split()

                for word in word_list:
                    if len(word) > 6:
                        words.append(word)
            else:
                print("Предупреждение: элемент 'description' отсутствует или пуст.")
        else:
            print("Ошибка: элемент не имеет метода 'find'.")
    return words


def count_words(words):
    """Функция подсчета частоты встречаемости слов"""
    counts_word = {}

    for word in words:
        if word in counts_word:
            counts_word[word] += 1
        else:
            counts_word[word] = 1
    return counts_word


file_name = 'newsafr.xml'
parser = ET.XMLParser(encoding='utf-8')
tree = ET.parse(file_name, parser)
root = tree.getroot()
news_list = root.findall('channel/item')
words = fetch_words(news_list)
counts_word = count_words(words)
top_10 = sorted(counts_word.items(), key=lambda x: x[1], reverse=True)[:10]

print(f'Топ 10 самых часто встречающихся в новостях слов,\nв файле {file_name}, длиннее 6 символов:')
for word, count in top_10:
    print(f'{word} - {count}')
