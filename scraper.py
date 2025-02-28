import json
import time
import requests
from selenium import webdriver # selenium 4.20.0
from selenium.webdriver.chrome.service import Service as ChromeService
import ScraperFC
import openpyxl

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

def SinglePlayer(RealIDPlayer):
    sofa = ScraperFC.Sofascore()
    data = sofa.scrape_player_league_stats('24/25','EPL')
    last_row = data.index[-1]
    last_column = data.columns.get_loc(data.columns[-1])
    i = 0
    Found = False
    while(not Found and i<last_column):
        if last_column == 53:
            checking_id = data.iloc[i,52]
            print(checking_id)
            if RealIDPlayer == checking_id:
                goals = data.iloc[i,0]
                assists = data.iloc[i,10]
                
                Found = True

            else:
                i+=1
        else:
            col = 0
            Goals_condition, Assists_coniditon, Id_condition = False
            for col in range(last_column):
                if "player id"==data.iloc[0,col]:
                    Id_condition = True
                    i_made = col
                elif "goals" == data.iloc[0,col]:
                    Goals_condition = True
                    g = col
                elif "assists" == data.iloc[0,col]:                  
                    Assists_coniditon = True
                    a = col
                elif Id_condition is True and Goals_condition is True and Assists_coniditon is True:
                    break
            checking_id = data.iloc[i,i_made]
            print(checking_id)
            if RealIDPlayer == checking_id:
                goals = data.iloc[i,g]
                assists = data.iloc[i,a]
                
                Found = True
                print(True)
            else:
                i+=1
                
    if(Found):
        return(int(goals),int(assists))
    else:
        print("Player doesn't exist")
        return 0
                    
                
