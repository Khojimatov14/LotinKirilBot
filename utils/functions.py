import string
import requests
from collections import Counter


def detect_language(text):
    first_letters = [char for char in text if char.isalpha()][:10]
    latin_letters = set(string.ascii_letters)
    cyrillic_letters = set("\u0410\u0411\u0412\u0413\u0414\u0415\u0416\u0417\u0418\u0419\u041a\u041b\u041c\u041d\u041e\u041f\u0420\u0421\u0422\u0423\u0424\u0425\u0426\u0427\u0428\u0429\u042a\u042b\u042c\u042d\u042e\u042f\u0430\u0431\u0432\u0433\u0434\u0435\u0436\u0437\u0438\u0439\u043a\u043b\u043c\u043d\u043e\u043f\u0440\u0441\u0442\u0443\u0444\u0445\u0446\u0447\u0448\u0449\u044a\u044b\u044c\u044d\u044e\u044f")
    letter_counts = Counter(first_letters)
    latin_count = sum(count for char, count in letter_counts.items() if char in latin_letters)
    cyrillic_count = sum(count for char, count in letter_counts.items() if char in cyrillic_letters)
    return "en" if latin_count > cyrillic_count else "ru"


def get_words(text):
    url = 'https://lotin.uz/api/translate'
    mod = "lattocyr"

    if detect_language(text=text) == "ru":
        mod = "cyrtolat"

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Origin': 'https://lotin.uz',
        'Referer': 'https://lotin.uz/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    
    payload = {
        'mod': mod,
        'text': text,
        'ignoreHtml': True
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json().get('result', '')