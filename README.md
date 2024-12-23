# JBNU WSD HW3: 구인구직 백엔드 서버

## 프로젝트 소개
이 프로젝트는 사람인 데이터를 활용하여 구인구직 백엔드 서버를 개발하는 과제입니다. Flask를 사용하여 RESTful API를 구현하며, JWT 인증을 적용하고, Swagger를 통해 API 문서화를 제공하며 JCloud를 통해 클라우드 배포를 지원합니다.

---

## 주요 기능
- **사람인 채용 공고 크롤링**: 다양한 기술 스택과 지역 조건으로 채용 공고 데이터를 수집합니다.
- **채용 공고 데이터 관리**:
  - 공고 추가, 수정, 삭제, 검색 및 필터링.
  - 통계 API를 통한 회사별/기술별/공고별 데이터 집계.
- **회원 관리**:
  - 회원가입 및 로그인 기능 제공 (JWT 인증).
  - 역할 기반 접근 제어(`admin`, `employer`, `applicant`).
- **관심 공고 및 지원 관리**:
  - 공고 북마크 기능 제공.
  - 공고에 대한 지원 추가, 조회 및 취소.
- **API 문서화**:
  - Swagger UI를 통한 API 엔드포인트 확인 및 테스트.

---

## 사용 기술
- **백엔드**: Python (Flask)
- **데이터베이스**: MySQL
- **인증**: JWT (Access/Refresh Token)
- **API 문서화**: Swagger (OpenAPI 3.0)
- **배포**: JCloud
- **크롤링**: BeautifulSoup, Requests

---

## 프로젝트 구조

```
job_backend/
├── app/
│   ├── __init__.py         # Flask 앱 초기화
│   ├── controllers/        # API 컨트롤러
│   ├── models/             # 데이터베이스 모델
│   ├── middlewares/        # 인증 및 권한 미들웨어
│   ├── utils/              # 유틸리티 (DB, JWT, Redis 등)
│   └── static/swagger.yaml # API 문서화 파일
├── crawl_db_data/          # 크롤링 및 DB 데이터 초기화 관련 파일
├── .env                    # 환경 변수 파일
├── requirements.txt        # 의존성 패키지 목록
├── run.py                  # Flask 앱 실행
└── README.md               # 프로젝트 문서
```

---

## 설치 및 실행

### 1. 클론
```bash
git clone https://github.com/Nua3196/job_backend.git
cd job_backend
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 환경 변수 설정
`.env.example` 파일을 참고하여 `.env` 파일을 생성하고, 필요한 값을 설정합니다.
```plaintext
DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
SECRET_KEY=your_secret_key
REFRESH_SECRET_KEY=your_refresh_secret_key
JWT_ACCESS_TOKEN_EXPIRES=1
JWT_REFRESH_TOKEN_EXPIRES=168
```

### 4. 필수 패키지 설치
```bash
pip install -r requirements.txt
```

### 5. 데이터베이스 초기화
- MySQL에서 필요한 테이블 생성:
  ```sql
  CREATE DATABASE job_db;
  USE job_db;

  -- 테이블 정의는 별도로 제공된 SQL 스크립트를 참조하세요.
  ```
- `tech`와 `location` 데이터를 삽입:
  ```bash
  python crawl_db_data/tech_loc.py
  ```

### 6. 크롤링 데이터 처리
- 사전에 관리자 권한 계정 생성:
  ```bash
  python crawl_db_data/user_admin.py
  ```
생성한 관리자 id를 크롤링한 채용공고의 creator로 사용합니다. job_company.py의 admin_id를 해당 id로 변경합니다.

- 사람인 채용 데이터를 크롤링하고 저장:
  ```bash
  python crawl_db_data/crawl_jobs.py
  python crawl_db_data/job_company.py
  ```

### 7. 애플리케이션 실행
```bash
python run.py
```

---

## API 문서
Swagger UI를 통해 API 엔드포인트를 확인하고 테스트할 수 있습니다.

- **Swagger URL**: <https://your-deployed-swagger-url>

---

## 테스트
- Postman이나 Swagger UI를 사용하여 API 테스트를 진행할 수 있습니다.
- 주요 테스트 항목:
  - 회원가입, 로그인, 로그아웃.
  - 공고 CRUD, 검색 및 필터링.
  - 관심 공고 추가/삭제, 지원 관리.
  - 통계 데이터 확인.

---

## 기여
1. Fork 저장소
2. 새로운 브랜치 생성 (`git checkout -b feature/YourFeature`)
3. 변경 사항 커밋 (`git commit -m 'Add some feature'`)
4. 브랜치 푸시 (`git push origin feature/YourFeature`)
5. Pull Request 요청

---

## 라이센스
이 프로젝트는 교육 목적으로 사용되며, 상업적 목적으로 재배포가 허용되지 않습니다.

---