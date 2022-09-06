import cassiopeia as cass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from io import BytesIO
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from decouple import config

client = MongoClient(f"mongodb+srv://{config('MONGODB_USERNAME')}:{config('MONGODB_PASSWORD')}@leaguebot.3wl3vhh.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
league_db = client["leaguebot"]
champions = league_db["champions"]

cass.set_riot_api_key(config("RIOT_API_KEY"))


def prep_champ_names():
    full_champion_list = []
    champ_list = cass.get_champions("EUW")
    for league_champ in champ_list:
        if league_champ.name.startswith("Nunu"):
            full_champion_list.append("nunu")
        elif league_champ.name.startswith("Renata"):
            full_champion_list.append("renata")
        else:
            full_champion_list.append(league_champ.name.replace("'", "").replace(" ", "").lower())
    return full_champion_list


def seed_data():
    champions.drop()
    for name in prep_champ_names():
        try:
            url = f"https://u.gg/lol/champions/{name}/build"
        except:
            print("Could not find a champion profile at: ", f"https://u.gg/lol/champions/{name}/build")
        else:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.set_window_position(0, 0)
            driver.set_window_size(1920, 1080)
            driver.get(url)

            # deal with privacy setting acceptance
            WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.CLASS_NAME, "css-47sehv"))
            ).click()
            driver.implicitly_wait(5)

            # get rune div from u.gg
            element = driver.find_element(
                by=By.XPATH,
                value="/html/body/div[3]/div/div[2]/div[2]/div/div/div/div/div/div/div/div[5]/div/div[2]/div/div[1]",
            )
            rune_file = BytesIO(element.screenshot_as_png)

            # get build div from u.gg
            element = driver.find_element(
                by=By.XPATH,
                value="/html/body/div[3]/div/div[2]/div[2]/div/div/div/div/div/div/div/div[5]/div/div[9]",
            )
            build_file = BytesIO(element.screenshot_as_png)

            # get skills div from u.gg
            element = driver.find_element(
                by=By.XPATH,
                value="/html/body/div[3]/div/div[2]/div[2]/div/div/div/div/div/div/div/div[5]/div/div[6]",
            )
            skill_file = BytesIO(element.screenshot_as_png)

            driver.quit()
        champions.insert_one(
            {"name": name,
             "runes": rune_file.getvalue(),
             "build": build_file.getvalue(),
             "skills": skill_file.getvalue()
             }
        )


seed_data()
