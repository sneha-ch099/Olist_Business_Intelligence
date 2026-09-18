import streamlit as st
import pandas as pd

from src.data_loader import load_data
from src.product_analysis import product_kpis


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Product Analysis",
    page_icon="📦",
    layout="wide"
)


# --------------------------------------------------
# LOAD & CACHE PRODUCT DATA
# --------------------------------------------------

@st.cache_data(show_spinner="Loading product data...")
def get_product_data():

    data = load_data()

    orders = data["orders"].copy()
    order_items = data["order_items"].copy()
    products = data["products"].copy()
    categories = data["product_category"].copy()

    # Create product sales data
    sales = orders.merge(
        order_items,
        on="order_id",
        how="left"
    )

    sales = sales.merge(
        products,
        on="product_id",
        how="left"
    )

    sales = sales.merge(
        categories,
        on="product_category_name",
        how="left"
    )

    # Calculate item total
    sales["item_total"] = (
        sales["price"].fillna(0)
        + sales["freight_value"].fillna(0)
    )

    return sales


sales = get_product_data()


# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("📦 Product Analysis")

st.write(
    "Business Question: "
    "Which products and product categories generate "
    "the most sales and orders?"
)


# --------------------------------------------------
# PRODUCT FILTER
# --------------------------------------------------

st.subheader("🔎 Product Filters")

selected_category = st.multiselect(
    "Select Product Category",
    sorted(
        sales["product_category_name_english"]
        .dropna()
        .unique()
    )
)


# --------------------------------------------------
# APPLY FILTER
# --------------------------------------------------

filtered_sales = sales

if selected_category:

    filtered_sales = filtered_sales[
        filtered_sales["product_category_name_english"].isin(
            selected_category
        )
    ]


# --------------------------------------------------
# PRODUCT ANALYSIS
# --------------------------------------------------

product_data = product_kpis(filtered_sales)


st.divider()


# --------------------------------------------------
# PRODUCT KPIs
# --------------------------------------------------

st.subheader("📊 Product KPIs")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Total Products",
        f"{product_data['total_products']:,}"
    )

with col2:

    st.metric(
        "Total Categories",
        f"{product_data['total_categories']:,}"
    )

with col3:

    average_price = product_data["average_product_price"]

    if pd.isna(average_price):
        average_price = 0

    st.metric(
        "Average Product Price",
        f"₹{average_price:,.2f}"
    )


st.divider()


# --------------------------------------------------
# SALES BY PRODUCT CATEGORY
# --------------------------------------------------

st.subheader("📈 Sales by Product Category")

category_sales = (
    product_data["category_sales"]
    .head(10)
    .reset_index()
)

category_sales.columns = [
    "Product Category",
    "Sales"
]

st.bar_chart(
    category_sales,
    x="Product Category",
    y="Sales",
    width="stretch"
)


st.divider()


# --------------------------------------------------
# ORDERS BY PRODUCT CATEGORY
# --------------------------------------------------

st.subheader("🛒 Orders by Product Category")

category_orders = (
    product_data["category_orders"]
    .head(10)
    .reset_index()
)

category_orders.columns = [
    "Product Category",
    "Orders"
]

st.bar_chart(
    category_orders,
    x="Product Category",
    y="Orders",
    width="stretch"
)


st.divider()


# --------------------------------------------------
# CATEGORY PERFORMANCE TABLE
# --------------------------------------------------

st.subheader("📋 Category Performance")

category_performance = category_sales.copy()

category_performance["Orders"] = (
    category_performance["Product Category"]
    .map(
        product_data["category_orders"]
    )
)

st.dataframe(
    category_performance,
    width="stretch",
    hide_index=True
)


st.divider()


# --------------------------------------------------
# BUSINESS INTERPRETATION
# --------------------------------------------------

st.subheader("💡 Business Interpretation")

if not filtered_sales.empty:

    top_sales_category = (
        product_data["category_sales"].index[0]
        if not product_data["category_sales"].empty
        else "N/A"
    )

    top_orders_category = (
        product_data["category_orders"].index[0]
        if not product_data["category_orders"].empty
        else "N/A"
    )

    st.write(
        f"""
        - The selected data contains **{product_data['total_products']:,} products**
        across **{product_data['total_categories']:,} product categories**.

        - The average product price is
        **₹{average_price:,.2f}**.

        - **{top_sales_category}** has the highest sales
        among the displayed categories.

        - **{top_orders_category}** has the highest number of orders
        among the displayed categories.
        """
    )

else:

    st.warning(
        "No product data is available for the selected category."
    )