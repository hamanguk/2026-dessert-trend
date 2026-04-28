# 데이터로 보는 2026 디저트 트렌드 지도

부경대 4학년 팀 프로젝트 — 네이버 데이터랩 검색어 트렌드를 수집·시각화하고, 닷홈(Dothome)에 정적 대시보드로 배포합니다.

## 폴더 구조

```
dessert-trend-dashboard/
├── .env.example          # API 키 템플릿 (이걸 복사해서 .env 만들기)
├── .gitignore
├── requirements.txt
├── README.md
│
├── backend/              # 데이터 수집 / 분석 (파이썬)
│   ├── naverapi.py       # 메인: 트렌드 수집 + 기본 그래프
│   └── analysis/         # 팀원별 분석 스크립트
│       ├── age_analysis.py        # (담당자 A) 연령별 분석
│       ├── keyword_compare.py     # (담당자 B) 키워드 비교
│       └── device_trend.py        # (담당자 C) 기기별 트렌드
│
├── data/                 # 수집된 raw / 전처리 CSV
├── notebooks/            # 탐색용 Jupyter 노트북
│
└── web/                  # 닷홈에 업로드할 정적 사이트
    ├── index.html        # 메인 대시보드
    ├── css/style.css
    ├── js/main.js
    └── images/           # backend 가 생성한 그래프 PNG
```

## 처음 세팅 (각자 자기 PC에서)

```bash
# 1. 가상환경 (선택)
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Mac/Linux

# 2. 패키지 설치
pip install -r requirements.txt

# 3. API 키 설정
copy .env.example .env          # Windows
# cp .env.example .env          # Mac/Linux
# → .env 열어서 본인 NAVER_CLIENT_ID / SECRET 입력

# 4. 실행
python backend/naverapi.py
```

## 팀 협업 규칙

- **API 키는 절대 커밋 금지** — `.env` 는 `.gitignore` 에 들어가 있음
- 분석 스크립트는 `backend/analysis/` 에 본인 담당 파일로 작업
- 결과 그래프는 `web/images/` 에 PNG 로 저장 → `index.html` 에서 `<img>` 로 불러옴
- 새 그래프 추가 시: `web/index.html` 의 카드 영역에 `<img src="images/파일명.png">` 추가

## 닷홈 배포

`web/` 폴더 내용을 통째로 닷홈 FTP `html/` 디렉터리에 업로드.
