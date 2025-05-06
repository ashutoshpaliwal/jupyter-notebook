#!/usr/bin/env python
# coding: utf-8

# In[1]:


import calendar
from datetime import datetime, date
from collections import defaultdict

def generate_monthly_bill(item_list: list, target_month: str) -> dict:
    """
    Generates a bill for the given month based on the item list.

    Parameters:
    item_list (list): List of dictionaries with item details.
    target_month (str): Month in "YYYY-MM" format (e.g., "2024-11").

    Returns:
    dict: A dictionary with grouped line items and total revenue.
    """
    # Parse the target month and determine its start and end dates
    year, month = map(int, target_month.split('-'))
    month_start = date(year, month, 1)
    month_end = date(year, month, calendar.monthrange(year, month)[1])

    # Dictionary to hold grouped items
    grouped_items = defaultdict(lambda: {'qty': 0, 'amount': 0.0})

    for item in item_list:
        # Parse and validate item dates
        try:
            item_start = datetime.strptime(item['start_date'], '%Y-%m-%d').date()
            item_stop = datetime.strptime(item['stop_date'], '%Y-%m-%d').date()
        except (ValueError, KeyError):
            continue  # Skip items with invalid or missing dates

        # Determine the overlap between the item's active period and the target month
        active_start = max(item_start, month_start)
        active_end = min(item_stop, month_end)
        if active_start > active_end:
            continue  # No overlap; skip this item

        # Calculate the number of active days in the target month
        active_days = (active_end - active_start).days + 1
        total_days_in_month = (month_end - month_start).days + 1
        active_fraction = active_days / total_days_in_month

        # Normalize rate and quantity
        try:
            rate = float(item['rate'])
            qty = int(item['qty'])
        except (ValueError, KeyError):
            continue  # Skip items with invalid or missing rate/qty

        # Calculate the prorated amount
        amount = rate * qty * active_fraction

        # Define the billing period string
        billing_period = f"{active_start.strftime('%Y-%m-%d')} to {active_end.strftime('%Y-%m-%d')}"

        # Create a grouping key
        group_key = (item['item_code'], rate, billing_period)

        # Aggregate quantities and amounts
        grouped_items[group_key]['qty'] += qty
        grouped_items[group_key]['amount'] += amount

    # Prepare the final line items
    line_items = []
    total_revenue = 0.0
    for (item_code, rate, billing_period), data in grouped_items.items():
        amount = round(data['amount'], 2)
        line_items.append({
            'item_code': item_code,
            'rate': rate,
            'qty': data['qty'],
            'amount': amount,
            'billing_period': billing_period
        })
        total_revenue += amount

    return {
        'line_items': line_items,
        'total_revenue': round(total_revenue, 2)
    }


# In[2]:


item_list = [
    {
        "idx": 1,
        "item_code": "Executive Desk (4*2)",
        "qty": 10,
        "rate": "1000",
        "start_date": "2023-11-01",
        "stop_date": "2024-10-17",
    },
    {
        "idx": 2,
        "item_code": "Executive Desk (4*2)",
        "qty": "10",
        "rate": "1080",
        "start_date": "2024-10-18",
        "stop_date": "2025-10-31",
    },
    # Add more items as needed
]

target_month = "2024-11"
bill = generate_monthly_bill(item_list, target_month)
print(bill)


# In[ ]:




