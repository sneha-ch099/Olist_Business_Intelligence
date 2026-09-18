import pandas as pd
import streamlit as st
from google import genai

# --------------------------------------------------
# GEMINI CLIENT
# --------------------------------------------------

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


# --------------------------------------------------
# CUSTOMER AI ANALYSIS
# --------------------------------------------------

def get_top_customers(data, top_n=10):

    customers = data["customers"]
    orders = data["orders"]

    customer_orders = orders.merge(
        customers[
            ["customer_id", "customer_unique_id"]
        ],
        on="customer_id",
        how="left"
    )

    result = (
        customer_orders
        .groupby("customer_unique_id")["order_id"]
        .nunique()
        .reset_index(name="orders")
        .sort_values(
            "orders",
            ascending=False
        )
        .head(top_n)
    )

    return result

# --------------------------------------------------
# SALES AI ANALYSIS
# --------------------------------------------------

def get_highest_sales_month(sales):

    sales = sales.copy()

    sales["order_purchase_timestamp"] = pd.to_datetime(
        sales["order_purchase_timestamp"],
        errors="coerce"
    )

    monthly_sales = (
        sales
        .dropna(subset=["order_purchase_timestamp"])
        .set_index("order_purchase_timestamp")
        .resample("ME")["item_total"]
        .sum()
        .reset_index()
    )

    monthly_sales.columns = [
        "Month",
        "Sales"
    ]

    monthly_sales = monthly_sales.sort_values(
        "Sales",
        ascending=False
    )

    return monthly_sales

# --------------------------------------------------
# PRODUCT AI ANALYSIS
# --------------------------------------------------

def get_products_high_sales_low_rating(sales):

    product_data = (
        sales
        .dropna(subset=["product_id"])
        .groupby("product_id")
        .agg(
            sales=("item_total", "sum"),
            average_rating=("review_score", "mean"),
            items_sold=("order_item_id", "count")
        )
        .reset_index()
    )

    # Use the median as the data-based threshold
    # for identifying relatively high sales.
    high_sales_threshold = product_data["sales"].median()

    result = product_data[
        (product_data["sales"] >= high_sales_threshold) &
        (product_data["average_rating"] < 3)
    ].sort_values(
        "sales",
        ascending=False
    )

    return result

# --------------------------------------------------
# SELLER AI ANALYSIS
# --------------------------------------------------

def get_top_sellers(sales, top_n=10):

    result = (
        sales
        .dropna(subset=["seller_id"])
        .groupby("seller_id")
        .agg(
            revenue=("item_total", "sum"),
            orders=("order_id", "nunique"),
            items_sold=("order_item_id", "count")
        )
        .reset_index()
        .sort_values(
            "revenue",
            ascending=False
        )
        .head(top_n)
    )

    return result

# --------------------------------------------------
# DELIVERY AI ANALYSIS
# --------------------------------------------------

def get_late_delivery_by_state(sales):

    sales = sales.copy()

    sales["order_delivered_customer_date"] = pd.to_datetime(
        sales["order_delivered_customer_date"],
        errors="coerce"
    )

    sales["order_estimated_delivery_date"] = pd.to_datetime(
        sales["order_estimated_delivery_date"],
        errors="coerce"
    )

    sales["delay_days"] = (
        sales["order_delivered_customer_date"]
        - sales["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400

    delivery_data = (
        sales
        .dropna(subset=["customer_state", "delay_days"])
        .groupby("customer_state")
        .agg(
            total_delivered_orders=("order_id", "nunique"),
            late_orders=("delay_days", lambda x: (x > 0).sum())
        )
        .reset_index()
    )

    delivery_data["late_delivery_rate"] = (
        delivery_data["late_orders"]
        / delivery_data["total_delivered_orders"]
    ) * 100

    return delivery_data.sort_values(
        "late_delivery_rate",
        ascending=False
    )

# --------------------------------------------------
# CROSS-ANALYSIS: DELIVERY & REVIEW SCORE
# --------------------------------------------------

def get_delivery_review_analysis(sales):

    sales = sales.copy()

    sales["order_delivered_customer_date"] = pd.to_datetime(
        sales["order_delivered_customer_date"],
        errors="coerce"
    )

    sales["order_estimated_delivery_date"] = pd.to_datetime(
        sales["order_estimated_delivery_date"],
        errors="coerce"
    )

    sales["delay_days"] = (
        sales["order_delivered_customer_date"]
        - sales["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400

    analysis = (
        sales
        .dropna(subset=["delay_days", "review_score"])
        .assign(
            delivery_status=lambda x: x["delay_days"].apply(
                lambda value: "Late" if value > 0 else "On-Time"
            )
        )
        .groupby("delivery_status")
        .agg(
            orders=("order_id", "nunique"),
            average_review_score=("review_score", "mean")
        )
        .reset_index()
    )

    return analysis

# --------------------------------------------------
# GEMINI BUSINESS EXPLANATION
# --------------------------------------------------

def generate_ai_explanation(question, evidence):

    prompt = f"""
You are a business intelligence analyst for an e-commerce company.

A manager asked:
{question}

The following information was calculated directly
from the Olist dataset using Pandas:

{evidence}

Explain the result in simple business language.

Your response should:
1. Directly answer the manager's question.
2. Use only the evidence provided.
3. Do not invent or change any numbers.
4. Highlight important business patterns.
5. Provide a practical business recommendation.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )
        return response.text

    except Exception as e:
        return (
            "Gemini is temporarily unavailable right now. "
            "The data analysis was completed successfully, "
            "but the AI explanation could not be generated. "
            "Please try again after a few minutes."
        )