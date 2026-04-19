import json
import pandas as pd
import streamlit.components.v1 as components
from utils.file_loader import load_resource


def _load_featured_dogs() -> list[dict]:
    """CSV에서 추천견 3마리를 선별."""
    df = pd.read_csv("data/korea_dog_list_fixed.csv", encoding="utf-8-sig")

    shelters_map = {}
    with open("data/shelter_info.json", "r", encoding="utf-8") as f:
        shelters_map = json.load(f)

    # 사회도 + 친화도가 높은 상위 3마리 선택
    df["추천점수"] = df["사회도"].astype(int) + df["친화도"].astype(int)
    top3 = df.nlargest(3, "추천점수").head(3)

    dogs = []
    for _, row in top3.iterrows():
        region = str(row["지역"])
        shelter = shelters_map.get(region, {})
        age_month = int(row["나이(월)"])
        age_text = f"{age_month}개월" if age_month < 12 else f"{age_month // 12}살"
        dogs.append({
            "name": str(row["이름"]),
            "breed": str(row["품종"]),
            "age": age_text,
            "gender": str(row["성별"]),
            "region": region,
            "shelter_name": shelter.get("name", ""),
        })
    return dogs


def render():
    css_content = load_resource("css/style.css")

    featured = _load_featured_dogs()

    emojis = ["🦮", "🐩", "🐕‍🦺"]
    colors = ["#F2C4CE", "#C8E6C9", "#FDE8E4"]

    cards_html = ""
    for i, d in enumerate(featured):
        cards_html += f"""
        <div class="dog-card">
          <div class="dog-card-img" style="background:{colors[i]}">{emojis[i]}</div>
          <div class="dog-card-body">
            <div class="dog-card-name">{d['name']}</div>
            <div class="dog-card-info">{d['breed']} · {d['age']} · {d['gender']}</div>
            <div class="dog-card-region">📍 {d['region']} · {d['shelter_name']}</div>
          </div>
        </div>
        """

    html_code = f"""
    <style>{css_content}</style>

    <section id="page-main" class="page active">
      <div class="paw-bg">🐾</div>

      <!-- 히어로 -->
      <div class="hero">
        <div class="hero-bg-emoji">🐕</div>
        <div class="hero-badge">🐾 새로운 가족을 만나보세요</div>
        <h1>당신에게 딱 맞는<br>가족을 찾아드립니다</h1>
        <p>매일 기다리는 소중한 생명들, 지금 만나보세요</p>
      </div>

      <!-- 추천견 -->
      <div class="section-header">
        <div>
          <div class="sec-title">🐶 이달의 추천견 🩷</div>
          <div class="sec-sub">사회성과 친화력이 가장 높은 친구들을 소개합니다</div>
        </div>
      </div>
      <div class="dog-cards">
        {cards_html}
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

    components.html(html_code, height=1000)
