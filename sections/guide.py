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
    
    <!-- ─── PAGE 4: 입양 안내 ─────────────────────────────────────────────── -->
    <section id="page-guide" class="page">
      <div class="paw-bg">🐾</div>
      <div class="page-title">📖 입양 안내 &amp; 기르는 법 🌿</div>
      <div class="page-sub">준비된 반려인이 되는 첫걸음</div>

      <div class="guide-cols">
        <!-- 왼쪽 -->
        <div>
          <!-- 품종별 가이드 -->
          <div class="card" style="margin-bottom:18px;">
            <div style="font-weight:700;font-size:15px;color:#3D2B1F;margin-bottom:12px;">🐕 품종별 가이드 🌿</div>

            <select id="breed-select" class="form-select" onchange="updateBreedGuide(this.value)">
              <option>골든 리트리버</option>
              <option>말티즈</option>
              <option>포메라니안</option>
              <option>비숑 프리제</option>
              <option>진돗개</option>
            </select>

            <div class="breed-card">
              <div class="breed-emoji" id="breed-emoji">🦮</div>
              <div>
                <div class="breed-name" id="breed-name-display">골든 리트리버</div>
                <div class="breed-tag">추천 매칭 품종 🌿</div>
              </div>
            </div>

            <div class="card-light">🧬 <strong>활동성</strong> — <span id="breed-activity"></span></div>
            <div class="card-light">😊 <strong>케어 방법</strong> — <span id="breed-care"></span></div>
            <div class="card-light">⚠️ <strong>주의사항</strong> — <span id="breed-note"></span></div>
          </div>

          <!-- 타임라인 -->
          <div class="card">
            <div style="font-weight:700;font-size:15px;color:#3D2B1F;margin-bottom:18px;">🗺️ 입양 절차 타임라인 🌿</div>
            <div class="timeline">
              <div class="tl-step">
                <div class="tl-dot" style="background:#E8A598;">💬</div>
                <div class="tl-label" style="color:#E8A598;">상담</div>
                <div class="tl-desc">온라인/전화<br>사전 상담</div>
              </div>
              <div class="tl-arrow">→</div>
              <div class="tl-step">
                <div class="tl-dot" style="background:#7BAE8A;">🏠</div>
                <div class="tl-label" style="color:#7BAE8A;">방문</div>
                <div class="tl-desc">보호소 직접<br>방문 &amp; 만남</div>
              </div>
              <div class="tl-arrow">→</div>
              <div class="tl-step">
                <div class="tl-dot" style="background:#F2C4CE;">🤝</div>
                <div class="tl-label" style="color:#C4748E;">임시 보호</div>
                <div class="tl-desc">2주간<br>적응 기간</div>
              </div>
              <div class="tl-arrow">→</div>
              <div class="tl-step">
                <div class="tl-dot" style="background:#3D2B1F;">🎉</div>
                <div class="tl-label" style="color:#3D2B1F;">정식 입양</div>
                <div class="tl-desc">서류 완료<br>&amp; 입양 확정</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 오른쪽: 체크리스트 -->
        <div class="card">
          <div style="font-weight:700;font-size:15px;color:#3D2B1F;margin-bottom:14px;">✅ 입양 전 체크리스트</div>
          <div class="check-item check-ok">
            <span class="check-icon">✅</span>
            <span>최소 10~15년을 함께할 준비가 됐나요?</span>
          </div>
          <div class="check-item check-ok">
            <span class="check-icon">✅</span>
            <span>집 안에 반려동물이 있어도 되나요?</span>
          </div>
          <div class="check-item check-no">
            <span class="check-icon">⬜</span>
            <span>병원 / 건강 관리 비용을 감당할 수 있나요?</span>
          </div>
          <div class="check-item check-ok">
            <span class="check-icon">✅</span>
            <span>가족 모두가 반려동물을 원하나요?</span>
          </div>
          <div class="check-item check-no">
            <span class="check-icon">⬜</span>
            <span>여행/출장 시 돌봐줄 사람이 있나요?</span>
          </div>
          <div class="check-item check-ok">
            <span class="check-icon">✅</span>
            <span>반려동물 등록을 할 예정인가요?</span>
          </div>
        </div>
      </div>

      <!-- FAQ -->
      <div style="font-weight:700;font-size:15px;color:#3D2B1F;margin-bottom:12px;">❓ 자주 묻는 질문 (FAQ) 🩷</div>

      <div class="faq-item">
        <button class="faq-q" onclick="toggleFAQ(this)">
          Q. 아파트에서도 강아지를 키울 수 있나요?
          <span class="faq-arrow">▼</span>
        </button>
        <div class="faq-a">
          네! 소형견은 아파트 환경에서도 잘 적응합니다. 하루 30분 이상 산책과 규칙적인 운동을 제공해주세요.
        </div>
      </div>

      <div class="faq-item">
        <button class="faq-q" onclick="toggleFAQ(this)">
          Q. 처음 강아지를 키우는데 어떤 품종이 좋을까요?
          <span class="faq-arrow">▼</span>
        </button>
        <div class="faq-a">
          비숑 프리제, 말티즈, 골든 리트리버가 초보자에게 인기 있는 품종입니다. 퍼펙트 매칭으로 맞춤 추천을 받아보세요!
        </div>
      </div>

      <div class="faq-item">
        <button class="faq-q" onclick="toggleFAQ(this)">
          Q. 입양 후 파양이 가능한가요?
          <span class="faq-arrow">▼</span>
        </button>
        <div class="faq-a">
          파양은 강아지에게 큰 상처를 줍니다. 입양 전 충분히 고민해 주시고, 어려움이 생기면 상담을 먼저 요청해주세요.
        </div>
      </div>

      <div class="faq-item">
        <button class="faq-q" onclick="toggleFAQ(this)">
          Q. 입양 비용은 얼마인가요?
          <span class="faq-arrow">▼</span>
        </button>
        <div class="faq-a">
          보호소마다 다르지만 일반적으로 기본 건강검진, 예방접종, 중성화 비용 포함 10~20만원 수준입니다.
        </div>
      </div>
    </section>
    """

    # 2. Streamlit 화면에 렌더링
    components.html(html_code, height=1000)
