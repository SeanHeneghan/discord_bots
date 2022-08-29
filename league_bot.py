from decouple import config
import discord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import BytesIO


intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("__"):
        cmd = message.content.split()[0].replace('__', '')
        
        if cmd == 'runes':
            if len(message.content.split()) > 1:
                champion = message.content.split()[1]
                if type(champion) != str or len(message.content.split()) > 2:
                    await message.channel.send("Please only call the function via __*action* *champion* *game_mode*.")
                else:
                    try:
                        url = f'https://u.gg/lol/champions/{champion}/build'
                    except:
                        await message.channel.send("Not a valid League Of Legends Champion.")
                    else:
                        # set chrome options
                        chrome_options = Options()
                        chrome_options.headless = True
                        
                        # initialise driver
                        driver = webdriver.Chrome(options=chrome_options, executable_path=r"C:\Users\seanh\Downloads\chromedriver_win32\chromedriver.exe")
                        driver.set_window_position(0, 0)
                        driver.set_window_size(1920, 1080)
                        driver.get(url)
                        
                        # deal with privacy setting acceptance
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME,'css-47sehv'))).click()
                        
                        # get rune div from u.gg
                        element = driver.find_element(by=By.XPATH, value="/html/body/div[3]/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div/div[5]/div/div[2]/div/div[1]")
                        file = BytesIO(element.screenshot_as_png)
                        
                        # pm the user the div as an image
                        await message.author.send(file=discord.File(file, 'image.png'))
                        driver.quit()
            else:
                await message.channel.send("Please supply a champion.")

        if cmd == 'build':
            if len(message.content.split()) > 1:
                champion = message.content.split()[1]
                if type(champion) != str or len(message.content.split()) > 2:
                    await message.channel.send("Please only call the function via __*action* *champion* *game_mode*.")
                else:
                    try:
                        url = f'https://u.gg/lol/champions/{champion}/build'
                    except:
                        await message.channel.send("Not a valid League Of Legends Champion.")
                    else:
                        # set chrome options
                        chrome_options = Options()
                        chrome_options.headless = True
                        
                        # initialise driver
                        driver = webdriver.Chrome(options=chrome_options, executable_path=r"C:\Users\seanh\Downloads\chromedriver_win32\chromedriver.exe")
                        driver.set_window_position(0, 0)
                        driver.set_window_size(1920, 1080)
                        driver.get(url)
                        
                        # deal with privacy setting acceptance
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME,'css-47sehv'))).click()
                        
                        # get build div from u.gg
                        element = driver.find_element(by=By.XPATH, value="/html/body/div[3]/div/div[2]/div[2]/div/div/div/div/div/div/div/div[5]/div/div[7]")
                        file = BytesIO(element.screenshot_as_png)
                        
                        # pm the user the div as an image
                        await message.author.send(file=discord.File(file, 'image.png'))
                        driver.quit()
            else:
                await message.channel.send("Please supply a champion.")

        if cmd == 'skills':
            if len(message.content.split()) > 1:
                champion = message.content.split()[1]
                if type(champion) != str or len(message.content.split()) > 2:
                    await message.channel.send("Please only call the function via __*action* *champion* *game_mode*.")
                else:
                    try:
                        url = f'https://u.gg/lol/champions/{champion}/build'
                    except:
                        await message.channel.send("Not a valid League Of Legends Champion.")
                    else:
                        # set chrome options
                        chrome_options = Options()
                        chrome_options.headless = True
                        
                        # initialise driver
                        driver = webdriver.Chrome(options=chrome_options, executable_path=r"C:\Users\seanh\Downloads\chromedriver_win32\chromedriver.exe")
                        driver.set_window_position(0, 0)
                        driver.set_window_size(1920, 1080)
                        driver.get(url)
                        
                        # deal with privacy setting acceptance
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME,'css-47sehv'))).click()
                        
                        # get skills div from u.gg
                        element = driver.find_element(by=By.XPATH, value="/html/body/div[3]/div/div[2]/div[2]/div/div/div/div/div/div/div/div[5]/div/div[4]")
                        file = BytesIO(element.screenshot_as_png)
                        
                        # pm the user the div as an image
                        await message.author.send(file=discord.File(file, 'image.png'))
                        driver.quit()
            else:
                await message.channel.send("Please supply a champion.")


@client.event
async def on_presence_update(before, after):
    activity = after.activity
    if activity and \
        activity.name == 'League of Legends' and \
        activity.state == 'In Game':
        
        champion = activity.large_image_text.lower().replace("'", "").replace(".", "").replace(" ", "")
        user = client.get_user(after.id)
        await user.send(f'Hey, I noticed you are playing {champion}. Here are some pieces of information that might help you out.')
        url = f'https://u.gg/lol/champions/{champion}/build'
        # set chrome options
        chrome_options = Options()
        chrome_options.headless = True
        
        # initialise driver
        driver = webdriver.Chrome(options=chrome_options, executable_path=r"C:\Users\seanh\Downloads\chromedriver_win32\chromedriver.exe")
        driver.set_window_position(0, 0)
        driver.set_window_size(1920, 1080)
        driver.get(url)
        
        # deal with privacy setting acceptance
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME,'css-47sehv'))).click()
        
        element = driver.find_element(by=By.XPATH, value="/html/body/div[3]/div/div[2]/div[2]/div/div/div/div/div/div/div/div[5]/div/div[4]")
        file = BytesIO(element.screenshot_as_png)
        await user.send(f"This is the skilling order for {champion}.", file=discord.File(file, 'image.png'))
        
        element = driver.find_element(by=By.XPATH, value="/html/body/div[3]/div/div[2]/div[2]/div/div/div/div/div/div/div/div[5]/div/div[7]")
        file = BytesIO(element.screenshot_as_png)
        await user.send(f"These are the items you should be building for {champion}, in order.", file=discord.File(file, 'image.png'))
        driver.quit()

client.run(config('CLIENT_RUN_KEY'))
