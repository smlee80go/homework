import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# 아래 빈 칸('')을 채워보세요
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

trs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
# 아래 빈 칸('')을 채워보세요
for tr in trs:
    rank = tr.select_one('td.number').text[0:2].strip()

    title = tr.select_one('td.info > a').text.strip()
    artist = tr.select_one('td.info > a.artist').text

    # 1~10위 까지만 DB에 저장하기
    int_rank = int(tr.select_one('td.number').text[0:2].strip())
    if int_rank <= 10:
        best10 = {'rank': rank, 'title': title, 'star': artist}
        print(best10)   #확인용
        db.song_best10.insert_one(best10)


    print(rank, title, artist)
