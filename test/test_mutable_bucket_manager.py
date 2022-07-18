import pytest
from hashindex.mutable_bucket_manager import MutableBucketManager
from hashindex.constants import HASH_MIN, HASH_MAX


@pytest.mark.parametrize(
    "keys,query,result", [
        ([1], 1, (None, None)),
        ([1, 2, 3], 2, (1, 3)),
        ([3, 2, 1], 2, (1, 3)),
        ([0, -20, -10], -10, (-20, 0)),
        ([HASH_MIN, 0, HASH_MAX], 0, (HASH_MIN, HASH_MAX)),
        ([HASH_MIN], HASH_MIN, (None, None)),
        ([HASH_MAX], HASH_MAX, (None, None))
    ]
)
def test_get_neighbors(keys, query, result):
    mb = MutableBucketManager()
    for i, key in enumerate(keys):
        mb[key] = i
    assert mb.get_neighbors(query) == result


@pytest.mark.parametrize(
    "keys,query,result", [
        ([1], 1, 1),
        ([1], 2, 1),
        ([1], HASH_MAX, 1),
        ([HASH_MIN], 1, HASH_MIN),
        ([HASH_MIN], HASH_MIN, HASH_MIN),
        ([HASH_MIN], HASH_MAX, HASH_MIN),
        ([1, 2], 1, 1),
        ([1, 2], 2, 2),
    ]
)
def test_get_bucket_key_for(keys, query, result):
    mb = MutableBucketManager()
    for i, key in enumerate(keys):
        mb[key] = i
    assert mb.get_bucket_key_for(query) == result
