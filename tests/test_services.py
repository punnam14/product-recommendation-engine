#!/usr/bin/env python
"""
Custom Unit Test Runner for Service Layer

Usage:
    python test_services.py
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.services.product_service import ProductService
from backend.services.llm_service import LLMService

# Sample test data
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
]

def print_result(test_name, result, message=None):
    status = "PASSED" if result else "FAILED"
    print(f"{status} - {test_name}")
    if message and not result:
        print(f"  → {message}")

def test_get_product_by_id():
    try:
        ps = ProductService()
        ps.products = sample_products
        product = ps.get_product_by_id("prod001")
        return product["name"] == "Test Shoe", None
    except Exception as e:
        return False, str(e)

def test_get_products_by_category():
    try:
        ps = ProductService()
        ps.products = sample_products
        result = ps.get_products_by_category("Electronics")
        if len(result) != 1 or result[0]["id"] != "prod002":
            return False, "Unexpected result length or wrong product returned"
        return True, None
    except Exception as e:
        return False, str(e)

def test_filter_products_for_llm_basic():
    try:
        llm = LLMService()
        user_prefs = {"priceRange": "all", "categories": ["Electronics"], "brands": []}
        browsing = [sample_products[1]]
        result = llm._filter_products_for_llm(user_prefs, browsing, sample_products)
        if not isinstance(result, list):
            return False, "Result is not a list"
        if not all(p["price"] <= 200 for p in result):
            return False, "Some product prices are above expected cap"
        return True, None
    except Exception as e:
        return False, str(e)

def main():
    print("\n" + "="*80)
    print(" Running Service Layer Tests")
    print("="*80)

    results = [
        ("ProductService.get_product_by_id", *test_get_product_by_id()),
        ("ProductService.get_products_by_category", *test_get_products_by_category()),
        ("LLMService._filter_products_for_llm_basic", *test_filter_products_for_llm_basic()),
    ]

    passed = 0
    for name, result, message in results:
        print_result(name, result, message)
        passed += result

    print("\n" + "-"*80)
    print(f"Tests passed: {passed}/{len(results)} ({(passed/len(results)) * 100:.0f}%)")

    if passed == len(results):
        print("\nAll service-level tests passed!")
    else:
        print("\nSome service tests failed. Check messages above for more info.")

if __name__ == "__main__":
    main()