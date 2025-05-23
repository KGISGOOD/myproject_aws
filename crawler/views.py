import requests
from bs4 import BeautifulSoup
import random
import time
from django.shortcuts import render

def index(request):
    return render(request, 'crawler/index.html')

def scrape(request):
    url = 'https://www.ptt.cc/bbs/food/index.html'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.ptt.cc/bbs/food/index.html'
    }

    session = requests.Session()
    session.headers.update(headers)
    session.cookies.set('over18', '1', domain='www.ptt.cc')

    time.sleep(random.randint(1,3))  # 隨機等待1~3秒

    try:
        response = session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = soup.find_all('div', class_='title')

        results = []
        for title_div in titles:
            a_tag = title_div.find('a')
            if a_tag:
                results.append({
                    'title': a_tag.text.strip(),
                    'link': 'https://www.ptt.cc' + a_tag['href']
                })

    except Exception as e:
        results = [{'title': f"發生錯誤：{str(e)}", 'link': '#'}]

    return render(request, 'crawler/scrape.html', {'results': results})
