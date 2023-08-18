from datetime import datetime
from typing import Dict, Any
from src.exceptions import ReceiptError
import uuid
from inspect import getmembers, isfunction
import src.points_rules as points_rules


import logging


class Receipt:
    """A simple class that represents a receipt."""

    def __init__(self, receipt: Dict[str, Any]) -> None:
        """When created it will create a new uid and parse data.

        Raises:
            ReceiptError: If can't parse date/time or some data is missing.
        """
        self.uid = str(uuid.uuid4())
        self.points = 0
        try:
            self.retailer = receipt["retailer"].strip()
            self.purchase_date = self._format_date(receipt["purchaseDate"])
            self.purchase_time = self._format_time(receipt["purchaseTime"])
            self.items = receipt["items"]
            self.total = float(receipt["total"])
        except KeyError as e:
            raise ReceiptError(f"Could not find {e} key in receipt.")

    def calculate_points(self) -> None:
        """Calcule receipt points for this receipt based on a set of rules.

        This function will read ALL functions in the points_calculator module.
        To add a new rule simply create a new function that receives a receipt and
        return an int

        Example:

        def new_rule(receipt):
            # some code

            return points
        """
        total = 0

        for name, fn in getmembers(points_rules, isfunction):
            result = fn(self)
            logging.info(f"fn {name} returned: {result}")
            total += result

        self.total = total

    def _format_date(self, purchase_date: str):
        date_format = "%Y-%m-%d"
        try:
            return datetime.strptime(purchase_date, date_format)
        except ValueError:
            str_error = f"Could not parse date {purchase_date} for receipt {self.uid}"
            logging.error(str_error)
            raise ReceiptError(str_error)

    def _format_time(self, purchase_time: str):
        date_format = "%H:%M"
        try:
            return datetime.strptime(purchase_time, date_format)
        except ValueError:
            str_error = f"Could not parse date {purchase_time} for receipt {self.uid}"
            logging.error(str_error)
            raise ReceiptError(str_error)
