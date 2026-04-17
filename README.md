# 🐾 Paw-Ong (포옹): 새로운 가족 찾기 서비스

사용자의 성향, 주거 환경, 가용 시간을 분석하여 최적의 유기견을 매칭해주고 올바른 반려 문화를 가이드하는 Streamlit 기반 웹 서비스입니다.

---

## 📂 프로젝트 폴더 구조 (Project Structure)

```text
paw-ong/
├── assets/images/           # 이미지 리소스 관리
│   ├── banners/             # 메인 및 페이지별 배너 이미지
│   └── dogs/                # 반려견 개체별 사진 (ID 매칭 권장)
├── css/                     
│   └── style.css            # 커스텀 스타일 시트
├── data/                    
│   └── dog_list.csv         # [핵심] 반려견 및 매칭 데이터셋
├── js/                      
│   └── app.js               # 프론트엔드 보조 로직
├── pages/                   # Streamlit 멀티 페이지 폴더
│   ├── 1_doglist.py         # [Page 2] 반려견 리스트 & 필터링
│   ├── 2_matching.py        # [Page 3] 사용자 성향 기반 매칭 검사
│   ├── 3_guide.py           # [Page 4] 입양 안내 및 양육 가이드
│   └── 4_story.py           # [Page 5] 입양 후기 및 커뮤니티
├── .gitignore               # Git 추적 제외 설정
├── README.md                # 프로젝트 문서
├── app.py                   # [Page 1] 메인 페이지 (Service Entry)
├── index.html               # 기본 HTML (필요 시 활용)
└── requirements.txt         # 필수 라이브러리 목록
