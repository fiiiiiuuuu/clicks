import os
import requests
import urllib.parse
from dotenv import load_dotenv


def shorten_link(user_url, api_key):
    vk_url = 'https://api.vk.com/method/utils.getShortLink'
    response = requests.post(vk_url, data={"access_token": api_key, "url": user_url, "v": "5.199"})
    response.raise_for_status()
    return response.json()['response']['short_url']


def count_clicks(api_key, short_link):
    short_link = urllib.parse.urlsplit(short_link)
    vk_url = 'https://api.vk.com/method/utils.getLinkStats'
    response = requests.post(vk_url, data={"access_token": api_key, "key": short_link.path.lstrip('/'), "interval": "forever", "v": "5.199"})
    response.raise_for_status()
    stats = response.json()
    return stats['response']['stats'][0]['views']


def is_shorten_link(user_url, api_key):
    vk_url = 'https://api.vk.com/method/utils.getShortLink'
    response = requests.post(vk_url, data={"access_token": api_key, "url": user_url, "v": "5.199"})
    response.raise_for_status()
    data = response.json()
    if 'error' in data:
        return True
    return False
    
def main():
    load_dotenv('.env')
    vk_api_key = os.environ['VK_API_KEY']
    user_url = input("Введите ссылку:")

    try:
        if is_shorten_link(user_url, vk_api_key) is True:
            print(f"Статистика переходов: {count_clicks(vk_api_key, user_url)}")
        else:
            short_link = shorten_link(user_url, vk_api_key)
            print(f"Сокращенная ссылка: {short_link}")
            print(f"Статистика переходов: {count_clicks(vk_api_key, short_link)}")
    except KeyError as e:
        print(f"Ошибка в ключе: {e}")
        print("Ответ VK не соответствует параметрам, проверьте ссылку!")
    except requests.exceptions.HTTPError:
        print("Ответ не был получен!")
    except IndexError:
        print("Статистика кликов отсутсвует!")


if __name__ == "__main__":
    main()