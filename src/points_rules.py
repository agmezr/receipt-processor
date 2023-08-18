"""ALL functions in this file are used as a set of rules to calculate the total points in a receipt."""
import datetime
import math

def is_alphanumeric(receipt) -> int:
    """One point for every alphanumeric character in the retailer name."""
    total = 0
    for letter in receipt.retailer:
        if letter.isalnum():
            total += 1
    return total

def is_multiple_of_a_quarter(receipt) -> int :
    """25 points if the total is a multiple of 0.25."""
    if (receipt.total * 4) == int( receipt.total * 4):
        return 25
    return 0

def total_amount_no_cents(receipt) -> int:
    """50 points if the total is a round dollar amount with no cents."""
    total = receipt.total
    return 50 if int(total) == total else 0

def total_items(receipt) -> int:
    """5 points for every two items on the receipt."""
    return len(receipt.items) // 2 * 5

def calculcate_item_description(receipt) -> int:
    """If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. 
    
    The result is the number of points earned."""
    total = 0 
    for item in receipt.items:
        description = item["shortDescription"].strip()
        price = item["price"]

        if len(description) % 3 == 0:
            total += math.ceil(float(price) * 0.2)
    return total

def purchase_odd_day(receipt) -> int:
    """6 points if the day in the purchase date is odd."""
    purchase_day = receipt.purchase_date.day
    return 6 if purchase_day % 2 == 1 else 0

def purchase_time_correct(receipt) -> int:
    """10 points if the time of purchase is after 2:00pm and before 4:00pm."""
    start_time = datetime.datetime(1900,1,1,14,00)
    end_time = datetime.datetime(1900,1,1,16,00)
    if start_time <= receipt.purchase_time <= end_time:
        return 10
    return 0