import requests
import time

PATH = 'https://comic.naver.com/api/webtoon/titlelist/weekday?order=user'

if __name__ == '__main__':
    response = requests.get(PATH)
    data = response.json()
    print(data)

    # time.sleep(10)/