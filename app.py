import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide")

# 2. Data Load
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(r"C:\Users\smmblz\Downloads\SampleSuperstoreDataset.csv", encoding="windows-1252")
    except:
        df = pd.read_csv(r"C:\Users\smmblz\Downloads\SampleSuperstore.csv", encoding="windows-1252")
        
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.to_period('M').dt.to_timestamp()
    return df

df = load_data()

# 3. Sidebar Filters
st.sidebar.title("Dashboard Slicers")
years = sorted(df['Year'].unique().tolist())
selected_year = st.sidebar.multiselect("Select Year(s):", years, default=years)

regions = sorted(df['Region'].unique().tolist())
selected_region = st.sidebar.multiselect("Select Region(s):", regions, default=regions)

categories = sorted(df['Category'].unique().tolist())
selected_category = st.sidebar.multiselect("Select Category(s):", categories, default=categories)

# Apply Filter
filtered_df = df[
    (df['Year'].isin(selected_year)) &
    (df['Region'].isin(selected_region)) &
    (df['Category'].isin(selected_category))
]

# 4. Title & 5 Core KPIs
st.title("📊 Executive Retail Sales & Profitability Dashboard")
st.markdown("---")

sales = filtered_df['Sales'].sum()
profit = filtered_df['Profit'].sum()
margin = (profit / sales * 100) if sales > 0 else 0
orders = filtered_df['Order ID'].nunique()
aov = sales / orders if orders > 0 else 0

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Total Sales", f"${sales:,.0f}")
kpi2.metric("Total Profit", f"${profit:,.0f}", delta=f"{margin:.1f}% Margin")
kpi3.metric("Profit Margin", f"{margin:.2f}%")
kpi4.metric("Total Orders", f"{orders:,}")
kpi5.metric("Avg Order Value", f"${aov:,.1f}")

st.markdown("<br>", unsafe_allow_html=True)

# 5. Charts Row 1: Time Trend & Sub-Category
c1, c2 = st.columns([1.2, 1])

with c1:
    st.subheader("Monthly Sales vs Profit Trend")
    trend = filtered_df.groupby('Month')[['Sales', 'Profit']].sum().reset_index()
    fig_line = px.line(trend, x='Month', y=['Sales', 'Profit'], markers=True,
                       color_discrete_map={'Sales': '#1E3D59', 'Profit': '#17B978'})
    st.plotly_chart(fig_line, use_container_width=True)

with c2:
    st.subheader("Sales vs Profit by Sub-Category")
    subcat = filtered_df.groupby('Sub-Category')[['Sales', 'Profit']].sum().reset_index().sort_values(by='Sales')
    fig_bar = px.bar(subcat, y='Sub-Category', x='Sales', color='Profit', orientation='h', color_continuous_scale='RdYlGn')
    st.plotly_chart(fig_bar, use_container_width=True)

# 6. Charts Row 2: Regional & Segment
c3, c4 = st.columns(2)

with c3:
    st.subheader("Regional Performance")
    reg = filtered_df.groupby('Region')[['Sales', 'Profit']].sum().reset_index()
    fig_reg = px.bar(reg, x='Region', y=['Sales', 'Profit'], barmode='group')
    st.plotly_chart(fig_reg, use_container_width=True)

with c4:
    st.subheader("Sales by Customer Segment")
    seg = filtered_df.groupby('Segment')['Sales'].sum().reset_index()
    fig_pie = px.pie(seg, names='Segment', values='Sales', hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)
