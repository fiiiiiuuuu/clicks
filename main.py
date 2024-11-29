import os
import requests
import urllib.parse
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')


def shorten_link(token):
    vk_url = 'https://api.vk.com/method/utils.getShortLink'
    try:
        response = requests.post(vk_url, data={"access_token": token, "url": user_url, "v": "5.199"})
        response.raise_for_status()
        return response.json()['response']['short_url']
    except KeyError:
        print("Ответ VK не соответсвует параметрам, проверьте ссылку!")
    except requests.exceptions.HTTPError:
        print("Ответ не был получен!")


def count_clicks(token, key):
    vk_url = 'https://api.vk.com/method/utils.getLinkStats'
    try:
        response = requests.post(vk_url, data={"access_token": token, "key": key.path.lstrip('/'), "interval": "forever", "v": "5.199"})
        response.raise_for_status()
        return response.json()['response']['stats'][0]['views']
    except requests.exceptions.HTTPError:
        print("Ответ не был получен!")
    except IndexError:
        return None


def is_shorten_link(user_url):
    if parsed_user_url.netloc == "vk.cc":
        return user_url
    else:
        return shorten_link(API_KEY)


if __name__ == "__main__":
    user_url = input("Введите ссылку:")

    if not user_url.startswith('https://' or 'http://'):
        user_url = 'http://' + user_url
    
    parsed_user_url = urllib.parse.urlsplit(user_url)
    short_link = is_shorten_link(user_url)
    parsed_url = urllib.parse.urlparse(short_link)

    print(f"Сокращенная ссылка: {short_link}")
    print(f"Статистика переходов: {count_clicks(API_KEY, parsed_url)}")