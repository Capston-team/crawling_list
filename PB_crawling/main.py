from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert

from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import folium
import collections
from collections import OrderedDict
import csv
import lxml

service= Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(5)
url = 'https://www.paris.co.kr/store/'
driver.get(url)

# 위치 권한 거부 옵션
option = webdriver.ChromeOptions()
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = { "popups": 0 }

# alert = Alert(driver)
# alert.dismiss()

#driver.switch_to.alert().dismiss();

pb = []

# 검색해서 매장찾기 클릭
search = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div[1]/div[1]/div[1]/ul/li[2]/a')
search.send_keys(Keys.ENTER)
time.sleep(1)


# 도/시 선택 클릭
label = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div[1]/div[1]/div[1]/div/form/div[2]/div[1]/div/div[2]/span')
driver.execute_script("arguments[0].click();", label)
time.sleep(1)

list_box = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div[1]/div[1]/div[1]/div/form/div[2]/div[1]/div/div[3]/div/div[1]')
city_list = list_box.find_elements(by=By.TAG_NAME, value='li')
# city_list = list_box.find_elements_by_tag_name('li')

# "도시/선택" 반복 클릭
for list in city_list:
    #"도시/선택"은 클릭에서 제외
    if '0' == list.get_attribute('data-index'):
        continue

    driver.execute_script("arguments[0].click();", list)
    time.sleep(1)
    src = driver.page_source
    print(src)
    soup = BeautifulSoup(src, 'lxml')
    # print(soup.find_all('div', 'store-list-item'))
    # store_list = driver.find_elements(by=By.ID, value='store_list')
    name = soup.find('h3', {'class': 'store-name'})
    break



time.sleep(3)


