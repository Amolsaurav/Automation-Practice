# Automated Test Execution Summary

## Overview
- **Total Tests:** 37
- **Passed:** 34
- **Failed:** 3
- **Errors:** 0
- **Skipped:** 0
- **Pass Rate:** 91.9%
- **Total Duration:** 277.22 seconds

---

## ⚠️ Failure Analysis & Search Fix Locations
*(Failed tests listed first with human-readable reasons and exact file locations)*

### 1. Contact Us Form (Chromium)
- **Category:** UI Test
- **Status:** FAILED
- **Duration:** 33.184s
- **Failure Reason:** playwright._impl._errors.TimeoutError: Page.wait_for_selector: Timeout 30000ms exceeded.
- **Where to Search for Fixes:**
  - 📄 Test script: `generated/tests/ui/test_scenarios_1.py` (function `test_contact_us_form`)
- **Raw Failure Details:**
```text
playwright._impl._errors.TimeoutError: Page.wait_for_selector: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("text=submitted successfully") to be visible
```

### 2. Search Product (Chromium)
- **Category:** UI Test
- **Status:** FAILED
- **Duration:** 3.290s
- **Failure Reason:** Assertion Error: assert 34 == 0
- **Where to Search for Fixes:**
  - 📄 Test script: `generated/tests/ui/test_scenarios_1.py` (function `test_search_product`)
  - 📄 Page Object class: `generated/pages/products_page.py` (`ProductsPage`)
- **Raw Failure Details:**
```text
assert 34 == 0
 +  where 34 = get_product_cards_count()
 +    where get_product_cards_count = <generated.pages.products_page.ProductsPage object at 0x000001E06EF53B10>.get_product_cards_count
```

### 3. Remove Products from Cart (Chromium)
- **Category:** UI Test
- **Status:** FAILED
- **Duration:** 17.187s
- **Failure Reason:** Assertion Error: assert 0 == 2
- **Where to Search for Fixes:**
  - 📄 Test script: `generated/tests/ui/test_scenarios_2.py` (function `test_remove_products_from_cart`)
  - 📄 Page Object class: `generated/pages/cart_page.py` (`CartPage`)
- **Raw Failure Details:**
```text
assert 0 == 2
 +  where 0 = get_cart_items_count()
 +    where get_cart_items_count = <generated.pages.cart_page.CartPage object at 0x000001E0709BF130>.get_cart_items_count
```

---

## 📋 Detailed Test Case Results

### API Test Suite (13/13 Passed)

- ✅ **Get All Products**
  - **File:** `generated/tests/api/test_api_suite.py` (Function: `test_get_all_products`)
  - **Status:** PASSED (1.906s)

- ✅ **Post All Products**
  - **File:** `generated/tests/api/test_api_suite.py` (Function: `test_post_all_products`)
  - **Status:** PASSED (0.335s)

- ✅ **Get All Brands**
  - **File:** `generated/tests/api/test_api_suite.py` (Function: `test_get_all_brands`)
  - **Status:** PASSED (0.334s)

- ✅ **Put All Brands**
  - **File:** `generated/tests/api/test_api_suite.py` (Function: `test_put_all_brands`)
  - **Status:** PASSED (0.380s)

- ✅ **Post Search Product**
  - **File:** `generated/tests/api/test_api_suite.py` (Function: `test_post_search_product`)
  - **Status:** PASSED (0.510s)

- ✅ **Post Search Product Missing Param**
  - **File:** `generated/tests/api/test_api_suite.py` (Function: `test_post_search_product_missing_param`)
  - **Status:** PASSED (0.387s)

- ✅ **Post Verify Login Valid Details**
  - **File:** `generated/tests/api/test_api_suite.py` (Function: `test_post_verify_login_valid_details`)
  - **Status:** PASSED (0.930s)

- ✅ **Post Verify Login Missing Email**
  - **File:** `generated/tests/api/test_api_suite.py` (Function: `test_post_verify_login_missing_email`)
  - **Status:** PASSED (0.504s)

- ✅ **Delete Verify Login**
  - **File:** `generated/tests/api/test_api_suite.py` (Function: `test_delete_verify_login`)
  - **Status:** PASSED (0.325s)

- ✅ **Post Verify Login Invalid Details**
  - **File:** `generated/tests/api/test_api_suite.py` (Function: `test_post_verify_login_invalid_details`)
  - **Status:** PASSED (0.498s)

- ✅ **Create and Delete User Account**
  - **File:** `generated/tests/api/test_api_suite.py` (Function: `test_create_and_delete_user_account`)
  - **Status:** PASSED (0.966s)

- ✅ **Update User Account**
  - **File:** `generated/tests/api/test_api_suite.py` (Function: `test_update_user_account`)
  - **Status:** PASSED (0.933s)

- ✅ **Get User Detail by Email**
  - **File:** `generated/tests/api/test_api_suite.py` (Function: `test_get_user_detail_by_email`)
  - **Status:** PASSED (0.841s)

### UI Test Suite (21/24 Passed)

- ✅ **Register User Valid (Chromium)**
  - **File:** `generated/tests/ui/test_auth.py` (Function: `test_register_user_valid[chromium]`)
  - **Status:** PASSED (13.820s)

- ✅ **Register User Invalid and Missing Data (Chromium)**
  - **File:** `generated/tests/ui/test_auth.py` (Function: `test_register_user_invalid_and_missing_data[chromium]`)
  - **Status:** PASSED (10.214s)

- ✅ **Login User Valid (Chromium)**
  - **File:** `generated/tests/ui/test_auth.py` (Function: `test_login_user_valid[chromium]`)
  - **Status:** PASSED (8.387s)

- ✅ **Login User Invalid (Chromium)**
  - **File:** `generated/tests/ui/test_auth.py` (Function: `test_login_user_invalid[chromium]`)
  - **Status:** PASSED (4.027s)

- ✅ **Logout User (Chromium)**
  - **File:** `generated/tests/ui/test_auth.py` (Function: `test_logout_user[chromium]`)
  - **Status:** PASSED (7.263s)

- ❌ **Contact Us Form (Chromium)**
  - **File:** `generated/tests/ui/test_scenarios_1.py` (Function: `test_contact_us_form[chromium]`)
  - **Status:** FAILED (33.184s)
  - **Reason:** playwright._impl._errors.TimeoutError: Page.wait_for_selector: Timeout 30000ms exceeded.
  - **Fix Location:** `generated/tests/ui/test_scenarios_1.py`

- ✅ **Test Cases Page (Chromium)**
  - **File:** `generated/tests/ui/test_scenarios_1.py` (Function: `test_test_cases_page[chromium]`)
  - **Status:** PASSED (3.223s)

- ✅ **Products and Product Detail (Chromium)**
  - **File:** `generated/tests/ui/test_scenarios_1.py` (Function: `test_products_and_product_detail[chromium]`)
  - **Status:** PASSED (3.112s)

- ❌ **Search Product (Chromium)**
  - **File:** `generated/tests/ui/test_scenarios_1.py` (Function: `test_search_product[chromium]`)
  - **Status:** FAILED (3.290s)
  - **Reason:** Assertion Error: assert 34 == 0
  - **Fix Location:** `generated/tests/ui/test_scenarios_1.py`, `generated/pages/products_page.py`

- ✅ **Subscription (Chromium)**
  - **File:** `generated/tests/ui/test_scenarios_1.py` (Function: `test_subscription[chromium]`)
  - **Status:** PASSED (4.469s)

- ✅ **Cart Operations (Chromium)**
  - **File:** `generated/tests/ui/test_scenarios_1.py` (Function: `test_cart_operations[chromium]`)
  - **Status:** PASSED (8.300s)

- ✅ **Register While Checkout (Chromium)**
  - **File:** `generated/tests/ui/test_scenarios_2.py` (Function: `test_register_while_checkout[chromium]`)
  - **Status:** PASSED (28.357s)

- ✅ **Register Before Checkout (Chromium)**
  - **File:** `generated/tests/ui/test_scenarios_2.py` (Function: `test_register_before_checkout[chromium]`)
  - **Status:** PASSED (11.849s)

- ✅ **Login Before Checkout (Chromium)**
  - **File:** `generated/tests/ui/test_scenarios_2.py` (Function: `test_login_before_checkout[chromium]`)
  - **Status:** PASSED (15.752s)

- ✅ **Invalid Payment (Chromium)**
  - **File:** `generated/tests/ui/test_scenarios_2.py` (Function: `test_invalid_payment[chromium]`)
  - **Status:** PASSED (9.912s)

- ✅ **Invalid Checkout State (Chromium)**
  - **File:** `generated/tests/ui/test_scenarios_2.py` (Function: `test_invalid_checkout_state[chromium]`)
  - **Status:** PASSED (5.965s)

- ❌ **Remove Products from Cart (Chromium)**
  - **File:** `generated/tests/ui/test_scenarios_2.py` (Function: `test_remove_products_from_cart[chromium]`)
  - **Status:** FAILED (17.187s)
  - **Reason:** Assertion Error: assert 0 == 2
  - **Fix Location:** `generated/tests/ui/test_scenarios_2.py`, `generated/pages/cart_page.py`

- ✅ **Categories and Brands (Chromium)**
  - **File:** `generated/tests/ui/test_scenarios_2.py` (Function: `test_categories_and_brands[chromium]`)
  - **Status:** PASSED (6.860s)

- ✅ **Search Login and Cart Persistence (Chromium)**
  - **File:** `generated/tests/ui/test_scenarios_2.py` (Function: `test_search_login_and_cart_persistence[chromium]`)
  - **Status:** PASSED (13.831s)

- ✅ **Product Review (Chromium)**
  - **File:** `generated/tests/ui/test_scenarios_2.py` (Function: `test_product_review[chromium]`)
  - **Status:** PASSED (5.007s)

- ✅ **Recommended Items (Chromium)**
  - **File:** `generated/tests/ui/test_scenarios_2.py` (Function: `test_recommended_items[chromium]`)
  - **Status:** PASSED (6.344s)

- ✅ **Checkout Address Details (Chromium)**
  - **File:** `generated/tests/ui/test_scenarios_2.py` (Function: `test_checkout_address_details[chromium]`)
  - **Status:** PASSED (16.851s)

- ✅ **Download Invoice (Chromium)**
  - **File:** `generated/tests/ui/test_scenarios_2.py` (Function: `test_download_invoice[chromium]`)
  - **Status:** PASSED (24.321s)

- ✅ **Scroll Behavior (Chromium)**
  - **File:** `generated/tests/ui/test_scenarios_2.py` (Function: `test_scroll_behavior[chromium]`)
  - **Status:** PASSED (6.844s)

