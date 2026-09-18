import streamlit as st
import pandas as pd

from src.data_loader import load_data
from src.seller_analysis import seller_kpis


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Seller Analysis",
    page_icon="🏪",
    layout="wide"
)


# --------------------------------------------------
# LOAD & CACHE SELLER DATA
# --------------------------------------------------

@st.cache_data(show_spinner="Loading seller data...")
def get_seller_data():

    data = load_data()

    orders = data["orders"].copy()
    order_items = data["order_items"].copy()
    sellers = data["sellers"].copy()

    sales = orders.merge(
        order_items,
        on="order_id",
        how="left"
    )

    sales = sales.merge(
        sellers,
        on="seller_id",
        how="left"
    )

    sales["item_total"] = (
        sales["price"].fillna(0)
        + sales["freight_value"].fillna(0)
    )

    return sales


sales = get_seller_data()


# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("🏪 Seller Analysis")

st.write(
    "Business Question: "
    "Which sellers generate the most sales and orders, "
    "and where are sellers located?"
)


# --------------------------------------------------
# SELLER FILTERS
# --------------------------------------------------

st.subheader("🔎 Seller Filters")

col1, col2 = st.columns(2)

with col1:

    selected_state = st.multiselect(
        "Select Seller State",
        sorted(
            sales["seller_state"]
            .dropna()
            .unique()
        )
    )

with col2:

    selected_city = st.multiselect(
        "Select Seller City",
        sorted(
            sales["seller_city"]
            .dropna()
            .unique()
        )
    )


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_sales = sales

if selected_state:

    filtered_sales = filtered_sales[
        filtered_sales["seller_state"].isin(
            selected_state
        )
    ]

if selected_city:

    filtered_sales = filtered_sales[
        filtered_sales["seller_city"].isin(
            selected_city
        )
    ]


# --------------------------------------------------
# SELLER ANALYSIS
# --------------------------------------------------

seller_data = seller_kpis(filtered_sales)


st.divider()


# --------------------------------------------------
# SELLER KPIs
# --------------------------------------------------

st.subheader("📊 Seller KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Sellers",
        f"{seller_data['total_sellers']:,}"
    )

with col2:

    st.metric(
        "Seller Revenue",
        f"₹{seller_data['seller_sales'].sum():,.2f}"
    )

with col3:

    st.metric(
        "Orders Handled",
        f"{filtered_sales['order_id'].nunique():,}"
    )

with col4:

    st.metric(
        "Items Sold",
        f"{len(filtered_sales):,}"
    )


st.divider()


# --------------------------------------------------
# SELLER LOCATION OVERVIEW
# --------------------------------------------------

st.subheader("🌎 Seller Location Overview")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Seller States",
        f"{seller_data['seller_states']:,}"
    )

with col2:

    st.metric(
        "Seller Cities",
        f"{seller_data['seller_cities']:,}"
    )


st.divider()


# --------------------------------------------------
# TOP SELLERS BY REVENUE
# --------------------------------------------------

st.subheader("💰 Top Sellers by Revenue")

seller_revenue = (
    seller_data["seller_sales"]
    .head(10)
    .reset_index()
)

seller_revenue.columns = [
    "Seller ID",
    "Revenue"
]

seller_revenue["Seller"] = (
    seller_revenue["Seller ID"].str[:8] + "..."
)

st.bar_chart(
    seller_revenue,
    x="Seller",
    y="Revenue",
    width="stretch"
)


st.divider()


# --------------------------------------------------
# TOP SELLERS BY ORDERS
# --------------------------------------------------

st.subheader("🛒 Top Sellers by Orders")

seller_orders = (
    seller_data["seller_orders"]
    .head(10)
    .reset_index()
)

seller_orders.columns = [
    "Seller ID",
    "Orders"
]

seller_orders["Seller"] = (
    seller_orders["Seller ID"].str[:8] + "..."
)

st.bar_chart(
    seller_orders,
    x="Seller",
    y="Orders",
    width="stretch"
)


st.divider()


# --------------------------------------------------
# SELLER PERFORMANCE TABLE
# --------------------------------------------------

st.subheader("📋 Seller Performance")

seller_performance = (
    seller_data["seller_sales"]
    .reset_index()
)

seller_performance.columns = [
    "Seller ID",
    "Revenue"
]

seller_performance["Orders"] = (
    seller_performance["Seller ID"]
    .map(seller_data["seller_orders"])
)

seller_performance["Items Sold"] = (
    filtered_sales
    .groupby("seller_id")["order_item_id"]
    .count()
    .reindex(seller_performance["Seller ID"])
    .values
)

seller_performance = seller_performance.head(10)

st.dataframe(
    seller_performance,
    width="stretch",
    hide_index=True
)


st.divider()


# --------------------------------------------------
# BUSINESS INTERPRETATION
# --------------------------------------------------

st.subheader("💡 Business Interpretation")

if not filtered_sales.empty:

    top_revenue_seller = (
        seller_data["seller_sales"].index[0]
        if not seller_data["seller_sales"].empty
        else "N/A"
    )

    top_order_seller = (
        seller_data["seller_orders"].index[0]
        if not seller_data["seller_orders"].empty
        else "N/A"
    )

    st.write(
        f"""
        - The selected data contains **{seller_data['total_sellers']:,} sellers**.
        - Total seller revenue is **₹{seller_data['seller_sales'].sum():,.2f}**.
        - Sellers handled **{filtered_sales['order_id'].nunique():,} orders**
        in the selected data.
        - A total of **{len(filtered_sales):,} items** were sold.
        - Seller **{top_revenue_seller}** generated the highest revenue
        among the displayed sellers.
        - Seller **{top_order_seller}** handled the highest number of orders
        among the displayed sellers.
        """
    )

else:

    st.warning(
        "No seller data is available for the selected filters."
    )