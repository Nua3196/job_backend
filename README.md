# JBNU WSD HW3: 구인구직 백엔드 서버

## 프로젝트 소개
이 프로젝트는 사람인 데이터를 활용하여 구인구직 백엔드 서버를 개발하는 과제입니다. Flask를 사용해 RESTful API를 구현하며, JCloud를 통해 클라우드 배포가 진행됩니다.

## 주요 기능
- 사람인 채용 공고 크롤링
- 채용 공고 데이터 저장 및 검색
- 회원가입 및 로그인 (JWT 인증)
- 관심 공고 및 지원 관리
- Swagger 문서를 통한 API 문서화

## 사용 기술
- Python (Flask)
- MySQL 또는 MongoDB
- JWT 인증
- Swagger (API 문서화)
- JCloud (배포)

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

### 3. 필수 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 애플리케이션 실행
```bash
python app.py
```

## API 문서
Swagger UI를 통해 API 엔드포인트를 확인하고 테스트할 수 있습니다.

- **Swagger URL**: <https://your-deployed-swagger-url>

## 기여
1. Fork 저장소
2. 새로운 브랜치 생성 (`git checkout -b feature/YourFeature`)
3. 변경 사항 커밋 (`git commit -m 'Add some feature'`)
4. 브랜치 푸시 (`git push origin feature/YourFeature`)
5. Pull Request 요청