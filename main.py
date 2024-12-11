import os
import requests
import urllib.parse
from dotenv import load_dotenv


def shorten_link(user_url, api_key):
    vk_url = 'https://api.vk.com/method/utils.getShortLink'
    response = requests.post(vk_url, data={"access_token": api_key, "url": user_url, "v": "5.199"})
    response.raise_for_status()
    return response.json()['response']['short_url']


def count_clicks(api_key, key):
    vk_url = 'https://api.vk.com/method/utils.getLinkStats'
    response = requests.post(vk_url, data={"access_token": api_key, "key": key.path.lstrip('/'), "interval": "forever", "v": "5.199"})
    response.raise_for_status()
    stats = response.json()
    return stats['response']['stats'][0]['views']


def is_shorten_link(parsed_user_url):
    return parsed_user_url.netloc == "vk.cc"


def main():
    load_dotenv('.env')
    VK_API_KEY = os.environ['VK_API_KEY']
    user_url = input("Введите ссылку:")

    if not user_url.startswith('https://' or 'http://'):
        user_url = 'http://' + user_url
    
    parsed_user_url = urllib.parse.urlsplit(user_url)
    if is_shorten_link(parsed_user_url):
        short_link = user_url
    else:
        short_link = shorten_link(user_url, VK_API_KEY)
    parsed_url = urllib.parse.urlparse(short_link)
    try:
        print(f"Сокращенная ссылка: {short_link}")
        print(f"Статистика переходов: {count_clicks(VK_API_KEY, parsed_url)}")
    except KeyError:
        print("Ответ VK не соответствует параметрам, проверьте ссылку!")
    except requests.exceptions.HTTPError:
        print("Ответ не был получен!")
    except IndexError:
        print("Статистика кликов отсутсвует!")


if __name__ == "__main__":
    main()