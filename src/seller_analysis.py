def seller_kpis(sales):

    # Total sellers
    total_sellers = sales["seller_id"].nunique()

    # Active sellers
    active_sellers = sales["seller_id"].nunique()

    # Number of seller states
    seller_states = sales["seller_state"].nunique()

    # Number of seller cities
    seller_cities = sales["seller_city"].nunique()

    # Sales by seller
    seller_sales = (
        sales.groupby("seller_id")["item_total"]
        .sum()
        .sort_values(ascending=False)
    )

    # Orders handled by seller
    seller_orders = (
        sales.groupby("seller_id")["order_id"]
        .nunique()
        .sort_values(ascending=False)
    )

    return {
        "total_sellers": total_sellers,
        "active_sellers": active_sellers,
        "seller_states": seller_states,
        "seller_cities": seller_cities,
        "seller_sales": seller_sales,
        "seller_orders": seller_orders,
    }