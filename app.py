import streamlit as st
import pandas as pd
import altair as alt

from src.data_loader import load_data
from src.data_cleaning import clean_data
from src.data_model import create_sales_model
from src.dashboard_filters import apply_dashboard_filters
from src.customer_analysis import customer_kpis
from src.sales_analysis import sales_kpis
from src.product_analysis import product_kpis
from src.seller_analysis import seller_kpis
from src.delivery_analysis import delivery_kpis


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Olist Business Intelligence",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# LOAD AND PREPARE DATA
# ============================================================

@st.cache_data
def prepare_data():

    data = load_data()

    cleaned_data = clean_data(data)

    sales = create_sales_model(cleaned_data)

    return cleaned_data, sales


data, sales = prepare_data()


# ============================================================
# NEW: Apply interactive dashboard filters
# ============================================================

sales = apply_dashboard_filters(sales)


# ============================================================
# ORIGINAL KPI CALCULATIONS
# ============================================================

customer_data = customer_kpis(data)
sales_data = sales_kpis(sales)
product_data = product_kpis(sales)
seller_data = seller_kpis(sales)
delivery_data = delivery_kpis(sales)


# ============================================================
# HEADER
# ============================================================

st.title("📊 Olist Business Intelligence Dashboard")

st.markdown(
    """
    ### Executive Business Overview

    Monitor sales, customers, products, sellers and delivery
    performance from one interactive dashboard.
    """
)


# ============================================================
# DASHBOARD FILTERS
# ============================================================

st.subheader("🔎 Dashboard Filters")

filter_col1, filter_col2 = st.columns(2)


with filter_col1:

    selected_state = st.selectbox(
        "Customer State",
        ["All"]
        + sorted(
            sales["customer_state"]
            .dropna()
            .unique()
            .tolist()
        )
    )


with filter_col2:

    selected_category = st.selectbox(
        "Product Category",
        ["All"]
        + sorted(
            sales[
                "product_category_name_english"
            ]
            .dropna()
            .unique()
            .tolist()
        )
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_sales = sales.copy()


if selected_state != "All":

    filtered_sales = filtered_sales[
        filtered_sales["customer_state"]
        == selected_state
    ]


if selected_category != "All":

    filtered_sales = filtered_sales[
        filtered_sales[
            "product_category_name_english"
        ]
        == selected_category
    ]


# ============================================================
# FILTERED KPIs
# ============================================================

filtered_sales_data = sales_kpis(
    filtered_sales
)


filtered_customer_data = {
    "total_customers":
        filtered_sales[
            "customer_unique_id"
        ].nunique()
}


filtered_product_data = product_kpis(
    filtered_sales
)


filtered_seller_data = seller_kpis(
    filtered_sales
)


filtered_delivery_data = delivery_kpis(
    filtered_sales
)


# ============================================================
# EXECUTIVE PERFORMANCE
# ============================================================

st.divider()

st.subheader("📌 Executive Performance")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "💰 Total Revenue",
        f"₹{filtered_sales_data['total_revenue']:,.2f}"
    )


with col2:

    st.metric(
        "🛒 Total Orders",
        f"{filtered_sales_data['total_orders']:,}"
    )


with col3:

    st.metric(
        "👥 Total Customers",
        f"{filtered_customer_data['total_customers']:,}"
    )


with col4:

    st.metric(
        "📦 Average Order Value",
        f"₹{filtered_sales_data['average_order_value']:,.2f}"
    )


# ============================================================
# BUSINESS SNAPSHOT
# ============================================================

st.subheader("📊 Business Snapshot")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🛍️ Products",
        f"{filtered_product_data['total_products']:,}"
    )


with col2:

    st.metric(
        "🏪 Sellers",
        f"{filtered_seller_data['total_sellers']:,}"
    )


with col3:

    st.metric(
        "🚚 Avg Delivery",
        f"{filtered_delivery_data['average_delivery_days']:.2f} days"
    )


with col4:

    st.metric(
        "⏱️ On-Time Delivery",
        f"{filtered_delivery_data['on_time_percentage']:.2f}%"
    )


# ============================================================
# WHAT NEEDS ATTENTION?
# ============================================================

st.divider()

st.subheader("🚨 What Needs Attention?")


attention_items = []


# ------------------------------------------------------------
# DELIVERY CHECK
# ------------------------------------------------------------

on_time_rate = filtered_delivery_data[
    "on_time_percentage"
]


if on_time_rate < 75:

    attention_items.append(
        f"🚚 **Delivery performance requires attention:** "
        f"on-time delivery is currently "
        f"**{on_time_rate:.2f}%**."
    )

elif on_time_rate < 90:

    attention_items.append(
        f"⚠️ **Delivery performance should be monitored:** "
        f"on-time delivery is "
        f"**{on_time_rate:.2f}%**."
    )

else:

    attention_items.append(
        f"✅ **Delivery performance:** "
        f"on-time delivery is "
        f"**{on_time_rate:.2f}%**."
    )


# ------------------------------------------------------------
# TOP SELLER
# ------------------------------------------------------------

seller_sales = filtered_seller_data[
    "seller_sales"
]


if not seller_sales.empty:

    top_seller_id = seller_sales.index[0]

    top_seller_value = seller_sales.iloc[0]

    short_seller = str(
        top_seller_id
    )[:8]

    attention_items.append(
        f"🏪 **Top seller:** "
        f"`{short_seller}...` "
        f"with item sales of "
        f"**₹{top_seller_value:,.2f}**."
    )


# ------------------------------------------------------------
# TOP CATEGORY
# ------------------------------------------------------------

category_sales = filtered_product_data[
    "category_sales"
]


if not category_sales.empty:

    top_category = category_sales.index[0]

    top_category_value = category_sales.iloc[0]

    attention_items.append(
        f"📦 **Top product category:** "
        f"**{top_category}** "
        f"with item sales of "
        f"**₹{top_category_value:,.2f}**."
    )


# ------------------------------------------------------------
# DISPLAY ATTENTION ITEMS
# ------------------------------------------------------------

for item in attention_items:

    st.info(item)


# ============================================================
# MONTHLY SALES TREND
# ============================================================

st.divider()

st.subheader("📈 Monthly Sales Trend")


monthly_sales_chart = (
    filtered_sales_data[
        "monthly_sales"
    ].copy()
)


monthly_sales_chart.index = (
    monthly_sales_chart.index
    .strftime("%Y-%m")
)


st.line_chart(
    monthly_sales_chart,
    width="stretch"
)


# ============================================================
# SALES INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Sales Insights")

monthly_sales_insights = filtered_sales_data["monthly_sales"].copy()

# Remove months with zero or negative sales
active_monthly_sales = monthly_sales_insights[
    monthly_sales_insights > 0
]

# Highest active sales period
if not active_monthly_sales.empty:

    highest_period = active_monthly_sales.idxmax()
    highest_value = active_monthly_sales.max()

    # Lowest active sales period
    lowest_period = active_monthly_sales.idxmin()
    lowest_value = active_monthly_sales.min()

    insight_col1, insight_col2 = st.columns(2)

    # --------------------------------------------------------
    # HIGHEST SALES
    # --------------------------------------------------------

    with insight_col1:

        st.success(
            f"""
            **📈 Highest Sales Period**

            📅 {highest_period.strftime("%B %Y")}

            💰 ₹{highest_value:,.2f}
            """
        )

    # --------------------------------------------------------
    # LOWEST ACTIVE SALES
    # --------------------------------------------------------

    with insight_col2:

        st.warning(
            f"""
            **📉 Lowest Active Sales Period**

            📅 {lowest_period.strftime("%B %Y")}

            💰 ₹{lowest_value:,.2f}

            *Zero-sales/incomplete periods are excluded.*
            """
        )

else:

    st.info(
        "No active sales periods are available for the selected filters."
    )


# ============================================================
# WHAT-IF BUSINESS SIMULATOR
# ============================================================

st.divider()

st.subheader("🎯 What-If Business Simulator")

st.markdown(
    """
    Use the slider to see how a hypothetical increase in orders
    could affect recorded sales.

    **Note:** This is a scenario analysis based on the assumption
    that revenue changes proportionally with the number of orders.
    It is not a prediction of future revenue.
    """
)

# ------------------------------------------------------------
# ORDER INCREASE SLIDER
# ------------------------------------------------------------

order_increase = st.slider(
    "📦 Hypothetical Order Increase (%)",
    min_value=0,
    max_value=50,
    value=10,
    step=5
)

# ------------------------------------------------------------
# CURRENT REVENUE
# ------------------------------------------------------------

current_revenue = filtered_sales_data["total_revenue"]

# ------------------------------------------------------------
# CALCULATE WHAT-IF REVENUE
# ------------------------------------------------------------

revenue_increase = (
    current_revenue * order_increase / 100
)

what_if_revenue = (
    current_revenue + revenue_increase
)

# ------------------------------------------------------------
# DISPLAY RESULTS
# ------------------------------------------------------------

sim_col1, sim_col2, sim_col3 = st.columns(3)

with sim_col1:

    st.metric(
        "Current Recorded Sales",
        f"₹{current_revenue:,.2f}"
    )

with sim_col2:

    st.metric(
        "Estimated Additional Sales",
        f"₹{revenue_increase:,.2f}",
        delta=f"{order_increase}% scenario"
    )

with sim_col3:

    st.metric(
        "What-If Sales",
        f"₹{what_if_revenue:,.2f}",
        delta=f"₹{revenue_increase:,.2f}"
    )

# ------------------------------------------------------------
# CURRENT VS WHAT-IF CHART
# ------------------------------------------------------------

st.markdown("### 📊 Current vs What-If Sales")

chart_data = {
    "Current Sales": current_revenue,
    f"What-If (+{order_increase}%)": what_if_revenue
}

st.bar_chart(
    chart_data,
    width="stretch"
)

# ------------------------------------------------------------
# INTERPRETATION
# ------------------------------------------------------------

if order_increase == 0:

    st.info(
        "No increase has been selected. The scenario remains "
        "the same as the current recorded sales."
    )

else:

    st.success(
        f"""
        💡 **Scenario Insight:** If recorded sales increased
        proportionally with a hypothetical **{order_increase}%**
        increase in orders, sales would move from
        **₹{current_revenue:,.2f}** to approximately
        **₹{what_if_revenue:,.2f}**.

        This calculation is based only on the selected scenario
        and assumes revenue changes proportionally with orders.
        """
    )


# ============================================================
# TOP PRODUCT CATEGORIES BY SALES
# ============================================================

st.divider()

st.subheader("📦 Top Product Categories by Sales")

category_chart = (
    filtered_product_data["category_sales"]
    .head(10)
    .reset_index()
)

# Rename columns
category_chart = category_chart.rename(
    columns={
        "product_category_name_english": "Category",
        "item_total": "Sales"
    }
)

# Sort so highest sales appear at the top
category_chart = category_chart.sort_values(
    "Sales",
    ascending=True
)

# Create horizontal bar chart
category_bar = (
    alt.Chart(category_chart)
    .mark_bar()
    .encode(
        x=alt.X(
            "Sales:Q",
            title="Sales (₹)",
            axis=alt.Axis(format=",.0f")
        ),
        y=alt.Y(
            "Category:N",
            title="Product Category",
            sort=None
        ),
        tooltip=[
            alt.Tooltip(
                "Category:N",
                title="Category"
            ),
            alt.Tooltip(
                "Sales:Q",
                title="Sales",
                format=",.2f"
            )
        ]
    )
    .properties(
        height=400
    )
)

st.altair_chart(
    category_bar,
    use_container_width=True
)


# ============================================================
# TOP SELLERS BY SALES
# ============================================================

st.divider()

st.subheader("🏪 Top Sellers by Sales")

seller_chart = (
    filtered_seller_data["seller_sales"]
    .head(10)
    .reset_index()
)

# Create short seller IDs
seller_chart["Seller"] = (
    seller_chart["seller_id"]
    .astype(str)
    .str[:8]
    + "..."
)

# Rename sales column
seller_chart = seller_chart.rename(
    columns={
        "item_total": "Sales"
    }
)

# Sort lowest to highest so highest appears at top
seller_chart = seller_chart.sort_values(
    "Sales",
    ascending=True
)

# Create horizontal bar chart
seller_bar = (
    alt.Chart(seller_chart)
    .mark_bar()
    .encode(
        x=alt.X(
            "Sales:Q",
            title="Sales (₹)",
            axis=alt.Axis(format=",.0f")
        ),
        y=alt.Y(
            "Seller:N",
            title="Seller",
            sort=None
        ),
        tooltip=[
            alt.Tooltip(
                "Seller:N",
                title="Seller"
            ),
            alt.Tooltip(
                "Sales:Q",
                title="Sales",
                format=",.2f"
            )
        ]
    )
    .properties(
        height=400
    )
)

st.altair_chart(
    seller_bar,
    use_container_width=True
)


# ============================================================
# GEOGRAPHIC SALES ANALYSIS
# ============================================================

st.divider()

st.subheader("🗺️ Sales & Orders by Brazilian State")

state_analysis = (
    filtered_sales
    .dropna(subset=["customer_state"])
    .groupby("customer_state")
    .agg(
        sales=("item_total", "sum"),
        orders=("order_id", "nunique"),
        customers=("customer_unique_id", "nunique")
    )
    .reset_index()
)

state_analysis["average_order_value"] = (
    state_analysis["sales"]
    / state_analysis["orders"]
)

state_analysis = state_analysis.sort_values(
    "sales",
    ascending=False
)

# Display summary table
st.dataframe(
    state_analysis.rename(
        columns={
            "customer_state": "State",
            "sales": "Sales (₹)",
            "orders": "Orders",
            "customers": "Customers",
            "average_order_value": "Avg. Order Value (₹)"
        }
    ),
    use_container_width=True,
    hide_index=True
)

# State sales chart
state_chart = (
    alt.Chart(state_analysis.head(10))
    .mark_bar()
    .encode(
        x=alt.X(
            "sales:Q",
            title="Sales (₹)",
            axis=alt.Axis(format=",.0f")
        ),
        y=alt.Y(
            "customer_state:N",
            title="Brazilian State",
            sort="-x"
        ),
        tooltip=[
            alt.Tooltip(
                "customer_state:N",
                title="State"
            ),
            alt.Tooltip(
                "sales:Q",
                title="Sales",
                format=",.2f"
            ),
            alt.Tooltip(
                "orders:Q",
                title="Orders",
                format=","
            ),
            alt.Tooltip(
                "customers:Q",
                title="Customers",
                format=","
            ),
            alt.Tooltip(
                "average_order_value:Q",
                title="Avg. Order Value",
                format=",.2f"
            )
        ]
    )
    .properties(
        height=400
    )
)

st.altair_chart(
    state_chart,
    use_container_width=True
)


# ============================================================
# DELIVERY PERFORMANCE
# ============================================================

st.divider()

st.subheader("🚚 Delivery Performance by State")


delivery_chart = (
    filtered_delivery_data[
        "delivery_by_state"
    ]
    .head(10)
    .reset_index()
)


st.bar_chart(
    delivery_chart,
    x="customer_state",
    y="delivery_days",
    width="stretch"
)


# ============================================================
# MONTH-OVER-MONTH SALES COMPARISON
# ============================================================

st.divider()

st.header("📊 Month-over-Month Sales Comparison")

st.write(
    "Compare recorded sales across two months "
    "to understand how sales performance changed."
)

date_col = "order_purchase_timestamp"
sales_col = "price"

if date_col in sales.columns and sales_col in sales.columns:

    comparison_data = sales[[date_col, sales_col]].copy()

    comparison_data[date_col] = pd.to_datetime(
        comparison_data[date_col],
        errors="coerce"
    )

    comparison_data[sales_col] = pd.to_numeric(
        comparison_data[sales_col],
        errors="coerce"
    )

    comparison_data = comparison_data.dropna(
        subset=[date_col, sales_col]
    )

    if not comparison_data.empty:

        comparison_data["Month"] = (
            comparison_data[date_col].dt.to_period("M")
        )

        monthly_sales = (
            comparison_data.groupby("Month")[sales_col]
            .sum()
            .sort_index()
        )

        available_months = monthly_sales.index.tolist()

        if len(available_months) >= 2:

            month_labels = {
                month: str(month)
                for month in available_months
            }

            default_previous = len(available_months) - 2
            default_current = len(available_months) - 1

            col1, col2 = st.columns(2)

            with col1:
                previous_month = st.selectbox(
                    "Select First Month",
                    options=available_months,
                    index=default_previous,
                    format_func=lambda month: month.strftime("%B %Y"),
                    key="mom_first_month"
                )

            with col2:
                current_month = st.selectbox(
                    "Select Second Month",
                    options=available_months,
                    index=default_current,
                    format_func=lambda month: month.strftime("%B %Y"),
                    key="mom_second_month"
                )

            first_sales = float(monthly_sales.loc[previous_month])
            second_sales = float(monthly_sales.loc[current_month])

            if first_sales != 0:
                percentage_change = (
                    (second_sales - first_sales)
                    / abs(first_sales)
                ) * 100
            else:
                percentage_change = None

            metric1, metric2, metric3 = st.columns(3)

            metric1.metric(
                f"Sales — {previous_month.strftime('%b %Y')}",
                f"₹{first_sales:,.2f}"
            )

            metric2.metric(
                f"Sales — {current_month.strftime('%b %Y')}",
                f"₹{second_sales:,.2f}"
            )

            if percentage_change is not None:
                metric3.metric(
                    "Sales Change",
                    f"{percentage_change:+.2f}%",
                    delta=f"{second_sales - first_sales:+,.2f} ₹"
                )
            else:
                metric3.metric(
                    "Sales Change",
                    "N/A",
                    help="Percentage change cannot be calculated from a zero starting value."
                )
            
            chart_data = pd.DataFrame({
                "Month": [
                    previous_month.strftime("%b %Y"),
                    current_month.strftime("%b %Y")
                ],
                "Recorded Sales (₹)": [
                    first_sales,
                    second_sales
                ]
            })

            
            st.bar_chart(
                chart_data.set_index("Month"),
                horizontal=True
            )


            st.caption(
                "Sales are calculated by summing the order-item price "
                "values in the selected months. This is recorded sales, "
                "not net profit. The comparison uses the currently "
                "filtered sales data."
            )

        else:
            st.info(
                "At least two months of data are needed for comparison."
            )

    else:
        st.info("No valid sales records are available for comparison.")

else:
    st.warning(
        "The sales data must contain order_purchase_timestamp "
        "and price columns for this comparison."
    )


# ============================================================
# DASHBOARD INFORMATION
# ============================================================

st.divider()

st.subheader("ℹ️ Dashboard Information")

st.caption(
    "This dashboard uses calculated information from the "
    "Olist historical dataset. Revenue/sales represent "
    "recorded sales values and should not be interpreted "
    "as net profit."
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:10px;">
        <small>
        📊 Olist Business Intelligence |
        Customer • Sales • Product • Seller • Delivery • AI
        </small>
    </div>
    """,
    unsafe_allow_html=True
)