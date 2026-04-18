import streamlit.components.v1 as components
from utils.file_loader import load_resource

def render():
    # 1. 파일 경로 정의
    css_content = load_resource("css/style.css")
    js_content = load_resource("js/app.js")

    # HTML 코드 (상단에 스타일 삽입)
    html_code = f"""
    <style>{css_content}</style>
    <script>{js_content}</script>
    
    <!-- ─── PAGE 2: 반려견 리스트 ─────────────────────────────────────────── -->
    <section id="page-list" class="page">
      <div class="paw-bg">🐾</div>
      <div class="page-title">현재 반려견 리스트 🩷</div>
      <div class="page-sub">보호소에서 기다리는 친구들을 만나보세요</div>

      <!-- 필터 -->
      <div class="filters">
        <input id="search-input"  class="filter-input"  type="text" placeholder="🔍  이름 또는 품종 검색...">
        <select id="filter-status" class="filter-select">
          <option>전체</option>
          <option>입양가능</option>
          <option>임시보호중</option>
          <option>입양완료</option>
        </select>
        <select id="filter-size" class="filter-select">
          <option>전체</option>
          <option>소형</option>
          <option>중형</option>
          <option>대형</option>
        </select>
        <select id="filter-act" class="filter-select">
          <option>전체</option>
          <option>낮음</option>
          <option>보통</option>
          <option>높음</option>
        </select>
      </div>

      <div class="result-count" id="result-count"></div>

      <!-- 테이블 -->
      <div class="table-wrap">
        <div class="table-head">
          <span>번호</span>
          <span>이름</span>
          <span>품종</span>
          <span>나이</span>
          <span>성별</span>
          <span>지역</span>
          <span>상태</span>
          <span>크기</span>
        </div>
        <div id="dog-tbody"></div>
      </div>

      <div class="pagination" id="pagination"></div>
    </section>
    """

    # 2. Streamlit 화면에 렌더링
    components.html(html_code, height=1000)
