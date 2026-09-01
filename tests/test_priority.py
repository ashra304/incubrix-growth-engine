from src.priority import calculate_priority


def test_priority_a():

    result = calculate_priority(
        qualified=True,
        commercial_signal=True,
        incubrix_need=True,
        contactable=True,
        active_30d=True,
        long_form_60d=True,
    )

    assert result.priority == "A"
    assert result.score == 100


def test_priority_b():

    result = calculate_priority(
        qualified=True,
        commercial_signal=True,
        incubrix_need=True,
        contactable=False,
        active_30d=True,
        long_form_60d=False,
    )

    assert result.priority == "B"
    assert result.score == 65


def test_priority_c():

    result = calculate_priority(
        qualified=True,
        commercial_signal=False,
        incubrix_need=False,
        contactable=True,
        active_30d=True,
        long_form_60d=False,
    )

    assert result.priority == "C"
    assert result.score == 30


def test_rejected_creator():

    result = calculate_priority(
        qualified=False,
        commercial_signal=True,
        incubrix_need=True,
        contactable=True,
        active_30d=True,
        long_form_60d=True,
    )

    assert result.priority == "REJECTED"
    assert result.score == 0


print("Priority test OK")