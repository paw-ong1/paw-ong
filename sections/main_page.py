import json
import streamlit as st
import streamlit.components.v1 as components
from utils.file_loader import load_resource
from utils.data_loader import load_dog_df, get_featured_dogs, get_stats, get_region_stats


def _safe_json(obj):
    """JSON 직렬화 후 </script> 시퀀스를 이스케이프한다."""
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


@st.cache_data
def _load_static_data():
    """통계·지역 데이터 — 결정론적이므로 캐시 적용."""
    df = load_dog_df()
    return _safe_json(get_stats(df=df)), _safe_json(get_region_stats(df=df))


def render():
    css_content = load_resource("css/style.css")
    js_content  = load_resource("js/app.js")

    try:
        stats_json, regions_json = _load_static_data()
    except Exception as e:
        st.error(f"데이터 로드 오류: {e}")
        return

    # 추천견 — session_state에 저장해 버튼 클릭 후 재렌더링 시에도 같은 강아지 유지
    # (새 세션 시작 시 또는 메인 페이지 첫 진입 시에만 새로 뽑음)
    if "main_featured_dogs" not in st.session_state:
        st.session_state.main_featured_dogs = get_featured_dogs()
    featured_dogs = st.session_state.main_featured_dogs

    # ── 상단 iframe: 히어로 + 통계 ──────────────────────────────────────────
    top_html = f"""
    <style>{css_content}</style>
    <script>
      const STATS   = {stats_json};
      const REGIONS = {regions_json};
    </script>
    <script>{js_content}</script>

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
    </section>
    """
    components.html(top_html, height=560)

    # ── 이달의 추천견 (Streamlit 네이티브 — iframe 밖) ──────────────────────
    # iframe 밖에서 렌더링해야 st.button으로 session_state를 통한 페이지 이동이 가능
    st.markdown("""
    <style>
    /* 추천견 입양 신청 버튼 스타일 */
    div[data-testid="stButton"][class*="st-key-featured_btn"] > button {
        background: #E8A598;
        color: white;
        border: none;
        border-radius: 20px;
        padding: 7px 0;
        font-size: 13px;
        font-weight: 700;
        font-family: 'Noto Sans KR', sans-serif;
        width: 100%;
        cursor: pointer;
        transition: background 0.2s;
        margin-top: 0;
    }
    div[data-testid="stButton"][class*="st-key-featured_btn"] > button:hover {
        background: #7BAE8A;
        color: white;
    }
    </style>
    <div class="section-header" style="padding: 0 4px; margin-bottom: 10px;">
      <div>
        <div class="sec-title">🐶 이달의 추천견 🩷</div>
        <div class="sec-sub">보호소에서 기다리는 친구들을 소개합니다</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    EMOJIS = ['🦮', '🐩', '🐕‍🦺']
    COLORS = ['#F2C4CE', '#C8E6C9', '#FDE8E4']

    cols = st.columns(3)
    for i, (col, dog) in enumerate(zip(cols, featured_dogs)):
        with col:
            st.markdown(f"""
            <div class="dog-card">
              <div class="dog-card-img" style="background:{COLORS[i % 3]}">{EMOJIS[i % 3]}</div>
              <div class="dog-card-body">
                <div class="dog-card-name">{dog['이름']}</div>
                <div class="dog-card-info">{dog['품종']} · {dog['나이']} · {dog['성별']}</div>
                <div class="dog-card-region">📍 {dog['지역']}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("입양 신청 →", key=f"featured_btn_{i}", use_container_width=True):
                st.session_state.page = "dog_list"
                st.session_state.selected_dog_id = int(dog['id'])
                st.rerun()

    # ── 하단 iframe: 지역별 현황 + 3단계 프로세스 ──────────────────────────
    bottom_html = f"""
    <style>{css_content}</style>
    <script>
      const REGIONS = {regions_json};
    </script>
    <script>{js_content}</script>

    <section id="page-main" class="page active">
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
      </div>
    </section>
    """
    components.html(bottom_html, height=480)

    # ── CTA 버튼 (iframe 밖 Streamlit 네이티브) ─────────────────────────────
    st.markdown("""
    <style>
    div[data-testid="stButton"].cta-btn > button {
        background: linear-gradient(135deg, #E8A598, #C07B6A);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 14px 32px;
        font-size: 16px;
        font-weight: 700;
        width: 100%;
        cursor: pointer;
    }
    div[data-testid="stButton"].cta-btn > button:hover {
        background: linear-gradient(135deg, #C07B6A, #A0604A);
    }
    </style>
    """, unsafe_allow_html=True)
    _, col, _ = st.columns([1, 2, 1])
    with col:
        if st.button("🔍 지금 매칭 시작하기 →", use_container_width=True, key="cta_matching"):
            st.session_state.page = "matching"
            st.rerun()
