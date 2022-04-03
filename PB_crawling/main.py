import csv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(5)
url = 'https://www.paris.co.kr/store/'
driver.get(url)

# 위치 권한 거부 옵션
option = webdriver.ChromeOptions()
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"popups": 0}

# 검색해서 매장찾기 클릭
search = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div[1]/div[1]/div[1]/ul/li[2]/a')
search.send_keys(Keys.ENTER)
time.sleep(1)

# 도/시 선택 클릭
label = driver.find_element(by=By.XPATH,
                            value='//*[@id="main"]/div[1]/div[1]/div[1]/div/form/div[2]/div[1]/div/div[2]/span')
driver.execute_script("arguments[0].click();", label)
time.sleep(1)

list_box = driver.find_element(by=By.XPATH,
                               value='//*[@id="main"]/div[1]/div[1]/div[1]/div/form/div[2]/div[1]/div/div[3]/div/div[1]')
city_list = list_box.find_elements(by=By.TAG_NAME, value='li')


# 매장명 리스트로 가져옴
def get_name(store_name):
    name_list = []
    for name in store_name:
        name_list.append(name.get_text().strip('\n'))

    return name_list


# 주소 리스트로 가져옴
def get_addr(store_addr):
    addr_list = []
    for addr in store_addr:
        addr_list.append(addr.get_text().strip('\n'))
    return addr_list


# 위도 리스트로 가져옴
def get_latitude(store_list):
    latitude = []

    for item in store_list:
        latitude.append(item['data-latitude'])

    return latitude


# 경도 리스트로 가져옴
def get_longitude(store_list):
    longitude = []

    for item in store_list:
        longitude.append(item['data-longitude'])

    return longitude


pb = []
# "도시/선택" 반복 클릭
for list in city_list:
    # "도시/선택"은 클릭에서 제외
    if '0' == list.get_attribute('data-index'):
        continue

    driver.execute_script("arguments[0].click();", list)
    time.sleep(1)
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')

    # 페이지에서 매장명, 주소, 위도, 경도 가져오기
    store_list = soup.findAll('div', {'class': 'store-list-item'})
    store_addr = soup.findAll("p", attrs={"class": "store-addr"})
    store_name = soup.findAll("h3", attrs={"class": "store-name"})

    name = get_name(store_name)
    addr = get_addr(store_addr)
    latitude = get_latitude(store_list)
    longitude = get_longitude(store_list)

    pb.append({'Branch': name, 'Location': addr, 'Latitude': latitude, 'Longitude': longitude})

    # print(pb)


# csv 파일에 쓰기
def set_data(pb):
    f = open('PB.csv', 'w', newline='')
    fieldname = ['Branch', 'Location', 'Latitude', 'Longitude']
    writer = csv.DictWriter(f, fieldnames=fieldname)
    writer.writeheader()

    for i in range(len(store_list)):
        for j in pb:
            writer.writerow({'Branch': j['Branch'][i], 'Location': j['Location'][i],
                             'Latitude': j['Latitude'][i], 'Longitude': j['Longitude'][i]})


set_data(pb)

time.sleep(2)

driver.close()
