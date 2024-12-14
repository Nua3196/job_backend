import requests
from bs4 import BeautifulSoup

class NaverWebtoonCrawler:
    def __init__(self):
        self.base_url = "https://comic.naver.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://comic.naver.com'
        }

    def get_webtoon_list(self, day='all'):
        """요일별 웹툰 목록 가져오기"""
        try:
            url = f"{self.base_url}/webtoon"
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            print(soup)

            webtoons = []

            # 웹툰 아이템 찾기
            webtoon_items = soup.select('.component_wrap')

            for item in webtoon_items:
                try:
                    # 기본 정보 추출
                    title = item.select_one('.text')
                    author = item.select_one('.author')
                    rating = item.select_one('.rating_number')
                    thumbnail = item.select_one('img')
                    link = item.select_one('a')

                    webtoon_info = {
                        'title': title.text.strip() if title else 'N/A',
                        'author': author.text.strip() if author else 'N/A',
                        'rating': rating.text.strip() if rating else 'N/A',
                        'thumbnail': thumbnail['src'] if thumbnail else 'N/A',
                        'link': self.base_url + link['href'] if link else 'N/A'
                    }

                    webtoons.append(webtoon_info)

                except Exception as e:
                    print(f"Error parsing webtoon item: {e}")
                    continue

            return webtoons

        except Exception as e:
            print(f"Error fetching webtoon list: {e}")
            return []

    def get_webtoon_details(self, webtoon_url):
        """특정 웹툰의 상세 정보 가져오기"""
        try:
            response = requests.get(webtoon_url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            # 상세 정보 추출
            title = soup.select_one('.detail_header .title')
            description = soup.select_one('.detail_info .detail_description')
            genre = soup.select_one('.detail_info .genre')
            age_rating = soup.select_one('.detail_info .age_rating')

            details = {
                'title': title.text.strip() if title else 'N/A',
                'description': description.text.strip() if description else 'N/A',
                'genre': genre.text.strip() if genre else 'N/A',
                'age_rating': age_rating.text.strip() if age_rating else 'N/A',
            }

            return details

        except Exception as e:
            print(f"Error fetching webtoon details: {e}")
            return None

    def get_episodes(self, webtoon_url, num_episodes=10):
        """특정 웹툰의 에피소드 목록 가져오기"""
        try:
            response = requests.get(webtoon_url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            episodes = []
            episode_items = soup.select('.episode_list .item')[:num_episodes]

            for item in episode_items:
                try:
                    title = item.select_one('.title_area .title')
                    date = item.select_one('.num')
                    rating = item.select_one('.rating_area .rating')
                    thumbnail = item.select_one('img')

                    episode_info = {
                        'title': title.text.strip() if title else 'N/A',
                        'date': date.text.strip() if date else 'N/A',
                        'rating': rating.text.strip() if rating else 'N/A',
                        'thumbnail': thumbnail['src'] if thumbnail else 'N/A'
                    }

                    episodes.append(episode_info)

                except Exception as e:
                    print(f"Error parsing episode item: {e}")
                    continue

            return episodes

        except Exception as e:
            print(f"Error fetching episodes: {e}")
            return []

def main():
    crawler = NaverWebtoonCrawler()

    # 전체 웹툰 목록 가져오기
    print("웹툰 목록을 가져오는 중...")
    webtoons = crawler.get_webtoon_list()

    if webtoons:
        # 웹툰 목록 저장
        print(f"총 {len(webtoons)}개의 웹툰 정보를 저장했습니다.")

        # 첫 번째 웹툰의 상세 정보와 에피소드 가져오기
        if webtoons[0]['link'] != 'N/A':
            print("\n첫 번째 웹툰의 상세 정보를 가져오는 중...")
            details = crawler.get_webtoon_details(webtoons[0]['link'])
            if details:
                print("상세 정보:")
                for key, value in details.items():
                    print(f"{key}: {value}")

            print("\n에피소드 목록을 가져오는 중...")
            episodes = crawler.get_episodes(webtoons[0]['link'])
            for episode in episodes:
                print(episode)
                exit()


if __name__ == "__main__":
    main()