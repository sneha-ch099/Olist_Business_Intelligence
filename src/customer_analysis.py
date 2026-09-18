def customer_analysis(data):

    customers = data["customers"]
    orders = data["orders"]

    total_customers = customers[
        "customer_unique_id"
    ].nunique()

    customer_orders = orders.merge(
        customers[
            ["customer_id", "customer_unique_id"]
        ],
        on="customer_id",
        how="left"
    )

    orders_per_customer = (
        customer_orders
        .groupby("customer_unique_id")["order_id"]
        .nunique()
    )

    repeat_customers = (
        orders_per_customer > 1
    ).sum()

    repeat_rate = (
        repeat_customers /
        total_customers
    ) * 100

    return {
        "total_customers": total_customers,
        "repeat_customers": repeat_customers,
        "repeat_rate": repeat_rate
    }


# Compatibility with the existing main dashboard
def customer_kpis(data):
    return customer_analysis(data)