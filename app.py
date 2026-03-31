
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Expense Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('refined_expenses.csv')
    df['Clean_Date'] = pd.to_datetime(df['Clean_Date'])
    return df

df = load_data()

st.sidebar.title("Navigation")
view_type = st.sidebar.radio("View Type", ["Expenses", "Credits/Refunds"])
is_credit_val = 1 if view_type == "Credits/Refunds" else 0

months = sorted(df['Month_Year'].unique())
selected_months = st.sidebar.multiselect("Select Months", options=months, default=months)

filtered_df = df[(df['Is_Credit'] == is_credit_val) & (df['Month_Year'].isin(selected_months))]

st.title(f"📊 {view_type} Dashboard")
st.metric("Total (INR)", f"₹{filtered_df['AMT'].sum():,.2f}")

c1, c2 = st.columns(2)
with c1:
    fig_line = px.line(filtered_df.groupby('Month_Year')['AMT'].sum().reset_index(), 
                       x='Month_Year', y='AMT', markers=True, title="Monthly Trend",
                       hover_data={'Month_Year': True, 'AMT': ':,.2f'})
    st.plotly_chart(fig_line, use_container_width=True)
with c2:
    fig_pie = px.pie(filtered_df, values='AMT', names='Category', hole=0.4, title="Category Mix")
    st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("Month-by-Month Matrix")
pivot = filtered_df.pivot_table(index='Category', columns='Month_Year', values='AMT', aggfunc='sum').fillna(0)
st.dataframe(pivot.style.format("₹{:,.0f}"))

st.subheader("Transaction Details")
st.dataframe(filtered_df[['Clean_Date', 'Description', 'Category', 'AMT']].sort_values('Clean_Date', ascending=False))
