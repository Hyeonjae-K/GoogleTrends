from flask import Flask, render_template
from selenium import webdriver
from apscheduler.schedulers.background import BackgroundScheduler
import time

# 크롤링 시점 기록을 위한 변수 선언
global_date = ''
global_hour = ''
# 데이터를 저장할 딕셔너리 생성
data = {}


# 크롤링 시점 기록
def set_time():
    global global_date, global_hour
    global_date = time.strftime("%Y%m%d")
    global_hour = time.strftime("%H")


# Google Trends 크롤러
def crawl_google():
    # 크롤링 시작 전 시간 업데이트
    set_time()
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
    save_path = "./data/{date}.txt".format(date=global_date)

    # 해당 경로에 txt 파일이 없을 경우 txt 파일 추가
    # 해당 경로의 파일에 데이터를 추가함
    with open(save_path, "a", encoding="UTF-8") as f:
        # 시간을 기록
        f.write(global_hour + "시\n")
        # 검색어와 url을 기록
        for rank in range(10):
            f.write(titles[rank].text + " " + urls[rank].get_attribute("href") + "\n")

    # Chrome driver 종료
    driver.close()


# 데이터를 읽어서 저장함
def read_data():
    # 데이터가 있는 파일의 경로 저장
    save_path = "./data/{date}.txt".format(date=global_date)
    
    # 해당 경로의 파일을 읽음
    with open(save_path, "r", encoding="UTF-8") as f:
        # 시간을 키로, 검색어와 url 리스트를 값으로 data에 저장
        while True:
            data_time = f.readline().strip()
            if data_time == '':
                break

            titles = []
            urls = []

            for rank in range(10):
                title, space, url = f.readline().strip().rpartition(" ")

                titles.append(title)
                urls.append(url)

            data[data_time] = {"titles": titles, "urls": urls}


# 0시가 됐을 때 data 변수를 초기화 하기 위한 함수
def clear_data():
    data.clear()


# 자동 실행을 위한 APScheduler 사용
sched = BackgroundScheduler()
sched.add_job(crawl_google, 'cron', minute='0')
sched.start()

# Flask 웹 페이지
app = Flask(__name__)


# 기본 path로 접속시 index.html 페이지를 반환
@app.route('/')
def index():
    read_data()
    # data 딕셔너리를 인자로 index.html에 전달
    return render_template("index.html", data=data)


# Flask 실행
if __name__ == '__main__':
    crawl_google()
    app.run()