import streamlit as st
import pandas as pd
import os
import random
import requests
from pathlib import Path


# ══════════════════════════════════════════════════════════════════════════════
# 데이터 로드
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    base      = Path(__file__).parent.parent
    breeds_df = pd.read_csv(base / "data" / "dog_breeds.csv",           encoding="utf-8-sig")
    korea_df  = pd.read_csv(base / "data" / "korea_dog_list_fixed.csv", encoding="utf-8-sig")
    return breeds_df, korea_df


@st.cache_data
def build_breed_image_map():
    """품종 → 사용 가능한 이미지 경로 목록 캐싱."""
    base    = Path(__file__).parent.parent
    img_dir = base / "assets" / "images" / "dogs"
    try:
        _, korea_df = load_data()
    except Exception:
        return {}
    breed_map: dict = {}
    for _, row in korea_df.iterrows():
        breed  = row.get("품종", "")
        dog_id = row.get("아이디", "")
        path   = img_dir / f"{dog_id}-1.jpg"
        if path.exists():
            breed_map.setdefault(breed, []).append(str(path))
    return breed_map


def get_breed_image(breed_name: str):
    bmap  = build_breed_image_map()
    paths = bmap.get(breed_name, [])
    if not paths:
        paths = bmap.get("믹스견", [])
    return random.choice(paths) if paths else None


def get_dog_image_path(dog_id: str):
    base = Path(__file__).parent.parent
    path = base / "assets" / "images" / "dogs" / f"{dog_id}-1.jpg"
    return str(path) if path.exists() else None


# ══════════════════════════════════════════════════════════════════════════════
# 설문 정의 — 30개 · 섹션 5개
# ══════════════════════════════════════════════════════════════════════════════
SECTIONS = ["🏠 주거 환경", "🚶 라이프스타일", "🐾 경험 & 성향", "🐕 선호 특성", "💰 실용 조건"]

QUESTIONS = [
    # ── 섹션 0: 주거 환경 (Q1~6) ─────────────────────────────────────────────
    {
        "id": "housing_type", "section": 0,
        "label": "Q1. 현재 주거 형태는 무엇인가요?",
        "options": ["아파트 (저층 1~5층)", "아파트 (중·고층 6층+)", "빌라 / 연립주택",
                    "단독주택 (마당 있음)", "단독주택 (마당 없음)", "오피스텔", "원룸 / 고시원"],
        "weights": {"아파트 (저층 1~5층)": 2, "아파트 (중·고층 6층+)": 2, "빌라 / 연립주택": 2,
                    "단독주택 (마당 있음)": 5, "단독주택 (마당 없음)": 3,
                    "오피스텔": 1, "원룸 / 고시원": 1},
    },
    {
        "id": "housing_size", "section": 0,
        "label": "Q2. 집의 실내 면적은 대략?",
        "options": ["10평 미만", "10~20평", "20~30평", "30~45평", "45~60평", "60평 이상"],
        "weights": {"10평 미만": 1, "10~20평": 2, "20~30평": 3, "30~45평": 4, "45~60평": 5, "60평 이상": 5},
    },
    {
        "id": "yard", "section": 0,
        "label": "Q3. 강아지가 뛰어놀 수 있는 외부 공간은?",
        "options": ["넓은 사유 마당 있음 (50㎡+)", "작은 마당 / 테라스", "단지 내 산책로 (도보 2분)",
                    "인근 공원 (도보 5분)", "인근 공원 (도보 10분+)", "산책 공간 없음"],
        "weights": {"넓은 사유 마당 있음 (50㎡+)": 5, "작은 마당 / 테라스": 4,
                    "단지 내 산책로 (도보 2분)": 3, "인근 공원 (도보 5분)": 2,
                    "인근 공원 (도보 10분+)": 2, "산책 공간 없음": 1},
    },
    {
        "id": "noise_neighbor", "section": 0,
        "label": "Q4. 층간소음 / 이웃 소음 민감도는?",
        "options": ["매우 예민 (소음 민원 경험)", "꽤 예민한 편", "보통",
                    "별로 신경 안 씀", "전혀 상관없음 (단독주택 등)"],
        "weights": {"매우 예민 (소음 민원 경험)": 1, "꽤 예민한 편": 2, "보통": 3,
                    "별로 신경 안 씀": 4, "전혀 상관없음 (단독주택 등)": 5},
    },
    {
        "id": "other_pets", "section": 0,
        "label": "Q5. 현재 집에 다른 반려동물이 있나요?",
        "options": ["없음", "고양이 1마리", "고양이 여러 마리", "소형견 1마리",
                    "소형견 여러 마리", "중·대형견", "고양이 + 강아지 혼합"],
        "weights": {"없음": 3, "고양이 1마리": 2, "고양이 여러 마리": 2,
                    "소형견 1마리": 3, "소형견 여러 마리": 2, "중·대형견": 2,
                    "고양이 + 강아지 혼합": 2},
    },
    {
        "id": "children", "section": 0,
        "label": "Q6. 함께 사는 어린아이(12세 미만)가 있나요?",
        "options": ["없음", "영유아 (0~3세)", "미취학 (4~6세)",
                    "초등 저학년 (7~9세)", "초등 고학년 (10~12세)", "복수 연령대 혼합"],
        "weights": {"없음": 3, "영유아 (0~3세)": 3, "미취학 (4~6세)": 3,
                    "초등 저학년 (7~9세)": 3, "초등 고학년 (10~12세)": 3, "복수 연령대 혼합": 3},
        "flag": "has_children",
    },
    # ── 섹션 1: 라이프스타일 (Q7~12) ──────────────────────────────────────────
    {
        "id": "walk_time", "section": 1,
        "label": "Q7. 하루 평균 산책 가능 시간은?",
        "options": ["15분 미만", "15~30분", "30분~1시간", "1~1.5시간", "1.5~2시간", "2시간 이상"],
        "weights": {"15분 미만": 1, "15~30분": 1, "30분~1시간": 2,
                    "1~1.5시간": 3, "1.5~2시간": 4, "2시간 이상": 5},
    },
    {
        "id": "activity_pref", "section": 1,
        "label": "Q8. 평소 본인의 활동성은?",
        "options": ["주로 집에서 쉼 (집순이/집돌이)", "가벼운 산책 즐김",
                    "주 2~3회 운동", "매일 운동함", "조깅·등산 등 강도 높은 활동"],
        "weights": {"주로 집에서 쉼 (집순이/집돌이)": 1, "가벼운 산책 즐김": 2,
                    "주 2~3회 운동": 3, "매일 운동함": 4, "조깅·등산 등 강도 높은 활동": 5},
    },
    {
        "id": "alone_time", "section": 1,
        "label": "Q9. 강아지가 하루 혼자 있어야 하는 시간은?",
        "options": ["1시간 미만", "1~3시간", "3~5시간", "5~7시간", "7~9시간", "9시간 이상"],
        "weights": {"1시간 미만": 5, "1~3시간": 4, "3~5시간": 3,
                    "5~7시간": 2, "7~9시간": 1, "9시간 이상": 1},
    },
    {
        "id": "travel_freq", "section": 1,
        "label": "Q10. 장거리 여행 · 출장 빈도는?",
        "options": ["거의 없음 (연 1~2회)", "분기 1회", "월 1회", "월 2~3회", "거의 매주"],
        "weights": {"거의 없음 (연 1~2회)": 5, "분기 1회": 4, "월 1회": 3, "월 2~3회": 2, "거의 매주": 1},
    },
    {
        "id": "work_type", "section": 1,
        "label": "Q11. 주된 근무 / 생활 형태는?",
        "options": ["전업주부 / 은퇴 (거의 집에)", "재택근무 (주 5일)",
                    "유연근무 (주 2~3일 출근)", "일반 직장 (9~6시)", "교대근무 / 불규칙"],
        "weights": {"전업주부 / 은퇴 (거의 집에)": 5, "재택근무 (주 5일)": 4,
                    "유연근무 (주 2~3일 출근)": 3, "일반 직장 (9~6시)": 2, "교대근무 / 불규칙": 1},
    },
    {
        "id": "family_member", "section": 1,
        "label": "Q12. 강아지를 함께 돌봐줄 사람이 있나요?",
        "options": ["나 혼자", "파트너 / 배우자", "가족 2명", "가족 3명 이상", "전문 펫시터 이용 가능"],
        "weights": {"나 혼자": 1, "파트너 / 배우자": 2, "가족 2명": 3,
                    "가족 3명 이상": 4, "전문 펫시터 이용 가능": 3},
    },
    # ── 섹션 2: 경험 & 성향 (Q13~18) ─────────────────────────────────────────
    {
        "id": "experience", "section": 2,
        "label": "Q13. 강아지를 키워본 경험은?",
        "options": ["전혀 없음 (완전 초보)", "어릴 때 가족이 키움 (직접 케어 아님)",
                    "성인 후 1~2년 경험", "3~5년 경험", "5년 이상 경험"],
        "weights": {"전혀 없음 (완전 초보)": 1, "어릴 때 가족이 키움 (직접 케어 아님)": 2,
                    "성인 후 1~2년 경험": 3, "3~5년 경험": 4, "5년 이상 경험": 5},
    },
    {
        "id": "training", "section": 2,
        "label": "Q14. 훈련에 투자할 수 있는 시간 · 의지는?",
        "options": ["거의 없음 (훈련 자신 없음)", "주 1회 정도", "매일 5~10분",
                    "매일 15~20분", "매일 30분 이상 (전문 훈련 목표)"],
        "weights": {"거의 없음 (훈련 자신 없음)": 1, "주 1회 정도": 2, "매일 5~10분": 2,
                    "매일 15~20분": 3, "매일 30분 이상 (전문 훈련 목표)": 5},
    },
    {
        "id": "noise_tolerance", "section": 2,
        "label": "Q15. 강아지 짖음 소리에 대한 내성은?",
        "options": ["매우 예민 (조용한 견종 필수)", "조금 예민", "보통", "괜찮은 편", "전혀 신경 안 씀"],
        "weights": {"매우 예민 (조용한 견종 필수)": 1, "조금 예민": 2, "보통": 3,
                    "괜찮은 편": 4, "전혀 신경 안 씀": 5},
    },
    {
        "id": "allergy", "section": 2,
        "label": "Q16. 털 알레르기 또는 민감 반응이 있나요?",
        "options": ["심함 (저알레르기 견종 필수)", "약간 있음 (관리 가능)", "없음"],
        "weights": {"심함 (저알레르기 견종 필수)": 1, "약간 있음 (관리 가능)": 2, "없음": 3},
        "flag": "allergy_sensitive",
    },
    {
        "id": "shed_tolerance", "section": 2,
        "label": "Q17. 털 빠짐에 대한 허용 범위는?",
        "options": ["털 빠짐 절대 싫음", "아주 적은 것만 OK", "적당히는 OK",
                    "많아도 청소하면 됨", "전혀 상관없음"],
        "weights": {"털 빠짐 절대 싫음": 1, "아주 적은 것만 OK": 2, "적당히는 OK": 3,
                    "많아도 청소하면 됨": 4, "전혀 상관없음": 5},
    },
    {
        "id": "grooming", "section": 2,
        "label": "Q18. 미용 · 그루밍에 시간과 비용 투자 의향은?",
        "options": ["최소한만 (셀프 브러싱 정도)", "분기 1회 미용샵",
                    "월 1회 미용샵", "월 2회 이상 미용샵", "적극 투자 (전문 그루밍 정기)"],
        "weights": {"최소한만 (셀프 브러싱 정도)": 1, "분기 1회 미용샵": 2,
                    "월 1회 미용샵": 3, "월 2회 이상 미용샵": 4, "적극 투자 (전문 그루밍 정기)": 5},
    },
    # ── 섹션 3: 선호 특성 (Q19~24) ────────────────────────────────────────────
    {
        "id": "size_pref", "section": 3,
        "label": "Q19. 선호하는 강아지 크기는?",
        "options": ["초소형 (5kg 미만)", "소형 (5~10kg)", "중소형 (10~15kg)",
                    "중형 (15~25kg)", "대형 (25~40kg)", "초대형 (40kg 이상)", "상관없음"],
        "weights": None, "direct": "size_pref",
    },
    {
        "id": "temperament", "section": 3,
        "label": "Q20. 어떤 성격의 강아지를 원하나요?",
        "options": ["조용하고 차분한", "애교 많고 붙임성 있는", "활발하고 장난기 많은",
                    "독립적이고 의연한", "충성스럽고 보호 본능 강한", "호기심 많고 탐험 좋아하는"],
        "weights": {"조용하고 차분한": 1, "애교 많고 붙임성 있는": 3,
                    "활발하고 장난기 많은": 5, "독립적이고 의연한": 2,
                    "충성스럽고 보호 본능 강한": 3, "호기심 많고 탐험 좋아하는": 4},
    },
    {
        "id": "stranger_friendly", "section": 3,
        "label": "Q21. 낯선 사람에 대한 친화력 선호는?",
        "options": ["경계심 강했으면 (보호견 역할)", "약간 낯을 가리는 편",
                    "처음엔 낯가리지만 금방 친해지는", "누구에게나 친근한", "매우 사교적인"],
        "weights": {"경계심 강했으면 (보호견 역할)": 1, "약간 낯을 가리는 편": 2,
                    "처음엔 낯가리지만 금방 친해지는": 3, "누구에게나 친근한": 4, "매우 사교적인": 5},
    },
    {
        "id": "dog_friendly", "section": 3,
        "label": "Q22. 다른 강아지와 잘 지내는 것이 중요한가요?",
        "options": ["필수 (다견 가정)", "매우 중요", "있으면 좋겠음", "별로 중요하지 않음", "상관없음"],
        "weights": {"필수 (다견 가정)": 5, "매우 중요": 4, "있으면 좋겠음": 3,
                    "별로 중요하지 않음": 2, "상관없음": 2},
    },
    {
        "id": "energy_pref", "section": 3,
        "label": "Q23. 강아지의 에너지 레벨 선호도는?",
        "options": ["매우 차분 (실내 소파파)", "차분한 편", "보통",
                    "활동적 (매일 뛰어놀고 싶어함)", "매우 활동적 (스포츠 파트너)"],
        "weights": {"매우 차분 (실내 소파파)": 1, "차분한 편": 2, "보통": 3,
                    "활동적 (매일 뛰어놀고 싶어함)": 4, "매우 활동적 (스포츠 파트너)": 5},
    },
    {
        "id": "intelligence", "section": 3,
        "label": "Q24. 훈련 · 학습 능력이 뛰어난 강아지를 원하나요?",
        "options": ["별로 (개성 존중)", "약간", "보통 정도", "중요함 (명령 잘 따르길 원함)",
                    "매우 중요 (어질리티 · 특수훈련 목표)"],
        "weights": {"별로 (개성 존중)": 1, "약간": 2, "보통 정도": 3,
                    "중요함 (명령 잘 따르길 원함)": 4, "매우 중요 (어질리티 · 특수훈련 목표)": 5},
    },
    # ── 섹션 4: 실용 조건 (Q25~30) ────────────────────────────────────────────
    {
        "id": "budget_monthly", "section": 4,
        "label": "Q25. 월 반려동물 예산(사료·미용·병원 포함)은?",
        "options": ["5만원 미만", "5~10만원", "10~20만원", "20~35만원", "35~50만원", "50만원 이상"],
        "weights": {"5만원 미만": 1, "5~10만원": 1, "10~20만원": 2,
                    "20~35만원": 3, "35~50만원": 4, "50만원 이상": 5},
    },
    {
        "id": "vet_access", "section": 4,
        "label": "Q26. 주변 동물병원 접근성은?",
        "options": ["도보 5분 이내", "도보 10~15분", "차로 10분 이내", "차로 20~30분", "차로 30분 이상"],
        "weights": {"도보 5분 이내": 5, "도보 10~15분": 4, "차로 10분 이내": 3,
                    "차로 20~30분": 2, "차로 30분 이상": 1},
    },
    {
        "id": "age_pref", "section": 4,
        "label": "Q27. 입양하고 싶은 강아지 나이대는?",
        "options": ["어린 퍼피 (3개월 미만)", "퍼피 (3~6개월)", "어린 성견 (6개월~2년)",
                    "성견 (2~5년)", "시니어 (5~8년)", "노령견 (8년 이상)", "상관없음"],
        "weights": None, "direct": "age_pref",
    },
    {
        "id": "gender_pref", "section": 4,
        "label": "Q28. 선호하는 강아지 성별은?",
        "options": ["수컷", "암컷", "상관없음"],
        "weights": None, "direct": "gender_pref",
    },
    {
        "id": "neutered_pref", "section": 4,
        "label": "Q29. 중성화 여부에 대한 선호는?",
        "options": ["중성화 완료 강하게 선호", "중성화 완료면 좋겠음", "상관없음", "중성화 전 선호"],
        "weights": None, "direct": "neutered_pref",
    },
    {
        "id": "region_pref", "section": 4,
        "label": "Q30. 희망하는 강아지 보호 지역은?",
        "options": ["서울", "경기/인천", "부산/경남", "대구/경북",
                    "광주/전라", "대전/충청", "강원", "제주", "상관없음"],
        "weights": None, "direct": "region_pref",
    },
]

SECTION_QUESTIONS: dict = {}
for _i, _q in enumerate(QUESTIONS):
    SECTION_QUESTIONS.setdefault(_q["section"], []).append(_i)


# ══════════════════════════════════════════════════════════════════════════════
# 매칭 알고리즘
# ══════════════════════════════════════════════════════════════════════════════
def compute_breed_score(breed_row, answers, importance,
                        shed_w=1.0, bark_w=1.0, energy_w=1.0, social_w=1.0, train_w=1.0):
    def imp(q_id):
        return importance.get(q_id, 1.0)

    score, max_score = 0.0, 0.0

    def add(base_w, val, ideal, q_id=""):
        nonlocal score, max_score
        w = base_w * imp(q_id)
        max_score += w
        score += w * max(0.0, 1.0 - abs(float(val) - float(ideal)) / 4.0)

    energy       = float(breed_row.get("에너지_레벨", 3) or 3)
    walk_n       = answers.get("walk_time", 2)
    act_n        = answers.get("activity_pref", 2)
    trainability = float(breed_row.get("훈련_용이성", 3) or 3)
    exp_n        = answers.get("experience", 2)
    train_n      = answers.get("training", 2)
    bark         = float(breed_row.get("짖음_빈도", 3) or 3)
    noise_n      = answers.get("noise_tolerance", 3)
    shed         = float(breed_row.get("털_빠짐", 3) or 3)
    shed_n       = answers.get("shed_tolerance", 3)
    groom        = float(breed_row.get("그루밍_필요성", 3) or 3)
    groom_n      = answers.get("grooming", 2)
    apt          = float(breed_row.get("아파트_적합성", 3) or 3)
    housing_n    = answers.get("housing_type", 2)
    beginner     = float(breed_row.get("초보_적합성", 3) or 3)
    child_score  = float(breed_row.get("아이_친화력", 3) or 3)
    dog_fr       = float(breed_row.get("타견_친화력", 3) or 3)
    dog_need     = answers.get("dog_friendly", 2)
    energy_pref  = answers.get("energy_pref", 2)
    stranger     = float(breed_row.get("낯선사람_친화력", 3) or 3)
    stranger_p   = answers.get("stranger_friendly", 3)
    exercise     = float(breed_row.get("운동량", 3) or 3)

    add(15 * energy_w, energy,       (walk_n + act_n) / 2,  "walk_time")
    add(10 * train_w,  trainability, (exp_n + train_n) / 2, "training")
    add(10 * bark_w,   bark,         6 - noise_n,            "noise_tolerance")
    add(10 * shed_w,   shed,         6 - shed_n,             "shed_tolerance")
    add(8,             groom,        groom_n,                "grooming")
    add(12,            apt,          housing_n,              "housing_type")
    add(10 * train_w,  beginner,     exp_n,                  "experience")
    add(10 * energy_w, energy,       energy_pref,            "energy_pref")
    add(8  * energy_w, exercise,     walk_n,                 "walk_time")
    add(6,             stranger,     stranger_p,             "stranger_friendly")
    add(8  * social_w, dog_fr,       dog_need,               "dog_friendly")

    if answers.get("has_children"):
        add(15 * social_w, child_score, 5, "children")
    else:
        max_score += 15
        score     += 15 * 0.5

    if answers.get("allergy_sensitive"):
        al = answers.get("allergy_num", 3)
        if al == 1 and shed > 2:
            score -= 15 * imp("allergy")
    max_score += 5

    return round(min(100.0, (score / max_score) * 100), 1) if max_score > 0 else 50.0


def match_breeds(breeds_df, answers, importance, shed_w, bark_w, energy_w, social_w, train_w, top_n=5):
    rows = [(row, compute_breed_score(row, answers, importance, shed_w, bark_w, energy_w, social_w, train_w))
            for _, row in breeds_df.iterrows()]
    rows.sort(key=lambda x: x[1], reverse=True)
    return rows[:top_n]


def filter_korea_dogs(korea_df, breed_name, answers, top_n=3):
    df       = korea_df.copy()
    breed_df = df[df["품종"] == breed_name]
    if breed_df.empty:
        breed_df = df[df["품종"] == "믹스견"]

    gp = answers.get("gender_pref", "상관없음")
    if gp in ("수컷", "암컷"):
        tmp = breed_df[breed_df["성별"] == gp]
        if not tmp.empty:
            breed_df = tmp

    age_map = {
        "어린 퍼피 (3개월 미만)": (0, 3),  "퍼피 (3~6개월)": (3, 6),
        "어린 성견 (6개월~2년)":  (6, 24),  "성견 (2~5년)":   (24, 60),
        "시니어 (5~8년)":        (60, 96), "노령견 (8년 이상)": (96, 999),
    }
    ap = answers.get("age_pref", "상관없음")
    if ap in age_map:
        lo, hi = age_map[ap]
        try:
            tmp = breed_df[breed_df["나이(월)"].astype(float).between(lo, hi)]
            if not tmp.empty:
                breed_df = tmp
        except Exception:
            pass

    region_map = {
        "서울": ["서울"],       "경기/인천": ["경기", "인천"],
        "부산/경남": ["부산", "경남"], "대구/경북": ["대구", "경북"],
        "광주/전라": ["광주", "전북", "전남"], "대전/충청": ["대전", "충북", "충남", "세종"],
        "강원": ["강원"],       "제주": ["제주"],
    }
    rp = answers.get("region_pref", "상관없음")
    if rp in region_map:
        kws  = region_map[rp]
        mask = breed_df["지역"].apply(lambda x: any(k in str(x) for k in kws))
        tmp  = breed_df[mask]
        if not tmp.empty:
            breed_df = tmp

    return breed_df.head(top_n)


# ══════════════════════════════════════════════════════════════════════════════
# 자동 컬러 태그
# ══════════════════════════════════════════════════════════════════════════════
def make_tags(breed_row) -> list:
    def fv(k, default=3):
        try:
            return float(breed_row.get(k, default) or default)
        except Exception:
            return default

    apt   = fv("아파트_적합성")
    shed  = fv("털_빠짐", 5)
    child = fv("아이_친화력")
    beg   = fv("초보_적합성")
    bark  = fv("짖음_빈도", 5)
    enrg  = fv("에너지_레벨")
    dog_f = fv("타견_친화력")
    train = fv("훈련_용이성")
    size  = str(breed_row.get("크기_분류", ""))

    TAG = [
        (apt  >= 4,                           "#아파트OK",   "background:#E8F5E9;color:#2E7D32;border:1px solid #A5D6A7"),
        (shed <= 2,                           "#털빠짐적음", "background:#E3F2FD;color:#1565C0;border:1px solid #90CAF9"),
        (child >= 4,                          "#어린이친화", "background:#FCE4EC;color:#C62828;border:1px solid #F48FB1"),
        (beg  >= 4,                           "#초보자OK",   "background:#FFF8E1;color:#F57F17;border:1px solid #FFE082"),
        (bark <= 2,                           "#조용한편",   "background:#F3E5F5;color:#6A1B9A;border:1px solid #CE93D8"),
        (enrg <= 2,                           "#실내파",     "background:#FBE9E7;color:#BF360C;border:1px solid #FFAB91"),
        (enrg >= 4,                           "#활동파",     "background:#E8EAF6;color:#283593;border:1px solid #9FA8DA"),
        (dog_f >= 4,                          "#다견OK",     "background:#E0F7FA;color:#006064;border:1px solid #80DEEA"),
        (train >= 4,                          "#훈련쉬움",   "background:#F1F8E9;color:#33691E;border:1px solid #C5E1A5"),
        (shed <= 1,                           "#저알레르기", "background:#EDE7F6;color:#4527A0;border:1px solid #B39DDB"),
        ("대형" in size or "초대형" in size,  "#대형견",    "background:#EFEBE9;color:#4E342E;border:1px solid #BCAAA4"),
        ("소형" in size or "토이" in size,    "#소형견",    "background:#FFF3E0;color:#E65100;border:1px solid #FFCC80"),
    ]
    return [(name, sty) for cond, name, sty in TAG if cond][:6]


# ══════════════════════════════════════════════════════════════════════════════
# Claude AI 추천 이유
# ══════════════════════════════════════════════════════════════════════════════
def get_ai_reason(breed_name, score, answers, importance, breed_row):
    imp_qs  = [qid for qid, v in importance.items() if v >= 2.0]
    imp_str = ", ".join(imp_qs) if imp_qs else "없음"
    try:
        prompt = (
            f"반려견 매칭 플랫폼에서 사용자의 설문 결과를 분석했습니다.\n"
            f"추천 품종: '{breed_name}' (매칭 점수 {score}%)\n\n"
            f"[품종 특성]\n"
            f"- 에너지: {breed_row.get('에너지_레벨','?')}/5, 훈련: {breed_row.get('훈련_용이성','?')}/5\n"
            f"- 아파트 적합: {breed_row.get('아파트_적합성','?')}/5, 아이 친화: {breed_row.get('아이_친화력','?')}/5\n"
            f"- 털빠짐: {breed_row.get('털_빠짐','?')}/5, 짖음: {breed_row.get('짖음_빈도','?')}/5\n"
            f"- 기질: {breed_row.get('기질','?')}\n\n"
            f"[사용자 주요 답변]\n"
            f"- 주거: {answers.get('housing_type','?')}, 산책: {answers.get('walk_time','?')}\n"
            f"- 경험: {answers.get('experience','?')}, 활동성: {answers.get('activity_pref','?')}\n"
            f"- 어린아이: {'있음' if answers.get('has_children') else '없음'}\n"
            f"- 사용자가 중요하게 표시한 항목: {imp_str}\n\n"
            f"이 품종이 왜 이 사용자에게 맞는지 따뜻하고 친근한 말투로 3~4문장 설명해주세요. "
            f"한국어, 이모지 2~3개, 중요 항목도 언급해주세요."
        )
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Content-Type": "application/json"},
            json={"model": "claude-sonnet-4-20250514", "max_tokens": 350,
                  "messages": [{"role": "user", "content": prompt}]},
            timeout=15,
        )
        data = resp.json()
        text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
        return text.strip() or "AI 분석을 불러오지 못했습니다."
    except Exception as e:
        return f"AI 추천 이유를 불러오지 못했습니다. ({e})"


# ══════════════════════════════════════════════════════════════════════════════
# 이미지 렌더링 헬퍼 — 고정 비율 + object-fit:cover  (수정사항 ③)
# ══════════════════════════════════════════════════════════════════════════════
def render_fixed_image(img_path, height_px=200, fallback_emoji="🐾"):
    """항상 동일한 높이의 박스에 이미지를 채워 보여준다."""
    if img_path and os.path.exists(img_path):
        import base64
        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        ext = Path(img_path).suffix.lstrip(".")
        mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
        st.markdown(
            f'<div style="width:100%;height:{height_px}px;border-radius:12px;overflow:hidden;">'
            f'<img src="data:{mime};base64,{b64}" '
            f'style="width:100%;height:100%;object-fit:cover;border-radius:12px;" />'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div style="width:100%;height:{height_px}px;border-radius:12px;'
            f'background:#F5EDE8;display:flex;align-items:center;'
            f'justify-content:center;font-size:52px;">{fallback_emoji}</div>',
            unsafe_allow_html=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
# 위시리스트 강아지 상세 정보 화면  (수정사항 ⑤)
# ══════════════════════════════════════════════════════════════════════════════
def render_wish_detail(dog_id: str, korea_df, breeds_df):
    """korea_df + breeds_df를 조인해 강아지 상세 정보를 렌더링."""
    dog_rows = korea_df[korea_df["아이디"] == dog_id]
    if dog_rows.empty:
        st.error("강아지 정보를 찾을 수 없습니다.")
        return
    dog = dog_rows.iloc[0]
    breed_name = str(dog.get("품종", ""))

    breed_rows = breeds_df[breeds_df["품종명"] == breed_name]
    breed_info = breed_rows.iloc[0] if not breed_rows.empty else pd.Series()

    # 상단 뒤로 가기
    if st.button("← 매칭 결과로 돌아가기", key="back_from_detail"):
        st.session_state.match_step = "result"
        st.session_state.wish_detail_dog_id = None
        st.rerun()

    # ── 강아지 기본 정보 ──────────────────────────────────────────────────────
    img_path = get_dog_image_path(dog_id)
    col_photo, col_basic = st.columns([1, 2])

    with col_photo:
        render_fixed_image(img_path, height_px=280)

    with col_basic:
        try:
            age_m   = int(float(dog.get("나이(월)", 0)))
            age_str = f"{age_m // 12}살 {age_m % 12}개월" if age_m >= 12 else f"{age_m}개월"
        except Exception:
            age_str = "?"

        def star(val, max_v=5):
            try:
                n = int(float(val))
            except Exception:
                n = 0
            return "⭐" * n + "☆" * (max_v - n)

        vacc   = "✅ 완료" if str(dog.get("예방접종", "")).strip() == "완료" else "⬜ 미완료"
        deworm = "✅ 완료" if str(dog.get("구충여부", "")).strip() == "완료" else "⬜ 미완료"
        neuter = "✅ 완료" if str(dog.get("중성화", "")).strip() == "완료" else "⬜ 미완료"

        colors = [c for c in [dog.get("색상1"), dog.get("색상2"), dog.get("색상3")] if c and str(c) != "nan"]
        color_str = " / ".join(colors) if colors else "정보 없음"

        st.markdown(
            f'<div style="font-family:\'Gowun Batang\',serif;font-size:32px;font-weight:700;'
            f'color:#3D2B1F;margin-bottom:8px;">🐾 {dog.get("이름", "?")}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="font-size:18px;color:#7BAE8A;font-weight:600;margin-bottom:16px;">'
            f'{breed_name} · {age_str} · {dog.get("성별","?")} · {dog.get("지역","?")}</div>',
            unsafe_allow_html=True,
        )

        # 수치 격자
        st.markdown(
            f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:14px">'
            f'<div style="background:#F5EDE8;border-radius:10px;padding:10px;text-align:center">'
            f'<div style="font-size:13px;color:#A08070">건강 상태</div>'
            f'<div style="font-size:16px;font-weight:700;color:#3D2B1F">{star(dog.get("건강 상태",3))}</div></div>'
            f'<div style="background:#F5EDE8;border-radius:10px;padding:10px;text-align:center">'
            f'<div style="font-size:13px;color:#A08070">사회성</div>'
            f'<div style="font-size:16px;font-weight:700;color:#3D2B1F">{star(dog.get("사회도",3))}</div></div>'
            f'<div style="background:#F5EDE8;border-radius:10px;padding:10px;text-align:center">'
            f'<div style="font-size:13px;color:#A08070">친화도</div>'
            f'<div style="font-size:16px;font-weight:700;color:#3D2B1F">{star(dog.get("친화도",3))}</div></div>'
            f'<div style="background:#F5EDE8;border-radius:10px;padding:10px;text-align:center">'
            f'<div style="font-size:13px;color:#A08070">활동성</div>'
            f'<div style="font-size:16px;font-weight:700;color:#3D2B1F">{star(dog.get("활동성",3))}</div></div>'
            f'<div style="background:#E8F5E9;border-radius:10px;padding:10px;text-align:center">'
            f'<div style="font-size:13px;color:#A08070">예방접종</div>'
            f'<div style="font-size:14px;font-weight:700;color:#2E7D32">{vacc}</div></div>'
            f'<div style="background:#E8F5E9;border-radius:10px;padding:10px;text-align:center">'
            f'<div style="font-size:13px;color:#A08070">중성화</div>'
            f'<div style="font-size:14px;font-weight:700;color:#2E7D32">{neuter}</div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div style="font-size:15px;color:#5C4535;line-height:2">'
            f'📏 <b>크기:</b> {dog.get("크기","?")} &nbsp;|&nbsp; '
            f'✂️ <b>털 길이:</b> {dog.get("털길이","?")} &nbsp;|&nbsp; '
            f'🎨 <b>색상:</b> {color_str} &nbsp;|&nbsp; '
            f'💉 <b>구충:</b> {deworm}'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── 상세 설명 ─────────────────────────────────────────────────────────────
    st.markdown("---")
    if dog.get("상세설명"):
        st.markdown(
            f'<div style="background:#FDFAF8;border-radius:14px;padding:16px 20px;'
            f'font-size:17px;color:#3D2B1F;line-height:1.9;border:1px solid #F0E4DC">'
            f'📝 <b>상세 설명</b><br><br>{dog["상세설명"]}</div>',
            unsafe_allow_html=True,
        )

    # ── 품종 정보 (join) ──────────────────────────────────────────────────────
    if not breed_info.empty:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f'<div style="font-size:22px;font-weight:700;color:#3D2B1F;margin-bottom:14px">'
            f'🐕 {breed_name} 품종 가이드</div>',
            unsafe_allow_html=True,
        )

        def bv(k):
            try:
                return int(float(breed_info.get(k, 0) or 0))
            except Exception:
                return 0

        def bar(val, max_v=5, color="#E8A598"):
            pct = int(val / max_v * 100)
            return (
                f'<div style="background:#F0E4DC;border-radius:6px;height:8px;margin-top:4px">'
                f'<div style="background:{color};border-radius:6px;height:8px;width:{pct}%"></div>'
                f'</div>'
            )

        metrics = [
            ("⚡ 에너지 레벨",    bv("에너지_레벨"),    "#E8A598"),
            ("🎓 훈련 용이성",    bv("훈련_용이성"),    "#7BAE8A"),
            ("🧹 털 빠짐",        bv("털_빠짐"),        "#90CAF9"),
            ("🔊 짖음 빈도",      bv("짖음_빈도"),      "#CE93D8"),
            ("🏢 아파트 적합성",  bv("아파트_적합성"), "#7BAE8A"),
            ("👶 아이 친화력",    bv("아이_친화력"),    "#F48FB1"),
            ("🐕 타견 친화력",    bv("타견_친화력"),    "#80DEEA"),
            ("🌿 초보자 적합성",  bv("초보_적합성"),   "#FFE082"),
        ]

        cols = st.columns(4)
        for idx, (label, val, color) in enumerate(metrics):
            with cols[idx % 4]:
                st.markdown(
                    f'<div style="background:white;border-radius:10px;padding:12px;'
                    f'border:1px solid #F0E4DC;margin-bottom:8px">'
                    f'<div style="font-size:14px;color:#5C4535;font-weight:600">{label}</div>'
                    f'<div style="font-size:22px;font-weight:700;color:#3D2B1F;margin:6px 0">'
                    f'{val}/5</div>'
                    f'{bar(val, color=color)}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        if breed_info.get("기질"):
            st.markdown(
                f'<div style="background:#F5F9F6;border-radius:12px;padding:14px 18px;'
                f'font-size:16px;color:#3D2B1F;border:1px solid #C8E6C9;margin-top:10px">'
                f'💡 <b>기질:</b> {breed_info["기질"]}</div>',
                unsafe_allow_html=True,
            )
        if breed_info.get("설명"):
            st.markdown(
                f'<div style="background:#FDFAF8;border-radius:12px;padding:14px 18px;'
                f'font-size:16px;color:#5C4535;border:1px solid #F0E4DC;margin-top:10px;line-height:1.8">'
                f'📖 {breed_info["설명"]}</div>',
                unsafe_allow_html=True,
            )

        # 체고·체중 요약
        wm_lo = breed_info.get("최소_체중_수컷", "?")
        wm_hi = breed_info.get("최대_체중_수컷", "?")
        wf_lo = breed_info.get("최소_체중_암컷", "?")
        wf_hi = breed_info.get("최대_체중_암컷", "?")
        life  = breed_info.get("기대_수명", "?")
        st.markdown(
            f'<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px">'
            f'<div style="background:#FFF8E1;border-radius:10px;padding:12px 18px;font-size:15px">'
            f'⚖️ <b>체중</b><br>수컷 {wm_lo}~{wm_hi}lbs<br>암컷 {wf_lo}~{wf_hi}lbs</div>'
            f'<div style="background:#E8F5E9;border-radius:10px;padding:12px 18px;font-size:15px">'
            f'📅 <b>기대 수명</b><br>{life}등급</div>'
            f'<div style="background:#E3F2FD;border-radius:10px;padding:12px 18px;font-size:15px">'
            f'🎨 <b>색상</b><br>{str(breed_info.get("색상","?"))[:30]}</div>'
            f'<div style="background:#F3E5F5;border-radius:10px;padding:12px 18px;font-size:15px">'
            f'✂️ <b>털 유형</b><br>{str(breed_info.get("털_유형","?"))[:20]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── 입양 안내 연동 버튼 ───────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(f"📖 {breed_name} 입양 안내 보기", use_container_width=True, type="primary"):
        st.session_state.recommended_breed = breed_name
        st.session_state.page = "guide"
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# CSS  (수정사항 ④ — 폰트 크기 전반 상향)
# ══════════════════════════════════════════════════════════════════════════════
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Batang&family=Noto+Sans+KR:wght@300;400;600;700&display=swap');

/* ── 기본 ─────────────────────────────────────────────────────────────────── */
.match-header {
  font-family:'Gowun Batang',serif; font-size:32px;
  font-weight:700; color:#3D2B1F; margin-bottom:8px;
}
.match-sub { font-size:17px; color:#7BAE8A; margin-bottom:22px; }

/* ── 섹션 스텝 ────────────────────────────────────────────────────────────── */
.step-progress { display:flex; gap:0; align-items:center; margin:16px 0 6px; width:100%; }
.step-dot {
  width:44px; height:44px; border-radius:50%;
  display:flex; align-items:center; justify-content:center;
  font-size:16px; font-weight:700; flex-shrink:0; transition:all 0.25s;
}
.step-dot.done    { background:#7BAE8A; color:white; }
.step-dot.current { background:#E8A598; color:white; box-shadow:0 0 0 4px #F2C4CE; }
.step-dot.future  { background:#F0E4DC; color:#A08070; }
.step-line        { flex:1; height:4px; border-radius:2px; background:#F0E4DC; }
.step-line.done   { background:#7BAE8A; }
.step-labels      { display:flex; justify-content:space-between; margin-bottom:18px; }
.step-lbl         { font-size:13px; color:#A08070; text-align:center; width:44px; flex-shrink:0; line-height:1.5; }
.step-lbl.current { color:#E8A598; font-weight:700; }
.step-lbl.done    { color:#7BAE8A; }

/* ── 질문 카드 ─────────────────────────────────────────────────────────────── */
.q-card {
  background:white; border-radius:16px; padding:22px 26px;
  border:1px solid #F0E4DC; margin-bottom:18px;
  box-shadow:0 2px 10px rgba(0,0,0,0.05);
}
/* 질문 텍스트 */
.q-card .q-label { font-size:20px; font-weight:700; color:#3D2B1F; margin-bottom:8px; }

/* 라디오 버튼 글자 크기 */
div[data-baseweb="radio"] label p,
div[data-baseweb="radio"] label span {
  font-size:16px !important;
}

/* 체크박스 글자 */
div[data-baseweb="checkbox"] label p,
div[data-baseweb="checkbox"] label span {
  font-size:15px !important;
}

/* caption / st.caption 크기 */
.stCaption p { font-size:14px !important; }

/* expander 제목 */
details summary p { font-size:18px !important; font-weight:600 !important; }

/* ── 결과 카드 ─────────────────────────────────────────────────────────────── */
.result-breed {
  font-family:'Gowun Batang',serif; font-size:28px;
  font-weight:700; color:#3D2B1F;
}
.result-score-badge {
  background:#E8A598; color:white; border-radius:20px;
  padding:6px 20px; font-size:18px; font-weight:700;
  display:inline-block; margin:10px 0;
}
.score-bar-track { background:#F0E4DC; border-radius:8px; height:14px; margin:8px 0; }
.score-bar-fill  { background:linear-gradient(90deg,#E8A598,#7BAE8A); border-radius:8px; height:14px; }

/* ── 컬러 태그 ────────────────────────────────────────────────────────────── */
.tag-row { display:flex; flex-wrap:wrap; gap:8px; margin:12px 0; }
.ctag    { border-radius:14px; padding:5px 14px; font-size:13px; font-weight:700; display:inline-block; }

/* ── AI 박스 ──────────────────────────────────────────────────────────────── */
.ai-box {
  background:linear-gradient(135deg,#FDE8E4,#F5F9F6);
  border-radius:14px; padding:18px 22px; font-size:16px;
  color:#3D2B1F; border:1px solid #F2C4CE;
  margin-top:12px; line-height:1.9;
}
.ai-label { font-size:14px; color:#7BAE8A; font-weight:700; margin-bottom:10px; }

/* ── 강아지 이름·정보 ─────────────────────────────────────────────────────── */
.dog-name-text {
  font-weight:700; font-size:18px; color:#3D2B1F;
  text-align:center; margin-top:12px;
}
.dog-info-text { font-size:15px; color:#7D5A50; text-align:center; margin-top:4px; line-height:1.7; }
.dog-desc-text { font-size:13px; color:#A08070; text-align:center; margin-top:8px; line-height:1.6; }

/* ── 품종 격자 정보 ───────────────────────────────────────────────────────── */
.breed-grid-cell {
  background:#F5EDE8; border-radius:10px; padding:12px;
  font-size:15px; color:#5C4535; line-height:1.6;
}

/* ── 위시리스트 ───────────────────────────────────────────────────────────── */
.wish-item {
  background:white; border-radius:12px; padding:12px 14px;
  border:1px solid #F0E4DC; margin-bottom:10px;
}
.wish-name { font-weight:700; color:#3D2B1F; font-size:16px; }
.wish-info { color:#7D5A50; font-size:14px; margin-top:3px; }

/* ── 전체 기본 폰트 오버라이드 ────────────────────────────────────────────── */
section[data-testid="stAppViewContainer"] {
  font-size: 16px;
}
.stMarkdown p { font-size:16px; line-height:1.7; }
.stInfo p, .stWarning p { font-size:15px; }
</style>
"""

def render_top_breeds(top_breeds, a, korea_df, numeric):
    st.markdown("---")
    st.markdown("### 🎯 추천 품종 Top 5")
    st.caption("사이드바 슬라이더로 조건을 바꾸면 순위가 실시간 재정렬됩니다 🩷")

    for rank, (breed_row, score) in enumerate(top_breeds, 1):
        breed_name = str(breed_row.get("품종명", "알 수 없음"))
        rank_icon  = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][rank - 1]

        with st.expander(f"{rank_icon} {breed_name} — {score}% 일치", expanded=(rank == 1)):

            col_img, col_info = st.columns([1, 2])

            # 품종 이미지 — 고정 높이 (수정사항 ③)
            with col_img:
                img_path = get_breed_image(breed_name)
                render_fixed_image(img_path, height_px=220)

            with col_info:
                st.markdown(f'<div class="result-breed">{breed_name}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="result-score-badge">{score}% 일치!</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="score-bar-track">'
                    f'<div class="score-bar-fill" style="width:{score}%"></div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                # 컬러 태그
                tags = make_tags(breed_row)
                if tags:
                    tags_html = (
                        '<div class="tag-row">'
                        + "".join(f'<span class="ctag" style="{sty}">{name}</span>'
                                  for name, sty in tags)
                        + '</div>'
                    )
                    st.markdown(tags_html, unsafe_allow_html=True)

                # 품종 격자
                def fstr(k, default="?"):
                    v = breed_row.get(k, default)
                    return str(v)[:25] if v else default

                st.markdown(
                    f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:10px 0">'
                    f'<div class="breed-grid-cell">📏 <b>크기</b><br>{fstr("크기_분류")}</div>'
                    f'<div class="breed-grid-cell">🏷 <b>견종 그룹</b><br>{fstr("견종_그룹")}</div>'
                    f'<div class="breed-grid-cell">🎨 <b>색상</b><br>{fstr("색상")}</div>'
                    f'<div class="breed-grid-cell">✂️ <b>털 유형</b><br>{fstr("털_유형")}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                # ① 입양 안내 버튼 (수정사항 ①)
                if st.button(f"📖 {breed_name} 입양 안내 보기",
                             key=f"guide_btn_{rank}", use_container_width=True):
                    st.session_state.recommended_breed = breed_name
                    st.session_state.page = "guide"
                    st.rerun()

            # 설명 & 기질
            if breed_row.get("설명"):
                st.markdown(
                    f'<div style="font-size:16px;color:#5C4535;margin:12px 0;line-height:1.8;'
                    f'background:#FDFAF8;border-radius:12px;padding:14px">'
                    f'📖 {breed_row["설명"]}</div>',
                    unsafe_allow_html=True,
                )
            if breed_row.get("기질"):
                st.markdown(
                    f'<div style="font-size:15px;color:#7BAE8A;margin-bottom:12px">'
                    f'💡 <b>기질:</b> {breed_row["기질"]}</div>',
                    unsafe_allow_html=True,
                )

            # AI 추천 이유
            ai_key = f"ai_reason_{rank}"
            if rank == 1:
                if ai_key not in st.session_state:
                    with st.spinner("🤖 AI가 매칭 이유를 분석 중..."):
                        st.session_state[ai_key] = get_ai_reason(
                            breed_name, score, a, st.session_state.match_importance, breed_row)
                st.markdown(
                    f'<div class="ai-box"><div class="ai-label">🤖 AI 추천 이유</div>'
                    f'{st.session_state[ai_key]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                if st.button(f"🤖 AI 추천 이유 보기", key=f"ai_btn_{rank}"):
                    with st.spinner("분석 중..."):
                        st.session_state[ai_key] = get_ai_reason(
                            breed_name, score, a, st.session_state.match_importance, breed_row)
                if ai_key in st.session_state:
                    st.markdown(
                        f'<div class="ai-box"><div class="ai-label">🤖 AI 추천 이유</div>'
                        f'{st.session_state[ai_key]}</div>',
                        unsafe_allow_html=True,
                    )

            st.markdown("---")

            # ── 보호견 섹션 ────────────────────────────────────────────────
            st.markdown(f"#### 🐾 입양 가능한 '{breed_name}' 보호견")
            adopt_dogs = filter_korea_dogs(korea_df, breed_name, numeric, top_n=3)
            if adopt_dogs.empty:
                st.info("현재 이 품종의 보호견이 없어 다른 친구들을 소개합니다.")
                adopt_dogs = korea_df.sample(min(3, len(korea_df)))

            # ② 항상 3열 고정 (수정사항 ②③)
            adopt_list = list(adopt_dogs.iterrows())
            cols = st.columns(3)

            for col_i in range(3):
                with cols[col_i]:
                    if col_i >= len(adopt_list):
                        # 빈 칸 — 아무것도 렌더하지 않음
                        continue

                    _, dog   = adopt_list[col_i]
                    dog_id   = str(dog.get("아이디", ""))
                    img_path = get_dog_image_path(dog_id)

                    # ③ 고정 높이 이미지
                    render_fixed_image(img_path, height_px=180)

                    try:
                        age_m   = int(float(dog.get("나이(월)", 0)))
                        age_str = (f"{age_m // 12}살 {age_m % 12}개월"
                                   if age_m >= 12 else f"{age_m}개월")
                    except Exception:
                        age_str = "?"
                    try:
                        health  = int(float(dog.get("건강 상태", 3)))
                        h_stars = "⭐" * health
                    except Exception:
                        h_stars = "⭐⭐⭐"

                    # ④ 강아지 이름 · 정보 폰트 크기 상향
                    st.markdown(
                        f'<div class="dog-name-text">{dog.get("이름","?")}</div>'
                        f'<div class="dog-info-text">'
                        f'{dog.get("품종","?")} · {age_str}<br>'
                        f'{dog.get("성별","?")} · {dog.get("지역","?")}<br>'
                        f'크기: {dog.get("크기","?")} | 건강 {h_stars}'
                        f'</div>'
                        f'<div class="dog-desc-text">{str(dog.get("상세설명",""))[:55]}...</div>',
                        unsafe_allow_html=True,
                    )

                    # ❤️ 위시리스트 버튼
                    in_wish    = any(w["id"] == dog_id for w in st.session_state.match_wishlist)
                    wish_label = "❤️ 관심 목록에 있음" if in_wish else "🤍 관심 목록 추가"
                    if st.button(wish_label, key=f"wish_{dog_id}_{rank}",
                                 use_container_width=True):
                        if in_wish:
                            st.session_state.match_wishlist = [
                                w for w in st.session_state.match_wishlist
                                if w["id"] != dog_id
                            ]
                        else:
                            st.session_state.match_wishlist.append({
                                "id":     dog_id,
                                "name":   str(dog.get("이름", "?")),
                                "breed":  str(dog.get("품종", "?")),
                                "region": str(dog.get("지역", "?")),
                            })
                        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# 메인 render
# ══════════════════════════════════════════════════════════════════════════════
def render():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # 세션 초기화
    defaults = {
        "match_step":          "survey",
        "match_section_idx":   0,
        "match_answers":       {},
        "match_importance":    {},
        "match_wishlist":      [],
        "wish_detail_dog_id":  None,   # ⑤ 위시리스트 상세 조회용
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    st.markdown('<div class="match-header">🔍 퍼펙트 매칭 🩷</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="match-sub">5개 섹션 · 30개 질문으로 당신에게 딱 맞는 반려견을 찾아드립니다</div>',
        unsafe_allow_html=True,
    )

    # ── 사이드바: 위시리스트 ──────────────────────────────────────────────────
    with st.sidebar:
        if st.session_state.match_wishlist:
            st.markdown("---")
            st.markdown("### ❤️ 관심 목록")
            for dog in st.session_state.match_wishlist:
                st.markdown(
                    f'<div class="wish-item">'
                    f'<div class="wish-name">🐾 {dog["name"]}</div>'
                    f'<div class="wish-info">{dog["breed"]} · {dog["region"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                # ⑤ 상세 보기 버튼
                if st.button("🔍 상세 보기", key=f"detail_btn_{dog['id']}"):
                    st.session_state.wish_detail_dog_id = dog["id"]
                    st.session_state.match_step = "wish_detail"
                    st.rerun()

            if st.button("🗑 목록 초기화", key="clear_wish"):
                st.session_state.match_wishlist = []
                st.session_state.wish_detail_dog_id = None
                st.rerun()

    # ════════════════════════════════════════════════════════════════════════
    # ⑤ 위시리스트 강아지 상세 화면
    # ════════════════════════════════════════════════════════════════════════
    if st.session_state.match_step == "wish_detail":
        try:
            breeds_df, korea_df = load_data()
        except Exception as e:
            st.error(f"데이터 파일을 불러오지 못했습니다: {e}")
            return
        dog_id = st.session_state.wish_detail_dog_id
        if dog_id:
            render_wish_detail(dog_id, korea_df, breeds_df)
        else:
            st.session_state.match_step = "result"
            st.rerun()
        return

    # ════════════════════════════════════════════════════════════════════════
    # 설문 화면
    # ════════════════════════════════════════════════════════════════════════
    if st.session_state.match_step == "survey":
        sec_idx = st.session_state.match_section_idx
        total_s = len(SECTIONS)

        # 섹션 스텝 진행바
        dots = ""
        for i, sec in enumerate(SECTIONS):
            icon = "✓" if i < sec_idx else str(i + 1)
            cls  = "done" if i < sec_idx else ("current" if i == sec_idx else "future")
            dots += f'<div class="step-dot {cls}">{icon}</div>'
            if i < total_s - 1:
                dots += f'<div class="step-line {"done" if i < sec_idx else ""}"></div>'

        label_parts = ""
        for i, sec in enumerate(SECTIONS):
            lcls = "done" if i < sec_idx else ("current" if i == sec_idx else "")
            emo  = sec.split()[0]
            txt  = sec.split(" ", 1)[1] if " " in sec else sec
            label_parts += f'<div class="step-lbl {lcls}">{emo}<br>{txt}</div>'

        st.markdown(
            f'<div class="step-progress">{dots}</div>'
            f'<div class="step-labels">{label_parts}</div>',
            unsafe_allow_html=True,
        )

        answered = len([q for q in QUESTIONS if q["id"] in st.session_state.match_answers])
        st.caption(f"📋 전체 진행률: {answered}/30 문항 완료  |  현재 섹션: **{SECTIONS[sec_idx]}** ({sec_idx+1}/{total_s})")
        st.markdown("---")

        # 현재 섹션 질문
        for qi in SECTION_QUESTIONS[sec_idx]:
            q    = QUESTIONS[qi]
            prev = st.session_state.match_answers.get(q["id"])
            opts = q["options"]
            idx  = opts.index(prev) if prev in opts else 0

            # q-card div 안에 label을 먼저 렌더하고 radio는 Streamlit 위젯으로
            st.markdown(
                f'<div class="q-card"><div class="q-label">{q["label"]}</div></div>',
                unsafe_allow_html=True,
            )
            # 실제 라디오 (label_visibility hidden으로 중복 방지)
            choice = st.radio(
                label=q["label"], options=opts, index=idx,
                key=f"q_{q['id']}", label_visibility="collapsed", horizontal=True,
            )
            st.session_state.match_answers[q["id"]] = choice

            is_imp = st.checkbox(
                "⭐ 이 항목이 나에게 특히 중요해요 (매칭 가중치 2배 적용)",
                value=st.session_state.match_importance.get(q["id"], False),
                key=f"imp_{q['id']}",
            )
            st.session_state.match_importance[q["id"]] = is_imp

            if q.get("flag") == "has_children":
                st.session_state.match_answers["has_children"] = choice != "없음"
            if q.get("flag") == "allergy_sensitive":
                st.session_state.match_answers["allergy_sensitive"] = "심함" in choice
                st.session_state.match_answers["allergy_num"] = (
                    1 if "심함" in choice else 2 if "약간" in choice else 3
                )

            if q.get("weights") and choice in q["weights"]:
                st.session_state.match_answers[q["id"] + "_w"] = q["weights"][choice]
            if q.get("direct"):
                st.session_state.match_answers[q["direct"]] = choice

            st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)

        # 섹션 이동 버튼
        st.markdown("")
        col_prev, col_mid, col_next = st.columns([1, 2, 1])
        with col_prev:
            if sec_idx > 0:
                if st.button("← 이전 섹션", use_container_width=True):
                    st.session_state.match_section_idx -= 1
                    st.rerun()
        with col_mid:
            if st.button("🔍 지금 바로 매칭 보기", use_container_width=True):
                st.session_state.match_step = "result"
                st.rerun()
        with col_next:
            if sec_idx < total_s - 1:
                if st.button("다음 섹션 →", use_container_width=True, type="primary"):
                    st.session_state.match_section_idx += 1
                    st.rerun()
            else:
                if st.button("✅ 설문 완료 & 결과 보기", use_container_width=True, type="primary"):
                    st.session_state.match_step = "result"
                    st.rerun()

    # ════════════════════════════════════════════════════════════════════════
    # 결과 화면
    # ════════════════════════════════════════════════════════════════════════
    elif st.session_state.match_step == "result":
        try:
            breeds_df, korea_df = load_data()
        except Exception as e:
            st.error(f"데이터 파일을 불러오지 못했습니다: {e}")
            return

        # 사이드바 필터
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 🎛 결과 조건 재조절")
            st.caption("슬라이더 조절 시 순위가 실시간 재정렬됩니다")
            shed_w   = st.slider("🧹 털 빠짐 민감도",         0.5, 3.0, 1.0, 0.5)
            bark_w   = st.slider("🔇 층간소음 민감도",         0.5, 3.0, 1.0, 0.5)
            energy_w = st.slider("⚡ 에너지 레벨 중요도",      0.5, 3.0, 1.0, 0.5)
            social_w = st.slider("👶 아이/타견 친화력 중요도",  0.5, 3.0, 1.0, 0.5)
            train_w  = st.slider("🎓 훈련 난이도 중요도",       0.5, 3.0, 1.0, 0.5)

        # 답변 수치 변환
        a  = st.session_state.match_answers
        importance_mul = {qid: 2.0 if v else 1.0
                          for qid, v in st.session_state.match_importance.items()}

        def _w(k, default=2):
            return a.get(k + "_w", default)

        numeric = {
            "housing_type":      _w("housing_type",      2),
            "walk_time":         _w("walk_time",          2),
            "activity_pref":     _w("activity_pref",      2),
            "experience":        _w("experience",         2),
            "training":          _w("training",           2),
            "noise_tolerance":   _w("noise_tolerance",    3),
            "shed_tolerance":    _w("shed_tolerance",     3),
            "grooming":          _w("grooming",           2),
            "allergy_num":        a.get("allergy_num",    3),
            "energy_pref":       _w("energy_pref",        2),
            "stranger_friendly": _w("stranger_friendly",  3),
            "dog_friendly":      _w("dog_friendly",       2),
            "has_children":       a.get("has_children",   False),
            "allergy_sensitive":  a.get("allergy_sensitive", False),
            "gender_pref":        a.get("gender_pref",   "상관없음"),
            "age_pref":           a.get("age_pref",      "상관없음"),
            "region_pref":        a.get("region_pref",   "상관없음"),
        }

        top_breeds = match_breeds(
            breeds_df, numeric, importance_mul,
            shed_w, bark_w, energy_w, social_w, train_w, top_n=5
        )
        st.session_state.top_breeds_result = top_breeds

        # 상단 버튼
        col_a, col_b = st.columns([1, 2])
        with col_a:
            if st.button("← 설문 다시 하기"):
                st.session_state.match_step = "survey"
                st.session_state.match_section_idx = 0
                for k in [k for k in st.session_state if k.startswith("ai_reason_")]:
                    del st.session_state[k]
                st.rerun()
        with col_b:
            answered  = len([q for q in QUESTIONS if q["id"] in a])
            imp_count = sum(1 for v in st.session_state.match_importance.values() if v)
            st.caption(f"📋 {answered}/30 문항 완료  |  ⭐ {imp_count}개 중요 항목 반영")

        incomplete = [SECTIONS[i] for i in range(len(SECTIONS))
                      if i > st.session_state.match_section_idx]
        if incomplete:
            st.info(f"💡 아직 답변하지 않은 섹션: **{', '.join(incomplete)}** — 완료하면 더 정확해집니다!")
                            
        if "top_breeds_result" in st.session_state:
            top_breeds = st.session_state.top_breeds_result
            # 추천 품종 Top 5
            render_top_breeds(top_breeds, a, korea_df, numeric)

        # 하단 CTA
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🐕 전체 반려견 리스트 보기", use_container_width=True):
                st.session_state.page = "dog_list"
                st.rerun()
        with col2:
            if st.button("📖 입양 안내 보기", use_container_width=True):
                st.session_state.page = "guide"
                st.rerun()