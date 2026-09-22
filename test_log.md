### Test Execution Summary

- **Total Tests:** 37
- **Passed:** 34
- **Failed:** 3
- **Skipped:** 0
- **Total Execution Time:** 507.65s (~8m 27s)

### Overview
The test suite includes both API and UI test cases. API tests executed quickly and passed without failures. All 3 failures occurred within the UI test execution suite (`chromium` browser context).

### Key Failures
1. **Contact Us Form:** Expected success message was empty after submitting the form.
2. **Product Search:** Searching for a non-existent product keyword (`no_such_product_999`) unexpectedly returned 13 product cards instead of 0.
3. **Recommended Items:** Clicking 'Add to Cart' on a recommended item on the home page did not successfully increment or populate the cart (cart count remained 0).