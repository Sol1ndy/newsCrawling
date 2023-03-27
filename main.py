from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import re

title_text = []
link_text = []
source_text = []
date_text = []
contents_text = []
result = {}

RESULT_PATH = 'C:/Users/User/Desktop/python study/beautifulSoup_ws/crawling_result/'
now = datetime.now()


def date_cleansing(test):
    try:
        pattern = '\d+.(\d+).(\d+).'

        r = re.compile(pattern)
        match = r.search(test).group(0)
        date_text.append(match)

    except AttributeError:
        pattern = '\w* (\d\w*)'

        r = re.compile(pattern)
        match = r.search(test).group(1)
        date_text.append(match)

def contents_cleansing(contents):
    first = re.sub('<dl>.*?</a> </div> </dd> <dd>', '', str(contents)).strip()
    second = re.sub('<ul class="relation_lst">.*?</dd>', '', first).strip()
    last = re.sub('<.+?>', '', second).strip()
    contents_text.append(last)


def crawler(maxpage, query, sort, s_date, e_date):
    s_from = s_date.replace(".", "")
    e_to = e_date.replace(".", "")
    page = 1
    maxpage_t = (int(maxpage) - 1) * 10 + 1

    while page <= maxpage_t:
        url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort=" + sort + "&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(page)

        response = requests.get(url)
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')

        tags = soup.select('.news_tit')
        for tag in tags:
            title_text.append(tag.text)
            link_text.append(tag['href'])

        sourceList = soup.select('.info_group > .press')
        for source_list in sourceList:
            source_text.append(source_list.text)

        date_lists = soup.select('.info_group > span.info')
        for date_list in date_lists:
            if date_list.text.find("면") == -1:
                date_text.append(date_list.text)

        contents_lists = soup.select('.news_dsc')
        for contents_list in contents_lists:
            contents_cleansing(contents_list)

        result = {"date": date_text, "title": title_text, "source": source_text, "contents": contents_text,
                  "link": link_text}
        print(page)

        df = pd.DataFrame(result)
        page += 10

    outputFileName = '%s-%s-%s  %s:%s:%s' % (
    now.year, now.month, now.day, now.hour, now.minute, now.second)
    df.to_excel(RESULT_PATH + outputFileName, sheet_name='sheet1')


def main():
    info_main = input("=" * 50 + "\n" + "입력 형식에 맞게 입력해주세요." + "\n" + " 시작하시려면 Enter를 눌러주세요." + "\n" + "=" * 50)

    maxpage = input("최대 크롤링할 페이지 수 입력하시오: ")
    query = input("검색어 입력: ")
    sort = input("뉴스 검색 방식 입력(관련도순=0  최신순=1  오래된순=2): ")
    s_date = input("시작날짜 입력(2019.01.04):")
    e_date = input("끝날짜 입력(2019.01.05):")

    crawler(maxpage, query, sort, s_date, e_date)


main()
