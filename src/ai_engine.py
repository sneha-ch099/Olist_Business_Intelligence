import pandas as pd
import streamlit as st
from google import genai


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


# ============================================================
# CUSTOMER AI ANALYSIS
# ============================================================

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


# ============================================================
# SALES AI ANALYSIS
# ============================================================

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

    # Sort from highest sales to lowest sales
    monthly_sales = monthly_sales.sort_values(
        "Sales",
        ascending=False
    ).reset_index(drop=True)

    # Format month for better display
    monthly_sales["Month"] = (
        monthly_sales["Month"]
        .dt.strftime("%B %Y")
    )

    return monthly_sales


# ============================================================
# PRODUCT AI ANALYSIS
# ============================================================

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

    # Data-based threshold
    high_sales_threshold = product_data["sales"].median()

    result = product_data[
        (product_data["sales"] >= high_sales_threshold)
        &
        (product_data["average_rating"] < 3)
    ].sort_values(
        "sales",
        ascending=False
    )

    return result


# ============================================================
# SELLER AI ANALYSIS
# ============================================================

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


# ============================================================
# DELIVERY AI ANALYSIS
# ============================================================

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
        .dropna(
            subset=[
                "customer_state",
                "delay_days"
            ]
        )
        .groupby("customer_state")
        .agg(
            total_delivered_orders=(
                "order_id",
                "nunique"
            ),
            late_orders=(
                "delay_days",
                lambda x: (x > 0).sum()
            )
        )
        .reset_index()
    )

    delivery_data["late_delivery_rate"] = (
        delivery_data["late_orders"]
        /
        delivery_data["total_delivered_orders"]
    ) * 100

    return delivery_data.sort_values(
        "late_delivery_rate",
        ascending=False
    ).reset_index(drop=True)


# ============================================================
# CROSS-ANALYSIS:
# DELIVERY & REVIEW SCORE
# ============================================================

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
        .dropna(
            subset=[
                "delay_days",
                "review_score"
            ]
        )
        .assign(
            delivery_status=lambda x:
            x["delay_days"].apply(
                lambda value:
                "Late"
                if value > 0
                else "On-Time"
            )
        )
        .groupby("delivery_status")
        .agg(
            orders=(
                "order_id",
                "nunique"
            ),
            average_review_score=(
                "review_score",
                "mean"
            )
        )
        .reset_index()
    )

    return analysis


# ============================================================
# GEMINI BUSINESS EXPLANATION
# ============================================================

def generate_ai_explanation(question, evidence):

    prompt = f"""
You are a Business Intelligence Analyst analyzing the
Olist e-commerce dataset.

MANAGER'S QUESTION:
{question}

CALCULATED DATA EVIDENCE:
{evidence}


============================================================
STRICT DATA RULES
============================================================

1. Use ONLY the information contained in the calculated
   data evidence above.

2. Do NOT invent facts, numbers, causes, events, or
   explanations.

3. The evidence shows OBSERVED DATA PATTERNS only.
   Do not treat a pattern as proof of its cause.

4. NEVER claim that sales were caused or driven by:
   - Black Friday
   - Christmas
   - holidays
   - promotions
   - discounts
   - advertising
   - marketing campaigns
   - seasonal shopping
   - customer behavior
   - any external event

   UNLESS that information is explicitly present in
   the calculated evidence.

5. Do NOT describe the business as:
   - a startup
   - growing
   - successful
   - scaling
   - mature
   - failing
   - declining

   unless the evidence explicitly proves it.

6. Do NOT use causal phrases such as:
   "because of"
   "caused by"
   "driven by"
   "due to"
   "resulted from"
   "the reason was"
   "what drove"

   when the evidence does not establish causation.

7. If the cause cannot be determined from the evidence,
   explicitly state:

   "The available dataset does not contain enough
   information to determine the cause."

8. ALL monetary values are in INDIAN RUPEES.

9. ALWAYS use the ₹ symbol for monetary values.

10. NEVER use:
    $
    USD
    US$
    dollars
    dollar

11. Sales/revenue must NEVER be described as net profit.

12. Do not change, estimate, round, or invent numerical
    values from the evidence.

13. Recommendations must be based on the observed data,
    not on assumptions about marketing, promotions,
    holidays, or external events.


============================================================
RESPONSE FORMAT
============================================================

### 1. Direct Answer

Answer the manager's question directly using the
calculated evidence.

### 2. Key Evidence

Mention the most important figures that support
the answer.

### 3. Business Patterns

Describe only patterns that are directly visible
in the provided evidence.

Use wording such as:
- "The data shows..."
- "The highest value was..."
- "Several months recorded..."
- "The evidence indicates..."

Do NOT explain why the pattern occurred unless
the evidence explicitly provides the reason.

### 4. Practical Business Recommendation

Give 1–3 practical recommendations based directly
on the observed data.

Good examples include:
- investigate high-performing products
- examine high-performing sellers
- monitor high-sales periods
- investigate unusual or missing values
- compare customer or delivery performance

Do NOT recommend repeating a marketing campaign,
promotion, holiday strategy, or discount unless the
evidence explicitly contains information about it.

### 5. Data Limitation

Briefly explain what cannot be concluded from
the available evidence.

For example:

"The dataset shows the sales pattern, but it does
not contain enough information to determine the
external factors that caused the difference."


============================================================
STYLE
============================================================

Use simple, professional business language.

Do not over-explain.

Do not repeat the entire evidence table.

Do not make unsupported assumptions.

Remember:

DATA FIRST, INTERPRETATION SECOND.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        result = response.text or ""

        # ====================================================
        # FINAL CURRENCY CONVERSION
        # ====================================================

        # Convert every common dollar representation
        # to Indian Rupee symbol.
        result = result.replace("USD", "₹")
        result = result.replace("US$", "₹")
        result = result.replace("$", "₹")
        result = result.replace("dollars", "₹")
        result = result.replace("Dollars", "₹")
        result = result.replace("dollar", "₹")
        result = result.replace("Dollar", "₹")

        # Remove accidental duplicate rupee symbols
        result = result.replace("₹₹", "₹")

        return result

    except Exception as e:

        return (
            "Gemini is temporarily unavailable right now. "
            "The calculated data analysis was completed "
            "successfully, but the AI explanation could "
            "not be generated. Please try again later."
        )