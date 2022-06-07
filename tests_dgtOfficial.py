#! /bin/python
## Web scrapper for official DGT driving license tests ##

import time, re, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# THIS IS FOR CHROME v102. For other versions check: https://chromedriver.chromium.org/downloads
driver_path = "chromedriver102.exe"
baseURL = "https://sedeapl.dgt.gob.es/WEB_EXAM_AUTO/examen/loginExamen.jsp?tipoCuest=B"
file = 'Permiso_B_dgt.json'

allRepeated = 0
solved = []

# Selenium config
# Comment '--headless' to see what is going on or debug
service = Service(driver_path)
opt = Options()
opt.add_argument("--window-size=1920,1080")
opt.add_argument("--start-maximized")
opt.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=opt)

def extract():
    global allRepeated
    try:
        driver.get(baseURL)
        driver.execute_script('doSubmit()')
        driver.execute_script('isFinalizarExamen()')
        time.sleep(0.1)
        driver.execute_script('finalizarExamen()')
        time.sleep(0.1)
        repeats = 0
        for i in range(30):
            q = driver.find_element(By.ID,'textoPreguntaElem').text
            try: img = driver.find_element(By.XPATH, "//img[@id='imgPreguntaElem' and not(contains(@src,'ImagenBlanca'))]").get_attribute('src')
            except: img = ''
            opts = [op.text for op in driver.find_elements(By.XPATH, "//span[@class = 'arial16negro' and text() != '']")]
            a = driver.find_element(By.XPATH,"//tr/td/img[contains(@src,'correcta')]/ancestor::node()[2]//span").text
            # print(f"Pregunta: {q}\nImagen: {img}\nOpciones: {opts}\nSolución: {a}")

            if not any([True for elem in solved if q in elem.values()]):
                solved.append({'question': q, 'img': img, 'options': opts, 'solution': a})
            else:
                repeats += 1
                print(' Skip ', end='')

            if repeats > 10:
                allRepeated += 1
                break;
            driver.execute_script('preguntaSiguiente()')

            # Guardar preguntas actuales
            with open(file, 'w', encoding='utf8') as outfile:
                json_string = json.dumps(solved, indent=4, ensure_ascii=False)
                outfile.write(json_string)
        print()
        time.sleep(0.3)

    except Exception as e:
        driver.quit()
        print(e)

for x in range(30):
    if allRepeated > 5: break;
    print('Iteration',x)
    extract()
driver.quit()