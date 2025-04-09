"""
Custom Unit Test Runner for LLM Logic

Usage:
    python test_llm_logic.py
"""

import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BACKEND_DIR = os.path.join(ROOT_DIR, 'backend')
sys.path.insert(0, BACKEND_DIR)

from services.llm_service import LLMService

sample_products = [
    {
        "id": "prod001",
        "name": "Test Shoe",
        "category": "Footwear",
        "price": 89.99,
        "brand": "TestBrand",
        "tags": ["running", "lightweight"],
        "rating": 4.5,
        "inventory": 10,
    },
    {
        "id": "prod002",
        "name": "Test Headphones",
        "category": "Electronics",
        "price": 199.99,
        "brand": "TestSound",
        "tags": ["audio", "wireless"],
        "rating": 4.9,
        "inventory": 5,
    },
    {
        "id": "prod003",
        "name": "Eco Bottle",
        "category": "Home",
        "price": 29.99,
        "brand": "EcoBrand",
        "tags": ["reusable", "hydration"],
        "rating": 4.6,
        "inventory": 50,
    },
    {
        "id": "prod004",
        "name": "Reusable Kitchen Towels",
        "category": "Home",
        "price": 19.99,
        "brand": "EcoBrand",
        "tags": ["reusable", "kitchen", "eco-friendly"],
        "rating": 4.4,
        "inventory": 30,
    },
]

def print_result(test_name, result, message=None):
    status = "PASSED" if result else "FAILED"
    print(f"{status} - {test_name}")
    if message and not result:
        print(f"  → {message}")

def test_filter_products_for_llm_logic():
    try:
        llm = LLMService()
        user_prefs = {
            "priceRange": "under50",
            "categories": ["Home"],
            "brands": []
        }
        browsing = [sample_products[2]]  
        result = llm._filter_products_for_llm(user_prefs, browsing, sample_products)

        if not result:
            return False, "No filtered products returned"

        # All should be under $50
        if any(p["price"] > 50 for p in result):
            return False, "Filtered products exceed price cap"

        return True, None
    except Exception as e:
        return False, str(e)

def test_get_products_by_tags():
    try:
        llm = LLMService()
        tag_list = ["wireless"]
        exclude_ids = set()
        result = llm._get_products_by_tags(tag_list, sample_products, price_cap=200, exclude_ids=exclude_ids)
        if len(result) != 1 or result[0]["id"] != "prod002":
            return False, "Expected only Test Headphones for tag 'wireless'"
        return True, None
    except Exception as e:
        return False, str(e)

def test_get_related_tags_from_llm():
    try:
        llm = LLMService()
        browsed_tags = ["hydration"]
        catalog_tags = {"reusable", "hydration", "eco", "wireless", "running"}
        tags = llm._get_related_tags_from_llm(browsed_tags, catalog_tags)
        if not isinstance(tags, list):
            return False, "Returned tags is not a list"
        return True, None
    except Exception as e:
        return False, f"LLM error or bad config: {str(e)}"

def main():
    print("\n" + "="*80)
    print(" Running LLM Internal Logic Tests")
    print("="*80)

    tests = [
        ("LLMService._filter_products_for_llm", test_filter_products_for_llm_logic),
        ("LLMService._get_products_by_tags", test_get_products_by_tags),
        ("LLMService._get_related_tags_from_llm", test_get_related_tags_from_llm), 
    ]

    passed = 0
    for name, func in tests:
        result, msg = func()
        print_result(name, result, msg)
        passed += int(result)

    print("\n" + "-"*80)
    print(f"Tests passed: {passed}/{len(tests)} ({(passed / len(tests)) * 100:.0f}%)")

    if passed == len(tests):
        print("\nAll LLM logic tests passed!")
    else:
        print("\nSome LLM tests failed. Check messages above for details.")

if __name__ == "__main__":
    main()