import streamlit as st
import pandas as pd

from src.data_loader import load_data
from src.customer_analysis import customer_analysis


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Analysis",
    page_icon="👤",
    layout="wide"
)


# --------------------------------------------------
# LOAD DATA - CACHED FOR BETTER PERFORMANCE
# --------------------------------------------------

@st.cache_data(show_spinner="Loading customer data...")
def get_customer_data():
    data = load_data()

    customers = data["customers"].copy()
    orders = data["orders"].copy()

    return customers, orders


customers, orders = get_customer_data()


# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("👤 Customer Analysis")

st.write(
    "Business Question: "
    "Who are our most valuable customers and how frequently do they purchase?"
)


# --------------------------------------------------
# CUSTOMER FILTER
# --------------------------------------------------

st.subheader("🔎 Customer Filter")

selected_state = st.multiselect(
    "Select Customer State",
    sorted(
        customers["customer_state"]
        .dropna()
        .unique()
    )
)


# --------------------------------------------------
# APPLY CUSTOMER STATE FILTER
# --------------------------------------------------

if selected_state:

    filtered_customers = customers[
        customers["customer_state"].isin(selected_state)
    ]

    filtered_customer_ids = filtered_customers["customer_id"].unique()

    filtered_orders = orders[
        orders["customer_id"].isin(filtered_customer_ids)
    ]

else:

    filtered_customers = customers
    filtered_orders = orders


# --------------------------------------------------
# CUSTOMER ANALYSIS
# --------------------------------------------------

customer_data = customer_analysis({
    "customers": filtered_customers,
    "orders": filtered_orders
})


st.divider()


# --------------------------------------------------
# CUSTOMER KPIs
# --------------------------------------------------

st.subheader("📊 Customer KPIs")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Customers",
        f"{customer_data['total_customers']:,}"
    )

with col2:
    st.metric(
        "Repeat Customers",
        f"{customer_data['repeat_customers']:,}"
    )

with col3:
    st.metric(
        "Repeat Customer Rate",
        f"{customer_data['repeat_rate']:.2f}%"
    )


st.divider()


# --------------------------------------------------
# CUSTOMER LOCATION OVERVIEW
# --------------------------------------------------

st.subheader("🌎 Customer Location Overview")

col1, col2 = st.columns(2)

with col1:

    total_states = filtered_customers[
        "customer_state"
    ].nunique()

    st.metric(
        "Customer States",
        f"{total_states:,}"
    )

with col2:

    total_cities = filtered_customers[
        "customer_city"
    ].nunique()

    st.metric(
        "Customer Cities",
        f"{total_cities:,}"
    )


st.divider()


# --------------------------------------------------
# CUSTOMERS BY STATE
# --------------------------------------------------

st.subheader("📍 Customers by State")

customers_by_state = (
    filtered_customers
    .groupby("customer_state")["customer_unique_id"]
    .nunique()
    .sort_values(ascending=False)
    .reset_index()
)

customers_by_state.columns = [
    "Customer State",
    "Customers"
]

st.bar_chart(
    customers_by_state.set_index("Customer State"),
    y="Customers",
    width="stretch"
)


st.divider()


# --------------------------------------------------
# TOP CUSTOMER CITIES
# --------------------------------------------------

st.subheader("🏙️ Top Customer Cities")

customers_by_city = (
    filtered_customers
    .groupby("customer_city")["customer_unique_id"]
    .nunique()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

customers_by_city.columns = [
    "Customer City",
    "Customers"
]

st.dataframe(
    customers_by_city,
    width="stretch",
    hide_index=True
)


st.divider()


# --------------------------------------------------
# REPEAT CUSTOMER SUMMARY
# --------------------------------------------------

st.subheader("🔄 Repeat Customer Summary")

repeat_summary = pd.DataFrame({
    "Metric": [
        "Total Customers",
        "Repeat Customers",
        "Repeat Customer Rate"
    ],
    "Value": [
        f"{customer_data['total_customers']:,}",
        f"{customer_data['repeat_customers']:,}",
        f"{customer_data['repeat_rate']:.2f}%"
    ]
})

st.dataframe(
    repeat_summary,
    width="stretch",
    hide_index=True
)


st.divider()


# --------------------------------------------------
# BUSINESS INTERPRETATION
# --------------------------------------------------

st.subheader("💡 Business Interpretation")

st.write(
    f"""
    - The dashboard shows **{customer_data['total_customers']:,} total customers**
    in the selected data.
    - **{customer_data['repeat_customers']:,} customers** made more than one purchase.
    - The repeat customer rate is **{customer_data['repeat_rate']:.2f}%**.
    - The selected data covers **{filtered_customers['customer_state'].nunique():,} customer states**
    and **{filtered_customers['customer_city'].nunique():,} customer cities**.
    """
)