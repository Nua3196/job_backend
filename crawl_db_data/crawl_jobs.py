import random
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from itertools import product

def crawl_saramin(tech, location, pages=1):
    """
    사람인 채용공고를 크롤링하는 함수

    Args:
        keyword (str): 검색할 키워드
        pages (int): 크롤링할 페이지 수

    Returns:
        DataFrame: 채용공고 정보가 담긴 데이터프레임
    """

    jobs = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for page in range(1, pages + 1):
        url = f"https://www.saramin.co.kr/zf_user/jobs/list/job-category?page={page}&cat_kewd={tech}&loc_mcd={location}"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # 채용공고 목록 가져오기
            job_listings = soup.select('.list_item')

            for job in job_listings:
                try:
                    # 회사정보
                    company = job.select_one('.company_nm a')
                    company_name = company.text.strip() if company else ''
                    company_link = "https://www.saramin.co.kr" + company['href'] if company else ''

                    # 채용 제목
                    title_ele = job.select_one('.job_tit a')
                    title = title_ele.text.strip() if title_ele else ''

                    # 채용 링크
                    link = 'https://www.saramin.co.kr' + job.select_one('.job_tit a')['href']

                    # 경력 및 고용형태, 학력
                    recruit_info = job.select('.recruit_info ul li')
                    career = ''
                    education = None
                    for info in recruit_info:
                        career_info = info.select_one('p.career')
                        if career_info:
                            career = career_info.get_text(strip=True)
                            print("career_text1:", career)
                        education_info = info.select_one('p.education')
                        education = education_info.get_text(strip=True) if education_info else ''

                    # 마감일
                    deadline_ele = job.select_one('span.date')
                    deadline = deadline_ele.text.strip() if deadline_ele else ''

                    # 직무 분야
                    job_sector = job.select_one('.job_sector')
                    sector = None
                    if job_sector:
                        sector = ", ".join([tag.text.strip() for tag in job_sector.find_all('span')])
                    else:
                        sector = ""

                    jobs.append({
                        '회사명': company_name,
                        '회사정보': company_link,
                        '제목': title,
                        '링크': link,
                        '경력및고용형태': career,
                        '학력': education,
                        '마감일': deadline,
                        '직무분야': sector,
                    })

                    # print(jobs[-1])
                    # exit()

                except AttributeError as e:
                    print(f"항목 파싱 중 에러 발생: {e}")
                    continue

            print(f"{page}페이지 크롤링 완료")
            time.sleep(random.uniform(1, 3))  # 서버 부하 방지를 위한 딜레이

        except requests.RequestException as e:
            print(f"페이지 요청 중 에러 발생: {e}")
            continue

    return pd.DataFrame(jobs)


# 사용 예시
if __name__ == "__main__":
    tech = {"라즈베리파이": 186, "임베디드리눅스":320, "Android": 195, "Flask": 218}
    location = {"서울": 101000, "인천": 108000, "대전": 105000, "전북": 113000}
    # IT개발/데이터 직무에서, 기술 스택, 지역을 선택하고 페이지 크롤링(페이지당 50개개)

    tech_location_combinations = list(product(tech.items(), location.items()))
    all_data = []

    for (tech_name, tech_code), (loc_name, loc_code) in tech_location_combinations:
        print(f"크롤링 시작: 기술스택 - {tech_name}[{tech_code}], 지역 - {loc_name}[{loc_code}]")
        try:
            df = crawl_saramin(tech=tech_code, location=loc_code, pages=2)
            df['tech'] = tech_code
            df['location'] = loc_code

            print(df)
            all_data.append(df)
        except Exception as e:
            print(f"크롤링 중 오류 발생: 기술스택 - {tech_name}[{tech_code}], 지역 - {loc_name}[{loc_code}]")
            print(f"오류: {e}")

    total_df = pd.concat(all_data, ignore_index=True)
    total_df.to_csv('jobs.csv', index=False, encoding="UTF-8")
    print("크롤링 완료 및 CSV 파일 저장")