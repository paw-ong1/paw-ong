# 메인 페이지 기능 추가 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Paw-Ong 메인 페이지에 CSV 데이터를 연결하여 동적 추천견, 통계 카드, 지역별 현황, 매칭 CTA 버튼 이동을 구현한다.

**Architecture:** `main_page.py`(Python)에서 `korea_dog_list_fixed.csv`를 읽어 JSON으로 직렬화한 뒤 HTML `<script>` 태그에 전역변수(`FEATURED_DOGS`, `STATS`, `REGIONS`)로 주입한다. `app.js`의 render 함수들이 해당 변수를 사용해 DOM을 채운다. CTA 버튼은 `window.top.location.search`로 URL 쿼리 파라미터를 변경하고, `app.py`가 `st.query_params`로 이를 감지해 `session_state.page`를 설정한다.

**Tech Stack:** Python 3, pandas, streamlit 1.56.0, JavaScript (ES6), pytest

---

## File Map

| 파일 | 작업 |
|------|------|
| `utils/data_loader.py` | 신규 — CSV 로딩 및 변환 순수 함수 3개 |
| `tests/__init__.py` | 신규 — 테스트 패키지 초기화 (빈 파일) |
| `tests/test_data_loader.py` | 신규 — data_loader 단위 테스트 5개 |
| `css/style.css` | 수정 — `.stat-card`, `.region-badge` 스타일 추가 |
| `js/app.js` | 수정 — `renderFeatured()` 수정, `renderStats()` / `renderRegions()` / `goToMatching()` 신규 |
| `sections/main_page.py` | 수정 — JSON 주입, 통계 카드 · 지역 현황 HTML 추가, CTA 버튼 onclick 수정 |
| `app.py` | 수정 — `st.query_params` 기반 페이지 라우팅 추가 |

---

### Task 1: 테스트 환경 설정 및 data_loader 뼈대

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/test_data_loader.py`
- Create: `utils/data_loader.py`

- [ ] **Step 1: 실패하는 테스트 작성**

`tests/__init__.py` 생성 (빈 파일):
```python
```

`tests/test_data_loader.py` 생성:
```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.data_loader import get_featured_dogs, get_stats, get_region_stats


def test_get_featured_dogs_returns_three():
    dogs = get_featured_dogs()
    assert len(dogs) == 3


def test_get_featured_dogs_has_required_keys():
    dogs = get_featured_dogs()
    required = {'이름', '품종', '나이', '성별', '지역', '크기'}
    for dog in dogs:
        assert required.issubset(dog.keys()), f"missing keys in {dog}"


def test_get_stats_has_required_keys():
    stats = get_stats()
    assert {'total', 'regions', 'breeds'}.issubset(stats.keys())


def test_get_stats_total_is_positive():
    stats = get_stats()
    assert stats['total'] > 0


def test_get_region_stats_returns_list_with_region_and_count():
    regions = get_region_stats()
    assert isinstance(regions, list)
    assert len(regions) > 0
    assert 'region' in regions[0]
    assert 'count' in regions[0]
```

- [ ] **Step 2: 빈 data_loader.py 생성 후 테스트 실패 확인**

`utils/data_loader.py` 생성:
```python
# 구현 예정 — Task 2에서 완성
```

Run:
```bash
cd C:/aibigdata/12.Transfer_Learning/mini_project/paw-ong
python -m pytest tests/test_data_loader.py -v
```
Expected: FAIL — `ImportError: cannot import name 'get_featured_dogs'`

- [ ] **Step 3: 커밋**

```bash
git add tests/ utils/data_loader.py
git commit -m "test: add failing tests for data_loader"
```

---

### Task 2: data_loader.py 구현

**Files:**
- Modify: `utils/data_loader.py`

- [ ] **Step 1: 세 함수 구현**

`utils/data_loader.py`를 다음으로 교체한다:

```python
import pandas as pd

_CSV_PATH = 'data/korea_dog_list_fixed.csv'


def load_dog_df():
    """CSV를 읽어 DataFrame으로 반환한다."""
    return pd.read_csv(_CSV_PATH)


def get_featured_dogs(df=None, n=3):
    """CSV에서 랜덤 n마리를 뽑아 카드 표시용 dict 리스트로 반환한다.

    반환 키: 이름, 품종, 나이, 성별, 지역, 크기
    """
    if df is None:
        df = load_dog_df()
    cols = ['이름', '품종', '나이(월)', '성별', '지역', '크기']
    sample = df[cols].sample(min(n, len(df))).copy()
    sample['나이'] = sample['나이(월)'].apply(
        lambda m: f"{int(m) // 12}살" if int(m) >= 12 else f"{int(m)}개월"
    )
    return sample.drop(columns=['나이(월)']).to_dict(orient='records')


def get_stats(df=None):
    """총 등록견 수 / 보호 지역 수 / 품종 수를 dict로 반환한다."""
    if df is None:
        df = load_dog_df()
    return {
        'total':   len(df),
        'regions': int(df['지역'].nunique()),
        'breeds':  int(df['품종'].nunique()),
    }


def get_region_stats(df=None, top_n=6):
    """지역별 마리수 상위 top_n을 [{'region': str, 'count': int}] 형태로 반환한다."""
    if df is None:
        df = load_dog_df()
    counts = df['지역'].value_counts().head(top_n)
    return [{'region': str(k), 'count': int(v)} for k, v in counts.items()]
```

- [ ] **Step 2: 테스트 실행하여 전체 통과 확인**

Run:
```bash
cd C:/aibigdata/12.Transfer_Learning/mini_project/paw-ong
python -m pytest tests/test_data_loader.py -v
```
Expected:
```
tests/test_data_loader.py::test_get_featured_dogs_returns_three PASSED
tests/test_data_loader.py::test_get_featured_dogs_has_required_keys PASSED
tests/test_data_loader.py::test_get_stats_has_required_keys PASSED
tests/test_data_loader.py::test_get_stats_total_is_positive PASSED
tests/test_data_loader.py::test_get_region_stats_returns_list_with_region_and_count PASSED
5 passed
```

- [ ] **Step 3: 커밋**

```bash
git add utils/data_loader.py
git commit -m "feat: implement data_loader (get_featured_dogs, get_stats, get_region_stats)"
```

---

### Task 3: CSS 스타일 추가

**Files:**
- Modify: `css/style.css`

- [ ] **Step 1: 스타일 파일 끝에 추가**

`css/style.css` 맨 끝에 다음을 추가한다:

```css
/* ── 통계 카드 ─────────────────────────────────── */
.stats-row {
  display: flex;
  gap: 14px;
  margin: 20px 0;
}
.stat-card {
  flex: 1;
  background: #fff;
  border-radius: 16px;
  padding: 20px 16px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.07);
}
.stat-card .stat-icon  { font-size: 28px; margin-bottom: 8px; }
.stat-card .stat-num   { font-size: 26px; font-weight: 800; color: #3D2B1F; }
.stat-card .stat-label { font-size: 12px; color: #A08070; margin-top: 4px; }

/* ── 지역별 현황 ────────────────────────────────── */
.region-section { margin: 20px 0; }
.region-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 12px;
}
.region-badge {
  background: #FDE8E4;
  color: #7D4F5A;
  border-radius: 20px;
  padding: 6px 16px;
  font-size: 13px;
  font-weight: 600;
}
.region-badge span { color: #E8A598; margin-left: 4px; }
```

- [ ] **Step 2: 앱 실행하여 기존 페이지 정상 렌더링 확인**

Run:
```bash
cd C:/aibigdata/12.Transfer_Learning/mini_project/paw-ong
streamlit run app.py
```
Expected: 기존 메인 페이지가 정상 표시됨 (신규 클래스는 아직 HTML에 없으므로 시각적 변화 없음)

- [ ] **Step 3: 커밋**

```bash
git add css/style.css
git commit -m "style: add stat-card and region-badge styles"
```

---

### Task 4: app.js — render 함수 3개 추가 및 수정

**Files:**
- Modify: `js/app.js`

- [ ] **Step 1: renderFeatured() 교체**

`js/app.js`에서 기존 `renderFeatured()` 함수 전체를 다음으로 교체한다 (기존: line 57-74):

```javascript
function renderFeatured() {
  const container = document.getElementById('featured-dogs');
  if (!container) return;

  // FEATURED_DOGS: main_page.py(Python)가 주입하는 전역변수
  const dogs = (typeof FEATURED_DOGS !== 'undefined') ? FEATURED_DOGS : [];
  if (dogs.length === 0) {
    container.innerHTML = '<p style="color:#A08070;text-align:center;">데이터를 불러오는 중...</p>';
    return;
  }

  container.innerHTML = dogs.map((d, i) => `
    <div class="dog-card">
      <div class="dog-card-img" style="background:${FEATURED_COLORS[i % 3]}">${FEATURED_EMOJIS[i % 3]}</div>
      <div class="dog-card-body">
        <div class="dog-card-name">${d['이름']}</div>
        <div class="dog-card-info">${d['품종']} · ${d['나이']} · ${d['성별']}</div>
        <div class="dog-card-region">📍 ${d['지역']}</div>
        <button class="dog-card-btn" onclick="navigate('list')">입양 신청 →</button>
      </div>
    </div>
  `).join('');
}
```

- [ ] **Step 2: renderStats() 추가**

`js/app.js`에서 `renderFeatured()` 함수 바로 아래에 다음을 추가한다:

```javascript
function renderStats() {
  const container = document.getElementById('stats-row');
  if (!container) return;

  // STATS: main_page.py(Python)가 주입하는 전역변수
  const s = (typeof STATS !== 'undefined') ? STATS : { total: 0, regions: 0, breeds: 0 };

  container.innerHTML = `
    <div class="stat-card">
      <div class="stat-icon">🐾</div>
      <div class="stat-num">${s.total.toLocaleString()}</div>
      <div class="stat-label">총 등록견</div>
    </div>
    <div class="stat-card">
      <div class="stat-icon">📍</div>
      <div class="stat-num">${s.regions}</div>
      <div class="stat-label">보호 지역</div>
    </div>
    <div class="stat-card">
      <div class="stat-icon">🐕</div>
      <div class="stat-num">${s.breeds}</div>
      <div class="stat-label">품종 수</div>
    </div>
  `;
}
```

- [ ] **Step 3: renderRegions() 추가**

`js/app.js`에서 `renderStats()` 바로 아래에 다음을 추가한다:

```javascript
function renderRegions() {
  const container = document.getElementById('region-badges');
  if (!container) return;

  // REGIONS: main_page.py(Python)가 주입하는 전역변수
  const regions = (typeof REGIONS !== 'undefined') ? REGIONS : [];
  if (regions.length === 0) return;

  container.innerHTML = regions
    .map(r => `<div class="region-badge">${r.region} <span>${r.count}마리</span></div>`)
    .join('');
}
```

- [ ] **Step 4: goToMatching() 추가**

`js/app.js`에서 `updateWalkLabel()` 함수 바로 아래에 다음을 추가한다:

```javascript
function goToMatching() {
  // URL 쿼리 파라미터 변경 → Streamlit 재실행 → app.py가 ?page=matching 감지
  window.top.location.search = '?page=matching';
}
```

- [ ] **Step 5: DOMContentLoaded 초기화 블록 업데이트**

`js/app.js`의 `document.addEventListener('DOMContentLoaded', () => {` 블록에서 `// Page 1` 섹션을 다음으로 교체한다:

기존:
```javascript
  // Page 1
  renderFeatured();
```

교체:
```javascript
  // Page 1
  renderFeatured();
  renderStats();
  renderRegions();
```

- [ ] **Step 6: 커밋**

```bash
git add js/app.js
git commit -m "feat: add renderStats, renderRegions, goToMatching; update renderFeatured to use injected data"
```

---

### Task 5: main_page.py 업데이트 — JSON 주입 및 HTML 구조 변경

**Files:**
- Modify: `sections/main_page.py`

- [ ] **Step 1: main_page.py 전체 교체**

`sections/main_page.py`를 다음으로 교체한다:

```python
import json
import streamlit.components.v1 as components
from utils.file_loader import load_resource
from utils.data_loader import get_featured_dogs, get_stats, get_region_stats


def render():
    css_content = load_resource("css/style.css")
    js_content  = load_resource("js/app.js")

    # CSV → JSON 직렬화 (Python → JS 전역변수로 주입)
    featured_json = json.dumps(get_featured_dogs(), ensure_ascii=False)
    stats_json    = json.dumps(get_stats(),          ensure_ascii=False)
    regions_json  = json.dumps(get_region_stats(),   ensure_ascii=False)

    html_code = f"""
    <style>{css_content}</style>
    <script>
      const FEATURED_DOGS = {featured_json};
      const STATS         = {stats_json};
      const REGIONS       = {regions_json};
    </script>
    <script>{js_content}</script>

    <!-- ─── PAGE 1: 메인 ──────────────────────────────────────────────── -->
    <section id="page-main" class="page active">
      <div class="paw-bg">🐾</div>

      <!-- 히어로 -->
      <div class="hero">
        <div class="hero-bg-emoji">🐕</div>
        <div class="hero-badge">🐾 새로운 가족을 만나보세요</div>
        <h1>당신에게 딱 맞는<br>가족을 찾아드립니다</h1>
        <p>매일 기다리는 소중한 생명들, 지금 만나보세요</p>
      </div>

      <!-- 통계 카드 -->
      <div class="stats-row" id="stats-row"></div>

      <!-- 추천견 -->
      <div class="section-header">
        <div>
          <div class="sec-title">🐶 이달의 추천견 🩷</div>
          <div class="sec-sub">보호소에서 기다리는 친구들을 소개합니다</div>
        </div>
        <button class="btn-outline" onclick="navigate('list')">전체 보기 →</button>
      </div>
      <div class="dog-cards" id="featured-dogs"></div>

      <!-- 지역별 현황 -->
      <div class="region-section card">
        <div class="sec-title">📍 지역별 현황 🌿</div>
        <div class="region-badges" id="region-badges"></div>
      </div>

      <!-- 3단계 프로세스 -->
      <div class="card step-card">
        <div class="sec-title" style="margin-bottom:20px;">🐾 3단계 매칭 프로세스 🌿</div>
        <div class="steps-row">
          <div class="step">
            <div class="step-circle" style="background:#E8A598;">1</div>
            <div class="step-label">조건 검사</div>
            <div class="step-desc">나의 라이프스타일과<br>환경 정보를 입력해요</div>
          </div>
          <div class="step-arrow">→</div>
          <div class="step">
            <div class="step-circle" style="background:#7BAE8A;">2</div>
            <div class="step-label">AI 매칭</div>
            <div class="step-desc">나의 조건에 맞는<br>강아지를 찾아드려요</div>
          </div>
          <div class="step-arrow">→</div>
          <div class="step">
            <div class="step-circle" style="background:#F2C4CE; color:#7D4F5A;">3</div>
            <div class="step-label">입양 확정</div>
            <div class="step-desc">새 가족과의 행복한<br>시작을 응원해요 🩷</div>
          </div>
        </div>
        <button class="btn-primary" onclick="goToMatching()">🔍 지금 매칭 시작하기 →</button>
      </div>
    </section>
    """

    components.html(html_code, height=1200)
```

- [ ] **Step 2: 앱 실행하여 전체 동작 확인**

Run:
```bash
cd C:/aibigdata/12.Transfer_Learning/mini_project/paw-ong
streamlit run app.py
```

체크리스트:
- 통계 카드 3개 (총 등록견 1,330 / 보호 지역 / 품종 수) 정상 표시
- 추천견 3마리 카드 표시 (이름, 품종, 나이, 지역 포함)
- 지역별 현황 배지 (경기, 서울, 부산 등 상위 6곳) 표시
- 기존 히어로 · 추천견 · 3단계 섹션 디자인 유지

- [ ] **Step 3: 새로고침하여 추천견 변경 확인**

브라우저에서 `R` 또는 새로고침 버튼 클릭.  
Expected: 추천견 3마리가 이전과 다른 강아지로 변경됨.

- [ ] **Step 4: 커밋**

```bash
git add sections/main_page.py
git commit -m "feat: connect main page to CSV data (featured dogs, stats, regions)"
```

---

### Task 6: CTA 버튼 — 매칭 페이지 이동 연결

**Files:**
- Modify: `app.py`

- [ ] **Step 1: app.py 세션 초기화 블록 수정**

`app.py`에서 다음 기존 코드를:

```python
# 세션 초기화
if "page" not in st.session_state:
    st.session_state.page = "main"
```

다음으로 교체한다:

```python
# 세션 초기화 — URL 쿼리 파라미터 우선 적용
if "page" not in st.session_state:
    _valid = {"main", "dog_list", "matching", "guide", "story"}
    _qp = st.query_params.get("page", "main")
    st.session_state.page = _qp if _qp in _valid else "main"
```

- [ ] **Step 2: 앱 실행하여 CTA 버튼 동작 확인**

Run:
```bash
cd C:/aibigdata/12.Transfer_Learning/mini_project/paw-ong
streamlit run app.py
```

메인 페이지 하단 "지금 매칭 시작하기 →" 버튼 클릭.  
Expected: URL이 `?page=matching`으로 바뀌고 매칭 페이지가 로드됨.

- [ ] **Step 3: 커밋**

```bash
git add app.py
git commit -m "feat: support ?page= query param routing for CTA button navigation"
```

---

## 성공 기준 최종 체크리스트

- [ ] 새로고침마다 추천견 3마리가 달라진다
- [ ] 통계 카드 — 총 등록견 1,330 / 보호 지역 N곳 / 품종 N종 표시
- [ ] 지역별 현황 배지가 CSV 실제 데이터 반영 (경기 353 등)
- [ ] "지금 매칭 시작하기 →" 버튼 클릭 시 매칭 페이지로 이동
- [ ] 기존 CSS 디자인 유지 (히어로, 추천견 카드, 3단계 카드 스타일 깨지지 않음)
- [ ] 모든 pytest 테스트 통과
