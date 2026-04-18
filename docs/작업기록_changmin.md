# 작업 기록 - changmin (feature/changmin)

## 담당 역할
- 메인 페이지 스타일 통일 (사이드바/상단과 일치)
- 반려견 리스트에 보호소 위치 정보 연동
- 가상 데이터와 실제 데이터 혼합 방안 구현

---

## 데이터 혼합 전략

### 문제
- 현재: JS에 하드코딩된 가상 강아지 20마리 (app.js DOGS 배열)
- 미활용: `data/korea_dog_list_fixed.csv` 에 1,330마리 데이터 존재
- 위치 정보: 단순 텍스트("서울", "경기" 등)만 있고 실제 보호소 정보 없음

### 선택한 방식: CSV 데이터 + 실제 보호소 위치 매핑
- CSV의 `지역` 필드(17개 시/도)에 실제 보호소 정보를 매핑
- 포인핸드(pawinhand.kr) / 공공데이터포털 기반 보호소 정보 활용
- API 키 없이 정적 매핑 방식으로 구현 (JSON 파일)

### 이미지 매칭 방식: CSV 아이디 → 파일명 직접 매칭
- CSV `아이디` 필드와 이미지 파일명이 1:1 대응 (`{아이디}-1.jpg`)
- `assets/images/dogs/` 폴더에 1,330장 이미지 존재
- Streamlit static serving(`static/dogs/`)으로 이미지 제공

### 위치 표시 방식: 텍스트 주소 + Google Maps
- 보호소명 + 주소 + 전화번호를 텍스트로 표시
- Google Maps 임베드로 위치 시각화

---

## 작업 내역

### Task 1: 보호소 매핑 데이터 생성 ✅
- [x] `data/shelter_info.json` - 17개 시/도별 실제 보호소 정보
- 포인핸드/공공데이터 기반 실제 보호소명, 주소, 좌표 수집
- 각 보호소별 이름, 주소, 전화번호, 위도/경도 포함

### Task 2: CSV 데이터 연동 ✅
- [x] `sections/dog_list.py` - Python(pandas)으로 CSV 로드 → JSON으로 JS에 전달
- [x] `sections/main_page.py` - 추천견을 사회도+친화도 기준으로 CSV에서 선별
- 기존 `js/app.js` 하드코딩 방식 대신 Python → JS 데이터 전달 구조로 변경
- 1,330마리 전체 데이터 활용

### Task 3: 위치 정보 표시 ✅
- [x] 반려견 리스트에서 카드 클릭 시 상세 패널 (모달) 표시
- [x] 보호소명 + 주소 + 전화번호 텍스트 표시
- [x] Google Maps 임베드로 위치 지도 표시
- [x] 지역 필터 드롭다운 추가 (17개 시/도)

### Task 4: 메인 페이지 스타일 통일 ✅
- [x] 사이드바(#F5EDE8) / 상단 / 본문 색상 팔레트 일치
- [x] Streamlit 상단 헤더 배경색을 #FDF6F0으로 통일
- [x] 폰트(Gowun Batang + Noto Sans KR) 일관성 확인

### Task 5: 카드형 리스트 + 이미지 연동 ✅
- [x] 테이블 → 카드형 레이아웃 변경 (왼쪽 사진 + 오른쪽 정보)
- [x] CSV 아이디 기반 이미지 자동 매칭 (1,330마리 전부 사진 연동)
- [x] Streamlit static serving 설정 (`.streamlit/config.toml`)
- [x] `static/dogs/` → `assets/images/dogs/` 연결
- [x] 이미지 로드 실패 시 이모지 placeholder 표시

### Task 6: 필터 UX 개선 ✅
- [x] 필터 드롭다운 위에 라벨 추가 (상태, 크기, 활동성, 지역)
- [x] 결과 카운트에 활성 필터 태그 표시
  - 필터 미적용: `🐕 총 1330마리`
  - 필터 적용: `🐕 1330마리 중 245마리 | 상태: 입양가능  크기: 소형  지역: 서울`

---

## 수정/생성된 파일 목록
| 파일 | 변경 내용 |
|------|----------|
| `data/shelter_info.json` | 신규 - 17개 시/도별 보호소 정보 (이름, 주소, 전화번호, GPS) |
| `sections/dog_list.py` | 전면 재작성 - CSV 연동, 카드형 리스트, 이미지, 상세 패널, 필터 |
| `sections/main_page.py` | CSV 기반 추천견 (사회도+친화도 상위 3마리 + 보호소명) |
| `css/style.css` | 상단 헤더 스타일 통일, 테이블 grid 컬럼 조정 |
| `.streamlit/config.toml` | 신규 - static file serving 활성화 |
| `static/dogs/` | 신규 - 이미지 서빙 폴더 (assets/images/dogs 복사) |
| `docs/작업기록_changmin.md` | 신규 - 이 작업 기록 문서 |

---

## 기술 스택
- **프레임워크**: Streamlit (Python)
- **프론트엔드**: HTML/CSS/JS (Streamlit components.html)
- **데이터**: CSV (pandas) + JSON (보호소 매핑)
- **이미지**: Streamlit static serving (`enableStaticServing = true`)
- **지도**: Google Maps Embed
