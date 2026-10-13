
import streamlit as st
import pandas as pd


def apply_dashboard_filters(sales):
    """
    Adds Start Date and End Date filters to the sidebar.
    Returns a filtered copy of the sales DataFrame.
    """

    if sales is None or sales.empty:
        return sales.copy() if sales is not None else pd.DataFrame()

    filtered = sales.copy()

    date_col = "order_purchase_timestamp"

    # Convert purchase dates safely
    if date_col not in filtered.columns:
        st.sidebar.warning(
            "Purchase date column was not found. Date filtering is unavailable."
        )
        return filtered

    filtered[date_col] = pd.to_datetime(
        filtered[date_col],
        errors="coerce"
    )

    valid_dates = filtered[date_col].dropna()

    if valid_dates.empty:
        st.sidebar.warning(
            "No valid purchase dates are available."
        )
        return filtered.iloc[0:0].copy()

    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

    # ----------------------------------------
    # DATE FILTERS — SIDEBAR ONLY
    # ----------------------------------------
    with st.sidebar:
        st.header("📅 Date Filters")

        start_date = st.date_input(
            "Start Date",
            value=min_date,
            min_value=min_date,
            max_value=max_date,
            key="sidebar_start_date_filter"
        )

        end_date = st.date_input(
            "End Date",
            value=max_date,
            min_value=min_date,
            max_value=max_date,
            key="sidebar_end_date_filter"
        )

        st.caption(
            f"Available data: {min_date} to {max_date}"
        )

    # ----------------------------------------
    # APPLY DATE FILTER
    # ----------------------------------------
    if start_date > end_date:
        st.sidebar.error(
            "Start Date cannot be later than End Date."
        )
        return filtered.iloc[0:0].copy()

    filtered = filtered[
        filtered[date_col].notna()
        & (filtered[date_col].dt.date >= start_date)
        & (filtered[date_col].dt.date <= end_date)
    ].copy()

    return filtered
