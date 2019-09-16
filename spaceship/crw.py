import time # 해시태그를 분석하기 위한 Twitter 모듈
from selenium import webdriver # 페이지 스크롤링을 위한 모듈
from selenium.webdriver.common.keys import Keys
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
# 크롤링할 url 주소
url = "https://www.instagram.com/explore/tags/강아지/"
# 다운로드 받은 driver 주소
DRIVER_DIR = '/path/to/chromedriver'
# 크롬 드라이버를 이용해 임의로 크롬 브라우저를 실행시켜 조작한다.
driver = webdriver.Chrome("C:\\instagram-crawler-master\\chromedriver.exe")
# driver.implicitly_wait(5) 5초대기
driver.get(url)
totalCount = driver.find_element_by_class_name('g47SY ').text #총 게시물 수
print("총 게시물:", totalCount)
# body 태그를 태그 이름으로 찾기
elem = driver.find_element_by_tag_name("body")
alt_list = []
pagedowns = 1
# 스크롤을 30번 진행한다.
while pagedowns < 30:
        # PAGE_DOWN(스크롤)에 따라서 결과 값이 달라진다.
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(1) # 페이지 스크롤 타이밍을 맞추기 위해 sleep
        img = driver.find_elements_by_css_selector('div.KL4Bh > img')
        for i in img:
            if not i.get_attribute('alt') in alt_list:
                alt_list.append(i.get_attribute('alt'))
        pagedowns += 1

f=open("instagram.txt", "wt", encoding='utf-8')
for i in range(len(alt_list)):
    f.write(alt_list[i])