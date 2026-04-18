import streamlit as st

st.set_page_config(page_title="🐾 반려동물 입양 매칭", layout="wide")

# CSS 주입
with open("css/style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 세션 초기화
if "page" not in st.session_state:
    st.session_state.page = "main"

# 사이드바
with st.sidebar:
    st.markdown("""
    <div class="logo-area">
      <span class="logo-icon">🐾</span>
      <span class="logo-text">반려동물 입양</span>
    </div>
    """, unsafe_allow_html=True)

    pages = {
        "main":     "🏠 메인 페이지",
        "dog_list":     "🐕 반려견 리스트",
        "matching": "🔍 퍼펙트 매칭",
        "guide":    "📖 입양 안내 & 기르는 법",
        "story":    "💌 스토리",
    }
    for key, label in pages.items():
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()

    st.markdown("""
    <div class="sidebar-footer">
      🐾 보호소 반려동물과<br>따뜻한 가족을 이어드립니다
    </div>
    """, unsafe_allow_html=True)

# 페이지 라우팅
page = st.session_state.page

if page == "main":
    from sections.main_page import render
elif page == "dog_list":
    from sections.dog_list import render
elif page == "matching":
    from sections.matching import render
elif page == "guide":
    from sections.guide import render
elif page == "story":
    from sections.story import render

render()