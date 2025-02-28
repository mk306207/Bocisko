import json
import time
import requests
from selenium import webdriver # selenium 4.20.0
from selenium.webdriver.chrome.service import Service as ChromeService
import ScraperFC


from webdriver_manager.chrome import ChromeDriverManager # version 4.0.1
def PLData(sofa_link: str, SofaAPI_key):
    baseURL = None

    chromedriver_path = r'C:\Users\kolbe\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe' #ChromeDriverManager.install() did't work for me idk why here i put where i have installed my chromedrivers manually
    options = webdriver.ChromeOptions()
    options.set_capability(
        "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
    )
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=ChromeService(chromedriver_path), options=options)
    driver.set_page_load_timeout(10)

    try:
        driver.get(sofa_link)
    except:
        print("Error in loading site")
        pass

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #time.sleep(1)
    logs_raw = driver.get_log("performance")

    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
    found = False
    for x in logs:
        if SofaAPI_key in x['params'].get('headers', {}).get(':path', ''):
            #print(x['params'].get('headers', {}).get(':path'))
            baseURL = x['params'].get('headers', {}).get(':path')
            found = True
            break

    if not found:
        print("Nie znaleziono odpowiednich danych w logach.")
        return 0

    baseURL = "https://www.sofascore.com" + baseURL

    response = requests.get(baseURL)

    if response.status_code == 200:
        data = response.json()
        with open("response_data.txt", "w") as file:
            json.dump(data, file, indent=4)
        return data
    else:
        print("ERROR")



def PlayerData(sofa_link: str):

    baseURL = "https://www.sofascore.com/api/v1/unique-tournament/17/season/61627/statistics?limit=20&order=-rating&accumulation=total&group=summary"
    chromedriver_path = r'C:\Users\kolbe\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'
    options = webdriver.ChromeOptions()
    options.set_capability(
        "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
    )
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=ChromeService(chromedriver_path), options=options)
    driver.set_page_load_timeout(10)

    try:
        driver.get(sofa_link)
        
    except:
        print("Error in loading site")
        pass

    response = requests.get(baseURL)

    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        print("ERROR")

def SinglePlayer(RealIDPlayer,player_slug):
    sofa = ScraperFC.Sofascore()
    headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
    }
    sofa_link=f"https://www.sofascore.com/pl/zawodnik/{player_slug}/{RealIDPlayer}"
    baseURL = f"https://www.sofascore.com/api/v1/player/{RealIDPlayer}/statistics"
    chromedriver_path = r'C:\Users\kolbe\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'
    options = webdriver.ChromeOptions()
    options.set_capability(
        "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
    )
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=ChromeService(chromedriver_path), options=options)
    driver.set_page_load_timeout(10)

    try:
        driver.get(sofa_link)
        print(True)
        
    except:
        print("Error in loading site")
        pass
    
    #print(sofa.get_valid_seasons(sofa,"EPL"))
    response = requests.get(baseURL, headers=headers)
    data = sofa.scrape_player_league_stats('24/25','EPL')
    data.to_excel("scraper_fc.xlsx", index=False)
        # for s in seasons:
        #     statistics = s['statistics']
        #     season_year = s['year']
        #     with open("response_data.txt", "w") as file:
        #         json.dump(s, file, indent=4)
            # if(season_year == "24/25"):
                # goals = statistics['goals']
                # print(f"{season_year}g = {goals}")
                # print(s)
            
    # else:
    #     print("ERROR")