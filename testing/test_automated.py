
import pytest
from fastapi.testclient import TestClient
from mock_main import app  # Replace with actual import once backend is ready

client = TestClient(app)

# -------------------- /pow --------------------

@pytest.mark.parametrize("base, exponent, expected", [
    (2, 3, 8),
    (5, 0, 1),
    (2, -1, 0.5)
])
def test_pow_valid(base, exponent, expected):
    response = client.post("/pow", json={"base": base, "exponent": exponent})
    assert response.status_code == 200
    assert response.json()["result"] == expected

def test_pow_invalid():
    response = client.post("/pow", json={"base": "a", "exponent": "b"})
    assert response.status_code == 422

# -------------------- /fibonacci --------------------

@pytest.mark.parametrize("n, expected", [
    (10, 55),
    (0, 0)
])
def test_fibonacci_valid(n, expected):
    response = client.get(f"/fibonacci?n={n}")
    assert response.status_code == 200
    assert response.json()["result"] == expected

def test_fibonacci_negative():
    response = client.get("/fibonacci?n=-1")
    assert response.status_code == 422

# -------------------- /factorial --------------------

@pytest.mark.parametrize("n, expected", [
    (5, 120),
    (0, 1)
])
def test_factorial_valid(n, expected):
    response = client.get(f"/factorial?n={n}")
    assert response.status_code == 200
    assert response.json()["result"] == expected

def test_factorial_negative():
    response = client.get("/factorial?n=-5")
    assert response.status_code == 422

# -------------------- /login --------------------

def test_login_valid():
    response = client.post("/login", json={"username": "user", "password": "pass123"})
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_invalid_password():
    response = client.post("/login", json={"username": "user", "password": "wrong"})
    assert response.status_code == 401

def test_login_missing_field():
    response = client.post("/login", json={"username": "user"})
    assert response.status_code == 422


# -------------------- Authenticated /pow --------------------

def test_pow_with_valid_token():
    headers = {"Authorization": "Bearer valid_token"}
    response = client.post("/pow", json={"base": 2, "exponent": 2}, headers=headers)
    assert response.status_code == 200
    assert response.json()["result"] == 4.0

def test_pow_with_invalid_token():
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.post("/pow", json={"base": 2, "exponent": 2}, headers=headers)
    assert response.status_code == 401

def test_pow_without_token():
    response = client.post("/pow", json={"base": 2, "exponent": 2})
    assert response.status_code == 401


# -------------------- Error Handling --------------------

def test_fibonacci_missing_param():
    response = client.get("/fibonacci")
    assert response.status_code == 422

def test_pow_malformed_json():
    response = client.post("/pow", data="{ base: 2, exponent: 2")  # invalid JSON
    assert response.status_code in (400, 422)

# -------------------- Caching (assumes Redis or in-memory caching enabled) --------------------

def test_fibonacci_cache_effectiveness():
    import time
    n = 25
    start1 = time.time()
    r1 = client.get(f"/fibonacci?n={n}")
    duration1 = time.time() - start1

    start2 = time.time()
    r2 = client.get(f"/fibonacci?n={n}")
    duration2 = time.time() - start2

    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r1.json()["result"] == r2.json()["result"]
    assert duration2 <= duration1  # cached version should be faster or equal

# -------------------- Logging (basic functional presence) --------------------

def test_log_file_written():
    import os
    import time

    log_path = "logs/app.log"
    client.get("/factorial?n=3")  # Trigger a simple logged route
    time.sleep(0.1)  # Allow for async write

    assert os.path.exists(log_path), "Log file should exist"
    with open(log_path, "r") as log_file:
        contents = log_file.read()
    assert "factorial" in contents.lower()
