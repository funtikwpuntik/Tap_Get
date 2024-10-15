import logging
import requests
import datetime
from time import sleep

import get_access_token
import random

headers = {
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'authorization': 'Bearer ',
    'cache-control': 'no-cache',
    'content-id': '',
    'content-type': 'application/json',
    'origin': 'https://app.tapswap.club',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://app.tapswap.club/',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
    'x-app': 'tapswap_server',
    'x-cv': '657',
    'x-touch': '1',
}

json_data = {
    'taps': 450,
    'time': 1725975796284,
}

headers_turbo = {
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'authorization': 'Bearer ',
    'cache-id': 'ee9Er6VW',
    'content-type': 'application/json',
    'origin': 'https://app.tapswap.club',
    'priority': 'u=1, i',
    'referer': 'https://app.tapswap.club/',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
    'x-app': 'tapswap_server',
    'x-cv': '657',
    'x-touch': '1',
}

json_data_turbo = {
    'type': 'turbo',
}

# id * time % id
time_turbo = int(str(datetime.datetime.timestamp(datetime.datetime.today())).replace('.', '')[:-6])


def new_headers():
    settings = get_access_token.access_token()
    user_id = "id_telegram"
    k = 10 ** 21
    time = int(str(datetime.datetime.timestamp(datetime.datetime.today())).replace('.', '')[:-3])

    print(str(time), 'Время')
    print(int(user_id * time / k * k % user_id), 'Контент айди')

    headers['content-id'] = str(int(user_id * time / k * k % user_id))
    headers['cache-id'] = settings['cache_id']
    headers['authorization'] = settings['access_token']

    json_data['time'] = time
    json_data['taps'] = int(settings['energy'] / 12)
    return settings


while True:
    try:
        settings = new_headers()
    except Exception as ex:
        print('Ошибка подключения', ex)
        continue

    new_time_turbo = int(str(datetime.datetime.timestamp(datetime.datetime.today())).replace('.', '')[:-6])
    if new_time_turbo - time_turbo > 0:
        time_turbo = new_time_turbo
        if settings['turbo']['cnt'] > 1:
            headers_turbo['cache-id'] = settings['cache_id']
            headers_turbo['authorization'] = settings['access_token']
            response_turbo = requests.post('https://api.tapswap.club/api/player/apply_boost', headers=headers_turbo,
                                           json=json_data_turbo)
            time = int(str(datetime.datetime.timestamp(datetime.datetime.today())).replace('.', '')[:-3])
            json_data['time'] = time
            json_data['taps'] = 450
            count = 0
            while count < 3:
                response = requests.post('https://api.tapswap.club/api/player/submit_taps', headers=headers,
                                         json=json_data)
                print(response)
                if response.status_code == 201:
                    count += 1
                    print("TURBO")
                    sleep(random.randint(1, 5))
                if response.status_code == 400:
                    print("FAILED TURBO")
                    new_headers()

    response = requests.post('https://api.tapswap.club/api/player/submit_taps', headers=headers, json=json_data)
    print(response, response.json())
    while response.status_code != 201:
        sleep(10)
        new_headers()
        response = requests.post('https://api.tapswap.club/api/player/submit_taps', headers=headers, json=json_data)
        print(response)
    time_sleep = random.randint(50, 1500)
    print(time_sleep // 60, time_sleep % 60, sep=':')
    sleep(time_sleep)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename='log.txt')
