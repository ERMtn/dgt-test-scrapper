#! /bin/python
## Web scrapper driving license tests from vialtest.com ##
import time, re, json
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service



driver_path = "chromedriver102.exe"
baseURL = "https://vialtest.com/dgt-examenes/permiso-B/test-de-autoescuela"
# baseURL = "https://vialtest.com/dgt-examenes/permiso-D/test-de-autoescuela"
file = 'Tests-B_vialtest.json'

allRepeated = 0
solved = []

# Selenium configuration
# Comment '--headless' to see what is going on or debug
service = Service(driver_path)
opt = Options()
opt.add_argument("--window-size=1920,1080")
opt.add_argument("--start-maximized")
opt.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=opt)

def fillTest():
    global allRepeated
    driver.get(baseURL)
    time.sleep(0.6)
    btn = driver.find_element(By.ID, 'bt-corrector')
    preguntas = driver.find_elements(By.XPATH, "//input[@value = 'option1']")
    for p in preguntas:
        id = p.get_attribute('id')
        driver.find_element(By.XPATH, f"//label[@for = '{id}']").click()
    btn.click()
    time.sleep(0.35)
    extractAnswers()

def extractAnswers():
    preguntas = driver.find_elements(By.XPATH, "//div[contains(@id, 'quest_')]")
    driver.find_element(By.XPATH,"//a[text()='Ver corrección']").click()
    repetidas = 0
    for p in preguntas:
        q = p.find_element(By.CLASS_NAME, 'quiz').text
        q = re.sub("[0-9]{1,2}\.\s",'',q)
        try:
            img = p.find_element(By.CLASS_NAME, 'img-responsive').get_attribute('src')
        except:
            img = ''
        a = p.find_element(By.CLASS_NAME, 'passq').find_element(By.TAG_NAME, 'label').text
        opts = [op.text for op in p.find_elements(By.TAG_NAME, 'label')]
        # print(f'{q} ({img})\n  {"  ".join(opts)}\nCorrecta: {a}\n')
        time.sleep(0.12)
        if not any([True for elem in solved if q in elem.values()]):
            # print(f'Added "{q}"')
            solved.append({'question':q, 'img': img, 'options':opts, 'solution':a})
        else:
            repetidas += 1
            print(' Skip ',end='')

    if repetidas == 30: allRepeated += 1

x = 0
while(True):
    print('Iteración',x)
    fillTest()
    with open(file,'w', encoding='utf-8') as outfile:
        json_string = json.dumps(solved, indent=4, ensure_ascii=False)
        outfile.write(json_string)

    print(len(solved))
    if allRepeated > 5:
        driver.quit()
        print(F'\n EXTRAIDAS {len(solved)} PREGUNTAS DE "{baseURL}"')
        exit(0)
    x += 1