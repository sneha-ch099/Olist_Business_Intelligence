import pandas as pd


def sales_kpis(sales):
    # Total sales revenue
    total_revenue = sales["item_total"].sum()

    # Number of orders
    total_orders = sales["order_id"].nunique()

    # Average Order Value
    average_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )

    # Total products/items sold
    total_items = len(sales)

    # Average item price
    average_item_price = sales["price"].mean()

    # Total freight value
    total_freight = sales["freight_value"].sum()

    # Sales by product category
    category_sales = (
        sales.groupby("product_category_name_english")["item_total"]
        .sum()
        .sort_values(ascending=False)
    )

    # Monthly sales
    sales["order_purchase_timestamp"] = pd.to_datetime(
        sales["order_purchase_timestamp"],
        errors="coerce"
    )

    monthly_sales = (
        sales.dropna(subset=["order_purchase_timestamp"])
        .set_index("order_purchase_timestamp")
        .resample("ME")["item_total"]
        .sum()
    )

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "average_order_value": average_order_value,
        "total_items": total_items,
        "average_item_price": average_item_price,
        "total_freight": total_freight,
        "category_sales": category_sales,
        "monthly_sales": monthly_sales,
    }