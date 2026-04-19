import sys
import os
import pytest
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


@pytest.fixture(scope="session")
def sample_df():
    return pd.DataFrame({
        '이름':    ['바둑이', '코코', '하루'],
        '품종':    ['믹스', '포메', '말티즈'],
        '나이(월)': [3, 14, 8],
        '성별':    ['수컷', '암컷', '수컷'],
        '지역':    ['서울', '부산', '서울'],
        '크기':    ['소형', '소형', '중형'],
    })
