# 🐾 Paw-Ong (포옹): 마음으로 잇는 새로운 가족

> **"당신의 환경과 반려견의 성향을 분석하여, 가장 완벽한 동행을 찾아드립니다."**
> Paw-Ong은 단순한 분양 리스트를 넘어, 데이터 기반의 매칭 시스템과 입양 후 가이드를 제공하는 유기견 입양 활성화 플랫폼입니다.

---

## ✨ 주요 기능 (Key Features)

### 1. 지능형 매칭 검사 (Matching Test)
- 사용자의 주거 형태(아파트/주택), 산책 가능 시간, 활동성, 털 빠짐 민감도를 분석합니다.
- 강아지의 사회성, 짖음 정도, 활동성 지표와 대조하여 가장 적합한 견종과 개체를 추천합니다.

### 2. 지역별 실시간 리스트 (Smart Filtering)
- 현재 보호소에서 대기 중인 강아지들을 지역, 나이, 크기별로 필터링하여 한눈에 확인합니다.

### 3. 맞춤형 양육 가이드 (Care Guide)
- 매칭된 견종의 유전적 특징, 주의해야 할 질병, 권장 산책량 등 초보 반려인을 위한 전문 정보를 제공합니다.

### 4. 입양 스토리 & 커뮤니티 (Success Stories)
- 실제 입양 가족들의 후기를 통해 유기견 입양에 대한 긍정적인 인식을 확산시킵니다.

---

## 📂 프로젝트 폴더 구조 (Project Structure)

```text
paw-ong/
├── assets/images/           # 이미지 리소스 관리
│   ├── banners/             # 메인 및 페이지별 배너 이미지
│   ├── dogs/                # 반려견 개체별 사진 (ID 매칭 권장)
│   ├── story/               # 입양후기 강아지 사진들
│   └── logo/                # 워터마크로 들어갈 로고
├── css/                     
│   └── style.css            # 웹 스타일 시트 (커스텀 디자인)
├── data/                    
│   └── dog_list.csv         # [Core] 반려견 및 매칭 데이터셋
├── js/                      
│   └── app.js               # 자바스크립트 로직
├── sections/                # Streamlit 멀티 페이지 구성
│   ├── main_page.py         # [Page 1] 메인 페이지
│   ├── dog_list.py          # [Page 2] 반려견 리스트 및 필터링
│   ├── matching.py          # [Page 3] 사용자 성향 기반 매칭 검사
│   ├── guide.py             # [Page 4] 입양 안내 및 양육 가이드
│   └── story.py             # [Page 5] 입양 후기 및 커뮤니티
├── utils/                   # 공통 함수
│   ├── file_loader.py       # 파일 로더 함수
├── .gitignore               # Git 추적 제외 설정 파일
├── README.md                # 프로젝트 설명 문서
├── app.py                   # 서비스 시작점
├── sample_ui.html           # 기본 HTML 구조
└── requirements.txt         # 설치 라이브러리 목록 (streamlit, pandas 등)
