#! /bin/python
# Web scrapper for driving license tests #
# THIS ONLY WORKS IF YOU HAVE SOME KIND OF NETWORK DNS AD-BLOCKER, LIKE Pi-Hole #

import time, json, os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# THIS IS FOR CHROME v102. For other versions check: https://chromedriver.chromium.org/downloads
driver_path = "chromedriver102.exe"
login = 'https://www.todotest.com/personal/usrreg.asp'
baseURL = "https://www.todotest.com"
fileBase = 'json/todotest'
if not os.path.exists('imgs'): os.mkdir('imgs')
if not os.path.exists('json'): os.mkdir('json')
solved = []
allRepeated = 0
totalSolved = 0

# Selenium config
# Comment '--headless' to see what is going on or debug
service = Service(driver_path)
opt = Options()
opt.add_argument("--window-size=1920,1080")
opt.add_argument("--start-maximized")
# opt.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=opt)


def downloadPicture(name,data):
    with open(f'imgs/{name}','wb') as outPng:
        outPng.write(data)

def clickAd():
    try:
        WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//img[contains(@id,'sas_')]")))
        driver.find_element(By.XPATH,"//img[contains(@id,'sas_')]").click() # Close ad
    except: time.sleep(0.01)

def acceptCookies():
    driver.find_element(By.XPATH, "//span[text() = 'ACEPTO']").click()


def extractLicenses():
    driver.get(baseURL)
    opts = driver.find_elements(By.XPATH, "//div[contains(@class,'mdl invert hme')]//a[contains(@title, 'permiso')]")
    return [{'url':a.get_attribute('href'),'name':a.get_attribute('title')} for a in opts]


def extractTests(l):
    global totalSolved
    driver.get(l['url'])
    driver.get(driver.find_element(By.XPATH, "//a[text()='Test oficiales de la DGT']").get_attribute('href'))
    tr = l['name'].maketrans(" /\\","_--")
    fileName = l['name'].translate(tr)
    solved = []
    driver.find_element(By.XPATH, "//label[@for='mod_es']").click()
    tests = [test.get_attribute('href') for test in driver.find_elements(By.XPATH, "//a[contains(@href,'test.asp?t')]")]
    for test in tests:
        driver.get(test)
        time.sleep(0.2)
        try:
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CLASS_NAME, 'x_close')))
            driver.find_element(By.CLASS_NAME, 'x_close').click() # Popup remove ads
        except: time.sleep(.01)

        try: driver.execute_script('Elimina_Resultats()')
        except: time.sleep(0)
        finally: time.sleep(0.1)

        for o in driver.find_elements(By.CLASS_NAME,'a'):
            o.click()
            time.sleep(0.02)

        for preg in driver.find_elements(By.XPATH, "//li/div[@class='cont_preg']"):
            try:
                img = preg.find_element(By.CLASS_NAME, 'img_p').get_attribute('src')
            except Exception as e:
                img = ''
            q = preg.find_element(By.CLASS_NAME,'preg').text[3:].strip()
            opts = preg.find_elements(By.CLASS_NAME, 'resp')
            sol = preg.find_element(By.CLASS_NAME,'p_cor').text.replace("\n","")
            if not any([True for elem in solved if q in elem.values()]):
                solved.append({'question': q, 'img': img, 'options': [o.text.replace("\n","") for o in opts], 'solution': sol})

    totalSolved += len(solved)
    # Save solved questions
    with open(f'{fileBase}/{fileName}.json','w', encoding='utf8') as fileout:
        json_string = json.dumps(solved, indent=4, ensure_ascii=False)
        fileout.write(json_string)
        print(f"TOTAL SOLVED: {totalSolved}")




# MAIN EXECUTION
start = time.time()
try:
    driver.get(login)
    acceptCookies()
    driver.find_element(By.ID, 'e_ini').send_keys('alt.t4-8ndyycv@yopmail.com')
    driver.find_element(By.ID, 'contra').send_keys('hu8v.RA_ngdTAiN')
    driver.find_element(By.ID, 'bot_ini').click()
    licenses = extractLicenses()
    for l in licenses:
        extractTests(l)

except Exception as e:
    print(f"ERROR:\n\t {repr(e)} ")
    driver.quit()
    exit(1)

driver.quit()
print(f"Extracted {totalSolved} questions from {baseURL} in {time.time()- start} seconds.")
exit(0)

