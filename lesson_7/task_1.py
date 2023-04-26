from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get('https://www.scrapethissite.com/pages/advanced/')

element = driver.find_element(By.ID, 'nav-login')
element.click()
element = driver.find_element(By.ID, 'email')
element.send_keys('enail@mail.ru')
element = driver.find_element(By.ID, 'password')
element.send_keys('1234')
element.send_keys(Keys.ENTER)

element = driver.find_element(By.CLASS_NAME, 'ui-pnotify-title')
print(element.text)