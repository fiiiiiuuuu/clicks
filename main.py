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


def is_shorten_link(user_url, api_key):
    vk_url = 'https://api.vk.com/method/utils.getShortLink'
    response = requests.post(vk_url, data={"access_token": api_key, "url": user_url, "v": "5.199"})
    response.raise_for_status()
    if 'error' in response.json():
        return user_url
    else:
        return shorten_link(user_url, api_key)
        

def main():
    load_dotenv('.env')
    vk_api_key = os.environ['VK_API_KEY']
    user_url = input("Введите ссылку:")
    
    short_link = is_shorten_link(user_url, vk_api_key)
    parsed_url = urllib.parse.urlparse(short_link)
    try:
        print(f"Сокращенная ссылка: {short_link}")
        print(f"Статистика переходов: {count_clicks(vk_api_key, parsed_url)}")
    except KeyError:
        print("Ответ VK не соответствует параметрам, проверьте ссылку!")
    except requests.exceptions.HTTPError:
        print("Ответ не был получен!")
    except IndexError:
        print("Статистика кликов отсутсвует!")


if __name__ == "__main__":
    main()