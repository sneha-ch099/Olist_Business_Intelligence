def product_kpis(sales):

    total_products = sales["product_id"].nunique()

    total_categories = sales["product_category_name_english"].nunique()

    average_product_price = sales["price"].mean()

    category_sales = (
        sales.groupby("product_category_name_english")["item_total"]
        .sum()
        .sort_values(ascending=False)
    )

    category_orders = (
        sales.groupby("product_category_name_english")["order_id"]
        .nunique()
        .sort_values(ascending=False)
    )

    return {
        "total_products": total_products,
        "total_categories": total_categories,
        "average_product_price": average_product_price,
        "category_sales": category_sales,
        "category_orders": category_orders,
    }