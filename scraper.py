import json
import time
import requests
from selenium import webdriver # selenium 4.20.0
from selenium.webdriver.chrome.service import Service as ChromeService
import ScraperFC
import openpyxl
import unicodedata
from webdriver_manager.chrome import ChromeDriverManager # version 4.0.1
from PLplayer import PLPlayer

Fixes = str.maketrans({
    "Ø": "O", "ø": "o",
    "Å": "A", "å": "a",
    "Æ": "AE", "æ": "ae",
    "Ä": "Ae", "ä": "ae",
    "Ö": "Oe", "ö": "oe",
    "Ü": "Ue", "ü": "ue",
    "ß": "ss",
    "Ç": "C", "ç": "c",
    "Ñ": "N", "ñ": "n",
    "É": "E", "é": "e",
    "È": "E", "è": "e",
    "Ê": "E", "ê": "e",
    "Ë": "E", "ë": "e",
    "Ł": "L", "ł": "l",
    "Đ": "D", "đ": "d",
    "Ń": "N", "ń": "n",
    "Š": "S", "š": "s",
    "Ž": "Z", "ž": "z"
})

def remove_accents(text):
    text = text.translate(Fixes)
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))

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
        return data
    else:
        print("ERROR")

def SinglePlayer(RealIDPlayer, prev_pointer=0):
    sofa = ScraperFC.Sofascore()
    data = sofa.scrape_player_league_stats('24/25','EPL')
    last_row = data.index[-1]
    last_column = data.columns.get_loc(data.columns[-1])
    Found = False
    while(not Found and prev_pointer<last_column):
        if last_column == 53:
            checking_id = data.iloc[prev_pointer,52]
            if RealIDPlayer == checking_id:
                goals = data.iloc[prev_pointer,0]
                assists = data.iloc[prev_pointer,10]
                Found = True

            else:
                prev_pointer+=1
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
            checking_id = data.iloc[prev_pointer,i_made]
            if RealIDPlayer == checking_id:
                goals = data.iloc[prev_pointer,g]
                assists = data.iloc[prev_pointer,a]
                
                Found = True
                print(True)
            else:
                prev_pointer+=1
                
    if(Found):
        return(int(goals),int(assists),prev_pointer)
    else:
        print("Player doesn't exist")
        return 0
    
def DirectPlayer(PlayerName):
    sofa = ScraperFC.Sofascore()
    dataPL = sofa.scrape_player_league_stats('24/25','EPL')
    dataLL = sofa.scrape_player_league_stats('24/25','La Liga')
    i = 0
    last_columnPL = dataPL.columns.get_loc(dataPL.columns[-1])
    last_columnLL = dataLL.columns.get_loc(dataLL.columns[-1])
    while(i<max(last_columnLL,last_columnPL)):
        if(i<last_columnPL):
            if(remove_accents(PlayerName) == remove_accents(dataPL.iloc[i,50])):
                goals = int(dataPL.iloc[i,0])
                assists = int(dataPL.iloc[i,10])
                team = dataPL.iloc[i,51]
                id = dataPL.iloc[i,52]
                ga = goals+assists
                player = PLPlayer(id,PlayerName,ga,team)
                print(player.show())
                return (True,player.show())
        if(i<last_columnLL):
            if(remove_accents(PlayerName) == remove_accents(dataLL.iloc[i,50])):
                goals = int(dataLL.iloc[i,0])
                assists = int(dataLL.iloc[i,10])
                team = dataLL.iloc[i,51]
                id = dataLL.iloc[i,52]
                ga = goals+assists
                player = PLPlayer(id,PlayerName,ga,team)
                print(player.show())
                return (True,player.show())
        i+=1
    return False