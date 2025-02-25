import json
import time
import requests
from selenium import webdriver # selenium 4.20.0
from selenium.webdriver.chrome.service import Service as ChromeService

from webdriver_manager.chrome import ChromeDriverManager # version 4.0.1

baseURL = None

chromedriver_path = r'C:\Users\kolbe\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe' #ChromeDriverManager.install() did't work for me idk why here i put where i have installed my chromedrivers manually
options = webdriver.ChromeOptions()
options.set_capability(
    "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
)

driver = webdriver.Chrome(service=ChromeService(chromedriver_path), options=options)
driver.set_page_load_timeout(10)

try:
    driver.get("https://www.sofascore.com/pl/turniej/pilka-nozna/england/premier-league/17#id:61627,tab:matches")
except:
    print("Error in loading site")
    pass

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

logs_raw = driver.get_log("performance")

logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
found = False
for x in logs:
    if 'total' in x['params'].get('headers', {}).get(':path', ''):
        #print(x['params'].get('headers', {}).get(':path'))
        baseURL = x['params'].get('headers', {}).get(':path')
        found = True
        break

if not found:
    print("Nie znaleziono odpowiednich danych w logach.")

baseURL = "https://www.sofascore.com" + baseURL

response = requests.get(baseURL)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("ERROR")

