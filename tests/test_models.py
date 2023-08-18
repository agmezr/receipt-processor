""" Tests for the model creation and validations."""
import datetime
from src import models
import pytest
from tests.utils import read_receipt
from src.exceptions import ReceiptError


@pytest.fixture
def target_receipt():
    """Reads the receipt and returns as a dict."""
    return read_receipt("receipt-target.json")


def test_create_model(target_receipt):
    """Tests creation of a new receipt."""
    receipt = models.Receipt(target_receipt)
    assert receipt.uid
    assert len(receipt.items) == 5
    assert receipt.total == 35.35
    assert isinstance(receipt.purchase_date, datetime.datetime)


@pytest.mark.parametrize(
    "json_receipt, expected",
    [
        ("receipt-target.json", 28),
        ("receipt-mm.json", 109),
        # this one triggers all rules
        ("receipt-custom-test.json", 10 + 50 + 25 + 5 + 6 + 10 + 2),
    ],
)
def test_points_calculated(json_receipt, expected):
    """Test points are calculated correctly."""
    receipt = models.Receipt(read_receipt(json_receipt))
    receipt.calculate_points()
    assert receipt.total == expected


@pytest.mark.parametrize(
    "json_receipt",
    [
        ("receipt-no-items.json"),
        ("receipt-no-date.json"),
        ("receipt-no-time.json"),
        ("receipt-invalid-time.json"),
        ("receipt-invalid-date.json"),
    ],
)
def test_exception_is_raised(json_receipt):
    with pytest.raises(ReceiptError):
        models.Receipt(read_receipt(json_receipt))
