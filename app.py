import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# 1. Page Configuration
st.set_page_config(
    page_title="Superstore Executive Analytics Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Data Loading Function
@st.cache_data
def load_data():
    home_dir = os.path.expanduser("~")
    search_paths = [
        "Sample - Superstore.csv",
        "SampleSuperstoreDataset.csv",
        "SampleSuperstore.csv",
        os.path.join(home_dir, "Downloads", "Sample - Superstore.csv"),
        os.path.join(home_dir, "Desktop", "Sample - Superstore.csv"),
    ]
    df = None
    for path in search_paths:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path, encoding="windows-1252")
                break
            except:
                try:
                    df = pd.read_csv(path, encoding="utf-8")
                    break
                except:
                    continue

    if df is None:
        st.error("⚠️ 'Sample - Superstore.csv' File not found. keep the file is the same folder.")
        st.stop()

    df.columns = df.columns.str.strip()
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.to_period('M').dt.to_timestamp()

    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce').fillna(0)
    df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce').fillna(0)
    df['Discount'] = pd.to_numeric(df['Discount'], errors='coerce').fillna(0)
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0)
    return df

df = load_data()

# 3. Session State for ALL Chart Cross-Filtering
filter_keys = [
    'selected_region', 'selected_subcat', 'selected_month', 
    'selected_segment', 'selected_city', 'selected_ship'
]
for k in filter_keys:
    if k not in st.session_state:
        st.session_state[k] = None

def reset_chart_clicks():
    for k in filter_keys:
        st.session_state[k] = None

# 4. Sidebar Controls 
with st.sidebar:
    st.markdown("### 🎨 **Theme Selection**")
    theme_choice = st.radio(
        "Display Mode:",
        options=["🌙 Dark Mode", "☀️ Light Mode"],
        horizontal=True
    )
    is_dark = "Dark" in theme_choice

    st.markdown("---")
    st.markdown("### 🎛️ **Dashboard Slicers**")
    
    # Year Range Slider
    min_year = int(df['Year'].min())
    max_year = int(df['Year'].max())
    year_range = st.slider(
        "📅 **Select Year Range:**",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )
    
    # Discount Range Slider
    max_disc = float(df['Discount'].max() * 100)
    discount_range = st.slider(
        "🏷️ **Discount % (Slider):**",
        min_value=0.0,
        max_value=max_disc,
        value=(0.0, max_disc),
        step=5.0
    )
    
    # Minimum Transaction Sales Slider
    sales_threshold = st.slider(
        "💵 **Min Transaction Sales ($):**",
        min_value=0,
        max_value=1000,
        value=0,
        step=25
    )

    st.markdown("---")
    categories = ['All'] + sorted(df['Category'].unique().tolist())
    selected_cat = st.selectbox("📦 **Category Slicer:**", options=categories)

    segments = ['All'] + sorted(df['Segment'].unique().tolist())
    selected_seg = st.selectbox("👥 **Customer Segment:**", options=segments)

    st.markdown("---")
    if st.button("🔄 Reset All Filters", use_container_width=True):
        reset_chart_clicks()
        st.rerun()

# 5. Dynamic Colors, Text Contrast Slider CSS
if is_dark:
    bg_app = "#0B0F17"
    sidebar_bg = "#0D131F"
    card_bg = "#131B2B"
    text_primary = "#F8FAFC"
    text_secondary = "#94A3B8"
    border_color = "rgba(255, 255, 255, 0.09)"
    plotly_template = "plotly_dark"
    grid_color = "rgba(255, 255, 255, 0.07)"
    slider_accent = "#38BDF8"
    banner_bg = "linear-gradient(135deg, #111827 0%, #1E293B 100%)"
    active_tag_bg = "rgba(56, 189, 248, 0.15)"
    active_tag_color = "#38BDF8"
else:
    bg_app = "#F8FAFC"
    sidebar_bg = "#FFFFFF"
    card_bg = "#FFFFFF"
    text_primary = "#0F172A"
    text_secondary = "#64748B"
    border_color = "rgba(0, 0, 0, 0.08)"
    plotly_template = "plotly_white"
    grid_color = "rgba(0, 0, 0, 0.06)"
    slider_accent = "#0284C7"
    banner_bg = "linear-gradient(135deg, #1E293B 0%, #334155 100%)"
    active_tag_bg = "rgba(2, 132, 199, 0.12)"
    active_tag_color = "#0284C7"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    
    .stApp {{
        background-color: {bg_app} !important;
        color: {text_primary} !important;
    }}
    
    /* Top White Header Bar Fix */
    header[data-testid="stHeader"], .stAppHeader {{
        background: transparent !important;
        background-color: transparent !important;
    }}
    
    [data-testid="stAppViewContainer"] {{
        background-color: {bg_app} !important;
    }}
    
    /* Sidebar Styling & Visibility */
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {border_color} !important;
    }}
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p {{
        color: {text_primary} !important;
    }}
    
    /* SLIDER BLUE COLOR FIX */
    div[data-testid="stSlider"], div[data-baseweb="slider"] {{
        background: transparent !important;
    }}
    div[data-baseweb="slider"] div[role="slider"] {{
        background-color: {slider_accent} !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0 0 6px rgba(56, 189, 248, 0.6) !important;
        width: 16px !important;
        height: 16px !important;
    }}
    div[data-testid="stSlider"] [data-testid="stMarkdownContainer"] p {{
        color: {slider_accent} !important;
        font-weight: 700 !important;
    }}
    div[data-testid="stSlider"] div[data-testid="stTickBar"] div {{
        color: {text_secondary} !important;
    }}

    /* Top Executive Banner */
    .hero-banner {{
        background: {banner_bg};
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 22px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }}
    .hero-badge {{
        display: inline-block;
        background: {active_tag_bg};
        color: {active_tag_color};
        border: 1px solid {active_tag_color};
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }}
    .hero-title {{
        font-size: 26px;
        font-weight: 800;
        color: #FFFFFF !important;
        margin: 0 0 8px 0;
        letter-spacing: -0.5px;
    }}
    .hero-desc {{
        font-size: 13.5px;
        line-height: 1.6;
        color: #E2E8F0 !important;
        margin: 0;
    }}
    .hero-highlights {{
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin-top: 12px;
        font-size: 12px;
        color: #94A3B8;
    }}
    .hero-chip {{
        background: rgba(255, 255, 255, 0.08);
        padding: 3px 10px;
        border-radius: 6px;
        color: #F1F5F9;
        font-weight: 500;
    }}
    
    /* KPI Cards */
    .kpi-card {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 14px;
        padding: 16px 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        transition: transform 0.2s ease;
    }}
    .kpi-card:hover {{
        transform: translateY(-2px);
    }}
    .kpi-title {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        color: {text_secondary};
        display: flex;
        justify-content: space-between;
    }}
    .kpi-value {{
        font-size: 24px;
        font-weight: 800;
        color: {text_primary};
        margin: 4px 0;
    }}
    .kpi-tag {{
        font-size: 11px;
        font-weight: 600;
        padding: 2px 7px;
        border-radius: 4px;
        display: inline-block;
    }}
    .tag-green {{ background: rgba(16, 185, 129, 0.15); color: #10B981; }}
    .tag-red {{ background: rgba(239, 68, 68, 0.15); color: #EF4444; }}
    .tag-blue {{ background: {active_tag_bg}; color: {active_tag_color}; }}

    /* Chart Containers */
    .chart-container {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 14px;
        padding: 16px 18px 10px 18px;
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    .chart-heading {{
        font-size: 14px;
        font-weight: 700;
        color: {text_primary};
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .hint-text {{
        font-size: 11px;
        font-weight: 600;
        color: {active_tag_color};
    }}
    
    .active-filter-bar {{
        background: {active_tag_bg};
        border-left: 4px solid {active_tag_color};
        padding: 8px 14px;
        border-radius: 8px;
        margin-bottom: 16px;
        font-size: 13px;
        color: {text_primary};
    }}
    </style>
""", unsafe_allow_html=True)

# 6. Apply Sliders and Sidebar Filters
filtered_df = df[
    (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1]) &
    (df['Discount'] * 100 >= discount_range[0]) & (df['Discount'] * 100 <= discount_range[1]) &
    (df['Sales'] >= sales_threshold)
]

if selected_cat != 'All':
    filtered_df = filtered_df[filtered_df['Category'] == selected_cat]

if selected_seg != 'All':
    filtered_df = filtered_df[filtered_df['Segment'] == selected_seg]

# 6.1 Apply ALL Chart Cross-Filters dynamically
active_filter_msg = []

if st.session_state['selected_month']:
    filtered_df = filtered_df[filtered_df['Month'] == pd.to_datetime(st.session_state['selected_month'])]
    active_filter_msg.append(f"Month: <b>{pd.to_datetime(st.session_state['selected_month']).strftime('%b %Y')}</b>")

if st.session_state['selected_subcat']:
    filtered_df = filtered_df[filtered_df['Sub-Category'] == st.session_state['selected_subcat']]
    active_filter_msg.append(f"Sub-Category: <b>{st.session_state['selected_subcat']}</b>")

if st.session_state['selected_region']:
    filtered_df = filtered_df[filtered_df['Region'] == st.session_state['selected_region']]
    active_filter_msg.append(f"Region: <b>{st.session_state['selected_region']}</b>")

if st.session_state['selected_segment']:
    filtered_df = filtered_df[filtered_df['Segment'] == st.session_state['selected_segment']]
    active_filter_msg.append(f"Segment: <b>{st.session_state['selected_segment']}</b>")

if st.session_state['selected_city']:
    filtered_df = filtered_df[filtered_df['City'] == st.session_state['selected_city']]
    active_filter_msg.append(f"City: <b>{st.session_state['selected_city']}</b>")

if st.session_state['selected_ship']:
    filtered_df = filtered_df[filtered_df['Ship Mode'] == st.session_state['selected_ship']]
    active_filter_msg.append(f"Ship Mode: <b>{st.session_state['selected_ship']}</b>")

# 7. Top Executive Project Banner
st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Superstore Retail Sales & Profitability Dashboard</div>
        <p class="hero-desc">
            This interactive dashboard comprehensively monitors and analyzes the <b>Sales Revenue, Profit Margins, and Operational Efficiency</b> of the retail business. With this analytical suite, you can <b>track multidimensional trends</b>, identify loss-making categories, evaluate high-profit regions, and perform <b>real-time cross-drilldown analysis</b> by clicking directly on ANY chart element (Bars, Lines, or Pie slices).
        </p>
        <div class="hero-highlights">
            <span class="hero-chip">✨ Multi-Range Sliders</span>
            <span class="hero-chip">🎯 100% Chart-to-Chart Cross-Filtering</span>
            <span class="hero-chip">📈 6 Interactive Visualizations</span>
            <span class="hero-chip">🌓 Dark / Light Mode Adaptive</span>
        </div>
    </div>
""", unsafe_allow_html=True)

if active_filter_msg:
    col_msg, col_btn = st.columns([5, 1])
    with col_msg:
        st.markdown(f"""
            <div class="active-filter-bar">
                <span>🎯 Active Interactive Drilldown: {' | '.join(active_filter_msg)}</span>
            </div>
        """, unsafe_allow_html=True)
    with col_btn:
        if st.button("Clear Chart Clicks", use_container_width=True):
            reset_chart_clicks()
            st.rerun()

# 8. KPI Metrics
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0.0
total_orders = filtered_df['Order ID'].nunique() if 'Order ID' in filtered_df.columns else len(filtered_df)
avg_order_value = (total_sales / total_orders) if total_orders > 0 else 0.0

col1, col2, col3, col4, col5 = st.columns(5)
tag_color = "tag-green" if profit_margin >= 0 else "tag-red"
tag_symbol = "▲" if profit_margin >= 0 else "▼"

with col1:
    st.markdown(f"""
        <div class="kpi-card" style="border-top: 3px solid #38BDF8;">
            <div class="kpi-title"><span>Total Revenue</span><span>💰</span></div>
            <div class="kpi-value">${total_sales:,.0f}</div>
            <div class="kpi-tag tag-blue">Filtered Gross</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="kpi-card" style="border-top: 3px solid #10B981;">
            <div class="kpi-title"><span>Net Profit</span><span>📈</span></div>
            <div class="kpi-value">${total_profit:,.0f}</div>
            <div class="kpi-tag {tag_color}">{tag_symbol} {profit_margin:.1f}% Yield</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="kpi-card" style="border-top: 3px solid #818CF8;">
            <div class="kpi-title"><span>Profit Margin</span><span>🎯</span></div>
            <div class="kpi-value">{profit_margin:.2f}%</div>
            <div class="kpi-tag tag-blue">Margin Ratio</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="kpi-card" style="border-top: 3px solid #F59E0B;">
            <div class="kpi-title"><span>Total Orders</span><span>🛒</span></div>
            <div class="kpi-value">{total_orders:,}</div>
            <div class="kpi-tag tag-blue">Transactions</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
        <div class="kpi-card" style="border-top: 3px solid #EC4899;">
            <div class="kpi-title"><span>Avg Order Value</span><span>💳</span></div>
            <div class="kpi-value">${avg_order_value:.1f}</div>
            <div class="kpi-tag tag-blue">Ticket Size</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# 9. Adaptive Plotly Layout
plot_layout = dict(
    template=plotly_template,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color=text_secondary, family='Plus Jakarta Sans'),
    xaxis=dict(showgrid=False, color=text_secondary),
    yaxis=dict(showgrid=True, gridcolor=grid_color, color=text_secondary)
)

line_fill = 'rgba(56, 189, 248, 0.08)' if is_dark else 'rgba(2, 132, 199, 0.08)'
primary_accent = '#38BDF8' if is_dark else '#0284C7'

# 10. ROW 1: Monthly Timeline & Clickable Sub-Category Bar
r1_c1, r1_c2 = st.columns([1.3, 1])

with r1_c1:
    st.markdown('<div class="chart-container"><div class="chart-heading"><span>📈 Monthly Sales & Profit Momentum</span><span class="hint-text">👆 Click point to filter</span></div>', unsafe_allow_html=True)
    if not filtered_df.empty:
        trend = filtered_df.groupby('Month')[['Sales', 'Profit']].sum().reset_index()
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=trend['Month'], y=trend['Sales'],
            mode='lines+markers', name='Sales ($)',
            line=dict(color=primary_accent, width=3, shape='spline'),
            fill='tozeroy', fillcolor=line_fill
        ))
        fig_trend.add_trace(go.Scatter(
            x=trend['Month'], y=trend['Profit'],
            mode='lines+markers', name='Profit ($)',
            line=dict(color='#10B981', width=2.5, shape='spline')
        ))
        fig_trend.update_layout(
            **plot_layout, height=310, margin=dict(l=10, r=10, t=10, b=10),
            hovermode='x unified',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color=text_primary))
        )
        trend_select = st.plotly_chart(fig_trend, use_container_width=True, on_select="rerun", selection_mode="points", key="month_chart")
        if trend_select and trend_select.get("selection", {}).get("points"):
            clicked_month = trend_select["selection"]["points"][0]["x"]
            if st.session_state['selected_month'] != clicked_month:
                st.session_state['selected_month'] = clicked_month
                st.rerun()
    else:
        st.info("No records matching the filter criteria.")
    st.markdown('</div>', unsafe_allow_html=True)

with r1_c2:
    st.markdown('<div class="chart-container"><div class="chart-heading"><span>📦 Sub-Category Margin</span><span class="hint-text">👆 Click bar to filter</span></div>', unsafe_allow_html=True)
    if not filtered_df.empty:
        subcat = filtered_df.groupby('Sub-Category')[['Sales', 'Profit']].sum().reset_index().sort_values(by='Sales', ascending=True)
        fig_sub = px.bar(
            subcat, y='Sub-Category', x='Sales', color='Profit',
            orientation='h',
            color_continuous_scale=['#EF4444', '#F59E0B', '#10B981']
        )
        fig_sub.update_layout(
            template=plotly_template,
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=text_secondary, family='Plus Jakarta Sans'),
            height=310, margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_colorbar=dict(title="Profit", thickness=8, len=0.7, tickfont=dict(color=text_secondary)),
            xaxis=dict(showgrid=True, gridcolor=grid_color, color=text_secondary),
            yaxis=dict(showgrid=False, color=text_secondary, dtick=1)
        )
        sub_select = st.plotly_chart(fig_sub, use_container_width=True, on_select="rerun", selection_mode="points", key="subcat_chart")
        if sub_select and sub_select.get("selection", {}).get("points"):
            clicked_subcat = sub_select["selection"]["points"][0]["y"]
            if st.session_state['selected_subcat'] != clicked_subcat:
                st.session_state['selected_subcat'] = clicked_subcat
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 11. ROW 2: Regional Performance & Customer Segments
r2_c1, r2_c2 = st.columns(2)

with r2_c1:
    st.markdown('<div class="chart-container"><div class="chart-heading"><span>🌍 Regional Breakdown</span><span class="hint-text">👆 Click bar to filter</span></div>', unsafe_allow_html=True)
    if not filtered_df.empty:
        reg = filtered_df.groupby('Region')[['Sales', 'Profit']].sum().reset_index()
        sales_bar_color = primary_accent
        profit_bar_color = '#818CF8' if is_dark else '#4F46E5'
        fig_reg = go.Figure(data=[
            go.Bar(name='Sales', x=reg['Region'], y=reg['Sales'], marker_color=sales_bar_color),
            go.Bar(name='Profit', x=reg['Region'], y=reg['Profit'], marker_color=profit_bar_color)
        ])
        fig_reg.update_layout(
            barmode='group', **plot_layout, height=290, margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color=text_primary))
        )
        reg_select = st.plotly_chart(fig_reg, use_container_width=True, on_select="rerun", selection_mode="points", key="region_chart")
        if reg_select and reg_select.get("selection", {}).get("points"):
            clicked_region = reg_select["selection"]["points"][0]["x"]
            if st.session_state['selected_region'] != clicked_region:
                st.session_state['selected_region'] = clicked_region
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with r2_c2:
    st.markdown('<div class="chart-container"><div class="chart-heading"><span>👥 Sales Share by Segment</span><span class="hint-text">👆 Click slice to filter</span></div>', unsafe_allow_html=True)
    if not filtered_df.empty:
        seg = filtered_df.groupby('Segment')['Sales'].sum().reset_index()
        donut_colors = ['#0EA5E9', '#6366F1', '#EC4899'] if is_dark else ['#0284C7', '#4F46E5', '#DB2777']
        donut_border = bg_app
        fig_pie = px.pie(
            seg, names='Segment', values='Sales', hole=0.6,
            color_discrete_sequence=donut_colors
        )
        fig_pie.update_traces(textinfo='percent+label', textposition='inside', marker=dict(line=dict(color=donut_border, width=2)))
        fig_pie.update_layout(
            template=plotly_template,
            paper_bgcolor='rgba(0,0,0,0)', font=dict(color=text_primary),
            height=290, margin=dict(l=10, r=10, t=10, b=10), showlegend=False
        )
        seg_select = st.plotly_chart(fig_pie, use_container_width=True, on_select="rerun", selection_mode="points", key="segment_chart")
        if seg_select and seg_select.get("selection", {}).get("points"):
            clicked_segment = seg_select["selection"]["points"][0].get("label")
            if clicked_segment and st.session_state['selected_segment'] != clicked_segment:
                st.session_state['selected_segment'] = clicked_segment
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 12. ROW 3: Top 10 Profitable Cities & Shipping Modes
r3_c1, r3_c2 = st.columns(2)

with r3_c1:
    st.markdown('<div class="chart-container"><div class="chart-heading"><span>🏙️ Top 10 Profitable Cities</span><span class="hint-text">👆 Click bar to filter</span></div>', unsafe_allow_html=True)
    if not filtered_df.empty:
        city_df = filtered_df.groupby('City')['Profit'].sum().reset_index().sort_values(by='Profit', ascending=False).head(10)
        fig_city = px.bar(
            city_df, x='Profit', y='City',
            orientation='h',
            color='Profit',
            color_continuous_scale=['#F59E0B', '#10B981'],
            labels={'Profit': 'Total Profit ($)', 'City': 'City'}
        )
        fig_city.update_layout(
            template=plotly_template,
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=text_secondary, family='Plus Jakarta Sans'),
            height=290, margin=dict(l=10, r=10, t=10, b=10),
            yaxis=dict(autorange="reversed", color=text_secondary, dtick=1),
            xaxis=dict(showgrid=True, gridcolor=grid_color, color=text_secondary),
            coloraxis_showscale=False
        )
        city_select = st.plotly_chart(fig_city, use_container_width=True, on_select="rerun", selection_mode="points", key="city_chart")
        if city_select and city_select.get("selection", {}).get("points"):
            clicked_city = city_select["selection"]["points"][0]["y"]
            if st.session_state['selected_city'] != clicked_city:
                st.session_state['selected_city'] = clicked_city
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with r3_c2:
    st.markdown('<div class="chart-container"><div class="chart-heading"><span>🚚 Shipping Mode Volume & Margin</span><span class="hint-text">👆 Click bar to filter</span></div>', unsafe_allow_html=True)
    if not filtered_df.empty:
        ship_df = filtered_df.groupby('Ship Mode')[['Sales', 'Profit']].sum().reset_index()
        fig_ship = go.Figure(data=[
            go.Bar(name='Sales', x=ship_df['Ship Mode'], y=ship_df['Sales'], marker_color='#06B6D4'),
            go.Bar(name='Profit', x=ship_df['Ship Mode'], y=ship_df['Profit'], marker_color='#10B981')
        ])
        fig_ship.update_layout(
            barmode='group', **plot_layout, height=290, margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color=text_primary))
        )
        ship_select = st.plotly_chart(fig_ship, use_container_width=True, on_select="rerun", selection_mode="points", key="ship_chart")
        if ship_select and ship_select.get("selection", {}).get("points"):
            clicked_ship = ship_select["selection"]["points"][0]["x"]
            if st.session_state['selected_ship'] != clicked_ship:
                st.session_state['selected_ship'] = clicked_ship
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 13. Data Table Expander
with st.expander("🔍 View Raw Filtered Records (Top 100 Rows)"):
    display_cols = ['Order Date', 'Order ID', 'Customer Name', 'Segment', 'Region', 'Category', 'Sub-Category', 'Sales', 'Profit', 'Discount']
    st.dataframe(filtered_df[display_cols].head(100), use_container_width=True)
