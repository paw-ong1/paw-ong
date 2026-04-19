from utils.data_loader import get_featured_dogs, get_stats, get_region_stats, load_dog_df


def test_get_featured_dogs_returns_three(sample_df):
    dogs = get_featured_dogs(df=sample_df)
    assert len(dogs) == 3


def test_get_featured_dogs_has_required_keys(sample_df):
    dogs = get_featured_dogs(df=sample_df)
    required = {'이름', '품종', '나이', '성별', '지역', '크기'}
    for dog in dogs:
        assert required.issubset(dog.keys()), f"missing keys in {dog}"


def test_get_stats_has_required_keys(sample_df):
    stats = get_stats(df=sample_df)
    assert {'total', 'regions', 'breeds'}.issubset(stats.keys())


def test_get_stats_total_is_positive(sample_df):
    stats = get_stats(df=sample_df)
    assert stats['total'] > 0


def test_get_region_stats_returns_list_with_region_and_count(sample_df):
    regions = get_region_stats(df=sample_df)
    assert isinstance(regions, list)
    assert len(regions) > 0
    assert 'region' in regions[0]
    assert 'count' in regions[0]


def test_load_dog_df_returns_nonempty_dataframe():
    df = load_dog_df()
    assert len(df) > 0
    expected_cols = {'이름', '품종', '나이(월)', '성별', '지역', '크기'}
    assert expected_cols.issubset(df.columns)
