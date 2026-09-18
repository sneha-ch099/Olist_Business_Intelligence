import pandas as pd


def create_sales_model(data):
    orders = data["orders"].copy()
    order_items = data["order_items"].copy()
    products = data["products"].copy()
    customers = data["customers"].copy()
    sellers = data["sellers"].copy()
    payments = data["order_payments"].copy()
    reviews = data["order_reviews"].copy()
    categories = data["product_category"].copy()

    # Merge orders with order items
    sales = orders.merge(
        order_items,
        on="order_id",
        how="left"
    )

    # Add product information
    sales = sales.merge(
        products,
        on="product_id",
        how="left"
    )

    # Add category translation
    sales = sales.merge(
        categories,
        on="product_category_name",
        how="left"
    )

    # Add customer information
    sales = sales.merge(
        customers,
        on="customer_id",
        how="left"
    )

    # Add seller information
    sales = sales.merge(
        sellers,
        on="seller_id",
        how="left"
    )

    # Add payment information
    payments_summary = (
        payments.groupby("order_id")
        .agg(
            total_payment_value=("payment_value", "sum"),
            payment_installments=("payment_installments", "max"),
            payment_types=("payment_type", lambda x: ", ".join(x.astype(str).unique()))
        )
        .reset_index()
    )

    sales = sales.merge(
        payments_summary,
        on="order_id",
        how="left"
    )

    # Add review information
    reviews_summary = (
        reviews.groupby("order_id")
        .agg(
            review_score=("review_score", "mean")
        )
        .reset_index()
    )

    sales = sales.merge(
        reviews_summary,
        on="order_id",
        how="left"
    )

    # Create delivery time
    sales["order_purchase_timestamp"] = pd.to_datetime(
        sales["order_purchase_timestamp"],
        errors="coerce"
    )

    sales["order_delivered_customer_date"] = pd.to_datetime(
        sales["order_delivered_customer_date"],
        errors="coerce"
    )

    sales["delivery_days"] = (
        sales["order_delivered_customer_date"]
        - sales["order_purchase_timestamp"]
    ).dt.days

    # Create total item value
    sales["item_total"] = (
        sales["price"].fillna(0)
        + sales["freight_value"].fillna(0)
    )

    return sales