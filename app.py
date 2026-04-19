import streamlit as st
import base64

st.set_page_config(page_title="🐾 반려동물 입양 매칭", layout="wide")

# CSS 주입
with open("css/style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 세션 초기화 — URL 쿼리 파라미터 우선 적용
if "page" not in st.session_state:
    current_url_page = st.query_params.get("page", "main")
    
    # 유효한 페이지 이름인지 확인 후 세션에 저장
    valid_pages = ["main", "dog_list", "matching", "guide", "story"]
    if current_url_page in valid_pages:
        st.session_state.page = current_url_page
    else:
        st.session_state.page = "main"

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# 이미지 경로 설정 (실제 경로 확인 필수)
img_base64 = get_base64_image("assets/images/logo/paw_ong_logo_brown.png")

# 사이드바
with st.sidebar:
    st.markdown(f"""
    <div class="logo-area">
      <img src="data:image/png;base64,{img_base64}" class="logo-icon" alt="발바닥 아이콘">
      <span class="logo-text">paw(포)옹</span>
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
            st.query_params["page"] = key
            st.rerun()
            
    # 현재 선택된 페이지의 key
    active_page_key = st.session_state.page
    st.markdown(f"""
        <style>
            /* 버튼 배경색과 텍스트 색상 수정 */
            div[class*="st-key-nav_{active_page_key}"] button {{
                background: #E8A598 !important;
                color: white !important;
            }}
            /* 버튼 안의 텍스트 굵기 적용 */
            div[class*="st-key-nav_{active_page_key}"] button p {{
                font-weight: 700 !important;
            }}
        </style>
    """, unsafe_allow_html=True)

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