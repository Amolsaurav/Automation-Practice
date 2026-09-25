# UI Test Requirements

This file is the source of truth for UI behavior. The generator must implement the journeys, test data, valid and invalid inputs, actions, and assertions described here. Do not invent a successful result when an invalid input is specified.

## Test data rules

- Use a unique email for every registration test, for example `ui_user_<timestamp>@example.com`.
- Use the same generated email and password throughout one test.
- Valid password: `ValidPass123!`.
- Invalid password: `WrongPass123!`.
- Valid search terms: `top`, `tshirt`, and `jean`.
- Invalid search term: a unique value such as `no_such_product_999`.
- Do not use or store a real user's password.
- Tests that create an account must clean it up through the UI or use a unique account so that reruns are independent.

## Authentication journeys

### 1. Register User - valid data

Precondition: the generated email does not already exist.

Steps:
1. Open `https://automationexercise.com`.
2. Click `Signup / Login`.
3. In the `New User Signup!` section, enter a valid name and unique email.
4. Click `Signup`.
5. Fill the account information with valid title, password, date of birth, first name, last name, company, address, country, state, city, zipcode, and mobile number.
6. Click `Create Account`.
7. Click `Continue`.

Assertions:
- The account-created confirmation is visible.
- The home page shows `Logged in as` and the registered name.

### 2. Register User - invalid and missing data

Run separate tests for each invalid condition. Navigate to `Signup / Login`, submit the affected form, and assert the real validation message or that the page refuses to continue.

Cases:
- Existing email: enter an email that is already registered, submit signup, and assert `Email Address already exist!`.
- Missing name: leave the name empty and assert browser or application validation.
- Invalid email: enter a malformed email such as `not-an-email` and assert email validation.
- Missing email: leave email empty and assert validation.
- Missing required account field: leave password or another required field empty and assert validation.
- Password mismatch, if a confirmation field exists: enter different values and assert the mismatch validation.

### 3. Login User - valid data

Precondition: a registered test account exists.

Steps:
1. Open the home page.
2. Click `Signup / Login`.
3. Enter the registered email and `ValidPass123!`.
4. Click `Login`.

Assertions:
- `Logged in as <name>` is visible.
- The user is not shown an error message.

### 4. Login User - invalid data

Run separate tests for invalid email, invalid password, and missing values.

Steps:
1. Open the home page and click `Signup / Login`.
2. Enter either an unregistered email, `WrongPass123!`, or leave one required field empty.
3. Click `Login`.

Assertions:
- For invalid credentials, `Your email or password is incorrect!` is visible.
- For missing or malformed values, browser or application validation is visible.
- `Logged in as` is not visible.

### 5. Logout User

Precondition: the user is logged in.

Steps:
1. Click `Logout`.

Assertions:
- The user is redirected to the login page.
- The authenticated navigation state is no longer visible.

## UI scenarios

For every scenario below, use the listed valid and invalid data where applicable. Each test must include the complete navigation sequence and at least one assertion beyond checking that a page loaded.

### 6. Contact Us Form

- Valid: open `Contact us`, enter name, valid email, subject, message, and upload a small text file if supported; submit and assert the success message.
- Invalid: submit with missing name, missing email, malformed email, or missing message; assert validation and remain on the form.

### 7. Test Cases page

- Click `Test Cases` from the home page and assert the test-case content is visible.
- Invalid navigation is not applicable; assert that no authentication is required.

### 8. Products and product detail

- Click `Products`, assert the products list and product cards are visible, open one product, and assert its name, category, price, availability, condition, and brand.
- Invalid: use a product detail URL only if it is returned by the application; assert an appropriate not-found or error response for an invalid product id.

### 9. Search Product

- Valid: open `Products`, enter `tshirt`, click `Search`, and assert every displayed result matches the search response or contains the search term.
- Invalid: search for `no_such_product_999` and assert an empty-result state or no matching product cards.
- Missing input: submit an empty search and assert the application handles it without a false positive.

### 10-11. Subscription

- Valid: enter a valid email in the home-page footer subscription field, submit, and assert `You have been successfully subscribed!`.
- Repeat the same flow from the Cart page.
- Invalid: submit an empty or malformed email and assert validation or that the success message is not shown.

### 12-13. Cart operations

- Valid: add two visible products, open `Cart`, assert both products, prices, quantities, and totals; increase one quantity and assert the updated quantity and total.
- Invalid: attempt to use an invalid quantity such as zero, a negative number, or non-numeric text if the UI permits editing; assert rejection or validation.

### 14-16. Checkout and order journeys

- Register while checkout: add a product, open Cart, click checkout, choose signup/login, register with unique valid data, return to checkout, enter valid payment data, place order, and assert order confirmation.
- Register before checkout: register first, add a product, open Cart, checkout, verify address and order details, place the order, and assert confirmation.
- Login before checkout: log in with valid credentials, add a product, checkout, verify address and order details, place the order, and assert confirmation.
- Invalid payment: leave card number, expiry, or CVC empty or malformed; assert validation and do not assert order success.
- Invalid checkout state: as a logged-out user, attempt checkout and assert that login or signup is required.

### 17. Remove Products From Cart

- Add at least two products, remove one, and assert it is absent while the other remains.
- Remove all products and assert the empty-cart state.

### 18-19. Categories and brands

- Valid: open a category or brand, assert the heading matches the selected value, and assert products are displayed.
- Invalid: use an unavailable category or brand only if the application exposes such navigation; assert the application does not show unrelated products as a successful result.

### 20. Search, login, and cart persistence

- Search for a valid product, add it to the cart, log in with valid credentials, return to Cart, and assert the selected product remains with the correct quantity.
- Invalid: search for a nonexistent product and assert it cannot be added.

### 21. Product review

- Valid: log in if required, open a product detail page, enter name, valid email, and review text, submit, and assert the review success message.
- Invalid: submit with missing name, malformed email, or empty review and assert validation.

### 22. Recommended items

- Scroll to recommended items, add one item, open Cart, and assert the recommended product is present.

### 23. Checkout address details

- Register with known address data, add a product, checkout, and assert delivery and billing address values match the registration data.

### 24. Download invoice

- Complete a valid order, click `Download Invoice`, assert a download event occurs, and assert the downloaded file is non-empty.

### 25-26. Scroll behavior

- Scroll to the page bottom and assert the footer is visible.
- For the arrow-button case, click the scroll-up arrow and assert the page returns near the top.
- For the no-arrow case, use supported page scrolling and assert the top content becomes visible.

## Implementation expectations

- Implement each journey as a page-object-based Playwright test under `generated/tests/ui/`.
- Keep page classes under `generated/pages/`; tests must call page-object methods instead of raw locators.
- Prefer accessible roles, labels, and stable attributes after inspecting the live page.
- Assert visible messages, URL/state changes, values, counts, downloads, and cart totals where relevant.
- Keep UI logic separate from API logic.
- Negative tests must prove that the invalid action was rejected; do not mark a test successful merely because no exception was raised.

## Acceptance criteria

- Every numbered scenario has a clear start state, action sequence, input data, and expected result.
- Valid and invalid paths are implemented as separate tests where their outcomes differ.
- Tests use independent data and can be rerun without relying on a previous test's browser state.