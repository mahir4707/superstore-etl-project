
import pandas as pd

from scripts.transform import transform_data


def test_transform_removes_exact_duplicates():
    raw = pd.DataFrame([
        {
            "Order ID": "CA-001",
            "Order Date": "01/01/2025",
            "Ship Date": "03/01/2025",
            "Product ID": "P-001",
            "Product Name": "Notebook",
            "Sales": 100.0,
            "Quantity": 2,
            "Profit": 20.0,
        },
        {
            "Order ID": "CA-001",
            "Order Date": "01/01/2025",
            "Ship Date": "03/01/2025",
            "Product ID": "P-001",
            "Product Name": "Notebook",
            "Sales": 100.0,
            "Quantity": 2,
            "Profit": 20.0,
        },
    ])

    cleaned = transform_data(raw)

    assert len(cleaned) == 1
    assert cleaned["ORDER_ID"].iloc[0] == "CA-001"


def test_transform_calculates_unit_price_and_margin():
    raw = pd.DataFrame([{
        "Order ID": "CA-002",
        "Order Date": "01/01/2025",
        "Ship Date": "03/01/2025",
        "Product ID": "P-002",
        "Product Name": "Desk Lamp",
        "Sales": 100.0,
        "Quantity": 4,
        "Profit": 25.0,
    }])

    cleaned = transform_data(raw)

    assert cleaned["UNIT_PRICE"].iloc[0] == 25.0
    assert cleaned["PROFIT_MARGIN"].iloc[0] == 0.25
    assert cleaned["SHIPPING_DAYS"].iloc[0] == 2



def test_transform_preserves_missing_financial_values():
    raw = pd.DataFrame([{
        "Order ID": "CA-003",
        "Order Date": "01/01/2025",
        "Ship Date": "03/01/2025",
        "Product ID": "P-003",
        "Product Name": "Mouse",
        "Sales": None,
        "Quantity": 2,
        "Profit": None,
    }])

    cleaned = transform_data(raw)

    assert pd.isna(cleaned["SALES"].iloc[0])
    assert pd.isna(cleaned["PROFIT"].iloc[0])
    assert bool(cleaned["SALES_WAS_MISSING"].iloc[0])
    assert bool(cleaned["PROFIT_WAS_MISSING"].iloc[0])


def test_transform_rejects_empty_dataframe():
    import pytest

    with pytest.raises(ValueError, match="empty dataset"):
        transform_data(pd.DataFrame())

