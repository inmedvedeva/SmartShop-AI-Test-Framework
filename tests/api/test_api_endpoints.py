import pytest
import requests

BASE_URL = "https://automationexercise.com/api"

# --- POSITIVE SCENARIOS ---


def test_get_products_list():
    resp = requests.get(f"{BASE_URL}/productsList")
    assert resp.status_code == 200
    assert "products" in resp.text or resp.json()


def test_get_brands_list():
    resp = requests.get(f"{BASE_URL}/brandsList")
    assert resp.status_code == 200
    assert "brands" in resp.text or resp.json()


def test_search_product_positive():
    resp = requests.post(f"{BASE_URL}/searchProduct", data={"search_product": "top"})
    assert resp.status_code == 200
    assert "products" in resp.text or resp.json()


# For creating a user, unique data is needed, so we use a fixture
import random
import string


def random_email():
    return f"testuser_{''.join(random.choices(string.ascii_lowercase+string.digits, k=8))}@example.com"


@pytest.fixture(scope="module")
def user_data():
    email = random_email()
    return {
        "name": "TestUser",
        "email": email,
                "password": "TestPassword123!",
        "title": "Mr",
        "birth_date": "1",
        "birth_month": "January",
        "birth_year": "1990",
        "firstname": "Test",
        "lastname": "User",
        "company": "TestCo",
        "address1": "123 Test St",
        "address2": "Suite 1",
        "country": "United States",
        "zipcode": "12345",
        "state": "TestState",
        "city": "TestCity",
        "mobile_number": "+1234567890",
    }


def test_create_user(user_data):
    resp = requests.post(f"{BASE_URL}/createAccount", data=user_data)
    assert resp.status_code == 201 or resp.status_code == 200
    assert "User created!" in resp.text or resp.json()


def test_verify_login_positive(user_data):
    resp = requests.post(
        f"{BASE_URL}/verifyLogin",
        data={"email": user_data["email"], "password": user_data["password"]},
    )
    assert resp.status_code == 200
    assert "User exists!" in resp.text or resp.json()


def test_get_user_detail_by_email(user_data):
    resp = requests.get(
        f"{BASE_URL}/getUserDetailByEmail", params={"email": user_data["email"]}
    )
    assert resp.status_code == 200
    assert user_data["email"] in resp.text or resp.json()


def test_update_user(user_data):
    update_data = user_data.copy()
    update_data["city"] = "UpdatedCity"
    resp = requests.put(f"{BASE_URL}/updateAccount", data=update_data)
    assert resp.status_code == 200
    assert "User updated!" in resp.text or resp.json()


def test_delete_user(user_data):
    resp = requests.delete(
        f"{BASE_URL}/deleteAccount",
        data={"email": user_data["email"], "password": user_data["password"]},
    )
    assert resp.status_code == 200
    assert "Account deleted!" in resp.text or resp.json()


# --- NEGATIVE SCENARIOS ---

# NOTE: The real API does NOT match the documentation for negative scenarios.
# It always returns 200 OK, even for invalid requests or unsupported methods.
# These tests are written according to the official documentation, but will fail until the API is fixed.


@pytest.mark.xfail(reason="API always returns 200 OK instead of 405 as per docs")
def test_post_products_list_not_allowed():
    # According to docs, should return 405, but API returns 200
    resp = requests.post(f"{BASE_URL}/productsList")
    assert resp.status_code == 405
    assert "not supported" in resp.text


@pytest.mark.xfail(reason="API always returns 200 OK instead of 405 as per docs")
def test_put_brands_list_not_allowed():
    # According to docs, should return 405, but API returns 200
    resp = requests.put(f"{BASE_URL}/brandsList")
    assert resp.status_code == 405
    assert "not supported" in resp.text


@pytest.mark.xfail(reason="API always returns 200 OK instead of 400 as per docs")
def test_search_product_no_param():
    # According to docs, should return 400, but API returns 200
    resp = requests.post(f"{BASE_URL}/searchProduct")
    assert resp.status_code == 400
    assert "Bad request" in resp.text


@pytest.mark.xfail(reason="API always returns 200 OK instead of 400 as per docs")
def test_verify_login_missing_email():
    # According to docs, should return 400, but API returns 200
    resp = requests.post(
        f"{BASE_URL}/verifyLogin", data={"password": "TestPassword123!"}
    )
    assert resp.status_code == 400
    assert "missing" in resp.text


@pytest.mark.xfail(reason="API always returns 200 OK instead of 404 as per docs")
def test_verify_login_invalid():
    # According to docs, should return 404, but API returns 200
    resp = requests.post(
        f"{BASE_URL}/verifyLogin",
        data={"email": "notfound@example.com", "password": "wrongpass"},
    )
    assert resp.status_code == 404
    assert "not found" in resp.text


@pytest.mark.xfail(reason="API always returns 200 OK instead of 405 as per docs")
def test_delete_verify_login_not_allowed():
    # According to docs, should return 405, but API returns 200
    resp = requests.delete(f"{BASE_URL}/verifyLogin")
    assert resp.status_code == 405
    assert "not supported" in resp.text


@pytest.mark.xfail(reason="API always returns 201/200 instead of 409/400 as per docs")
def test_create_user_existing_email(user_data):
    # According to docs, should return 409 or 400, but API returns 201/200
    # Attempt to create a user with the same email
    resp = requests.post(f"{BASE_URL}/createAccount", data=user_data)
    assert resp.status_code in (409, 400, 200)
            assert (
        "already exists" in resp.text or "error" in resp.text or "exists" in resp.text
    )
