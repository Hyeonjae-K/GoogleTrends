from flask import Flask, render_template
from selenium import webdriver


# Google Trends 크롤러
def crawl_google():
    # Chrome driver 열기
    driver = webdriver.Chrome()
    # Google Trends url 접속
    driver.get("https://trends.google.com/trends/?geo=KR")

    # div태그에 list-item-title클래스를 갖는 모든 태그를 titles에 list형태로 저장
    titles = driver.find_elements_by_css_selector("div.list-item-title")
    # div태그의 list-item-container클래스를 갖는 모든 태그를 urls에 list형태로 저장
    urls = driver.find_elements_by_css_selector("a.list-item-container")

    # Chrome driver 종료
    driver.close()