from src.personalization import generate_personalization_hook


def test_commercial_and_need():

    result = generate_personalization_hook(
        creator_name="Technical Yogi",
        creator_segment="youtuber",
        commercial_signal=True,
        incubrix_need=True,
        active_30d=True,
        long_form_60d=True,
    )

    assert result is not None
    assert "Technical Yogi" in result
    assert "commercializing" in result
    assert "creator-business need" in result


def test_commercial_only():

    result = generate_personalization_hook(
        creator_name="Tech Creators",
        creator_segment="youtuber",
        commercial_signal=True,
        incubrix_need=False,
        active_30d=True,
        long_form_60d=False,
    )

    assert result is not None
    assert "Tech Creators" in result
    assert "commercial activity" in result


def test_need_only():

    result = generate_personalization_hook(
        creator_name="I-TECH CREATOR",
        creator_segment="youtuber",
        commercial_signal=False,
        incubrix_need=True,
        active_30d=True,
        long_form_60d=False,
    )

    assert result is not None
    assert "I-TECH CREATOR" in result
    assert "creator workflow" in result


def test_no_signals():

    result = generate_personalization_hook(
        creator_name="Technology Creators",
        creator_segment="youtuber",
        commercial_signal=False,
        incubrix_need=False,
        active_30d=False,
        long_form_60d=False,
    )

    assert result is not None
    assert "Technology Creators" in result


def test_empty_creator():

    result = generate_personalization_hook(
        creator_name="",
        creator_segment="youtuber",
        commercial_signal=True,
        incubrix_need=True,
        active_30d=True,
        long_form_60d=True,
    )

    assert result is None


print("Personalization test OK")