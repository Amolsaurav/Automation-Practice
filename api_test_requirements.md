# API Test Requirements

This file contains the API requirements for the Automation Exercise application. The project generator must use this file as the source of truth for backend request validation and status-code expectations.

## API requirements
1. Get All Products List
   - URL: https://automationexercise.com/api/productsList
   - Method: GET
   - Expected status: 200
   - Expected behavior: returns the full products list

2. POST To All Products List
   - URL: https://automationexercise.com/api/productsList
   - Method: POST
   - Expected status: 405
   - Expected behavior: method not supported

3. Get All Brands List
   - URL: https://automationexercise.com/api/brandsList
   - Method: GET
   - Expected status: 200
   - Expected behavior: returns all brands list

4. PUT To All Brands List
   - URL: https://automationexercise.com/api/brandsList
   - Method: PUT
   - Expected status: 405
   - Expected behavior: method not supported

5. POST To Search Product
   - URL: https://automationexercise.com/api/searchProduct
   - Method: POST
   - Parameter: search_product, for example top, tshirt, jean
   - Expected status: 200
   - Expected behavior: returns searched products list

6. POST To Search Product without search_product parameter
   - URL: https://automationexercise.com/api/searchProduct
   - Method: POST
   - Expected status: 400
   - Expected behavior: bad request because search_product is missing

7. POST To Verify Login with valid details
   - URL: https://automationexercise.com/api/verifyLogin
   - Method: POST
   - Parameters: email, password
   - Expected status: 200
   - Expected behavior: user exists

8. POST To Verify Login without email parameter
   - URL: https://automationexercise.com/api/verifyLogin
   - Method: POST
   - Parameter: password
   - Expected status: 400
   - Expected behavior: email or password missing

9. DELETE To Verify Login
   - URL: https://automationexercise.com/api/verifyLogin
   - Method: DELETE
   - Expected status: 405
   - Expected behavior: method not supported

10. POST To Verify Login with invalid details
   - URL: https://automationexercise.com/api/verifyLogin
   - Method: POST
   - Parameters: email, password with invalid values
   - Expected status: 404
   - Expected behavior: user not found

11. POST To Create/Register User Account
   - URL: https://automationexercise.com/api/createAccount
   - Method: POST
   - Parameters: name, email, password, title, birth_date, birth_month, birth_year, firstname, lastname, company, address1, address2, country, zipcode, state, city, mobile_number
   - Expected status: 201
   - Expected behavior: user created

12. DELETE METHOD To Delete User Account
   - URL: https://automationexercise.com/api/deleteAccount
   - Method: DELETE
   - Parameters: email, password
   - Expected status: 200
   - Expected behavior: account deleted

13. PUT METHOD To Update User Account
   - URL: https://automationexercise.com/api/updateAccount
   - Method: PUT
   - Parameters: name, email, password, title, birth_date, birth_month, birth_year, firstname, lastname, company, address1, address2, country, zipcode, state, city, mobile_number
   - Expected status: 200
   - Expected behavior: user updated

14. GET user account detail by email
   - URL: https://automationexercise.com/api/getUserDetailByEmail
   - Method: GET
   - Parameter: email
   - Expected status: 200
   - Expected behavior: returns user detail JSON

## API implementation expectations
- Each API case should be implemented as a request-based test under generated/tests/api/.
- Keep API-specific logic separate from UI logic.
- Validate both status code and response shape where relevant.
- Use requests-based assertions; do not mix UI Playwright logic into API tests.
- Reuse common helpers only when they are truly API-related.
