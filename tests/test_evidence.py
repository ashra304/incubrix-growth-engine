from src.evidence import detect_incubrix_need


def test_incubrix_need():

    videos = [
        {
            "title": "How I Automate My Creator Workflow",
            "description": (
                "Managing content and scaling my creator business "
                "has become difficult."
            ),
            "url": "https://www.youtube.com/watch?v=need123",
        }
    ]

    need, evidence_url = detect_incubrix_need(videos)

    assert need is True
    assert evidence_url == (
        "https://www.youtube.com/watch?v=need123"
    )


def test_no_incubrix_need():

    videos = [
        {
            "title": "My Weekend Vlog",
            "description": (
                "Here is what I did this weekend."
            ),
            "url": "https://www.youtube.com/watch?v=normal123",
        }
    ]

    need, evidence_url = detect_incubrix_need(videos)

    assert need is False
    assert evidence_url is None


print("IncuBrix need test OK")