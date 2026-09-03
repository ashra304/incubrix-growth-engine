#!/usr/bin/env python3
"""
Test the enhancements made to evidence detection.
Tests implicit commercial and IncuBrix need signals.
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.evidence import (
    detect_commercial_signal,
    detect_incubrix_need,
    extract_business_contact,
)

def test_implicit_commercial_signals():
    """Test that implicit commercial keywords are detected."""
    
    # Test course/coaching signals
    videos = [
        {
            "title": "My Online Course for Content Creators",
            "description": "I teach creators how to grow their audience through coaching and training programs.",
            "url": "https://youtube.com/watch?v=1",
        }
    ]
    
    signal, url = detect_commercial_signal(videos)
    assert signal is True, f"Expected True, got {signal} for course/coaching content"
    print("  PASS: Course/coaching signals detected")
    
    # Test service/consulting signals
    videos = [
        {
            "title": "Let Me Manage Your YouTube Channel",
            "description": "Professional consulting services for content strategy and channel optimization.",
            "url": "https://youtube.com/watch?v=2",
        }
    ]
    
    signal, url = detect_commercial_signal(videos)
    assert signal is True, f"Expected True, got {signal} for service/consulting content"
    print("  PASS: Service/consulting signals detected")
    
    # Test membership/subscription signals
    videos = [
        {
            "title": "Join My Exclusive Membership Community",
            "description": "Subscribe to my channel membership for exclusive content and perks.",
            "url": "https://youtube.com/watch?v=3",
        }
    ]
    
    signal, url = detect_commercial_signal(videos)
    assert signal is True, f"Expected True, got {signal} for membership/subscription content"
    print("  PASS: Membership/subscription signals detected")

def test_implicit_incubrix_need_signals():
    """Test that implicit IncuBrix need keywords are detected."""
    
    # Test batch/automation/scaling signals
    videos = [
        {
            "title": "How to Batch Record Your YouTube Videos",
            "description": "Learn to batch produce content for efficiency and consistency.",
            "url": "https://youtube.com/watch?v=a",
        },
        {
            "title": "Scaling My Creator Business",
            "description": "Managing growth and automation of my content production.",
            "url": "https://youtube.com/watch?v=b",
        },
        {
            "title": "Automating My Social Media Posting",
            "description": "Saving time with scheduling and productivity tools.",
            "url": "https://youtube.com/watch?v=c",
        }
    ]
    
    signal, url = detect_incubrix_need(videos)
    assert signal is True, f"Expected True, got {signal} for implicit need signals (3+ matches)"
    print("  PASS: Implicit IncuBrix need signals detected (batch/automation/scaling)")

def test_explicit_commercial_signals():
    """Test that explicit commercial keywords still work."""
    
    videos = [
        {
            "title": "Sponsored Video - My Favorite Product",
            "description": "This video is sponsored by XYZ company.",
            "url": "https://youtube.com/watch?v=x",
        }
    ]
    
    signal, url = detect_commercial_signal(videos)
    assert signal is True, f"Expected True, got {signal} for explicit sponsored content"
    print("  PASS: Explicit commercial signals still detected")

def test_explicit_incubrix_need_signals():
    """Test that explicit IncuBrix need keywords still work."""
    
    videos = [
        {
            "title": "My Video Editing Workflow",
            "description": "Using CapCut for professional editing.",
            "url": "https://youtube.com/watch?v=y",
        }
    ]
    
    signal, url = detect_incubrix_need(videos)
    assert signal is True, f"Expected True, got {signal} for explicit editing content"
    print("  PASS: Explicit IncuBrix need signals still detected")

def test_contact_extraction():
    """Test that contact extraction finds multiple types of contacts."""
    
    # Test email extraction
    contact_type, contact, url = extract_business_contact(
        description="Email me at business@example.com for inquiries.",
        profile_url="https://youtube.com/c/testchannel"
    )
    assert contact_type == "business_email", f"Expected business_email, got {contact_type}"
    assert contact == "business@example.com"
    print("  PASS: Email extraction works")
    
    # Test website extraction
    contact_type, contact, url = extract_business_contact(
        description="Visit my business website at https://mybusiness.com for more info.",
        profile_url="https://youtube.com/c/testchannel"
    )
    assert contact_type == "website", f"Expected website, got {contact_type}"
    assert contact is not None and "mybusiness.com" in contact
    print("  PASS: Website extraction works")
    
    # Test booking page extraction
    contact_type, contact, url = extract_business_contact(
        description="Book me for speaking engagements at https://calendly.com/speaker",
        profile_url="https://youtube.com/c/testchannel"
    )
    assert contact_type == "booking_page", f"Expected booking_page, got {contact_type}"
    assert contact is not None and "calendly" in contact.lower()
    print("  PASS: Booking page extraction works")

def run_enhancement_tests():
    """Run all enhancement tests."""
    
    print("=" * 60)
    print("TESTING EVIDENCE DETECTION ENHANCEMENTS")
    print("=" * 60)
    print()
    
    print("Testing Implicit Commercial Signals:")
    print("-" * 60)
    try:
        test_implicit_commercial_signals()
    except AssertionError as e:
        print(f"  FAIL: {e}")
        return False
    
    print()
    print("Testing Implicit IncuBrix Need Signals:")
    print("-" * 60)
    try:
        test_implicit_incubrix_need_signals()
    except AssertionError as e:
        print(f"  FAIL: {e}")
        return False
    
    print()
    print("Testing Explicit Signals Still Work:")
    print("-" * 60)
    try:
        test_explicit_commercial_signals()
        test_explicit_incubrix_need_signals()
    except AssertionError as e:
        print(f"  FAIL: {e}")
        return False
    
    print()
    print("Testing Contact Extraction:")
    print("-" * 60)
    try:
        test_contact_extraction()
    except AssertionError as e:
        print(f"  FAIL: {e}")
        return False
    
    print()
    print("=" * 60)
    print("ALL ENHANCEMENT TESTS PASSED!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = run_enhancement_tests()
    sys.exit(0 if success else 1)
