[![Version](https://img.shields.io/pypi/pyversions/selenium)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/Selenium-4.2.0-blue)](https://selenium-python.readthedocs.io/)

# DGT test scrapper
You will need to check your installed [Chrome browser version](chrome://settings/help) then download the appropriate *chromedriver* version. This was tested with Chrome v102.
<center>

[![Chromedriver](https://img.shields.io/badge/Chromedriver-%3E%3D%20102-lightgrey)](https://chromedriver.chromium.org/downloads/)
</center>

This will extract all questions with images and solutions into a JSON format.
```
[
  {
    "question": " ... ",
    "img": "https://... ",
    "options": [
      "A) ... ",
      "B) ... ",
      "C) ... ",
          ...
    ],
    "solution": "B) ... "
  },
  { ... }
]
```



---
## Supported sites
- [sedeapl.dgt.gob.es](https://sedeapl.dgt.gob.es/WEB_EXAM_AUTO/service/TiposExamenesServlet#)
- [vialtest.com](https://vialtest.com/dgt-examenes/)
---
## Other test sources
- [revista-dgt.es](https://revista.dgt.es/es/test/)
