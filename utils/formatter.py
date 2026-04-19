def get_activity_text(row):
    """에너지, 운동량, 장난기 데이터를 조합해 케어 방법 문장 생성"""
    
    # 1. 데이터 추출 (결측치 대비 기본값 3 설정)
    energy = float(row.get("에너지_레벨", 3) or 3)
    exercise = float(row.get("운동량", 3) or 3)
    playfulness = float(row.get("장난기", 3) or 3)
    
    # 2. 종합 활동 지수 계산 (가중치 부여 가능)
    # 운동량이 실제 산책 강도에 가장 큰 영향을 주므로 40%, 나머지는 30%씩 배분
    activity_index = (energy * 0.3) + (exercise * 0.4) + (playfulness * 0.3)
    
    # 3. 지수에 따른 맞춤형 케어 문장 반환
    if activity_index >= 4.2:
        return "매우 높음"
    if activity_index >= 3.3:
        return "높음"
    if activity_index >= 2.5:
        return "보통"
    return "낮음"

def get_care_instruction(row):
    """
    다양한 견종 특성을 조합하여 종합 케어 가이드 문장 생성
    참고: 그루밍_필요성, 털_빠짐 , 털_길이 , 털_유형, 침_흘림, 훈련_용이성
    """
    # 1. 데이터 추출 및 기본값 처리
    def gv(key, default=3): return float(row.get(key, default) or default)

    # 위생/미용 관련
    grooming, shed, drool = gv("그루밍_필요성"), gv("털_빠짐"), gv("침_흘림")
    coat_len = gv("털_길이")
    # 교육 관련
    trainability = gv("훈련_용이성")

    # 미용 및 위생 (털 빠짐, 그루밍, 침 흘림 등)
    hygiene_notes = []
    if shed >= 4: hygiene_notes.append("매일 브러싱 권장 (털 빠짐 매우 심함)")
    elif grooming >= 4: hygiene_notes.append("정기적인 전문 미용과 세심한 피모 관리가 필수입니다")
    
    if drool >= 4: hygiene_notes.append("위생 수건 상시 준비 (침 흘림 잦음)")

    # [B-1] 실제 길이에 따른 관리법 (cm 기준 예시)
    if coat_len >= 10.0: # 장모 (Long)
        hygiene_notes.append("엉킴 방지를 위한 매일 빗질 필요")
    elif coat_len >= 3.0: # 중단모 (Medium)
        hygiene_notes.append("주 2~3회 죽은 털 제거 브러싱")
    elif coat_len > 0: # 단모 (Short)
        if shed >= 4.0:
            hygiene_notes.append("실리콘 브러시로 짧은 털 관리")
        else:
            hygiene_notes.append("매우 간편한 털 관리 수준")
    
    hygiene_msg = f"{', '.join(hygiene_notes)}" if hygiene_notes else "기본적인 관리로 청결 유지 가능"
    
    # 훈련 및 교육 (훈련 용이성)
    if trainability >= 4.5:
        train_msg = "매우 뛰어난 습득력 (상급 훈련 가능)"
    elif trainability <= 2.5:
        train_msg = "독립적인 성향 (인내심 있는 반복 교육 필요)"
    else:
        train_msg = "원만한 학습 능력 (기본적인 사회화 교육 적합)"

    return f"{', '.join([hygiene_msg, train_msg])}"


def get_precaution_note(row):
    """
    다양한 환경 적합성 및 본능 데이터를 조합해 주의사항 문장 생성
    참고: 초보/아파트 적합성, 짖음, 보호/사냥 본능, 친화력(아이/개/타인), 기온 내성
    """
    def gv(key, default=3): return float(row.get(key, default) or default)
    notes = []

    # 1. 초보자 및 주거 환경 (초보_적합성, 아파트_적합성, 짖음_빈도)
    if gv("초보_적합성") <= 2:
        notes.append("초보자에게는 다소 어려운 견종일 수 있음")
    
    if gv("아파트_적합성") <= 2 or gv("짖음_빈도") >= 4:
        notes.append("아파트 등 공동주택에서는 소음 관리 및 헛짖음 교육 필수")

    # 2. 본능 및 친화력 (보호/사냥 본능, 아이/타견/낯선사람 친화력)
    # 아이 친화력이 낮거나 보호/사냥 본능이 강한 경우
    if gv("아이_친화력") <= 2:
        notes.append("어린아이와의 합사 시 주의 및 감독 필요")
    
    if gv("보호_본능") >= 4 or gv("낯선사람_친화력") <= 2:
        notes.append("경계심이 강해 외부인 방문 시 주의가 필요")

    if gv("사냥_본능") >= 4 or gv("타견_친화력") <= 2:
        notes.append("산책 시 돌발행동이나 다른 개와의 마찰 주의")

    # 3. 환경 내성 (더위/추위 내성)
    if gv("더위_내성") <= 2:
        notes.append("더위에 취약하므로 여름철 실내 온도 관리 필수")
    if gv("추위_내성") <= 2:
        notes.append("추위에 민감하므로 겨울철 방한 용품 필요")

    # 4. 최종 결과 반환
    if not notes:
        return "특별한 주의사항보다는 꾸준한 사회화 교육을 권장합니다."
    
    # 가독성을 위해 불렛 포인트나 구분자로 연결
    return ", ".join(notes)

def build_display_db(df):
    """CSV 데이터를 영현님이 원하는 BREED_DB 형식으로 변환"""
    display_db = {}
    for _, row in df.iterrows():
        breed = row.get("품종명", "알 수 없음")
        display_db[breed] = {
            'activity': get_activity_text(row),
            'care': get_care_instruction(row),
            'note': get_precaution_note(row)
        }
    return display_db
