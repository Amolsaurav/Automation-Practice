import time
import requests
import pytest
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://automationexercise.com"

HTTP_SESSION = requests.Session()
HTTP_SESSION.mount(
    "https://",
    HTTPAdapter(
        max_retries=Retry(
            total=3,
            connect=3,
            read=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["DELETE", "GET", "POST", "PUT"],
        )
    ),
)

def _request_with_timeout(method, url, **kwargs):
    kwargs.setdefault("timeout", 30)
    return HTTP_SESSION.request(method, url, **kwargs)


requests.get = lambda url, **kwargs: _request_with_timeout("GET", url, **kwargs)
requests.post = lambda url, **kwargs: _request_with_timeout("POST", url, **kwargs)
requests.put = lambda url, **kwargs: _request_with_timeout("PUT", url, **kwargs)
requests.delete = lambda url, **kwargs: _request_with_timeout("DELETE", url, **kwargs)

def get_unique_email():
    return f"api_user_{int(time.time() * 1000)}@example.com"

def assert_api_status(response, expected_status):
    try:
        data = response.json()
        if "responseCode" in data:
            assert data["responseCode"] == expected_status, f"Expected internal responseCode {expected_status}, but got {data['responseCode']}. Body: {data}"
            return
    except Exception:
        pass
    assert response.status_code == expected_status, f"Expected HTTP status {expected_status}, but got {response.status_code}."


def test_get_all_products():
    res = requests.get(f"{BASE_URL}/api/productsList")
    assert_api_status(res, 200)
    data = res.json()
    assert "products" in data


def test_post_all_products():
    res = requests.post(f"{BASE_URL}/api/productsList")
    assert_api_status(res, 405)


def test_get_all_brands():
    res = requests.get(f"{BASE_URL}/api/brandsList")
    assert_api_status(res, 200)
    data = res.json()
    assert "brands" in data


def test_put_all_brands():
    res = requests.put(f"{BASE_URL}/api/brandsList")
    assert_api_status(res, 405)


def test_post_search_product():
    res = requests.post(f"{BASE_URL}/api/searchProduct", data={"search_product": "tshirt"})
    assert_api_status(res, 200)
    data = res.json()
    assert "products" in data


def test_post_search_product_missing_param():
    res = requests.post(f"{BASE_URL}/api/searchProduct")
    assert_api_status(res, 400)


def test_post_verify_login_valid_details():
    email = get_unique_email()
    register_payload = {
        "name": "API User",
        "email": email,
        "password": "ValidPass123!",
        "title": "Mr",
        "birth_date": "10",
        "birth_month": "May",
        "birth_year": "1990",
        "firstname": "John",
        "lastname": "Doe",
        "company": "API Corp",
        "address1": "123 API St",
        "address2": "Suite 5",
        "country": "United States",
        "zipcode": "10001",
        "state": "NY",
        "city": "New York",
        "mobile_number": "1234567890"
    }
    res_reg = requests.post(f"{BASE_URL}/api/createAccount", data=register_payload)
    assert_api_status(res_reg, 201)

    res = requests.post(f"{BASE_URL}/api/verifyLogin", data={"email": email, "password": "ValidPass123!"})
    assert_api_status(res, 200)


def test_post_verify_login_missing_email():
    res = requests.post(f"{BASE_URL}/api/verifyLogin", data={"password": "ValidPass123!"})
    assert_api_status(res, 400)


def test_delete_verify_login():
    res = requests.delete(f"{BASE_URL}/api/verifyLogin")
    assert_api_status(res, 405)


def test_post_verify_login_invalid_details():
    res = requests.post(f"{BASE_URL}/api/verifyLogin", data={"email": "non_existent_api_user@example.com", "password": "WrongPass123!"})
    assert_api_status(res, 404)


def test_create_and_delete_user_account():
    email = get_unique_email()
    register_payload = {
        "name": "API Register Delete",
        "email": email,
        "password": "ValidPass123!",
        "title": "Mr",
        "birth_date": "10",
        "birth_month": "May",
        "birth_year": "1990",
        "firstname": "John",
        "lastname": "Doe",
        "company": "API Corp",
        "address1": "123 API St",
        "address2": "Suite 5",
        "country": "United States",
        "zipcode": "10001",
        "state": "NY",
        "city": "New York",
        "mobile_number": "1234567890"
    }
    res_create = requests.post(f"{BASE_URL}/api/createAccount", data=register_payload)
    assert_api_status(res_create, 201)

    res_delete = requests.delete(f"{BASE_URL}/api/deleteAccount", data={"email": email, "password": "ValidPass123!"})
    assert_api_status(res_delete, 200)


def test_update_user_account():
    email = get_unique_email()
    register_payload = {
        "name": "API Register Update",
        "email": email,
        "password": "ValidPass123!",
        "title": "Mr",
        "birth_date": "10",
        "birth_month": "May",
        "birth_year": "1990",
        "firstname": "John",
        "lastname": "Doe",
        "company": "API Corp",
        "address1": "123 API St",
        "address2": "Suite 5",
        "country": "United States",
        "zipcode": "10001",
        "state": "NY",
        "city": "New York",
        "mobile_number": "1234567890"
    }
    res_create = requests.post(f"{BASE_URL}/api/createAccount", data=register_payload)
    assert_api_status(res_create, 201)

    update_payload = {**register_payload, "name": "API Updated Name"}
    res_update = requests.put(f"{BASE_URL}/api/updateAccount", data=update_payload)
    assert_api_status(res_update, 200)


def test_get_user_detail_by_email():
    email = get_unique_email()
    register_payload = {
        "name": "API Details User",
        "email": email,
        "password": "ValidPass123!",
        "title": "Mr",
        "birth_date": "10",
        "birth_month": "May",
        "birth_year": "1990",
        "firstname": "John",
        "lastname": "Doe",
        "company": "API Corp",
        "address1": "123 API St",
        "address2": "Suite 5",
        "country": "United States",
        "zipcode": "10001",
        "state": "NY",
        "city": "New York",
        "mobile_number": "1234567890"
    }
    res_create = requests.post(f"{BASE_URL}/api/createAccount", data=register_payload)
    assert_api_status(res_create, 201)

    res_get = requests.get(f"{BASE_URL}/api/getUserDetailByEmail", params={"email": email})
    assert_api_status(res_get, 200)
    data = res_get.json()
    assert "user" in data
    user_data = data["user"]
    assert user_data["email"] == email
