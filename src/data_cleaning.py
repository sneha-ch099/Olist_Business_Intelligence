import pandas as pd


def clean_data(data):
    customers = data["customers"].copy()
    geolocation = data["geolocation"].copy()
    order_items = data["order_items"].copy()
    order_payments = data["order_payments"].copy()
    order_reviews = data["order_reviews"].copy()
    orders = data["orders"].copy()
    products = data["products"].copy()
    sellers = data["sellers"].copy()
    product_category = data["product_category"].copy()

    # -----------------------------
    # Clean Orders
    # -----------------------------
    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for col in date_columns:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")

    # -----------------------------
    # Clean Order Payments
    # -----------------------------
    order_payments["payment_value"] = pd.to_numeric(
        order_payments["payment_value"], errors="coerce"
    )

    order_payments["payment_installments"] = pd.to_numeric(
        order_payments["payment_installments"], errors="coerce"
    )

    # -----------------------------
    # Clean Order Items
    # -----------------------------
    order_items["price"] = pd.to_numeric(
        order_items["price"], errors="coerce"
    )

    order_items["freight_value"] = pd.to_numeric(
        order_items["freight_value"], errors="coerce"
    )

    # -----------------------------
    # Clean Reviews
    # -----------------------------
    order_reviews["review_score"] = pd.to_numeric(
        order_reviews["review_score"], errors="coerce"
    )

    # -----------------------------
    # Clean Products
    # -----------------------------
    product_numeric_columns = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]

    for col in product_numeric_columns:
        products[col] = pd.to_numeric(
            products[col], errors="coerce"
        )

    # -----------------------------
    # Remove duplicate rows
    # -----------------------------
    customers = customers.drop_duplicates()
    geolocation = geolocation.drop_duplicates()
    order_items = order_items.drop_duplicates()
    order_payments = order_payments.drop_duplicates()
    order_reviews = order_reviews.drop_duplicates()
    orders = orders.drop_duplicates()
    products = products.drop_duplicates()
    sellers = sellers.drop_duplicates()
    product_category = product_category.drop_duplicates()

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