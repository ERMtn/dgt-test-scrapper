#! /bin/python
## Web scrapper for official DGT driving license tests ##

import time, json, os, re
from urllib import parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# THIS IS FOR CHROME v102. For other versions check: https://chromedriver.chromium.org/downloads
driver_path = "chromedriver102.exe"
baseURL = "https://sedeapl.dgt.gob.es/WEB_EXAM_AUTO/service/TiposExamenesServlet#"
examURL = "https://sedeapl.dgt.gob.es/WEB_EXAM_AUTO/examen/loginExamen.jsp?tipoCuest="
if not os.path.exists('imgs'): os.mkdir('imgs')
if not os.path.exists('json'): os.mkdir('json')
solved = []
total = 0
allRepeated = 0

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


def extract(tipo):
    global allRepeated
    try:
        file = f'json/tests_dgtSedeapl_{tipo}.json'
        driver.execute_script('doSubmit()')
        repeats = 0
        time.sleep(0.07)
        driver.execute_script('corregirExamen()')
        time.sleep(0.07)
        total = int(driver.find_element(By.XPATH,"//td[contains(text(), 'Total Preguntas')]").text[-3:].strip())
        for i in range(total):
            time.sleep(0.05)
            code = f"DGTSedeapl_{tipo}_{len(solved)}"
            driver.execute_script('renderizarRespuestasCorregidas()')
            driver.execute_script('actualizarIndicePreguntas()')
            q = driver.find_element(By.ID,'textoPreguntaElem').text
            if not any([True for elem in solved if q in elem.values()]):
                try:
                    img = driver.find_element(By.XPATH, "//img[@id='imgPreguntaElem' and not(contains(@src,'ImagenBlanca'))]")
                    img_name = f"DGT_Sedeapl_{img.get_attribute('src').split('/')[-1]}"
                except:
                    img_name = ''
                    img_data = ''
                answers = [op.text for op in driver.find_elements(By.XPATH, "//span[@class = 'arial16negro' and text() != '']")]
                a = driver.find_element(By.XPATH,"//tr/td/img[contains(@src,'correcta')]/ancestor::node()[2]//span").text
                correct = answers.index(a)
                # print(f"Pregunta: {q}\nImagen: {img_name}\nOpciones: {answers}\nSolución: {correct}\n")


                if img_name != '':
                    img_data = img.screenshot_as_png
                    downloadPicture(img_name, img_data)

                solved.append({'cod': code, 'answers': answers, 'question': q, 'correct': correct, 'img': img_name, 'legal': ''})
            else:
                repeats += 1
                print('s ', end='')
            if repeats >= total:
                allRepeated += 1
                break;
            driver.execute_script('preguntaSiguiente()')

        # Guardar preguntas actuales
        with open(file, 'w', encoding='utf8') as outfile:
            json_string = json.dumps({'data': solved}, indent=4, ensure_ascii=False)
            outfile.write(json_string)

    except Exception as e:
        print(repr(e))
        allRepeated += 1
        return

# MAIN EXECUTION
driver.get(baseURL)
enlaces = driver.find_elements(By.CLASS_NAME,'enlacesExamen')
tipos = [re.search("'(.*)'",e.get_attribute('onclick')).group(1) for e in enlaces]
for t in tipos[7:]:
    url = f"{examURL}{parse.quote(t)}"
    print(f"Tipo: {t} > goto {url}")
    for i in range(30):
        if allRepeated > 7: break;
        print('\tIteration',i, end=' ')
        driver.get(url)
        extract(t.replace(' ','_'))
        print(f' RA={allRepeated}')

    print(f'\tExtracted {len(solved)} questions for type {t}')
    total += len(solved)
    solved = []
    allRepeated = 0


# for x in range(30):
#     if allRepeated > 10: break;
#     print('Iteration',x)
#     extract(baseURL)

print(f'Extracted {total} questions from {baseURL}')
driver.quit()