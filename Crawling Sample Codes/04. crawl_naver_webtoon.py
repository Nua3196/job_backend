import requests
import json

PATH = 'https://comic.naver.com/api/article/list?titleId=641253&page=1'

if __name__ == '__main__':
    response = requests.get(PATH)
    data = response.json()
    print(data)

    episode_list = data['articleList']

    for episode in episode_list:
        print(json.dumps(episode, ensure_ascii=False, indent=2))

        exit()