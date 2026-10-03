# Superstore Executive Retail Analytics Dashboard 📊

**Program:** EncoderX Remote Internship (Batch 02) | **Track:** Data Science | **Task:** 04

## 📌 Project Overview
This project features a comprehensive, interactive Business Intelligence (BI) dashboard built with **Streamlit, Pandas, and Plotly**. The dashboard analyzes the **"Sample - Superstore"** dataset to monitor sales momentum, profitability, and operational efficiency across multiple regions and product categories.

## 🚀 Live Dashboard
* **Link:** [Insert your deployed Streamlit Cloud link here]

## 🛠️ Tech Stack & Tools
* **Framework:** Streamlit
* **Data Manipulation:** Python (Pandas)
* **Data Visualization:** Plotly Express & Plotly Graph Objects
* **UI Design:** Custom CSS, Glassmorphism, Dark/Light Mode Adaptive styling

## 📈 Dashboard Features
1. **Adaptive UI:** Dynamic switch between Dark Mode 🌙 and Light Mode ☀️.
2. **Interactive Slicers:** Range sliders for Year, Discount %, and Minimum Sales Threshold, alongside dropdowns for Category and Customer Segment.
3. **100% Cross-Filtering (Drilldown):** Clicking on any chart element (bar, line point, pie slice) instantly filters the entire dashboard.
4. **Data Explorer:** An expandable raw data table to inspect the filtered records directly.

## 📊 Key Performance Indicators (KPIs)
The dashboard tracks five core metrics at the top using custom-styled KPI cards with dynamic trend indicators (▲/▼):
1. **Total Revenue:** Gross sales generated.
2. **Net Profit:** Overall profit achieved.
3. **Profit Margin:** Percentage of profit relative to revenue.
4. **Total Orders:** Count of distinct transactions.
5. **Avg Order Value (AOV):** Average revenue per transaction.

## 📉 Visual Insights & Analysis
1. **Trend Analysis:** A spline area chart tracking Monthly Sales & Profit Momentum.
2. **Margin Breakdown:** A horizontal bar chart identifying highly profitable vs. loss-making sub-categories.
3. **Comparative Regional Analysis:** A grouped bar chart comparing sales and profit across regions (West, East, Central, South).
4. **Customer Segmentation:** A donut chart showing revenue share among Consumer, Corporate, and Home Office segments.
5. **Geographical Profitability:** Ranking the Top 10 most profitable cities.
6. **Operational Efficiency:** Evaluating Shipping Mode volume and associated margins.

## 📁 Repository Structure
* `app.py`: Main Streamlit dashboard application script.
* `Sample - Superstore.csv`: The dataset used for analysis.
* `requirements.txt`: Required Python dependencies.
* `README.md`: Project documentation.

## 💡 How to Run Locally
1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `streamlit run app.py`

---
