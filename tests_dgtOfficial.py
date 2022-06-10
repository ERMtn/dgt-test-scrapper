#! /bin/python
## Web scrapper for official DGT driving license tests ##

import time, json, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# THIS IS FOR CHROME v102. For other versions check: https://chromedriver.chromium.org/downloads
driver_path = "chromedriver102.exe"
baseURL = "https://sedeapl.dgt.gob.es/WEB_EXAM_AUTO/examen/loginExamen.jsp?tipoCuest=B"
file = 'json/tests_dgtSedeapl.json'
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


def extract():
    global allRepeated
    try:
        driver.get(baseURL)
        driver.execute_script('doSubmit()')
        repeats = 0
        for i in range(30):
            time.sleep(0.05)
            code = f'DGT_Sedeapl_{len(solved)}'
            driver.execute_script('renderizarRespuestasCorregidas()')
            driver.execute_script('actualizarIndicePreguntas()')
            q = driver.find_element(By.ID,'textoPreguntaElem').text
            try:
                img_name = f'{code}.png'
                img_data = driver.find_element(By.XPATH, "//img[@id='imgPreguntaElem' and not(contains(@src,'ImagenBlanca'))]").screenshot_as_png
                downloadPicture(img_name,img_data)

            except:
                img_name = ''
            answers = [op.text for op in driver.find_elements(By.XPATH, "//span[@class = 'arial16negro' and text() != '']")]
            a = driver.find_element(By.XPATH,"//tr/td/img[contains(@src,'correcta')]/ancestor::node()[2]//span").text
            correct = answers.index(a)
            # print(f"Pregunta: {q}\nImagen: {img_name}\nOpciones: {answers}\nSolución: {correct}\n")

            if not any([True for elem in solved if q in elem.values()]):
                solved.append({'cod': code, 'answers': answers, 'question': q, 'correct': correct, 'img': img_name, 'legal': ''})
            else:
                repeats += 1
                print(' Skip ', end='')

            if repeats > 29:
                allRepeated += 1
                break;
            driver.execute_script('preguntaSiguiente()')

            # Guardar preguntas actuales
            with open(file, 'w', encoding='utf8') as outfile:
                json_string = json.dumps({'data': solved}, indent=4, ensure_ascii=False)
                outfile.write(json_string)
        print()
        time.sleep(0.05)

    except Exception as e:
        driver.quit()
        print(e)

for x in range(30):
    if allRepeated > 15: break;
    print('Iteration',x)
    extract()

print(f'Extracted {len(solved)} questions from {baseURL}')
driver.quit()