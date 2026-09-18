import pandas as pd


def delivery_kpis(sales):

    # Make sure date columns are in datetime format
    sales = sales.copy()

    sales["order_delivered_customer_date"] = pd.to_datetime(
        sales["order_delivered_customer_date"],
        errors="coerce"
    )

    sales["order_estimated_delivery_date"] = pd.to_datetime(
        sales["order_estimated_delivery_date"],
        errors="coerce"
    )

    # Average delivery time
    average_delivery_days = sales["delivery_days"].mean()

    # Delivery delay
    sales["delay_days"] = (
        sales["order_delivered_customer_date"]
        -
        sales["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400

    # On-time delivery
    on_time_orders = (
        sales["delay_days"] <= 0
    ).sum()

    # Late delivery
    late_orders = (
        sales["delay_days"] > 0
    ).sum()

    total_delivered_orders = sales["delay_days"].notna().sum()

    if total_delivered_orders > 0:

        on_time_percentage = (
            on_time_orders /
            total_delivered_orders
        ) * 100

        late_percentage = (
            late_orders /
            total_delivered_orders
        ) * 100

        average_delay = (
            sales.loc[
                sales["delay_days"] > 0,
                "delay_days"
            ].mean()
        )

    else:

        on_time_percentage = 0
        late_percentage = 0
        average_delay = 0

    # Delivery time by customer state
    delivery_by_state = (
        sales
        .groupby("customer_state")["delivery_days"]
        .mean()
        .sort_values()
    )

    # Delivery time by seller state
    delivery_by_seller_state = (
        sales
        .groupby("seller_state")["delivery_days"]
        .mean()
        .sort_values()
    )

    return {
    "average_delivery_days": average_delivery_days,
    "on_time_percentage": on_time_percentage,
    "late_percentage": late_percentage,
    "average_delay": average_delay,
    "delivery_by_state": delivery_by_state,
    "delivery_by_seller_state": delivery_by_seller_state,
}