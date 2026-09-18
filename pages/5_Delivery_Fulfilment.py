import streamlit as st
import pandas as pd

from src.data_loader import load_data
from src.data_model import create_sales_model
from src.delivery_analysis import delivery_kpis


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Delivery & Fulfilment Analysis",
    page_icon="🚚",
    layout="wide"
)


# --------------------------------------------------
# LOAD & CACHE SALES MODEL
# --------------------------------------------------

@st.cache_data(show_spinner="Loading delivery data...")
def get_sales_data():

    data = load_data()

    sales = create_sales_model(data)

    return sales


sales = get_sales_data()


# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("🚚 Delivery & Fulfilment Analysis")

st.write(
    "Business Question: "
    "How efficiently are orders being delivered, "
    "and where are delivery delays occurring?"
)


# --------------------------------------------------
# FILTERS
# --------------------------------------------------

st.subheader("🔎 Delivery Filters")

col1, col2 = st.columns(2)

with col1:

    selected_customer_state = st.multiselect(
        "Select Customer State",
        sorted(
            sales["customer_state"]
            .dropna()
            .unique()
        )
    )

with col2:

    selected_seller_state = st.multiselect(
        "Select Seller State",
        sorted(
            sales["seller_state"]
            .dropna()
            .unique()
        )
    )


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_sales = sales

if selected_customer_state:

    filtered_sales = filtered_sales[
        filtered_sales["customer_state"].isin(
            selected_customer_state
        )
    ]


if selected_seller_state:

    filtered_sales = filtered_sales[
        filtered_sales["seller_state"].isin(
            selected_seller_state
        )
    ]


# --------------------------------------------------
# DELIVERY ANALYSIS
# --------------------------------------------------

delivery_data = delivery_kpis(filtered_sales)


st.divider()


# --------------------------------------------------
# DELIVERY KPIs
# --------------------------------------------------

st.subheader("📊 Delivery & Fulfilment KPIs")

col1, col2, col3, col4 = st.columns(4)


with col1:

    average_delivery = delivery_data[
        "average_delivery_days"
    ]

    if pd.isna(average_delivery):
        average_delivery = 0

    st.metric(
        "Average Delivery Days",
        f"{average_delivery:.2f}"
    )


with col2:

    st.metric(
        "On-Time Delivery Rate",
        f"{delivery_data['on_time_percentage']:.2f}%"
    )


with col3:

    st.metric(
        "Late Delivery Rate",
        f"{delivery_data['late_percentage']:.2f}%"
    )


with col4:

    average_delay = delivery_data[
        "average_delay"
    ]

    if pd.isna(average_delay):
        average_delay = 0

    st.metric(
        "Average Delay",
        f"{average_delay:.2f} days"
    )


st.divider()


# --------------------------------------------------
# DELIVERY PERFORMANCE BY CUSTOMER STATE
# --------------------------------------------------

st.subheader("📍 Average Delivery Days by Customer State")

delivery_by_state = (
    delivery_data["delivery_by_state"]
    .reset_index()
)

delivery_by_state.columns = [
    "Customer State",
    "Average Delivery Days"
]

st.bar_chart(
    delivery_by_state.set_index("Customer State"),
    y="Average Delivery Days",
    width="stretch"
)


st.divider()


# --------------------------------------------------
# DELIVERY PERFORMANCE BY SELLER STATE
# --------------------------------------------------

st.subheader("🏪 Average Delivery Days by Seller State")

delivery_by_seller_state = (
    delivery_data["delivery_by_seller_state"]
    .reset_index()
)

delivery_by_seller_state.columns = [
    "Seller State",
    "Average Delivery Days"
]

st.bar_chart(
    delivery_by_seller_state.set_index("Seller State"),
    y="Average Delivery Days",
    width="stretch"
)


st.divider()


# --------------------------------------------------
# DELIVERY PERFORMANCE TABLE
# --------------------------------------------------

st.subheader("📋 Delivery Performance")

delivery_summary = pd.DataFrame({

    "Metric": [
        "Average Delivery Days",
        "On-Time Delivery Rate",
        "Late Delivery Rate",
        "Average Delay"
    ],

    "Value": [
        f"{average_delivery:.2f} days",
        f"{delivery_data['on_time_percentage']:.2f}%",
        f"{delivery_data['late_percentage']:.2f}%",
        f"{average_delay:.2f} days"
    ]
})

st.dataframe(
    delivery_summary,
    width="stretch",
    hide_index=True
)


st.divider()


# --------------------------------------------------
# BUSINESS INTERPRETATION
# --------------------------------------------------

st.subheader("💡 Business Interpretation")

st.markdown(
    f"""
- The average delivery time in the selected data is
  **{average_delivery:.2f} days**.

- The on-time delivery rate is
  **{delivery_data['on_time_percentage']:.2f}%**.

- The late delivery rate is
  **{delivery_data['late_percentage']:.2f}%**.

- The average delay among late deliveries is
  **{average_delay:.2f} days**.
"""
)