#! /bin/python
## Web scrapper for official DGT driving license tests ##

import time, json, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service



# THIS IS FOR CHROME v102. For other versions check: https://chromedriver.chromium.org/downloads
driver_path = "chromedriver102.exe"
baseURL = "https://revista.dgt.es/es/test"
startNum = 241
file = 'json/tests_dgtRevista.json'
if not os.path.exists('imgs'): os.mkdir('imgs')
if not os.path.exists('json'): os.mkdir('json')
solved = []
allRepeated = 0

# Selenium config
# Comment '--headless' to see what is going on or debug
service = Service(driver_path)
opt = Options()
opt.add_argument("--window-size=1920,1080")
opt.add_argument("--start-maximized")
opt.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=opt)

def downloadPicture(name,data):
    with open(f'imgs/{name}','wb') as outPng:
        outPng.write(data)

def extract(num):
    pregs = driver.find_elements(By.XPATH,"//article[contains(@class, 'test')]")
    for i, preg in enumerate(pregs):
        code = f'Revista{num}_{i}'

        q = preg.find_element(By.CLASS_NAME,'tit_not').text[3:].strip()
        if not any([True for elem in solved if q in elem.values()]):
            try:
                img_name = f'{code}.png'
                img_data = preg.find_element(By.TAG_NAME, 'img').screenshot_as_png
            except:
                img_name = ''
                img_data = ''
            content = preg.find_element(By.CLASS_NAME,'content_test')
            answers = [op.text[2:].strip() for op in content.find_elements(By.TAG_NAME,"li")]
            sol = content.find_element(By.CLASS_NAME,"content_respuesta").find_element(By.CLASS_NAME,'opcion').get_attribute('innerHTML').lower()
            trans_table = sol.maketrans("abcdefg","0123456")
            correct = sol.translate(trans_table)
            # print(json.dumps({'cod': code, 'answers': answers, 'question': q, 'correct': int(correct), 'img': img, 'legal': ''}, indent=4, ensure_ascii=False))
            if img_data != '': downloadPicture(img_name, img_data)
            solved.append({'cod': code, 'answers': answers, 'question': q, 'correct': int(correct), 'img': img_name, 'legal': ''})

errors = 0
while errors < 5:
    print(f'Test {startNum}')
    nextURL = f'{baseURL}/Test-num-{startNum}.shtml'
    driver.get(nextURL)
    if(driver.find_element(By.TAG_NAME,'h1').text == 'Not Found'):
        errors += 1
    else:
        extract(startNum)

    with open(file, 'w', encoding='utf8') as outfile:
        json_string = json.dumps({'data': solved}, indent=4, ensure_ascii=False)
        outfile.write(json_string)
    startNum += 1

print(f'Extracted {len(solved)} questions from {baseURL}')
driver.quit()