# paw-ong


paw-ong/
├── assets/images/           # 이미지 리소스 관리
│   ├── banners/             # 메인 및 페이지별 배너 이미지 (.gitkeep)
│   └── dogs/                # 반려견 개체별 사진 (.gitkeep)
├── css/                     
│   └── style.css            # 웹 스타일 시트 (커스텀 디자인)
├── data/                    
│   └── .gitkeep             # 반려견 목록 및 견종 정보 데이터 저장 예정
├── js/                      
│   └── app.js               # 자바스크립트 로직 (필요 시 활용)
├── pages/                   # Streamlit 멀티 페이지 구성
│   ├── 1_doglist.py         # [페이지 2] 반려견 리스트 및 필터링
│   ├── 2_matching.py        # [페이지 3] 사용자 성향 기반 매칭 검사
│   ├── 3_guide.py           # [페이지 4] 입양 안내 및 양육 가이드
│   └── 4_story.py           # [페이지 5] 입양 후기 및 커뮤니티
├── .gitignore               # Git 추적 제외 설정 파일
├── README.md                # 프로젝트 설명 문서
├── app.py                   # [페이지 1] 메인 페이지 (서비스 시작점)
├── index.html               # 기본 HTML 구조 (필요 시 활용)
└── requirements.txt         # 설치가 필요한 라이브러리 목록
