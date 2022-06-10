#! /bin/python
## Web scrapper driving license tests from vialtest.com ##
import time, re, json
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
opt.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=opt)

def downloadPicture(name,data):
    with open(f'imgs/{name}','wb') as outPng:
        outPng.write(data)

def fillTest(url):
    global allRepeated
    driver.get(url)
    time.sleep(0.5)
    btn = driver.find_element(By.ID, 'bt-corrector')
    preguntas = driver.find_elements(By.XPATH, "//input[@value = 'option1']")
    for p in preguntas:
        id = p.get_attribute('id')
        driver.find_element(By.XPATH, f"//label[@for = '{id}']").click()
    btn.click()
    time.sleep(0.35)
    code = driver.find_element(By.XPATH,"//a[contains(@href,'dgt-examenes/permiso')]").text.replace(' ','_')
    extractAnswers(code)

def extractAnswers(code):
    preguntas = driver.find_elements(By.XPATH, "//div[contains(@id, 'quest_')]")
    driver.find_element(By.XPATH,"//a[text()='Ver corrección']").click()
    repeats = 0
    for p in preguntas:
        code = f'Vialtest-{code}_{len(solved)}'
        q = p.find_element(By.CLASS_NAME, 'quiz').text
        q = re.sub("[0-9]{1,2}\.\s",'',q)
        try:
            img_data = p.find_element(By.CLASS_NAME, 'img-responsive').screenshot_as_png
            img_name = f'{code}.png'
            downloadPicture(img_name,img_data)
        except:
            img_name = ''
        a = p.find_element(By.CLASS_NAME, 'passq').find_element(By.TAG_NAME, 'label').text
        opts = [op.text for op in p.find_elements(By.TAG_NAME, 'label')]
        # print(f'{q} ({img})\n  {"  ".join(opts)}\nCorrecta: {a}\n')
        time.sleep(0.12)
        if not any([True for elem in solved if q in elem.values()]):
            solved.append({'cod': code, 'answers': answers, 'question': q, 'correct': correct, 'img': img_name, 'legal': ''})
        else:
            repeats += 1
            print(' Skip ',end='')

    if repeats == 30: allRepeated += 1


# MAIN EXECUTION
for url in URLs:
    file = f'json/tests_vialtest_{url[0]}.json'
    for x in range(50):
        try:
            print('Iteration',x,f'({url[1]})')
            fillTest(url[1])
            with open(file,'w', encoding='utf-8') as outfile:
                json_string = json.dumps(solved, indent=4, ensure_ascii=False)
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