import pytest
from src.app import app
from tests.utils import read_receipt


@pytest.fixture
def client():
    return app.test_client()


@pytest.mark.parametrize(
    "receipt_name, points",
    [
        ("receipt-target.json", 28),
        ("receipt-mm.json", 109),
    ],
)
def test_receipt_creation(receipt_name, points, client):
    """Tests a new receipt can be created and retrieved."""
    json_receipt = read_receipt(receipt_name)
    response = client.post("/receipt/process", json=json_receipt)
    new_uid = response.json["id"]
    assert new_uid
    response = client.get(f"/receipt/{new_uid}/points")
    assert response
    assert response.status_code == 200
    assert response.json["points"] == points


@pytest.mark.parametrize(
    "receipt_name",
    [
        ("receipt-no-items.json"),
        ("receipt-no-date.json"),
        ("receipt-no-time.json"),
    ],
)
def test_bad_post_data(receipt_name, client):
    """Test a bad request is sent if wrong data commes froms the receipt."""
    json_receipt = read_receipt(receipt_name)
    response = client.post("/receipt/process", json=json_receipt)
    print(response.text)
    assert response.status_code == 400


def test_no_uid(client):
    """Tests a not found is return if no uid exists."""
    response = client.get(f"/receipt/1234/points")
    assert response
    assert response.status_code == 404
    assert "error" in response.json
