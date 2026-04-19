from sklearn import metrics
import streamlit.components.v1 as components
from utils.file_loader import load_resource
import base64
import html
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="스토리", layout="wide")

# -------------------------------------------------
# 경로
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets" / "images"
LOGO_DIR = ASSETS_DIR / "logo"
STORY_DIR = ASSETS_DIR / "story"

LOGO_CANDIDATES = [
    LOGO_DIR / "paw_ong_logo_brown.png",
    LOGO_DIR / "paw_ong_logo.png",
    LOGO_DIR / "logo.png",
    BASE_DIR / "1.png",
    BASE_DIR / "2.png",
    BASE_DIR / "3.png",
    BASE_DIR / "4.png",
    BASE_DIR / "5.png",
]

logo_path = next((p for p in LOGO_CANDIDATES if p.exists()), None)
watermark_path = logo_path


# -------------------------------------------------
# 유틸
# -------------------------------------------------
def img_to_base64(path: Path | None) -> str | None:
    if path and path.exists():
        return base64.b64encode(path.read_bytes()).decode()
    return None


def safe_text(text: str) -> str:
    return html.escape(text).replace("\n", "<br>")


def render_tags(tags: list[str]) -> str:
    return "".join(
        f"<span class='tag'>{html.escape(tag)}</span>"
        for tag in tags
    )


def render_stars(score: int) -> str:
    if score <= 0:
        return ""
    return "★" * score + "☆" * (5 - score)


def resolve_story_images(filenames: list[str]) -> list[Path]:
    paths = []
    for name in filenames:
        p1 = STORY_DIR / name
        p2 = BASE_DIR / name
        if p1.exists():
            paths.append(p1)
        elif p2.exists():
            paths.append(p2)
    return paths


logo_b64 = img_to_base64(logo_path)
watermark_b64 = img_to_base64(watermark_path)

def render():
    # 1. 파일 경로 정의
    css_content = load_resource("css/style.css")
    js_content = load_resource("js/app.js")

    # HTML 코드 (상단에 스타일 삽입)
    html_code = f"""
    <style>{css_content}</style>
    <script>{js_content}</script>
    """
    
    # <!-- ─── PAGE 5: 스토리 ────────────────────────────────────────────────── -->
    # -------------------------------------------------
    # CSS
    # -------------------------------------------------
    watermark_css = ""
    if watermark_b64:
        watermark_css = f"""
        .story-watermark {{
            position: fixed;
            right: 24px;
            bottom: 8px;
            width: 120px;
            height: 120px;
            background-image: url("data:image/png;base64,{watermark_b64}");
            background-repeat: no-repeat;
            background-size: contain;
            opacity: 0.05;
            pointer-events: none;
            z-index: 0;
        }}
        """

    st.markdown(
        f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang&family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap');

    header {{visibility:hidden;}}
    #MainMenu {{visibility:hidden;}}
    footer {{visibility:hidden;}}

    html, body, [class*="css"] {{
        font-family:'Noto Sans KR', sans-serif;
        background:#FDF6F0;
        color:#3D2B1F;
    }}

    .stApp {{
        background:#FDF6F0;
    }}

    .block-container {{
        max-width:1180px;
        padding-top:4.6rem;
        padding-bottom:2rem;
        position:relative;
        z-index:1;
    }}

    {watermark_css}

    .page-header {{
        display:flex;
        align-items:center;
        gap:10px;
        margin-bottom:6px;
    }}

    .page-title {{
        font-family:'Gowun Batang', serif;
        font-size:32px;
        font-weight:700;
        color:#3D2B1F;
        line-height:1.25;
    }}

    .page-sub {{
        font-size:14px;
        color:#7BAE8A;
        margin-bottom:18px;
    }}

    .sec-title {{
        font-family:'Gowun Batang', serif;
        font-size:24px;
        font-weight:700;
        color:#3D2B1F;
        margin:18px 0 14px 0;
    }}

    .metric-card {{
        background:#FFFFFF;
        border-radius:16px;
        padding:18px;
        border:1px solid #F0E4DC;
        box-shadow:0 2px 10px rgba(0,0,0,0.04);
        min-height:132px;
    }}

    .metric-label {{
        font-size:13px;
        color:#8B6555;
        margin-bottom:10px;
    }}

    .metric-value {{
        font-size:34px;
        font-weight:800;
        color:#E8A598;
        line-height:1.1;
        margin-bottom:8px;
    }}

    .metric-delta {{
        font-size:13px;
        color:#7BAE8A;
    }}

    .review-card {{
        background:#FFFFFF;
        border-radius:16px;
        padding:18px;
        border:1px solid #F0E4DC;
        box-shadow:0 2px 8px rgba(0,0,0,0.04);
        margin-bottom:18px;
        position:relative;
    }}

    .review-top {{
        display:flex;
        align-items:flex-start;
        gap:16px;
    }}

    .review-avatar {{
        width:64px;
        height:64px;
        border-radius:50%;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:28px;
        flex-shrink:0;
    }}

    .review-main {{
        flex:1;
        min-width:0;
        padding-right:120px;
    }}

    .review-head {{
        margin-bottom:4px;
    }}

    .review-title {{
        font-size:20px;
        font-weight:700;
        color:#3D2B1F;
        line-height:1.45;
    }}

    .review-date {{
        position:absolute;
        top:20px;
        right:22px;
        font-size:12px;
        color:#A08070;
        white-space:nowrap;
        text-align:right;
    }}

    .review-sub {{
        font-size:13px;
        color:#A08070;
        margin-bottom:10px;
    }}

    .review-text {{
        font-size:15px;
        line-height:1.8;
        color:#4A3728;
    }}

    .review-stars {{
        font-size:18px;
        color:#E3B73B;
        letter-spacing:1px;
        margin-top:8px;
    }}

    .review-tags {{
        display:flex;
        gap:8px;
        flex-wrap:wrap;
        margin-top:10px;
    }}

    .tag {{
        display:inline-block;
        padding:4px 10px;
        border-radius:999px;
        background:#F5F0EC;
        color:#8B6555;
        font-size:12px;
    }}

    .review-actions {{
        display:flex;
        align-items:center;
        gap:10px;
        margin-top:10px;
        font-size:13px;
        color:#8B6555;
    }}

    .like-count {{
        font-weight:700;
        color:#E08B7E;
        white-space: nowrap;
    }}

    .col-card {{
        background:#FFFFFF;
        border-radius:16px;
        padding:18px;
        border:1px solid #F0E4DC;
        box-shadow:0 2px 8px rgba(0,0,0,0.04);
        margin-bottom:14px;
    }}

    .col-tag {{
        display:inline-block;
        padding:4px 10px;
        border-radius:999px;
        background:#FDE8E4;
        color:#A36A72;
        font-size:12px;
        font-weight:700;
        margin-bottom:10px;
    }}

    .col-title {{
        font-size:18px;
        font-weight:700;
        line-height:1.45;
        color:#3D2B1F;
        margin-bottom:8px;
    }}

    .col-desc {{
        font-size:14px;
        color:#8B6555;
        line-height:1.7;
    }}

    .col-foot {{
        display:flex;
        justify-content:space-between;
        align-items:center;
        margin-top:12px;
        font-size:13px;
        color:#8B6555;
    }}

    .col-read {{
        color:#E8A598;
        font-weight:700;
    }}

    .write-card {{
        background:#FDE8E4;
        border:1px solid #F2C4CE;
        border-radius:16px;
        padding:18px;
    }}

    .write-title {{
        font-size:20px;
        font-weight:700;
        color:#3D2B1F;
        margin-bottom:6px;
    }}

    .write-desc {{
        font-size:14px;
        color:#8B6555;
        margin-bottom:14px;
    }}

    .stTextInput label,
    .stTextArea label {{
        color:#3D2B1F !important;
        font-weight:600 !important;
        font-size:14px !important;
    }}

    .stTextInput input,
    .stTextArea textarea {{
        border-radius:12px !important;
        font-size:15px !important;
        border:1px solid #E8D5C4 !important;
        background:white !important;
        color:#3D2B1F !important;
    }}

    .stButton button {{
        background:#E8A598;
        color:white;
        border:none;
        border-radius:14px;
        padding:10px 12px;
        font-size:14px;
        font-weight:700;
        width:70%;
        min-width:100px;
        white-space:nowrap;
        word-break:keep-all;
        overflow:hidden;
        text-overflow:ellipsis;
    }}

    .stButton button:hover {{
        background:#D99386;
        color:white;
    }}
    </style>
    <div class="story-watermark"></div>
    """,
        unsafe_allow_html=True,
    )

    # -------------------------------------------------
    # 로고 HTML (크기 최적화 버전)
    # -------------------------------------------------
    if logo_b64:
        logo_html = f"""
        <img src="data:image/png;base64,{logo_b64}" style="height:50px; width:auto; margin-right:12px; vertical-align:middle;">
        """
    else:
        logo_html = "🐾"

    # -------------------------------------------------
    # 데이터
    # -------------------------------------------------
    metrics = [
        ("총 매칭 성공", "20", "↑ 25% 지난달 대비"),
        ("입양 만족도", "98.2%", "후기 4.9 / 5.0 ⭐"),
        ("평균 매칭 소요", "14일", "기존 대비 -3일"),
        ("현재 기다리는 중", "24", "지금 입양 가능!"),
    ]
    
    reviews = [
        {
            "title": "루루가 가족이 되었어요",
            "date": "2026.04.16",
            "dog_name": "루루",
            "avatar": "🐶",
            "avatar_bg": "#F2C4CE",
            "region": "서울",
            "tags": ["#입양후기", "#새가족", "#포옹"],
            "stars": 5,
            "likes": 128,
            "images": ["review_lulu_1.jpg", "review_lulu_2.jpg"],
            "content": """포-옹을 통해 새로운 가족이 생겼어요
    아직 세상이 너무 무서운 루루이지만 차분히 잘 알려주고 행복하게 만들어줄 예정입니다
    견생역전 가자!""",
        },
        {
            "title": "모카 입양 한달차",
            "date": "2026.04.10",
            "dog_name": "모카",
            "avatar": "🐕",
            "avatar_bg": "#CFE8CF",
            "region": "경기",
            "tags": ["#한달차", "#적응중", "#포옹스토리"],
            "stars": 5,
            "likes": 96,
            "images": ["review_moca_1.jpg", "review_moca_2.jpg"],
            "content": """첫번째 사진은 입양 첫날이고 나머지는 최근이에요
    중성화도 하고 털도 많이 길어서 완전 예뿐 강아지 됐어요
    아직 예방접종이 안 끝나서 산책은 못 하지만🥹🥺
    집에서 장난감으로 놀고 노즈워크도 하고 가끔 코산책도 하면서 지내고 있어요 전보다 많이 활발해지고 완전히 집에 적응한 것 같아서 기뻐요😍""",
        },
        {
            "title": "12킬로 개린이 두부~",
            "date": "2026.04.05",
            "dog_name": "두부",
            "avatar": "🐾",
            "avatar_bg": "#F5D9DB",
            "region": "전북",
            "tags": ["#성장기록", "#시골강아지", "#폭풍성장"],
            "stars": 4,
            "likes": 74,
            "images": ["review_dubu_1.jpg"],
            "content": """시골 강아지 쑥쑥크고있어유
    힘이장난 아닙니다~^^
    사람 좋아하는 우리두부 4차접종 완료
    저녁에 특식으로 장어랑 삼겹살 간 안한거 급여했습니다
    처음 데려왔을때 5킬로였는데 지금무려 12킬로네요 쑥쑥 크고있습니다^^""",
        },
        {
            "title": "우리는 매일 매일이 추억이야",
            "date": "2026.03.28",
            "dog_name": "콩이",
            "avatar": "🐕‍🦺",
            "avatar_bg": "#E8D8C8",
            "region": "부산",
            "tags": ["#바다산책", "#피크닉", "#성장중"],
            "stars": 5,
            "likes": 143,
            "images": ["review_kongi_1.jpg", "review_kongi_2.jpg"],
            "content": """우리 콩이 산에도 가고 바다도 가고
    친구들 만나서 씐나게 뛰어놀고
    매일 매일 웃으며 잘 지내고 있어요
    오늘은 강가에 피크닉도 다녀왔네요 ㅎ
    여전히 순하고 착하고 이쁘게 무럭무럭 자라는 중입니다
    체중이 2.9kg에서 어느덧 13kg이 넘었네요
    세상 제일 이쁘고 착하고 귀엽고 소중한 우리콩이
    저희에게 보내주셔서 너무너무 감사드립니다""",
        },
        {
            "title": "별이 만난지 벌써 5년❤️",
            "date": "2026.03.15",
            "dog_name": "별이",
            "avatar": "🐩",
            "avatar_bg": "#EEDFCC",
            "region": "대구",
            "tags": ["#5년째", "#가족", "#사랑"],
            "stars": 5,
            "likes": 201,
            "images": ["review_byeol_1.jpg"],
            "content": """우리 별이를 만난지 5년이 되었어요.
    사랑을 알게해 준 우리 강아지. 너무 고마워.""",
        },
        {
            "title": "토리 데려온지 6일째",
            "date": "2026.03.11",
            "dog_name": "토리",
            "avatar": "🐶",
            "avatar_bg": "#D9E7F2",
            "region": "인천",
            "tags": ["#적응기", "#새로운시작", "#무병장수"],
            "stars": 5,
            "likes": 118,
            "images": ["review_tori_1.jpg", "review_tori_2.jpg"],
            "content": """모든 걸 다 줘도 아깝지 않을 우리 별땅이를 보낸지 대충 2년 반이 지났어요. 지금 쓰면서도 눈물이 나려고 하는데 ㅎㅎ
    실감이 안 났다고 해야하나 벌써 2년 반이 지났다는게 믿기지가 않더라고요.
    그러던 와중 여러 이유들이 합쳐서 이제는 새로운 아이를 안아줘도 괜찮지 않을까 하는 맘이 슬그머니… 포-옹을 하루에 몇 십번은 들락날락 한 것 같네요 ㅋㅋㅋ
    이런 내가 밉지는 않을까? 땅이가 슬퍼하면 어쩌지 이런저런 맘이 들었지만 결국 새 아이와 함께 살게 되었습니다.
    열악한 환경에 있는 아이에게 따뜻한 보금자리를 내어주고 싶다고 했지만… 사실은 제가 필요했던 것 같아요. 쟤네가 주는 사랑이 얼마나 따뜻한지 아니까 ㅎㅎ 다른 무엇으로도 채워지지가 않네요.
    
    토리는 아직 겁이 너무 많아요. 와서 냄새 맡아주면 감동받을 정도라. 언젠간 저 아이에게도 저에게도 서로가 당연해질 날이 오겠지요?
    상상이 안 가네요 ㅎㅎ 아직 남의 집 멍멍이 같달까요~~
    근데 얘가 얼마나 똑디인지… 겁낼까봐 아무것도 가르치지 않았는데 혼자 쉬도 가리고 응아도 가리고 ㅎㅎ 예뻐죽겠어요.
    잘했다고 쓰다듬어주고 싶건만 아직은 이른 것 같아서 참고 있습니다.
    이름은 토리예요. 오래오래 살으리 뭐 그런 무병장수의 의미를 담아… 이별을 겪어보니 그냥 건강만 해줬으면 좋겠네요.
    사랑으로 잘 키워보겠습니다. 지나가다 보셨다면 토리의 행복을 빌어주세요!""",
        },
    ]
    
    expert_columns = [
        {
            "tag": "건강 상식",
            "tag_style": "",
            "title": "강아지 치아 관리, 어떻게 해야 할까요?",
            "desc": "매일 양치질이 어렵다면 덴탈껌과 물 첨가제를 활용해보세요.",
            "author": "정이랑 수의사",
        },
        {
            "tag": "훈련 팁",
            "tag_style": "background:#E5F3E8;color:#4E8A5B;",
            "title": "새 집 적응 시 절대 하지 말아야 할 5가지",
            "desc": "처음 2주가 평생을 결정합니다. 강요보다 기다림이 필요해요.",
            "author": "박훈련 트레이너",
        },
    ]


    # -------------------------------------------------
    # 상단
    # -------------------------------------------------
    st.markdown(
        f"<div class='page-header'>{logo_html}<div class='page-title'>스토리 — 가족이 되었어요 ♡</div></div>",
        unsafe_allow_html=True,
    )
    
    st.markdown(
        "<div class='page-sub'>입양 후기와 전문가 칼럼을 함께해요</div>",
        unsafe_allow_html=True,
    )
    
    m1, m2, m3, m4 = st.columns(4)
    for col, (label, value, delta) in zip([m1, m2, m3, m4], metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{html.escape(label)}</div>
                    <div class="metric-value">{html.escape(value)}</div>
                    <div class="metric-delta">{html.escape(delta)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    
    st.write("")


    # -------------------------------------------------
    # 본문
    # -------------------------------------------------
    left, right = st.columns([3, 2], gap="large")

    with left:
        st.markdown("<div class='sec-title'>♡ 입양 후기 피드 ♡</div>", unsafe_allow_html=True)

        for idx, review in enumerate(reviews, start=1):
            title = html.escape(review["title"])
            date = html.escape(review["date"])
            dog_name = html.escape(review["dog_name"])
            avatar = html.escape(review["avatar"])
            avatar_bg = html.escape(review["avatar_bg"])
            region = html.escape(review["region"])
            content = safe_text(review["content"])
            stars = render_stars(review["stars"])
            tags_html = render_tags(review["tags"])

            st.markdown(
                f"""
                <div class="review-card">
                    <div class="review-top">
                        <div class="review-avatar" style="background:{avatar_bg};">{avatar}</div>
                        <div class="review-main">
                            <div class="review-head">
                                <div class="review-title">{title}</div>
                                <div class="review-date">{date}</div>
                            </div>
                            <div class="review-sub">{dog_name} · {region}</div>
                            <div class="review-text">{content}</div>
                            <div class="review-stars">{stars}</div>
                            <div class="review-tags">{tags_html}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            like_key = f"like_count_{idx}"
            clicked_key = f"liked_{idx}"

            if like_key not in st.session_state:
                st.session_state[like_key] = review["likes"]

            if clicked_key not in st.session_state:
                st.session_state[clicked_key] = False

            img_paths = resolve_story_images(review["images"])

            with st.expander(f"{review['dog_name']} 후기 사진 보기", expanded=True):
                if len(img_paths) == 0:
                    st.info("후기 사진을 assets/images/story 폴더에 넣으면 여기에 표시됩니다.")
                elif len(img_paths) == 1:
                    st.image(str(img_paths[0]), use_container_width=True)
                else:
                    cols = st.columns(2)
                    for i, path in enumerate(img_paths):
                        with cols[i % 2]:
                            st.image(str(path), use_container_width=True)

                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

                action_spacer, action_col1, action_col2 = st.columns([4.5, 1.2, 0.6])

                with action_col1:
                    if st.button(
                        "❤️좋아요" if not st.session_state[clicked_key] else "💖완료",
                        key=f"like_btn_{idx}",
                        disabled=st.session_state[clicked_key],
                        use_container_width=True
                    ):
                        st.session_state[like_key] += 1
                        st.session_state[clicked_key] = True

                with action_col2:
                    st.markdown(
                        f"""
                        <div class='review-actions' style='justify-content:flex-end; margin-top:6px;'>
                            <span class='like-count'>❤️ {st.session_state[like_key]}명 공감</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='sec-title'>전문가 칼럼 🌿</div>", unsafe_allow_html=True)

        for item in expert_columns:
            st.markdown(
                f"""
                <div class="col-card">
                    <div class="col-tag" style="{item["tag_style"]}">{html.escape(item["tag"])}</div>
                    <div class="col-title">{html.escape(item["title"])}</div>
                    <div class="col-desc">{html.escape(item["desc"])}</div>
                    <div class="col-foot">
                        <span>{html.escape(item["author"])}</span>
                        <span class="col-read">읽기 →</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div class="write-card">
                <div class="write-title">🐾 나도 후기 남기기</div>
                <div class="write-desc">입양 가족이라면 소중한 이야기를 공유해주세요!</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        writer = st.text_input("작성자")
        content = st.text_area("후기 내용", height=140)

        if st.button("✏️ 후기 작성하기"):
            if not writer.strip() or not content.strip():
                st.warning("작성자와 후기 내용을 입력해 주세요.")
            else:
                st.success("후기 등록 완료")

    # 2. Streamlit 화면에 렌더링
    components.html(html_code, height=1000)
