import json

from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")


def access_token():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("url_for_webapp")
    driver.wait_for_request(pat='challenge')
    settings = {}
    # Перехватываем запросы
    token = ''
    for request in driver.requests:
        if 'challenge' in request.url:
            di = json.loads(request.response.body.decode())
            token = di['access_token']
            settings['access_token'] = 'Bearer ' + di['access_token']
            settings['turbo'] = di['player']['boost'][1]
            settings['charge_level'] = di['player']['charge_level']
            settings['energy'] = di['player']['energy']
            settings['cache_id'] = request.headers.get('cache-id')
            print(json.dumps(settings, indent=4))
    driver.quit()
    if token:
        return settings
    else:
        return
