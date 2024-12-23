import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# MySQL 연결 설정
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = db.cursor()

# 관리자의 ID
admin_id = 7

# 회사 저장 또는 조회 함수
def get_or_create_company(name, link):
    cursor.execute("SELECT id FROM company WHERE name = %s", (name,))
    result = cursor.fetchone()

    if result:
        return result[0]

    cursor.execute("""
        INSERT INTO company (name, link)
        VALUES (%s, %s)
    """, (name, link))
    db.commit()

    return cursor.lastrowid

# 공고 ID 조회 또는 생성 함수
def get_or_create_job(row, company_id):
    cursor.execute("SELECT id FROM job WHERE link = %s", (row['링크'],))
    existing_job = cursor.fetchone()

    if existing_job:
        return existing_job[0]

    cursor.execute("""
        INSERT INTO job (company, creator, title, link, career_condition, education, deadline, job_sector)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        company_id,
        admin_id,
        row['제목'],
        row['링크'],
        row['경력및고용형태'],
        row['학력'],
        row['마감일'],
        row['직무분야']
    ))
    db.commit()

    return cursor.lastrowid

# job_location 삽입 함수
def add_job_location(job_id, location_id):
    cursor.execute("SELECT 1 FROM job_location WHERE job = %s AND location = %s", (job_id, location_id))
    if cursor.fetchone():
        return

    cursor.execute("INSERT INTO job_location (job, location) VALUES (%s, %s)", (job_id, location_id))
    db.commit()

# job_tech 삽입 함수
def add_job_tech(job_id, tech_id):
    cursor.execute("SELECT 1 FROM job_tech WHERE job = %s AND tech = %s", (job_id, tech_id))
    if cursor.fetchone():
        return

    cursor.execute("INSERT INTO job_tech (job, tech) VALUES (%s, %s)", (job_id, tech_id))
    db.commit()

# 유효성 검증 함수
def is_valid_row(row):
    """
    각 열의 값이 모두 비어있지 않은지 확인.

    Args:
        row (pd.Series): 데이터프레임의 한 행

    Returns:
        bool: 값이 비어 있지 않으면 True, 하나라도 비어 있으면 False
    """
    return row.notnull().all() and (row != "").all()

# CSV 처리 함수
def process_csv(file_path):
    """
    CSV 파일을 처리하여 공고, location, tech 데이터를 처리.

    Args:
        file_path (str): CSV 파일 경로
    """
    df = pd.read_csv(file_path)

    for _, row in df.iterrows():
        if not is_valid_row(row):
            print(f"유효하지 않은 행 건너뜀: {row.to_dict()}")
            continue

        company_name = row['회사명']
        company_link = row['회사정보']

        # 회사 ID 조회 또는 생성
        company_id = get_or_create_company(company_name, company_link)

        # 공고 ID 조회 또는 생성
        job_id = get_or_create_job(row, company_id)

        # job_location에 데이터 추가
        add_job_location(job_id, int(row['location']))

        # job_tech에 데이터 추가
        add_job_tech(job_id, int(row['tech']))

    print("CSV 데이터가 성공적으로 처리되었습니다.")

# 실행
process_csv('jobs.csv')