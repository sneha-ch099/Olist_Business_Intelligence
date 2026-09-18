import streamlit as st

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


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="GenAI Business Analyst",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("🤖 GenAI Business Analyst")

st.write(
    "Ask a business question about customers, sales, "
    "products, sellers, or delivery performance."
)

# --------------------------------------------------
# BUSINESS QUESTION
# --------------------------------------------------

st.subheader("💬 Business Question")

question = st.selectbox(
    "Select a question to analyze",
    [
        "Who are our top customers by number of orders?",
        "Which month had the highest sales?",
        "Which products have high sales but low ratings?",
        "Which sellers generated the highest revenue?",
        "Which states have the highest late delivery rate?",
        "Do late deliveries appear to be associated with lower review scores?"
    ]
)

st.write("**Selected Question:**", question)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data(show_spinner="Preparing AI analysis data...")
def get_ai_data():

    data = load_data()
    sales = create_sales_model(data)

    return data, sales


data, sales = get_ai_data()


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

st.divider()

if st.button("🔍 Analyze", type="primary"):

    with st.spinner("Analyzing your question..."):

        # ------------------------------------------
        # CUSTOMER
        # ------------------------------------------

        if question == "Who are our top customers by number of orders?":

            evidence = get_top_customers(data)

        # ------------------------------------------
        # SALES
        # ------------------------------------------

        elif question == "Which month had the highest sales?":

            evidence = get_highest_sales_month(sales)

        # ------------------------------------------
        # PRODUCT
        # ------------------------------------------

        elif question == "Which products have high sales but low ratings?":

            evidence = get_products_high_sales_low_rating(sales)

        # ------------------------------------------
        # SELLER
        # ------------------------------------------

        elif question == "Which sellers generated the highest revenue?":

            evidence = get_top_sellers(sales)

        # ------------------------------------------
        # DELIVERY
        # ------------------------------------------

        elif question == "Which states have the highest late delivery rate?":

            evidence = get_late_delivery_by_state(sales)

        # ------------------------------------------
        # CROSS-ANALYSIS
        # ------------------------------------------

        elif question == (
            "Do late deliveries appear to be associated "
            "with lower review scores?"
        ):

            evidence = get_delivery_review_analysis(sales)

        else:

            evidence = None

        # ------------------------------------------
        # DISPLAY ACTUAL DATA EVIDENCE
        # ------------------------------------------

        st.subheader("📊 Data Evidence")

        if evidence is not None:

            st.dataframe(
                evidence,
                width="stretch",
                hide_index=True
            )

            # --------------------------------------
            # SEND EVIDENCE TO GEMINI
            # --------------------------------------

            evidence_text = evidence.to_string(
                index=False
            )

            with st.spinner("Gemini is preparing the business analysis..."):

                ai_result = generate_ai_explanation(
                    question,
                    evidence_text
                )

            # --------------------------------------
            # DISPLAY AI ANALYSIS
            # --------------------------------------

            st.subheader("🤖 AI Analysis")

            st.write(ai_result)