import streamlit as st
import pandas as pd

from src.data_loader import load_data
from src.sales_analysis import sales_kpis


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Sales & Orders Analysis",
    page_icon="🛒",
    layout="wide"
)


# --------------------------------------------------
# LOAD & CACHE SALES DATA
# --------------------------------------------------

@st.cache_data(show_spinner="Loading sales data...")
def get_sales_data():

    data = load_data()

    orders = data["orders"].copy()
    order_items = data["order_items"].copy()
    products = data["products"].copy()
    customers = data["customers"].copy()
    categories = data["product_category"].copy()

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
        customers[
            ["customer_id", "customer_state"]
        ],
        on="customer_id",
        how="left"
    )

    sales = sales.merge(
        categories,
        on="product_category_name",
        how="left"
    )

    sales["order_purchase_timestamp"] = pd.to_datetime(
        sales["order_purchase_timestamp"],
        errors="coerce"
    )

    sales["item_total"] = (
        sales["price"].fillna(0)
        + sales["freight_value"].fillna(0)
    )

    return sales


sales = get_sales_data()


# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("🛒 Sales & Orders Analysis")

st.write(
    "Business Question: "
    "How are sales and orders performing across time and product categories?"
)


# --------------------------------------------------
# FILTERS
# --------------------------------------------------

st.subheader("🔎 Sales Filters")

col1, col2, col3 = st.columns(3)

with col1:

    selected_category = st.multiselect(
        "Select Product Category",
        sorted(
            sales["product_category_name_english"]
            .dropna()
            .unique()
        )
    )

with col2:

    selected_state = st.multiselect(
        "Select Customer State",
        sorted(
            sales["customer_state"]
            .dropna()
            .unique()
        )
    )

with col3:

    selected_status = st.multiselect(
        "Select Order Status",
        sorted(
            sales["order_status"]
            .dropna()
            .unique()
        )
    )


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_sales = sales

if selected_category:

    filtered_sales = filtered_sales[
        filtered_sales["product_category_name_english"].isin(
            selected_category
        )
    ]

if selected_state:

    filtered_sales = filtered_sales[
        filtered_sales["customer_state"].isin(
            selected_state
        )
    ]

if selected_status:

    filtered_sales = filtered_sales[
        filtered_sales["order_status"].isin(
            selected_status
        )
    ]


# --------------------------------------------------
# CALCULATE SALES KPIs
# --------------------------------------------------

sales_data = sales_kpis(filtered_sales)


st.divider()


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

st.subheader("📊 Sales & Orders KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Orders",
        f"{sales_data['total_orders']:,}"
    )

with col2:

    st.metric(
        "Total Sales",
        f"₹{sales_data['total_revenue']:,.2f}"
    )

with col3:

    st.metric(
        "Average Order Value",
        f"₹{sales_data['average_order_value']:,.2f}"
    )

with col4:

    st.metric(
        "Items Sold",
        f"{sales_data['total_items']:,}"
    )


st.divider()


# --------------------------------------------------
# ADDITIONAL SALES INFORMATION
# --------------------------------------------------

st.subheader("💰 Sales Overview")

col1, col2 = st.columns(2)

with col1:

    average_item_price = sales_data[
        "average_item_price"
    ]

    if pd.isna(average_item_price):
        average_item_price = 0

    st.metric(
        "Average Item Price",
        f"₹{average_item_price:,.2f}"
    )

with col2:

    st.metric(
        "Total Freight",
        f"₹{sales_data['total_freight']:,.2f}"
    )


st.divider()


# --------------------------------------------------
# MONTHLY SALES TREND
# --------------------------------------------------

st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    sales_data["monthly_sales"]
    .reset_index()
)

monthly_sales.columns = [
    "Month",
    "Sales"
]

st.line_chart(
    monthly_sales,
    x="Month",
    y="Sales",
    width="stretch"
)


st.divider()


# --------------------------------------------------
# SALES BY PRODUCT CATEGORY
# --------------------------------------------------

st.subheader("📦 Sales by Product Category")

category_sales = (
    sales_data["category_sales"]
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
# CATEGORY SALES TABLE
# --------------------------------------------------

st.subheader("📋 Product Category Sales")

st.dataframe(
    category_sales,
    width="stretch",
    hide_index=True
)


st.divider()


# --------------------------------------------------
# BUSINESS INTERPRETATION
# --------------------------------------------------

st.subheader("💡 Business Interpretation")

if not filtered_sales.empty:

    top_category = (
        sales_data["category_sales"].index[0]
        if not sales_data["category_sales"].empty
        else "N/A"
    )

    st.write(
        f"""
        - The dashboard records **{sales_data['total_orders']:,} orders**
        in the selected data.

        - Total sales value is
        **₹{sales_data['total_revenue']:,.2f}**.

        - The average order value is
        **₹{sales_data['average_order_value']:,.2f}**.

        - A total of **{sales_data['total_items']:,} items** were sold.

        - **{top_category}** is the highest-selling product category
        among the displayed categories.
        """
    )

else:

    st.warning(
        "No sales data is available for the selected filters."
    )