import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.data_loader import get_featured_dogs, get_stats, get_region_stats


def test_get_featured_dogs_returns_three():
    dogs = get_featured_dogs()
    assert len(dogs) == 3


def test_get_featured_dogs_has_required_keys():
    dogs = get_featured_dogs()
    required = {'이름', '품종', '나이', '성별', '지역', '크기'}
    for dog in dogs:
        assert required.issubset(dog.keys()), f"missing keys in {dog}"


def test_get_stats_has_required_keys():
    stats = get_stats()
    assert {'total', 'regions', 'breeds'}.issubset(stats.keys())


def test_get_stats_total_is_positive():
    stats = get_stats()
    assert stats['total'] > 0


def test_get_region_stats_returns_list_with_region_and_count():
    regions = get_region_stats()
    assert isinstance(regions, list)
    assert len(regions) > 0
    assert 'region' in regions[0]
    assert 'count' in regions[0]
