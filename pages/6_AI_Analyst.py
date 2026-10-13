import streamlit as st
import pandas as pd

from src.data_loader import load_data
from src.data_model import create_sales_model
from src.ai_engine import (
    get_top_customers,
    get_highest_sales_month,
    get_products_high_sales_low_rating,
    get_top_sellers,
    get_late_delivery_by_state,
    get_delivery_review_analysis,
    generate_ai_explanation
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="GenAI Business Analyst",
    page_icon="🤖",
    layout="wide"
)


# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data(show_spinner="Preparing business analysis data...")
def get_ai_data():

    data = load_data()
    sales = create_sales_model(data)

    return data, sales


data, sales = get_ai_data()


# ==================================================
# PAGE HEADER
# ==================================================

st.title("🤖 GenAI Business Analyst")

st.markdown(
    """
    ### Turn Olist data into business insights

    Select a business question and let Python calculate the
    evidence before Gemini provides the business interpretation.
    """
)

st.info(
    "💡 Python calculates the business evidence first. "
    "Gemini only interprets the calculated evidence."
)


# ==================================================
# QUICK BUSINESS QUESTIONS
# ==================================================

st.divider()

st.subheader("⚡ Quick Business Questions")

st.caption(
    "Choose a business area to investigate."
)

quick_questions = [
    ("👥", "Customer Analysis",
     "Top customers by number of orders"),

    ("📈", "Sales Analysis",
     "Highest-sales month"),

    ("📦", "Product Analysis",
     "High-sales, low-rated products"),

    ("🏪", "Seller Analysis",
     "Highest-revenue sellers"),

    ("🚚", "Delivery Analysis",
     "Highest late-delivery states"),

    ("⭐", "Customer Experience",
     "Delivery vs review scores")
]

quick_cols = st.columns(3)

for i, (icon, title, description) in enumerate(quick_questions):

    with quick_cols[i % 3]:

        st.markdown(
            f"""
            <div style="
                background-color:#19324a;
                padding:18px;
                border-radius:12px;
                margin-bottom:15px;
                min-height:120px;
            ">
                <h4 style="color:#4da6ff; margin-bottom:8px;">
                    {icon} {title}
                </h4>
                <p style="color:white;">
                    {description}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ==================================================
# BUSINESS QUESTION
# ==================================================

st.divider()

st.subheader("💬 Ask the Business Analyst")

questions = [
    "Who are our top customers by number of orders?",
    "Which month had the highest sales?",
    "Which products have high sales but low ratings?",
    "Which sellers generated the highest revenue?",
    "Which states have the highest late delivery rate?",
    "Do late deliveries appear to be associated with lower review scores?"
]

question = st.selectbox(
    "Select a business question",
    questions
)


# ==================================================
# ANALYSIS AREA
# ==================================================

analysis_area = {

    "Who are our top customers by number of orders?":
        "👥 Customer Intelligence",

    "Which month had the highest sales?":
        "📈 Sales Intelligence",

    "Which products have high sales but low ratings?":
        "📦 Product Intelligence",

    "Which sellers generated the highest revenue?":
        "🏪 Seller Intelligence",

    "Which states have the highest late delivery rate?":
        "🚚 Delivery Intelligence",

    "Do late deliveries appear to be associated with lower review scores?":
        "⭐ Customer Experience"
}

st.write(
    "**Analysis Area:**",
    analysis_area[question]
)

st.caption(
    "Python calculates the evidence first. "
    "Gemini then interprets only that evidence."
)


# ==================================================
# ANALYZE BUTTON
# ==================================================

st.divider()

analyze_button = st.button(
    "🔍 Analyze Business Question",
    type="primary",
    use_container_width=True
)


# ==================================================
# ANALYSIS
# ==================================================

if analyze_button:

    # ------------------------------------------------
    # CALCULATE EVIDENCE
    # ------------------------------------------------

    with st.spinner("Calculating business evidence..."):

        if question == "Who are our top customers by number of orders?":

            evidence = get_top_customers(
                data,
                top_n=10
            )

        elif question == "Which month had the highest sales?":

            evidence = get_highest_sales_month(
                sales
            )

        elif question == "Which products have high sales but low ratings?":

            evidence = get_products_high_sales_low_rating(
                sales
            )

        elif question == "Which sellers generated the highest revenue?":

            evidence = get_top_sellers(
                sales,
                top_n=10
            )

        elif question == "Which states have the highest late delivery rate?":

            evidence = get_late_delivery_by_state(
                sales
            )

        elif question == (
            "Do late deliveries appear to be associated "
            "with lower review scores?"
        ):

            evidence = get_delivery_review_analysis(
                sales
            )

        else:

            evidence = None


    # ==================================================
    # CHECK EVIDENCE
    # ==================================================

    if evidence is None or evidence.empty:

        st.warning(
            "No sufficient data was found for this analysis."
        )

        st.stop()


    # ==================================================
    # SAVE RAW EVIDENCE
    # ==================================================

    raw_evidence = evidence.copy()

    display_evidence = evidence.copy()


    # ==================================================
    # FORMAT DATES
    # ==================================================

    for column in display_evidence.columns:

        if pd.api.types.is_datetime64_any_dtype(
            display_evidence[column]
        ):

            display_evidence[column] = (
                display_evidence[column]
                .dt.strftime("%B %Y")
            )


    # ==================================================
    # FORMAT MONEY VALUES
    # ==================================================

    money_columns = [
        "Sales",
        "sales",
        "revenue",
        "item_total"
    ]

    for column in money_columns:

        if column in display_evidence.columns:

            display_evidence[column] = display_evidence[column].apply(
                lambda x:
                f"₹{x:,.2f}"
                if pd.notna(x)
                else "—"
            )


    # ==================================================
    # DATA EVIDENCE HEADER
    # ==================================================

    st.divider()

    st.subheader("📊 Data Evidence")

    st.write(
        "The following results were calculated directly "
        "from the Olist dataset."
    )


    # ==================================================
    # KPI CARDS
    # ==================================================

    evidence_col1, evidence_col2, evidence_col3 = st.columns(3)

    with evidence_col1:

        st.metric(
            "Rows Analyzed",
            f"{len(display_evidence):,}"
        )

    with evidence_col2:

        st.metric(
            "Data Fields",
            f"{len(display_evidence.columns):,}"
        )

    with evidence_col3:

        st.metric(
            "Analysis Area",
            analysis_area[question]
        )


    # ==================================================
    # DETAILED RESULTS
    # ==================================================

    st.subheader("📋 Detailed Results")

    st.dataframe(
        display_evidence,
        use_container_width=True,
        hide_index=True
    )


    # ==================================================
    # DOWNLOAD EVIDENCE
    # ==================================================

    csv_data = raw_evidence.to_csv(index=False)

    st.download_button(
        label="⬇️ Download Evidence CSV",
        data=csv_data,
        file_name="olist_ai_business_evidence.csv",
        mime="text/csv"
    )


    # ==================================================
    # AUTOMATIC VISUALIZATION
    # ==================================================

    st.divider()

    st.subheader("📈 Visual Business Evidence")


    # --------------------------------------------------
    # SALES
    # --------------------------------------------------

    if question == "Which month had the highest sales?":

        chart_data = raw_evidence.copy()

        if "Month" in chart_data.columns and "Sales" in chart_data.columns:

            chart_data["Month"] = pd.to_datetime(
                chart_data["Month"],
                errors="coerce"
            )

            chart_data = chart_data.dropna(
                subset=["Month"]
            )

            chart_data = chart_data.sort_values(
                "Month"
            )

            chart_data = chart_data.set_index(
                "Month"
            )

            st.line_chart(
                chart_data["Sales"],
                width="stretch"
            )


    # --------------------------------------------------
    # TOP CUSTOMERS
    # --------------------------------------------------

    elif question == "Who are our top customers by number of orders?":

        chart_data = raw_evidence.copy()

        chart_data["Customer"] = (
            chart_data["customer_unique_id"]
            .astype(str)
            .str[:8]
            + "..."
        )

        chart_data = chart_data.set_index(
            "Customer"
        )

        st.bar_chart(
            chart_data["orders"],
            width="stretch"
        )


    # --------------------------------------------------
    # PRODUCTS
    # --------------------------------------------------

    elif question == "Which products have high sales but low ratings?":

        chart_data = raw_evidence.copy()

        chart_data["Product"] = (
            chart_data["product_id"]
            .astype(str)
            .str[:8]
            + "..."
        )

        chart_data = chart_data.set_index(
            "Product"
        )

        st.bar_chart(
            chart_data["sales"],
            width="stretch"
        )


    # --------------------------------------------------
    # SELLERS
    # --------------------------------------------------

    elif question == "Which sellers generated the highest revenue?":

        chart_data = raw_evidence.copy()

        chart_data["Seller"] = (
            chart_data["seller_id"]
            .astype(str)
            .str[:8]
            + "..."
        )

        chart_data = chart_data.set_index(
            "Seller"
        )

        st.bar_chart(
            chart_data["revenue"],
            width="stretch"
        )


    # --------------------------------------------------
    # DELIVERY
    # --------------------------------------------------

    elif question == "Which states have the highest late delivery rate?":

        chart_data = raw_evidence.copy()

        chart_data = chart_data.set_index(
            "customer_state"
        )

        st.bar_chart(
            chart_data["late_delivery_rate"],
            width="stretch"
        )


    # --------------------------------------------------
    # DELIVERY VS REVIEWS
    # --------------------------------------------------

    elif question == (
        "Do late deliveries appear to be associated "
        "with lower review scores?"
    ):

        chart_data = raw_evidence.copy()

        chart_data = chart_data.set_index(
            "delivery_status"
        )

        st.bar_chart(
            chart_data["average_review_score"],
            width="stretch"
        )


    # ==================================================
    # EXACT EVIDENCE FOR GEMINI
    # ==================================================

    evidence_text = raw_evidence.to_string(
        index=False
    )


    # ==================================================
    # AI BUSINESS ANALYSIS
    # ==================================================

    st.divider()

    st.subheader("🤖 AI Business Analysis")

    st.info(
        "Gemini uses only the calculated evidence shown "
        "above to explain the business result."
    )


    with st.spinner(
        "Gemini is preparing the business interpretation..."
    ):

        ai_result = generate_ai_explanation(
            question,
            evidence_text
        )


    # ==================================================
    # DISPLAY AI RESULT
    # ==================================================

    st.success(
        "AI analysis generated successfully."
    )

    st.markdown(ai_result)


    # ==================================================
    # DOWNLOAD AI REPORT
    # ==================================================

    st.download_button(
        label="📄 Download AI Analysis",
        data=ai_result,
        file_name="olist_ai_business_analysis.txt",
        mime="text/plain"
    )


    # ==================================================
    # BUSINESS DECISION SUPPORT
    # ==================================================

    st.divider()

    st.subheader("💡 Business Decision Support")


    if question == "Which month had the highest sales?":

        st.info(
            "The highest-sales period can help management "
            "identify periods of stronger recorded sales "
            "and investigate the factors associated with "
            "those results."
        )


    elif question == "Who are our top customers by number of orders?":

        st.info(
            "High-order customers can be examined to understand "
            "repeat purchasing behaviour and customer activity."
        )


    elif question == "Which products have high sales but low ratings?":

        st.info(
            "Products with strong recorded sales but weaker ratings "
            "can be reviewed for product quality, customer "
            "expectations, and service issues."
        )


    elif question == "Which sellers generated the highest revenue?":

        st.info(
            "Top-performing sellers can be examined to understand "
            "patterns associated with stronger recorded sales."
        )


    elif question == "Which states have the highest late delivery rate?":

        st.info(
            "States with higher late-delivery rates can be examined "
            "for logistics, fulfilment, and delivery-service issues."
        )


    elif question == (
        "Do late deliveries appear to be associated "
        "with lower review scores?"
    ):

        st.info(
            "Comparing delivery status with review scores can help "
            "identify whether customer experience differs between "
            "on-time and late deliveries."
        )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "📌 AI explanations are based only on calculated evidence. "
    "The Olist dataset is historical, and sales/revenue should "
    "not be interpreted as net profit."
)