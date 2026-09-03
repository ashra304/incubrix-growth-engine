#!/usr/bin/env python3
"""
Simple test runner for the IncuBrix Growth Engine project.
Runs test functions directly without requiring pytest.
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import all test modules
test_modules = [
    "tests.test_evidence",
    "tests.test_qualification",
    "tests.test_contact",
]

def run_tests():
    total = 0
    passed = 0
    failed = 0
    
    print("=" * 60)
    print("RUNNING TESTS")
    print("=" * 60)
    print()
    
    for module_name in test_modules:
        try:
            module = __import__(module_name, fromlist=[""])
            
            # Get all test functions
            test_functions = [
                (name, getattr(module, name))
                for name in dir(module)
                if name.startswith("test_") and callable(getattr(module, name))
            ]
            
            if test_functions:
                print(f"\n{module_name}:")
                print("-" * 60)
                
                for func_name, func in test_functions:
                    total += 1
                    try:
                        func()
                        passed += 1
                        print(f"  PASS: {func_name}")
                    except AssertionError as e:
                        failed += 1
                        print(f"  FAIL: {func_name}")
                        print(f"        {str(e)}")
                    except Exception as e:
                        failed += 1
                        print(f"  ERROR: {func_name}")
                        print(f"         {type(e).__name__}: {str(e)}")
        
        except ImportError as e:
            print(f"Failed to import {module_name}: {e}")
    
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total:  {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print()
    
    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
