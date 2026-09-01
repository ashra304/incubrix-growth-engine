from src.evidence import extract_business_contact


# ---------------------------------------------------------
# Test 1: Normal business email
# ---------------------------------------------------------

description = """
Welcome to my channel!

For business inquiries: business@example.com

Follow me on YouTube for more videos.
"""

contact_type, contact, evidence_url = extract_business_contact(
    description=description,
    profile_url="https://www.youtube.com/channel/test",
)

assert contact_type == "business_email"
assert contact == "business@example.com"
assert evidence_url == "https://www.youtube.com/channel/test"


# ---------------------------------------------------------
# Test 2: Real-world trailing character problem
# ---------------------------------------------------------

description_with_trailing_character = """
Welcome to Technical Yogi!

For Business inquiries: teamyogiofficial@gmail.comI

Do not provide tech support over e-mail.
"""

contact_type, contact, evidence_url = extract_business_contact(
    description=description_with_trailing_character,
    profile_url="https://www.youtube.com/channel/technical-yogi",
)

assert contact_type == "business_email"
assert contact == "teamyogiofficial@gmail.com"
assert evidence_url == (
    "https://www.youtube.com/channel/technical-yogi"
)


print("Business contact extraction test OK")