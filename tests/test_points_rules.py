from src import points_rules
from unittest import mock
import pytest
from datetime import datetime


@pytest.mark.parametrize(
    "name, expected",
    [
        ("abc", 3),
        ("ABC123", 6),
        ("A B C D E 1 0", 7),
        ("m&m's", 3),
        ("!@#$^&*()_+A", 1),
    ],
)
def test_alpha_points(name, expected):
    """Tests correct points for alphanumeric numbers only."""
    receipt = mock.Mock()
    receipt.retailer = name
    points = points_rules.is_alphanumeric(receipt)
    assert points == expected


@pytest.mark.parametrize(
    "total, expected",
    [
        (30.0, 50),
        (30.1, 0),
        (130.1, 0),
        (130.9999999, 0),
        (130.00000, 50),
    ],
)
def test_no_cents_amount(total, expected):
    """Tests correct ammount for total."""
    receipt = mock.Mock()
    receipt.total = total
    points = points_rules.total_amount_no_cents(receipt)
    assert points == expected


@pytest.mark.parametrize(
    "total, expected",
    [
        (30.0, 25),
        (30.46, 0),
        (1, 25),
        (1.12, 0),
        (2, 25),
        (2.25, 25),
        (2.75, 25),
    ],
)
def test_is_multiple_one_quarter(total, expected):
    """Tests correct check for multiple of .25."""
    receipt = mock.Mock()
    receipt.total = total
    points = points_rules.is_multiple_of_a_quarter(receipt)
    assert points == expected


@pytest.mark.parametrize(
    "items, expected",
    [
        (
            [
                {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"},
            ],
            6,
        ),
        (
            [
                {
                    "shortDescription": "ABC",
                    "price": "1.2",
                },
                {
                    "shortDescription": "123",
                    "price": "101.3",
                },
            ],
            22,
        ),
    ],
)
def test_item_description(items, expected):
    """Tests correct ammount for item len."""
    receipt = mock.Mock()
    receipt.items = items
    points = points_rules.calculcate_item_description(receipt)
    assert points == expected


@pytest.mark.parametrize(
    "items, expected",
    [
        (["a", "b"], 5),
        (
            [
                "a",
            ],
            0,
        ),
        (["a", "b", "c", "d"], 10),
        (["a", "b", "c", "d", "e"], 10),
        (["a", "b", "c", "d", "e", "f"], 15),
    ],
)
def test_correct_items_amount(items, expected):
    """Tests correct amount for items in receipt."""
    receipt = mock.Mock()
    receipt.items = items
    points = points_rules.total_items(receipt)
    assert points == expected


@pytest.mark.parametrize(
    "day, expected",
    [
        (1, 6),
        (2, 0),
        (3, 6),
        (4, 0),
    ],
)
def test_odd_day(day, expected):
    """Tests correct ammount for odd purchase day."""
    receipt = mock.Mock()
    receipt.purchase_date = datetime(2000, 1, day)
    points = points_rules.purchase_odd_day(receipt)
    assert points == expected


@pytest.mark.parametrize(
    "hour, minute, expected",
    [
        (12, 0, 0),
        (15, 0, 10),
        (13, 59, 0),
        (15, 59, 10),
        (16, 1, 0),
        (22, 1, 0),
    ],
)
def test_between_time(hour, minute, expected):
    """Tests points are correct if time between 2pm and 4pm"""
    receipt = mock.Mock()
    receipt.purchase_time = datetime(1900, 1, 1, hour, minute)
    points = points_rules.purchase_time_correct(receipt)
    assert points == expected
