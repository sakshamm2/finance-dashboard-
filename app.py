import streamlit as st
import pandas as pd

st.set_page_config(page_title="Finance Pro Dashboard", layout="wide")

st.title("💰 Personal Finance Pro Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("data/transactions.csv")
df["Date"] = pd.to_datetime(df["Date"])

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.title("Filters")

category_filter = st.sidebar.multiselect(
    "Select Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

type_filter = st.sidebar.radio(
    "Select Type",
    ["All", "Income", "Expense"]
)

# Apply filters
filtered_df = df[df["Category"].isin(category_filter)]

if type_filter != "All":
    filtered_df = filtered_df[filtered_df["Type"] == type_filter]

# -----------------------------
# KPI METRICS
# -----------------------------
income = filtered_df[filtered_df["Type"] == "Income"]["Amount"].sum()
expense = filtered_df[filtered_df["Type"] == "Expense"]["Amount"].sum()
savings = income - expense

col1, col2, col3 = st.columns(3)

col1.metric("💰 Income", f"₹{income}")
col2.metric("💸 Expense", f"₹{expense}")
col3.metric("📈 Savings", f"₹{savings}")

# -----------------------------
# RAW DATA
# -----------------------------
st.subheader("📄 Data Preview")
st.dataframe(filtered_df)

# -----------------------------
# CATEGORY ANALYSIS
# -----------------------------
st.subheader("📊 Category Wise Spending")

expense_df = filtered_df[filtered_df["Type"] == "Expense"]

if not expense_df.empty:
    category = expense_df.groupby("Category")["Amount"].sum()
    st.bar_chart(category)
else:
    st.info("No expense data for selected filters")

# -----------------------------
# MONTHLY ANALYSIS
# -----------------------------
st.subheader("📈 Monthly Trend")

filtered_df["Month"] = filtered_df["Date"].dt.month
monthly = filtered_df.groupby("Month")["Amount"].sum()

st.line_chart(monthly)

# -----------------------------
# INSIGHTS ENGINE
# -----------------------------
st.subheader("🧠 AI Insights")

if not expense_df.empty:
    top_category = category.idxmax()
    st.write("🔹 Highest Spending Category:", top_category)

if income > 0:
    savings_rate = (savings / income) * 100

    st.write(f"🔹 Savings Rate: {savings_rate:.2f}%")

    if savings < 0:
        st.error("⚠️ You are overspending!")
    elif savings_rate > 40:
        st.success("✅ Excellent savings habit!")
    else:
        st.info("👍 Moderate financial health")
else:
    st.warning("No income data available")