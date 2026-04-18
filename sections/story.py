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
    
    <!-- ─── PAGE 5: 스토리 ────────────────────────────────────────────────── -->
    <section id="page-story" class="page">
      <div class="paw-bg">🐾</div>
      <div class="page-title">📖 스토리 — 행복한 재회 🩷</div>
      <div class="page-sub">입양 후기와 전문가 칼럼을 함께해요</div>

      <!-- 통계 -->
      <div class="metrics-row">
        <div class="metric-card">
          <div class="metric-label">🐾 총 매칭 성공</div>
          <div class="metric-value">2,847</div>
          <div class="metric-delta">↑ 이번달 +143</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">😊 입양 만족도</div>
          <div class="metric-value">98.2%</div>
          <div class="metric-delta">후기 4.9 / 5.0 ⭐</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">⏱️ 평균 매칭 소요</div>
          <div class="metric-value">3.2일</div>
          <div class="metric-delta">기존 대비 -68%</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">🐕 현재 대기중</div>
          <div class="metric-value">1,204</div>
          <div class="metric-delta">지금 입양 가능!</div>
        </div>
      </div>

      <div class="story-cols">
        <!-- 후기 피드 -->
        <div>
          <div style="font-weight:700;font-size:15px;color:#3D2B1F;margin-bottom:14px;">💌 입양 후기 피드 🩷</div>

          <div class="review-card">
            <div class="review-avatar" style="background:#F2C4CE;">🐕</div>
            <div class="review-body">
              <div class="review-top">
                <span class="review-name">조보라 님</span>
                <span class="review-date">2024.03.15</span>
              </div>
              <div class="review-text">
                처음엔 걱정이 많았지만 초코 덕분에 매일이 행복해요. 강력 추천합니다! ⭐⭐⭐⭐⭐
              </div>
              <div class="review-tags">
                <span class="review-tag">#입양완료</span>
                <span class="review-tag">#3년차</span>
              </div>
            </div>
          </div>

          <div class="review-card">
            <div class="review-avatar" style="background:#C8E6C9;">🐩</div>
            <div class="review-body">
              <div class="review-top">
                <span class="review-name">김뽀미 님</span>
                <span class="review-date">2024.03.07</span>
              </div>
              <div class="review-text">
                1인 가구라 외로웠는데 뽀미와 함께하며 집이 진짜 집 같아졌어요! ⭐⭐⭐⭐⭐
              </div>
              <div class="review-tags">
                <span class="review-tag">#1인가구</span>
                <span class="review-tag">#소형견</span>
              </div>
            </div>
          </div>

          <div class="review-card">
            <div class="review-avatar" style="background:#FDE8E4;">🐾</div>
            <div class="review-body">
              <div class="review-top">
                <span class="review-name">이해피 님</span>
                <span class="review-date">2024.02.28</span>
              </div>
              <div class="review-text">
                아이들이 정말 좋아해요. 가족 모두에게 활력이 생겼습니다 🩷 감사해요!
              </div>
              <div class="review-tags">
                <span class="review-tag">#가족입양</span>
                <span class="review-tag">#대형견</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 전문가 칼럼 -->
        <div>
          <div style="font-weight:700;font-size:15px;color:#3D2B1F;margin-bottom:14px;">📚 전문가 칼럼 🌿</div>

          <div class="col-card">
            <span class="col-tag" style="background:#FDE8E4;color:#C4748E;">건강 상식</span>
            <div class="col-title">강아지 치아 관리, 어떻게 해야 할까요?</div>
            <div class="col-desc">매일 양치질이 어렵다면 덴탈껌과 물 첨가제를 활용해보세요.</div>
            <div class="col-foot">
              <span class="col-author">👨‍⚕️ 김수의 수의사</span>
              <span class="col-read">읽기 →</span>
            </div>
          </div>

          <div class="col-card">
            <span class="col-tag" style="background:#E8F5E9;color:#2E7D32;">훈련 팁</span>
            <div class="col-title">새 집 적응 시 절대 하지 말아야 할 5가지</div>
            <div class="col-desc">처음 2주가 평생을 결정합니다. 강요보단 기다림이 필요해요.</div>
            <div class="col-foot">
              <span class="col-author">🐾 박훈련 트레이너</span>
              <span class="col-read">읽기 →</span>
            </div>
          </div>

          <!-- 후기 작성 -->
          <div class="col-card write-card">
            <div class="write-card-title">🐾 나도 후기 남기기</div>
            <div class="write-card-desc">입양 가족이라면 소중한 이야기를 공유해주세요!</div>
            <button class="btn-primary full"
                    onclick="alert('준비 중인 기능입니다. 곧 만나요! 🩷')">
              ✏️ 후기 작성하기
            </button>
          </div>
        </div>
      </div>
    </section>
    """

    # 2. Streamlit 화면에 렌더링
    components.html(html_code, height=1000)
