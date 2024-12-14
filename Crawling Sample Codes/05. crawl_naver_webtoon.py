import requests
from bs4 import BeautifulSoup

path = 'https://comic.naver.com/webtoon/detail?titleId=641253&no=520&week=fri'

if __name__ == '__main__':
    response = requests.get(path)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    # exit()

    # <div class="view_area" id="comic_view_area">
    # <div class="wt_viewer" id="sectionContWide" style="background:#FFFFFF">
    # <img alt="comic content" id="content_image_0" src="https://image-comic.pstatic.net/webtoon/641253/520/20240919234334_9647939873426c696c74bc1a372db0e7_IMAG01_1.jpg"/>

    img = soup.select_one('.wt_viewer img')
    print(img['src'])
    print('\n\n')
    exit()

    # find all
    images = soup.select('.wt_viewer img')
    for img in images:
        print(img['src'])