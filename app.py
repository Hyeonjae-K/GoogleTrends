from flask import Flask, render_template
from selenium import webdriver
import time

# 크롤링 시점 기록을 위한 변수 선언
global_date = ''
global_hour = ''


# 크롤링 시점 기록
def set_time():
    global global_date, global_hour
    global_date = time.strftime("%Y%m%d")
    global_hour = time.strftime("%H")


# Google Trends 크롤러
def crawl_google():
    # Chrome driver 열기
    driver = webdriver.Chrome()
    # Google Trends url 접속
    driver.get("https://trends.google.com/trends/?geo=KR")
    # 페이지를 모두 로드하기 위해 기다림
    time.sleep(1)

    # div태그에 list-item-title클래스를 갖는 모든 태그를 titles에 list형태로 저장
    titles = driver.find_elements_by_css_selector("div.list-item-title")
    # div태그의 list-item-container클래스를 갖는 모든 태그를 urls에 list형태로 저장
    urls = driver.find_elements_by_css_selector("a.list-item-container")
    # 크롤링한 데이터를 txt파일로 저장할 경로 지정
    # 날짜가 지나면 자동으로 다음 날짜의 txt파일을 생성하고 데이터 저장
    save_path = "./data/{date}.txt".format(date=global_date)

    with open(save_path, "a", encoding="UTF-8") as f:
        # 시간을 기록
        f.write(global_hour + "시\n")
        # 검색어와 url을 기록
        for rank in range(10):
            f.write(titles[rank].text + " " + urls[rank].get_attribute("href") + "\n")

    # Chrome driver 종료
    driver.close()


# Flask 웹 페이지
app = Flask(__name__)


# 기본 path로 접속시 index.html 페이지를 반환
@app.route('/')
def index():
    return render_template("index.html")


# Flask 실행
if __name__ == '__main__':
    app.run()