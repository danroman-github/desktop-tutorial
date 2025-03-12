import json
import requests
from bs4 import BeautifulSoup

keywords = ['дизайн', 'фото', 'веб', 'python']

url = 'https://habr.com/ru/articles/'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

articles = soup.find_all('article')

parsed_data = []

for article in articles:
    article_link = article.find('a', class_='tm-article-datetime-published')['href']
    article_link = f"https://habr.com{article_link}"

    article_response = requests.get(article_link)
    article_soup = BeautifulSoup(article_response.text, 'html.parser')

    content = article_soup.find('div', class_='tm-article-body')
    full_text = content.get_text(strip=True) if content else ''

    title = article.find('h2').text.strip()
    date_element = article.find('time')
    date = date_element['title'] if date_element else 'Дата не указана'

    if (any(keyword in title.lower() for keyword in keywords)
            or any(keyword in full_text.lower() for keyword in keywords)):
        parsed_data.append({
            'дата': date,
            'заголовок': title,
            'ссылка': article_link,
            'текст': full_text
        })

with open('improved.json', 'w', encoding='utf-8') as file:
    json.dump(parsed_data, file, ensure_ascii=False, indent=4)