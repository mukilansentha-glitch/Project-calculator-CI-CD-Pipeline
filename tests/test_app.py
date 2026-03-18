"""Unit and integration tests for the Flask DevOps Calculator app."""

import json
import pytest
from app import app, add, subtract, multiply, divide


# ── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def client():
    """Create a Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ── Unit tests: math functions ───────────────────────────────────────────────

class TestAdd:
    def test_positive_numbers(self):
        assert add(3, 4) == 7

    def test_negative_numbers(self):
        assert add(-1, -2) == -3

    def test_floats(self):
        assert abs(add(0.1, 0.2) - 0.3) < 1e-9

    def test_zero(self):
        assert add(0, 0) == 0


class TestSubtract:
    def test_positive(self):
        assert subtract(10, 4) == 6

    def test_result_negative(self):
        assert subtract(2, 5) == -3

    def test_zero(self):
        assert subtract(5, 0) == 5


class TestMultiply:
    def test_positive(self):
        assert multiply(3, 4) == 12

    def test_by_zero(self):
        assert multiply(99, 0) == 0

    def test_negative(self):
        assert multiply(-2, 3) == -6


class TestDivide:
    def test_even_division(self):
        assert divide(10, 2) == 5.0

    def test_float_result(self):
        assert abs(divide(1, 3) - 0.3333333) < 1e-5

    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(5, 0)

    def test_negative_dividend(self):
        assert divide(-10, 2) == -5.0


# ── Integration tests: Flask routes ─────────────────────────────────────────

class TestIndexRoute:
    def test_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_contains_title(self, client):
        response = client.get("/")
        assert b"DevOps Calculator" in response.data


class TestHealthRoute:
    def test_returns_ok(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "ok"


class TestCalculateRoute:
    def _post(self, client, payload):
        return client.post(
            "/calculate",
            data=json.dumps(payload),
            content_type="application/json",
        )

    def test_add(self, client):
        res = self._post(client, {"a": 5, "b": 3, "operation": "add"})
        assert res.status_code == 200
        assert json.loads(res.data)["result"] == 8

    def test_subtract(self, client):
        res = self._post(client, {"a": 10, "b": 4, "operation": "subtract"})
        assert json.loads(res.data)["result"] == 6

    def test_multiply(self, client):
        res = self._post(client, {"a": 6, "b": 7, "operation": "multiply"})
        assert json.loads(res.data)["result"] == 42

    def test_divide(self, client):
        res = self._post(client, {"a": 9, "b": 3, "operation": "divide"})
        assert json.loads(res.data)["result"] == 3.0

    def test_divide_by_zero(self, client):
        res = self._post(client, {"a": 5, "b": 0, "operation": "divide"})
        assert res.status_code == 400
        assert "error" in json.loads(res.data)

    def test_unknown_operation(self, client):
        res = self._post(client, {"a": 1, "b": 1, "operation": "modulo"})
        assert res.status_code == 400

    def test_invalid_numbers(self, client):
        res = self._post(client, {"a": "abc", "b": 2, "operation": "add"})
        assert res.status_code == 400

    def test_no_body(self, client):
        res = client.post("/calculate", content_type="application/json")
        assert res.status_code == 400
