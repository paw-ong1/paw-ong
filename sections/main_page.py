import json
import streamlit as st
import streamlit.components.v1 as components
from utils.file_loader import load_resource
from utils.data_loader import get_featured_dogs, get_stats, get_region_stats

# 추천견은 세션 단위로 고정 (매 rerun마다 재셔플 방지)
@st.cache_data
def _load_page_data():
    """CSV 데이터를 로드하고 JSON 문자열로 반환한다. 앱 재시작 전까지 캐시됨."""
    def _safe_json(obj):
        # </script> 시퀀스가 script 태그를 조기 종료하지 않도록 이스케이프
        return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")
    return (
        _safe_json(get_featured_dogs()),
        _safe_json(get_stats()),
        _safe_json(get_region_stats()),
    )


def render():
    css_content = load_resource("css/style.css")
    js_content  = load_resource("js/app.js")

    # CSV → JSON 직렬화 (Python → JS 전역변수로 주입)
    try:
        featured_json, stats_json, regions_json = _load_page_data()
    except Exception as e:
        st.error(f"데이터 로드 오류: {e}")
        return

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
