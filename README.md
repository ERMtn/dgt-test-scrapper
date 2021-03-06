[![Version](https://img.shields.io/pypi/pyversions/selenium)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/Selenium-4.2.0-blue)](https://selenium-python.readthedocs.io/)

# DGT test scrapper
Some Python scripts to extract driving license tests questions from official DGT (Dirección General de Tráfico) sources and other webs. THey will retrieve the question, choices, correct answer and image from the sources.

# Requirements and information
You will need to check your installed Chrome browser version (chrome://settings/help) then download the appropriate *chromedriver* version. This was tested with Chrome v102.0.5005.115.
<center>

[![Chromedriver](https://img.shields.io/badge/Chromedriver-%3E%3D%20102-lightgrey)](https://chromedriver.chromium.org/downloads/)
</center>

This will extract all questions with images and solutions into a JSON format.
```
{
    data: [
        {
            "cod": " ... ",
            "answers": [
                " ... ",
                " ... ",
                " ... ",
                  ...
            ],
            "question": " ... ",
            "correct": 0,
            "img": " ... ",
            "legal": " ... "
        },
        { ... }
    ]
}
```
The extracted questions can be found in the folder **json** and the related images are saved to **imgs**.

**Caution** If you execute all scripts the **imgs** folder will have **A TON** of images.



---
## Supported sites
- [sedeapl.dgt.gob.es](https://sedeapl.dgt.gob.es/WEB_EXAM_AUTO/service/TiposExamenesServlet#)
- [vialtest.com](https://vialtest.com/dgt-examenes/)
- [revista.dgt.es](https://revista.dgt.es/es/test/)
---
## Other test sources
- [todotest.com](https://www.todotest.com)
