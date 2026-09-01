from src.lead_loader import _to_int


def test_to_int():
    assert _to_int("1000") == 1000
    assert _to_int("") is None
    assert _to_int(None) is None


print("Loader test OK")