# 메인 페이지 기능 추가 — 디자인 스펙

**날짜**: 2026-04-19  
**프로젝트**: Paw-Ong (반려동물 입양 매칭 서비스)  
**대상 파일**: `sections/main_page.py`, `js/app.js`, `css/style.css`

---

## 배경 및 목표

현재 메인 페이지는 히어로 섹션, 추천견 3마리, 3단계 프로세스 카드로 구성되어 있으나 모두 `js/app.js`의 하드코딩 데이터(`DOGS` 배열)를 사용하는 정적 상태다. `data/korea_dog_list_fixed.csv`에 실제 강아지 데이터가 있음에도 연결되지 않아 "살아있는 서비스" 느낌이 없다.

**목표**: 실제 CSV 데이터를 메인 페이지에 연결하고, 통계 현황 및 지역별 분포를 보여주는 기능을 추가한다.

---

## 추가 기능 목록

| # | 기능 | 설명 |
|---|------|------|
| ① | 동적 추천견 | CSV에서 랜덤 3마리를 뽑아 매번 다른 강아지 표시 |
| ② | 현황 통계 카드 | 총 등록견 / 보호 지역 수 / 품종 수 표시 (3개 카드) |
| ③ | 매칭 CTA 버튼 연결 | 3단계 프로세스 하단 기존 버튼을 Streamlit session_state와 연결 |
| ⑤ | 지역별 현황 | 지역별 입양 대기 마리수를 배지 형태로 표시 |

---

## 레이아웃 구조

```
히어로 섹션 (기존 유지)
─────────────────────────────────────
[🐾 총 등록견 N마리] [📍 보호 지역 N곳] [🐕 품종 수 N종]        ← 통계 카드 3개
─────────────────────────────────────
🐶 이달의 추천견 🩷              [전체 보기 →]
[카드1]  [카드2]  [카드3]                                     ← 랜덤 3마리
─────────────────────────────────────
📍 지역별 현황
서울 N마리  경기 N마리  부산 N마리  ...                        ← 지역 배지
─────────────────────────────────────
🐾 3단계 매칭 프로세스
1.조건검사 → 2.AI매칭 → 3.입양확정
[🔍 매칭 시작하기 →]                                          ← CTA 버튼 (session_state 연결)
```

---

## 구현 방식

### 데이터 흐름 (방식 A: Python → JSON 직렬화)

```
korea_dog_list_fixed.csv
        ↓ pandas
main_page.py (Python)
  - df.sample(3)                    → featured_json  (추천견 3마리)
  - len(df), df['지역'].nunique(), df['품종'].nunique() → stats_json (통계 3종: 총마리수, 지역수, 품종수)
  - df.groupby('지역').size()        → region_json    (지역별 현황)
        ↓ json.dumps(force_ascii=False)
HTML <script> 태그에 전역 변수로 주입
        ↓
app.js
  - renderFeatured()  → FEATURED_DOGS 사용 (수정)
  - renderStats()     → STATS 사용 (신규)
  - renderRegions()   → REGIONS 사용 (신규)
```

### CTA 버튼 연결

현재 3단계 카드 하단의 `<button onclick="navigate('matching')">` 버튼은 JS 내부 navigate()만 호출해서 Streamlit `session_state.page`와 연결이 안 된 상태다. `components.html()` iframe 내부에서 Streamlit 상위 컨텍스트로 신호를 보내는 방법은 없으므로, 버튼 클릭 시 URL 쿼리 파라미터(`?page=matching`)를 변경하는 방식 또는 Streamlit의 `st.query_params`를 활용하는 방식으로 연결한다.

**구체적 방법**: `app.py`에서 `st.query_params`를 체크해서 페이지를 결정하고, HTML 버튼은 `window.parent.postMessage` 또는 링크 방식으로 Streamlit에 신호 전달.

> 대안: iframe 제약으로 인해 완전한 연결이 어려울 경우, 버튼 아래에 별도 Streamlit 버튼을 `components.html()` 밖에 추가하는 방식도 검토.

---

## 변경 파일 범위

| 파일 | 변경 내용 |
|------|----------|
| `sections/main_page.py` | pandas로 CSV 로딩, JSON 직렬화 후 HTML에 주입, 통계 카드 HTML 추가, 지역별 현황 HTML 추가 |
| `js/app.js` | `renderFeatured()` 수정 (FEATURED_DOGS 전역변수 사용), `renderStats()` 신규, `renderRegions()` 신규, DOMContentLoaded 초기화에 신규 함수 추가 |
| `css/style.css` | 통계 카드 스타일(`.stat-card`), 지역 배지 스타일(`.region-badge`) 추가 |

**건드리지 않는 파일**: `app.py`, `data/`, `sections/dog_list.py`, `sections/matching.py`, `sections/guide.py`, `sections/story.py`

---

## CSV 컬럼 매핑

`korea_dog_list_fixed.csv` 주요 컬럼:

| CSV 컬럼 | 용도 |
|---------|------|
| `이름` | 추천견 카드 이름 |
| `품종` | 추천견 카드 품종 |
| `나이(월)` | 추천견 카드 나이 (월 → 년 변환) |
| `성별` | 추천견 카드 성별 |
| `지역` | 지역별 현황 집계 |
| `크기` | 추천견 카드 크기 |
| `건강 상태` | (현재 미사용, 향후 확장 가능) |

통계: CSV에 입양상태 컬럼이 없으므로 총 등록견 수(1,330마리), 보호 지역 수(`지역` 컬럼 nunique), 품종 수(`품종` 컬럼 nunique)로 구성한다. 크기 컬럼 값: 소형/중형/대형/초대형.

---

## 성공 기준

1. 앱을 새로고침할 때마다 추천견 3마리가 달라진다.
2. 통계 카드에 총 등록견 수 / 보호 지역 수 / 품종 수가 CSV 기반 실제 숫자로 표시된다.
3. 지역별 현황 배지가 CSV 데이터를 반영한다.
4. 3단계 프로세스 하단 버튼이 매칭 페이지로 실제 이동한다.
5. 기존 CSS 디자인이 깨지지 않는다.
