import pandas as pd
from pathlib import Path


# Project data folder
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_data():
    customers = pd.read_csv(DATA_DIR / "olist_customers_dataset.csv")
    geolocation = pd.read_csv(DATA_DIR / "olist_geolocation_dataset.csv")
    order_items = pd.read_csv(DATA_DIR / "olist_order_items_dataset.csv")
    order_payments = pd.read_csv(DATA_DIR / "olist_order_payments_dataset.csv")
    order_reviews = pd.read_csv(DATA_DIR / "olist_order_reviews_dataset.csv")
    orders = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv")
    products = pd.read_csv(DATA_DIR / "olist_products_dataset.csv")
    sellers = pd.read_csv(DATA_DIR / "olist_sellers_dataset.csv")
    product_category = pd.read_csv(
        DATA_DIR / "product_category_name_translation.csv"
    )

    return {
        "customers": customers,
        "geolocation": geolocation,
        "order_items": order_items,
        "order_payments": order_payments,
        "order_reviews": order_reviews,
        "orders": orders,
        "products": products,
        "sellers": sellers,
        "product_category": product_category,
    }