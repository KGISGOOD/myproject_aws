from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def index(request):
    return render(request, 'crawler/index.html')

def scrape(request):
    url = 'https://www.ptt.cc/bbs/food/index.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 捕捉 HTTP 錯誤
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = soup.find_all('div', class_='title')

        results = []
        for title in titles:
            a_tag = title.find('a')
            if a_tag:
                results.append(a_tag.text.strip())

    except Exception as e:
        results = [f"發生錯誤：{str(e)}"]

    return render(request, 'crawler/scrape.html', {'results': results})
