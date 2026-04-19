import pandas as pd
import os as _os

_CSV_PATH = _os.path.join(_os.path.dirname(_os.path.dirname(__file__)), 'data', 'korea_dog_list_fixed.csv')


def load_dog_df():
    """CSV를 읽어 DataFrame으로 반환한다."""
    return pd.read_csv(_CSV_PATH)


def get_featured_dogs(df=None, n=3):
    """CSV에서 랜덤 n마리를 뽑아 카드 표시용 dict 리스트로 반환한다.

    반환 키: 이름, 품종, 나이, 성별, 지역, 크기
    """
    if df is None:
        df = load_dog_df()
    cols = ['이름', '품종', '나이(월)', '성별', '지역', '크기']
    sample = df[cols].sample(min(n, len(df))).copy()
    sample['나이'] = sample['나이(월)'].apply(
        lambda m: (f"{int(m) // 12}살" if int(m) >= 12 else f"{int(m)}개월") if pd.notna(m) else "나이 미상"
    )
    return sample.drop(columns=['나이(월)']).to_dict(orient='records')


def get_stats(df=None):
    """총 등록견 수 / 보호 지역 수 / 품종 수를 dict로 반환한다."""
    if df is None:
        df = load_dog_df()
    return {
        'total':   len(df),
        'regions': int(df['지역'].nunique()),
        'breeds':  int(df['품종'].nunique()),
    }


def get_region_stats(df=None, top_n=6):
    """지역별 마리수 상위 top_n을 [{'region': str, 'count': int}] 형태로 반환한다."""
    if df is None:
        df = load_dog_df()
    counts = df['지역'].value_counts(sort=True).head(top_n)  # 내림차순 정렬 보장
    return [{'region': str(k), 'count': int(v)} for k, v in counts.items()]
