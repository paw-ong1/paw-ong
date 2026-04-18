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
    
    <!-- ─── PAGE 3: 퍼펙트 매칭 ──────────────────────────────────────────── -->
    <section id="page-matching" class="page">
      <div class="paw-bg">🐾</div>
      <div class="page-title">🔍 퍼펙트 매칭 🩷</div>
      <div class="page-sub">당신의 라이프스타일에 맞는 강아지를 찾아드립니다</div>

      <div class="matching-cols">

        <!-- 왼쪽: 설문 폼 -->
        <div class="card form-card">
          <div class="form-card-title">📋 나의 환경 입력 🌿</div>

          <!-- 주거 형태 -->
          <div class="form-group">
            <label class="form-label">🏠 주거 형태</label>
            <div class="pill-group">
              <label class="pill">
                <input type="radio" name="housing" value="apt" checked>
                <span>🏢 아파트</span>
              </label>
              <label class="pill">
                <input type="radio" name="housing" value="house">
                <span>🏠 주택</span>
              </label>
              <label class="pill">
                <input type="radio" name="housing" value="officetel">
                <span>🏙️ 오피스텔</span>
              </label>
            </div>
          </div>

          <!-- 산책 시간 -->
          <div class="form-group">
            <label class="form-label">🚶 하루 산책 가능 시간</label>
            <div class="slider-val" id="walk-val">1시간</div>
            <input type="range" id="walk-slider" min="0" max="6" value="1"
                   oninput="updateWalkLabel(this.value)">
            <div style="display:flex;justify-content:space-between;font-size:11px;color:#A08070;margin-top:4px;">
              <span>0시간</span><span>6시간</span>
            </div>
          </div>

          <!-- 활동성 -->
          <div class="form-group">
            <label class="form-label">⚡ 활동성 선호도</label>
            <div class="pill-group">
              <label class="pill">
                <input type="radio" name="activity" value="calm" checked>
                <span>😴 조용한 편</span>
              </label>
              <label class="pill">
                <input type="radio" name="activity" value="active">
                <span>⚡ 활동적</span>
              </label>
            </div>
          </div>

          <!-- 알레르기 -->
          <div class="form-group">
            <label class="form-label">🌸 털 알레르기 여부</label>
            <div class="pill-group">
              <label class="pill">
                <input type="radio" name="allergy" value="ok" checked>
                <span>🙆 괜찮아요</span>
              </label>
              <label class="pill">
                <input type="radio" name="allergy" value="sensitive">
                <span>🚫 민감해요</span>
              </label>
            </div>
          </div>

          <!-- 반려 경험 -->
          <div class="form-group">
            <label class="form-label">🐾 반려 경험</label>
            <select id="experience" class="form-select">
              <option value="first">처음 키워요</option>
              <option value="1-3">1~3년</option>
              <option value="3years">3년 이상</option>
            </select>
          </div>

          <button class="btn-primary full" onclick="doMatch()">🔍 매칭 시작하기</button>
        </div>

        <!-- 오른쪽: 결과 -->
        <div class="card" style="min-height:360px;">

          <!-- 빈 상태 -->
          <div class="result-empty" id="result-empty">
            <div class="result-empty-icon">🐾</div>
            <div class="result-empty-text">조건을 입력하고<br>매칭을 시작해보세요!</div>
            <div class="result-empty-sub">당신에게 딱 맞는 반려견을 찾아드릴게요 🩷</div>
          </div>

          <!-- 결과 패널 -->
          <div id="result-panel" style="display:none;">

            <!-- 점수 히어로 -->
            <div class="card-pink result-hero">
              <div class="result-emoji" id="res-emoji">🦮</div>
              <div class="result-score" id="res-score">0% 일치!</div>
              <div class="result-desc"  id="res-breed"></div>
            </div>

            <!-- 매칭 점수 바 -->
            <div style="margin:16px 0 12px;">
              <div style="font-weight:700;font-size:14px;color:#3D2B1F;margin-bottom:12px;">🎯 매칭 결과 🩷</div>

              <div class="bar-group">
                <div class="bar-label-row">
                  <span>활동성 적합도</span>
                  <span id="bar-activity-val">—</span>
                </div>
                <div class="bar-track">
                  <div class="bar-fill" id="bar-activity-fill"></div>
                </div>
              </div>

              <div class="bar-group">
                <div class="bar-label-row">
                  <span>주거 적합도</span>
                  <span id="bar-housing-val">—</span>
                </div>
                <div class="bar-track">
                  <div class="bar-fill" id="bar-housing-fill"></div>
                </div>
              </div>

              <div class="bar-group">
                <div class="bar-label-row">
                  <span>경험 적합도</span>
                  <span id="bar-exp-val">—</span>
                </div>
                <div class="bar-track">
                  <div class="bar-fill" id="bar-exp-fill"></div>
                </div>
              </div>
            </div>

            <!-- AI 추천 이유 -->
            <div class="ai-box" id="res-reason"></div>

            <div style="margin-top:14px;">
              <button class="btn-primary full" onclick="navigate('list')">🐾 입양 신청하러 가기</button>
            </div>
          </div>

        </div>
      </div>
    </section>
    """

    # 2. Streamlit 화면에 렌더링
    components.html(html_code, height=1000)
