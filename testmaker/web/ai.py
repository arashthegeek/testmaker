#pip install selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

def quastiontojson(quastion):
    chrome_path = r"C:\Program Files\chrome-win64\chrome.exe"
    chromedriver_path = r"C:\Users\USER\Desktop\test lab\chromedriver-win64\chromedriver.exe"
    chrome_options = Options()
    chrome_options.binary_location = chrome_path
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    ai_url = "https://huggingface.co/deepseek-ai/DeepSeek-R1"
    driver.get(ai_url)

    cookie = {"name":"token","value":"nObSqlYIJPjHDYPrCFRHWWTukpDoOfLgbUVjVKomidbFRNOhthOyxyVCSlxhBLTIqtILVuyjIEYATmgkSTvnqcavIzjUlRSvEYykUbMyTkBGkPiLlJCkHWFtEziKhjfR","domain":"huggingface.co"}
    driver.add_cookie(cookie)

    driver.refresh()

    sleep(6)

    inputs = driver.find_elements(By.CSS_SELECTOR, '.rounded-t-none')
    input_text = inputs[0]
    input_submit = inputs[1]

    input_text.send_keys(quastion)
    input_submit.click()

    sleep(60)
    message_divs = driver.find_elements(By.CSS_SELECTOR, '.prose-widget')
    try:
        ai_response_div = message_divs[1]
    except:
        return None
        
    ai_response_paragraphs = ai_response_div.find_elements(By.CSS_SELECTOR, 'p')
    ai_response_text = ""
    #TODO try in here and if it has error jump to line 33
    for j in ai_response_paragraphs:
        print("j: "+str(j.text))
        ai_response_text += str(j.text)
        
    print(ai_response_text)
    
    ai_response_span = ai_response_div.find_elements(By.TAG_NAME, 'span')#hljs-punctuation hljs-attr hljs-string hljs-number hljs-literal and...

    ai_response_code = ""
    for x in ai_response_span:
        ai_response_code += x.text + " "
    return ai_response_code.replace('json Copy ','')