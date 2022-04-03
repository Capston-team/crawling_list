# 파리바게트 매장 크롤링(미완성)

* 크롤링 대상은 (매장명, 위도, 경도)입니다.

---
## 설치한 패키지 목록
* pip install beautifulSoup4
* pip install selenium
* pip install webdriver-manager
* pip install requests
---

## 부가 설명

맥북이 chromedriver를 인식하지 못해서 넣은 코드 입니다.
```python
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
```
