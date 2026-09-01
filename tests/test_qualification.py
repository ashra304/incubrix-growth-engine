from src.qualification import qualify_creator


def test_qualified_creator():

    result = qualify_creator(
        creator_segment="youtuber",
        country_iso2="US",
        primary_language="English",
        has_official_profile=True,
        has_stable_creator_id=True,
        active_30d=True,
        long_form_60d=False,
        commercial_signal=True,
        incubrix_need=True,
        contactable=True,
        complete_fields=True,
        unique_creator=True,
        evidence_within_30d=True,
    )

    assert result.qualified is True
    assert result.rejection_reasons == []


def test_rejected_creator():

    result = qualify_creator(
        creator_segment="agency",
        country_iso2="US",
        primary_language="English",
        has_official_profile=True,
        has_stable_creator_id=True,
        active_30d=True,
        long_form_60d=False,
        commercial_signal=True,
        incubrix_need=True,
        contactable=True,
        complete_fields=True,
        unique_creator=True,
        evidence_within_30d=True,
    )

    assert result.qualified is False
    assert "Not an approved creator segment" in result.rejection_reasons


print("Qualification test OK")