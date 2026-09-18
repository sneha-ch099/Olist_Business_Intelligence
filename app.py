import streamlit as st
from src.data_loader import load_data
from src.data_cleaning import clean_data
from src.data_model import create_sales_model
from src.customer_analysis import customer_kpis
from src.sales_analysis import sales_kpis
from src.product_analysis import product_kpis
from src.seller_analysis import seller_kpis
from src.delivery_analysis import delivery_kpis


st.set_page_config(
    page_title="Olist Business Intelligence",
    page_icon="📊",
    layout="wide"
)


@st.cache_data
def prepare_data():
    data = load_data()
    cleaned_data = clean_data(data)
    sales = create_sales_model(cleaned_data)

    return cleaned_data, sales


data, sales = prepare_data()

customer_data = customer_kpis(data)
sales_data = sales_kpis(sales)
product_data = product_kpis(sales)
seller_data = seller_kpis(sales)
delivery_data = delivery_kpis(sales)


st.title("📊 Olist Business Intelligence Dashboard")

st.markdown(
    """
    ### Business Intelligence Overview
    Explore customers, sales, products, sellers, and delivery performance.
    """
)

# Interactive Filters
st.subheader("🔎 Dashboard Filters")

filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    selected_state = st.selectbox(
        "Customer State",
        ["All"] + sorted(sales["customer_state"].dropna().unique().tolist())
    )

with filter_col2:
    selected_category = st.selectbox(
        "Product Category",
        ["All"] + sorted(
            sales["product_category_name_english"]
            .dropna()
            .unique()
            .tolist()
        )
    )

# Apply filters
filtered_sales = sales.copy()

if selected_state != "All":
    filtered_sales = filtered_sales[
        filtered_sales["customer_state"] == selected_state
    ]

if selected_category != "All":
    filtered_sales = filtered_sales[
        filtered_sales["product_category_name_english"] == selected_category
    ]

# Recalculate KPIs using filtered data
filtered_sales_data = sales_kpis(filtered_sales)

filtered_customer_data = {
    "total_customers": filtered_sales["customer_unique_id"].nunique()
}

filtered_product_data = product_kpis(filtered_sales)
filtered_seller_data = seller_kpis(filtered_sales)
filtered_delivery_data = delivery_kpis(filtered_sales)


# KPI cards

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Revenue",
        f"₹{filtered_sales_data['total_revenue']:,.2f}"
    )

with col2:
    st.metric(
        "Total Orders",
        f"{filtered_sales_data['total_orders']:,}"
    )

with col3:
    st.metric(
        "Total Customers",
        f"{filtered_customer_data['total_customers']:,}"
    )

with col4:
    st.metric(
        "Avg. Order Value",
        f"₹{filtered_sales_data['average_order_value']:,.2f}"
    )

# Monthly Sales Trend
st.divider()

st.subheader("📈 Monthly Sales Trend")

monthly_sales_chart = filtered_sales_data["monthly_sales"].copy()
monthly_sales_chart.index = monthly_sales_chart.index.strftime("%Y-%m")

st.line_chart(
    monthly_sales_chart,
    width="stretch"
)

st.divider()


st.subheader("📦 Business Overview")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total Products",
        f"{filtered_product_data['total_products']:,}"
    )

    st.metric(
        "Total Sellers",
        f"{filtered_seller_data['total_sellers']:,}"
    )

with col2:
    st.metric(
        "Average Delivery Days",
        f"{filtered_delivery_data['average_delivery_days']:.2f}"
    )

    st.metric(
        "On-Time Delivery",
        f"{filtered_delivery_data['on_time_percentage']:.2f}%"
    )


st.divider()

# Top Product Categories by Sales
st.subheader("💰 Top Product Categories by Sales")

category_chart = (
    filtered_product_data["category_sales"]
    .head(10)
    .reset_index()
)

st.bar_chart(
    category_chart,
    x="product_category_name_english",
    y="item_total",
    width="stretch"
)


# Top Sellers by Sales
st.subheader("🏪 Top Sellers by Sales")

seller_chart = (
    filtered_seller_data["seller_sales"]
    .head(10)
    .reset_index()
)

# Shorten seller IDs for better readability
seller_chart["Seller"] = (
    seller_chart["seller_id"].str[:8] + "..."
)

st.bar_chart(
    seller_chart,
    x="Seller",
    y="item_total",
    width="stretch"
)


# Delivery Performance by State
st.subheader("🚚 Delivery Performance by State")

delivery_chart = (
    filtered_delivery_data["delivery_by_state"]
    .head(10)
    .reset_index()
)

st.bar_chart(
    delivery_chart,
    x="customer_state",
    y="delivery_days",
    width="stretch"
)