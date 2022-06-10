#! /bin/python
## Web scrapper driving license tests from vialtest.com ##
import time, json, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


driver_path = "chromedriver102.exe"
URLs = [['B',"https://vialtest.com/dgt-examenes/permiso-B/test-de-autoescuela"], ['D',"https://vialtest.com/dgt-examenes/permiso-D/test-de-autoescuela"]]
if not os.path.exists('imgs'): os.mkdir('imgs')
if not os.path.exists('json'): os.mkdir('json')
solved = []
allRepeated = 0

# Selenium configuration
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

def fillTest(url):
    global allRepeated
    driver.get(url)
    time.sleep(0.3)
    btn = driver.find_element(By.ID, 'bt-corrector')
    preguntas = driver.find_elements(By.XPATH, "//input[@value = 'option1']")
    for p in preguntas:
        id = p.get_attribute('id')
        driver.find_element(By.XPATH, f"//label[@for = '{id}']").click()
    btn.click()
    time.sleep(0.2)
    code = driver.find_element(By.XPATH,"//ol[contains(@class,'breadcrumb')]//a[contains(@href,'dgt-examenes/permiso-')]").text.replace(' ','_')
    extractAnswers(code)

def extractAnswers(codeName):
    preguntas = driver.find_elements(By.XPATH, "//div[contains(@id, 'quest_')]")
    driver.find_element(By.XPATH,"//a[text()='Ver corrección']").click()
    repeats = 0
    for p in preguntas:
        code = f'VT-{codeName}_{len(solved)}'
        q = p.find_element(By.CLASS_NAME, 'quiz').text[3:].strip()
        if not any([True for elem in solved if q in elem.values()]):
            try:
                img = p.find_element(By.CLASS_NAME, 'img-responsive')
                img_name = f"VT-{img.get_attribute('src').split('/')[-1]}"
            except:
                img_name = ''
                img_data = ''
            answers = [op.text[2:].strip() for op in p.find_elements(By.TAG_NAME, 'label')]
            sol = p.find_element(By.CLASS_NAME, 'passq').find_element(By.TAG_NAME, 'label').text[2:].strip()
            correct = answers.index(sol)
            time.sleep(0.10)

            if img_name != '':
                img_data = img.screenshot_as_png
                downloadPicture(img_name, img_data)
            solved.append({'cod': code, 'answers': answers, 'question': q, 'correct': correct, 'img': img_name, 'legal': ''})
            # print({'cod': code, 'answers': answers, 'question': q, 'correct': correct, 'img': img_name, 'legal': ''})
        else:
            repeats += 1
            print(' s ',end='')

    if repeats == 30: allRepeated += 1


# MAIN EXECUTION
for url in URLs:
    file = f'json/tests_vialtest_{url[0]}.json'
    print('Extracting from: ',url[1])
    for x in range(70):
        try:
            print('\tIteration',x, end=' ')
            fillTest(url[1])
            with open(file,'w', encoding='utf-8') as outfile:
                json_string = json.dumps({ 'data': solved}, indent=4, ensure_ascii=False)
                outfile.write(json_string)
            print(len(solved))
            if allRepeated > 5:
                driver.quit()
                print(F'\n Extracted {len(solved)} questions from "{url}"')
                solved = []
                break
        except Exception as e:
            if 'invalid session' in str(e):
                driver.quit()
                print("\n ERROR: Invalid session.\n CLOSING PROGRAM")
            else:
                print(f"\n ERROR: {str(e)}\n")
        print()
    print(F'\n Extracted {len(solved)} questions from https://vialtest.com/dgt-examenes')

driver.quit()
