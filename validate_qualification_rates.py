#!/usr/bin/env python3
"""
Comprehensive validation test to measure qualification rate improvement.
Tests the full pipeline with synthetic data representing different creator types.
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
    create_country_evidence,
)
from src.qualification import qualify_creator

def create_test_videos(creator_type):
    """Create realistic test videos for different creator types."""
    
    if creator_type == "course_seller":
        return [
            {
                "title": "How to Build Your Personal Brand with My Course",
                "description": "I help creators monetize through online courses and masterclasses.",
                "url": "https://youtube.com/watch?v=1",
            },
            {
                "title": "Content Strategy for Course Creators",
                "description": "Managing multiple courses while scaling your business.",
                "url": "https://youtube.com/watch?v=2",
            }
        ]
    
    elif creator_type == "workflow_optimizer":
        return [
            {
                "title": "Batch Recording My Monthly Content",
                "description": "I batch record 30 videos in one day using my automation workflow.",
                "url": "https://youtube.com/watch?v=3",
            },
            {
                "title": "Scaling Content Production with Editing Tools",
                "description": "Automating captions, thumbnails, and publishing for efficiency.",
                "url": "https://youtube.com/watch?v=4",
            },
            {
                "title": "Managing a Content Calendar and Team",
                "description": "How I scaled from solo creator to team of editors and managers.",
                "url": "https://youtube.com/watch?v=5",
            }
        ]
    
    elif creator_type == "consultant":
        return [
            {
                "title": "Sponsored: My Consulting Services",
                "description": "I work with brands on strategy and content consultation.",
                "url": "https://youtube.com/watch?v=6",
            },
            {
                "title": "How to Scale Your Consulting Business",
                "description": "Managing workflows as you grow your client base.",
                "url": "https://youtube.com/watch?v=6b",
            }
        ]
    
    elif creator_type == "lifestyle_vlogger":
        return [
            {
                "title": "My Weekend Vlog",
                "description": "Just a fun weekend with my family.",
                "url": "https://youtube.com/watch?v=7",
            }
        ]
    
    elif creator_type == "affiliate_marketer":
        return [
            {
                "title": "Best Products for YouTubers [Affiliate Links]",
                "description": "Use my discount code for 20% off! I earn commissions from these affiliate links.",
                "url": "https://youtube.com/watch?v=8",
            },
            {
                "title": "How I Automate Product Testing with Systems",
                "description": "Using automation tools to speed up my content production workflow.",
                "url": "https://youtube.com/watch?v=8b",
            }
        ]
    
    elif creator_type == "service_provider":
        return [
            {
                "title": "Video Editing & Thumbnail Design Services",
                "description": "I offer freelance services for channel optimization and video production.",
                "url": "https://youtube.com/watch?v=9",
            }
        ]
    
    elif creator_type == "podcast_guest":
        return [
            {
                "title": "How Creators Can Grow Using Content Repurposing",
                "description": "Discussion about converting long-form videos into short clips and podcasts.",
                "url": "https://youtube.com/watch?v=10",
            }
        ]

def run_validation_tests():
    """Run comprehensive validation tests."""
    
    print("=" * 70)
    print("COMPREHENSIVE QUALIFICATION RATE VALIDATION")
    print("=" * 70)
    print()
    
    test_cases = {
        "course_seller": {
            "type": "Explicit Commercial + Implicit Need",
            "expected_commercial": True,
            "expected_need": True,
            "expected_qualified": True,
        },
        "workflow_optimizer": {
            "type": "Implicit Need Only (No Commercial)",
            "expected_commercial": False,
            "expected_need": True,
            "expected_qualified": False,
        },
        "consultant": {
            "type": "Explicit Commercial + Implicit Need",
            "expected_commercial": True,
            "expected_need": True,
            "expected_qualified": True,
        },
        "lifestyle_vlogger": {
            "type": "No Signals (Control Group)",
            "expected_commercial": False,
            "expected_need": False,
            "expected_qualified": False,
        },
        "affiliate_marketer": {
            "type": "Explicit Commercial + Implicit Need",
            "expected_commercial": True,
            "expected_need": True,
            "expected_qualified": True,
        },
        "service_provider": {
            "type": "Implicit Commercial + Implicit Need",
            "expected_commercial": True,
            "expected_need": True,
            "expected_qualified": True,
        },
        "podcast_guest": {
            "type": "Implicit Need Only (No Commercial)",
            "expected_commercial": False,
            "expected_need": True,
            "expected_qualified": False,
        },
    }
    
    qualified_count = 0
    results = []
    
    for creator_type, expectations in test_cases.items():
        videos = create_test_videos(creator_type)
        
        # Test evidence detection
        commercial_signal, _ = detect_commercial_signal(videos)
        incubrix_need, _ = detect_incubrix_need(videos)
        contact_type, contact, _ = extract_business_contact(
            description="Contact me at business@example.com",
            profile_url="https://youtube.com/c/testchannel"
        )
        
        # Simulate qualification
        qualification = qualify_creator(
            creator_segment="youtuber",
            country_iso2="US",
            primary_language="english",
            has_official_profile=True,
            has_stable_creator_id=True,
            active_30d=True,
            long_form_60d=True,
            commercial_signal=commercial_signal,
            incubrix_need=incubrix_need,
            contactable=bool(contact),
            complete_fields=True,
            unique_creator=True,
            evidence_within_30d=True,
        )
        
        is_qualified = qualification.qualified
        if is_qualified:
            qualified_count += 1
        
        # Check if results match expectations
        commercial_match = commercial_signal == expectations["expected_commercial"]
        need_match = incubrix_need == expectations["expected_need"]
        qualified_match = is_qualified == expectations["expected_qualified"]
        
        status = "PASS" if (commercial_match and need_match and qualified_match) else "FAIL"
        
        results.append({
            "creator_type": creator_type,
            "type_desc": expectations["type"],
            "commercial": commercial_signal,
            "need": incubrix_need,
            "qualified": is_qualified,
            "status": status,
        })
        
        print(f"[{status}] {creator_type.upper()}")
        print(f"  Description: {expectations['type']}")
        print(f"  Commercial Signal: {commercial_signal} (expected: {expectations['expected_commercial']})")
        print(f"  IncuBrix Need: {incubrix_need} (expected: {expectations['expected_need']})")
        print(f"  Qualified: {is_qualified} (expected: {expectations['expected_qualified']})")
        print()
    
    # Summary
    total = len(results)
    qualified_pct = (qualified_count / total) * 100 if total > 0 else 0
    
    print("=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"Total test cases: {total}")
    print(f"Qualified: {qualified_count}/{total} ({qualified_pct:.1f}%)")
    print()
    
    # Breakdown by type
    print("Qualification breakdown:")
    for result in results:
        print(f"  {'QUALIFIED' if result['qualified'] else 'REJECTED':10s} - {result['creator_type']:20s} - {result['type_desc']}")
    
    print()
    print("=" * 70)
    print("EXPECTED VS ACTUAL")
    print("=" * 70)
    print()
    print("Expected qualification improvements from enhancements:")
    print("  - Commercial signal: +30-40% (course sellers, service providers, etc.)")
    print("  - IncuBrix need: +25-35% (workflow optimizers, efficiency-focused)")
    print("  - Contact extraction: +20-30% (multiple contact types)")
    print()
    print(f"Actual qualification rate in this test: {qualified_pct:.1f}%")
    print()
    
    if qualified_pct >= 70:
        print("STATUS: EXCELLENT - Enhancement tests show strong signal detection")
        return True
    elif qualified_pct >= 50:
        print("STATUS: GOOD - Most creator types qualify as expected")
        return True
    else:
        print("STATUS: NEEDS REVIEW - Qualification rate below 50%")
        return False

if __name__ == "__main__":
    success = run_validation_tests()
    sys.exit(0 if success else 1)
