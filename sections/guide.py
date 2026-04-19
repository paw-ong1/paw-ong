import streamlit as st
import streamlit.components.v1 as components
from utils.file_loader import load_resource

BREED_DB = {
    '골든 리트리버': { 'emoji': '🦮', 'activity': '높음', 'care': '매일 1시간 이상 산책 필요', 'note': '털 빠짐 많음 — 정기 그루밍 필수' },
    '말티즈':        { 'emoji': '🐩', 'activity': '보통', 'care': '실내 활동으로도 충분',        'note': '눈물 자국 관리 필요' },
    '포메라니안':    { 'emoji': '🐕', 'activity': '보통', 'care': '하루 30분 산책 권장',          'note': '추위에 약함 — 보온 필수' },
    '비숑 프리제':   { 'emoji': '🐶', 'activity': '낮음', 'care': '실내 위주 생활 가능',          'note': '정기 미용 필수 (저알레르기)' },
    '진돗개':        { 'emoji': '🦊', 'activity': '높음', 'care': '넓은 공간 & 충분한 운동',     'note': '사회화 훈련이 중요' },
}

def render():
    # 1. 파일 경로 정의
    css_content = load_resource("css/style.css")

    # ==========================================
    # 동적 렌더링을 위한 데이터 세팅
    # ==========================================
    
    # 품종 리스트
    breeds = []
    if "top_breeds_result" in st.session_state:
      top_breeds = st.session_state.top_breeds_result
      breeds = [str(breed_row.get("품종명", "알 수 없음")) for breed_row, _ in top_breeds]
    
    # 체크리스트 데이터
    checklists = [
        {"question": "최소 10~15년을 함께할 준비가 됐나요?", "checked": True},
        {"question": "집 안에 반려동물이 있어도 되나요?", "checked": True},
        {"question": "병원 / 건강 관리 비용을 감당할 수 있나요?", "checked": False},
        {"question": "가족 모두가 반려동물을 원하나요?", "checked": True},
        {"question": "여행/출장 시 돌봐줄 사람이 있나요?", "checked": False},
        {"question": "반려동물 등록을 할 예정인가요?", "checked": True},
    ]
    
    # FAQ 데이터
    faqs = [
        {
            "q": "아파트에서도 강아지를 키울 수 있나요?", 
            "a": "네! 소형견은 아파트 환경에서도 잘 적응합니다. 하루 30분 이상 산책과 규칙적인 운동을 제공해주세요."
        },
        {
            "q": "처음 강아지를 키우는데 어떤 품종이 좋을까요?", 
            "a": "비숑 프리제, 말티즈, 골든 리트리버가 초보자에게 인기 있는 품종입니다. 퍼펙트 매칭으로 맞춤 추천을 받아보세요!"
        },
        {
            "q": "입양 후 파양이 가능한가요?", 
            "a": "파양은 강아지에게 큰 상처를 줍니다. 입양 전 충분히 고민해 주시고, 어려움이 생기면 상담을 먼저 요청해주세요."
        },
        {
            "q": "입양 비용은 얼마인가요?", 
            "a": "보호소마다 다르지만 일반적으로 기본 건강검진, 예방접종, 중성화 비용 포함 10~20만원 수준입니다."
        }
    ]

    # ==========================================
    # 전체 HTML 동적 생성
    # ==========================================
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    
    # 2. 상단 타이틀 섹션 (HTML 태그 활용)
    st.markdown("""
      <div class="paw-bg">🐾</div>
      <div class="page-title">📖 입양 안내 &amp; 기르는 법 🌿</div>
      <div class="page-sub">준비된 반려인이 되는 첫걸음</div>
    """, unsafe_allow_html=True)

    # 3. Streamlit 컬럼 레이아웃 시작
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        # --- 품종별 가이드 섹션 ---
        with st.container():
            st.markdown('<div style="font-weight:700;font-size:15px;color:#3D2B1F;margin-bottom:12px;">🐕 품종별 가이드 🌿</div>', unsafe_allow_html=True)
            
            if breeds:
                selected_breed = st.selectbox("품종 선택", breeds, label_visibility="collapsed")
                # TODO 
                info = BREED_DB[selected_breed]
                
                # HTML 카드 디자인 주입
                st.markdown(f"""
                        <div class="breed-card">
                          <div class="breed-emoji" id="breed-emoji">{info['emoji']}</div>
                          <div>
                            <div class="breed-name" id="breed-name-display">{selected_breed}</div>
                            <div class="breed-tag">추천 매칭 품종 🌿</div>
                          </div>
                        </div>
                        <div class="card-light">🧬 <strong>활동성</strong> — {info['activity']}</div>
                        <div class="card-light">😊 <strong>케어 방법</strong> — {info['care']}</div>
                        <div class="card-light">⚠️ <strong>주의사항</strong> — {info['note']}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                # HTML 카드 디자인 주입
                st.markdown(f"""
                        <div class="breed-card">
                          <div>
                            <div class="breed-tag">현재 매칭된 품종 데이터가 없습니다. 🐾</div>
                          </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        st.write("") # 간격 조절

        # --- 타임라인 섹션 ---
        with st.container():
            st.markdown('<div style="font-weight:700;font-size:15px;color:#3D2B1F;margin-bottom:18px;">🗺️ 입양 절차 타임라인 🌿</div>', unsafe_allow_html=True)
            
            # Streamlit 컬럼으로 타임라인 구조화
            t1, t2, t3, t4 = st.columns(4)
            steps = [
                {"icon": "💬", "color": "#E8A598", "label_color": "#E8A598",  "label": "상담", "desc": "온라인/전화<br>사전 상담"},
                {"icon": "🏠", "color": "#7BAE8A", "label_color": "#7BAE8A", "label": "방문", "desc": "보호소 직접<br>방문 & 만남"},
                {"icon": "🤝", "color": "#F2C4CE", "label_color": "#C4748E", "label": "임시 보호", "desc": "2주간<br>적응 기간"},
                {"icon": "🎉", "color": "#3D2B1F", "label_color": "#3D2B1F",  "label": "정식 입양", "desc": "서류 완료<br>& 입양 확정"}
            ]
            for i, col in enumerate([t1, t2, t3, t4]):
                with col:
                    # 화살표 HTML 정의 (마지막 인덱스가 아닐 때만 생성)
                    arrow_html = '<div class="tl-arrow">→</div>' if i < 3 else ''
                    st.markdown(f"""
                        <div class="tl-step">
                          <div class="tl-dot" style="background:{steps[i]['color']};">{steps[i]['icon']}</div>
                          <div class="tl-label" style="color:{steps[i]['label_color']};">{steps[i]['label']}</div>
                          <div class="tl-desc">{steps[i]['desc']}</div>
                        </div>
                        {arrow_html}
                    """, unsafe_allow_html=True)
    with col_right:
        # --- 체크리스트 섹션 ---
        with st.container():
            st.markdown('<div class="check-list">✅ 입양 전 체크리스트</div>', unsafe_allow_html=True)
            
            checklists = [
              "최소 10~15년을 함께할 준비가 됐나요?",
              "집 안에 반려동물이 있어도 되나요?",
              "병원 / 건강 관리 비용을 감당할 수 있나요?",
              "가족 모두가 반려동물을 원하나요?",
              "여행/출장 시 돌봐줄 사람이 있나요?",
              "반려동물 등록을 할 예정인가요?",
            ]
            
            # HTML 태그로 체크리스트 스타일 재현
            results = []
            for i, question in enumerate(checklists):
                # key를 고유하게 설정해야 상태가 유지됩니다.
                is_checked = st.checkbox(question, key=f"check_{i}")
                results.append(is_checked)  
                
            # 모든 항목이 체크되었는지 확인하는 기능
            total = len(checklists)
            checked_count = sum(results)
            progress_percentage = checked_count / total

            st.markdown("---") # 구분선

            # 3. 진행도 시각화
            cols = st.columns([8, 2])
            with cols[0]:
                # 프로그레스 바 (0.0 ~ 1.0)
                st.progress(progress_percentage)
            with cols[1]:
                st.markdown(f"**완료도: {int(progress_percentage * 100)}%**")

            # 4. 상태별 맞춤형 카드 디자인
            if checked_count == total:
                st.balloons() # 축하 효과 (선택사항)
                st.markdown(f"""
                    <div>
                        <div style="font-weight:700;font-size:15px;color:#3D2B1F;margin-bottom:18px;">🎉 완벽한 준비!</div>
                        <p>모든 체크리스트를 통과하셨습니다. 이제 새로운 가족을 맞이할 준비가 끝났어요.</p>
                    </div>
                """, unsafe_allow_html=True)
            elif checked_count >= total // 2:
                st.markdown(f"""
                    <div>
                        <div style="font-weight:700;font-size:15px;color:#3D2B1F;margin-bottom:18px;">⏳ 거의 다 왔어요!</div>
                        <p>{total - checked_count}개의 항목이 더 필요합니다. 신중하게 다시 한번 확인해 보세요.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div>
                        <div style="font-weight:700;font-size:15px;color:#3D2B1F;margin-bottom:18px;">🐾 차근차근 준비해요</div>
                        <p>현재 {checked_count}개 항목을 확인했습니다. 입양은 신중한 결정이 필요합니다.</p>
                    </div>
                """, unsafe_allow_html=True)
                
    # --- 하단 FAQ 섹션 ---
    st.markdown('<div class="check-list">❓ 자주 묻는 질문 (FAQ) 🩷</div>', unsafe_allow_html=True)
    
    faqs = [
        {"q": "아파트에서도 강아지를 키울 수 있나요?", "a": "네! 소형견은 아파트 환경에서도 잘 적응합니다. 하루 30분 이상 산책과 규칙적인 운동을 제공해주세요."},
        {"q": "처음 강아지를 키우는데 어떤 품종이 좋을까요?", "a": "비숑 프리제, 말티즈, 골든 리트리버가 초보자에게 인기 있는 품종입니다."},
        {"q": "입양 후 파양이 가능한가요?", "a": "파양은 강아지에게 큰 상처를 줍니다. 입양 전 충분히 고민해 주세요."},
        {"q": "입양 비용은 얼마인가요?", "a": "일반적으로 기본 건강검진, 예방접종 포함 10~20만원 수준입니다."}
    ]
    
    for faq in faqs:
        with st.expander(f"Q. {faq['q']}"):
            st.write(faq['a'])

if __name__ == "__main__":
    render()
