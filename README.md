# 📊 Olist Business Intelligence & GenAI System

An interactive Business Intelligence dashboard developed using Python, Pandas, and Streamlit to analyze customer behaviour, sales performance, products, sellers, and delivery operations using the Olist Brazilian E-Commerce dataset.

The system transforms raw e-commerce data into meaningful business insights through data cleaning, data modelling, KPI analysis, interactive dashboards, visualizations, and Generative AI.

## 📌 Project Overview

The Olist Business Intelligence & GenAI System provides a centralized platform for analyzing historical e-commerce business performance.

The application focuses on five major business areas:

1. Customer Analysis
2. Sales & Orders Analysis
3. Product Analysis
4. Seller Analysis
5. Delivery & Fulfilment Analysis

In addition, the system includes a GenAI Business Analyst powered by Google's Gemini API. It uses calculated data evidence to generate business-oriented explanations and recommendations for predefined business questions.

The main objective is to transform raw Olist data into actionable information that supports business analysis and decision-making.

**GitHub Repository:**  
https://github.com/sneha-ch099/Olist_Business_Intelligence

**Live Demo:** Add your Streamlit Cloud URL here if the latest version is deployed.

---

## 🎯 Problem Statement

The Olist e-commerce dataset contains information about customers, orders, products, sellers, payments, reviews, and delivery activities. However, this information is distributed across multiple datasets, making it difficult to obtain a consolidated view of business performance.

Business users need a system that transforms raw data into clear information about customers, sales and orders, product performance, seller performance, and delivery fulfilment.

This project addresses the problem by integrating and analysing relevant Olist datasets using Python and Pandas and presenting the results through an interactive Streamlit dashboard.

The system also incorporates Generative AI to explain calculated results in simple business language and support data-driven decision-making.

---

## 🎯 Project Objectives

The main objectives of the project are:

- To analyse customer behaviour and identify repeat customers.
- To evaluate sales and order performance using relevant KPIs and trends.
- To identify high-performing products and product categories.
- To analyse seller performance based on recorded sales and order activity.
- To evaluate delivery and fulfilment performance using delivery time and on-time delivery metrics.
- To develop an interactive Streamlit dashboard with KPI cards, filters, charts, and data tables.
- To implement date-based filtering and comparative sales analysis.
- To provide a What-If Business Simulator for hypothetical sales scenarios.
- To integrate Generative AI for explaining calculated results.
- To support business decisions through data-driven insights and visualizations.

---

## 📂 Dataset

The project uses the **Olist Brazilian E-Commerce Public Dataset**, which contains historical information about Brazilian e-commerce transactions.

Dataset source: [Olist Brazilian E-Commerce Dataset on Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

The datasets used include:

| Dataset | Description |
|---|---|
| `olist_customers_dataset.csv` | Customer information and location attributes |
| `olist_orders_dataset.csv` | Order details, status, and timestamps |
| `olist_order_items_dataset.csv` | Items associated with each order |
| `olist_products_dataset.csv` | Product attributes |
| `olist_sellers_dataset.csv` | Seller information |
| `olist_order_payments_dataset.csv` | Payment details |
| `olist_order_reviews_dataset.csv` | Customer review information |
| `product_category_name_translation.csv` | English translations of product categories |
| `olist_geolocation_dataset.csv` | Geographic coordinates and postal-code information |

The datasets are loaded, cleaned, and combined through relevant keys to create analytical data for the dashboard.

---

## 🧩 Data Model

The project integrates multiple datasets to support cross-functional business analysis.

The main relationships include:

- Customers are connected to orders through `customer_id`.
- Orders are connected to order items through `order_id`.
- Order items are connected to products through `product_id`.
- Order items are connected to sellers through `seller_id`.
- Orders are connected to payments through `order_id`.
- Orders are connected to reviews through `order_id`.
- Products are connected to category translations through `product_category_name`.
- Customer and seller location attributes support geographic analysis.

A consolidated sales dataset is created by joining relevant tables. This dataset supports sales, product, seller, and related analyses.

Customer-level and delivery analyses also use relevant order and customer information.

The data model enables information from multiple sources to be analysed together using Python and Pandas.

---

## 🏢 Business Areas and KPIs

### 1. Customer Analysis

The Customer Analysis module examines customer distribution and purchasing behaviour.

**Key Performance Indicators**

- Total Customers
- Repeat Customers
- Repeat Purchase Rate

**Business Questions**

- How many unique customers are present in the dataset?
- How many customers made repeat purchases?
- What is the repeat purchase rate?
- How does customer behaviour vary across locations?

### 2. Sales & Orders Analysis

The Sales & Orders module evaluates recorded sales and order performance.

**Key Performance Indicators**

- Total Orders
- Total Recorded Sales
- Average Order Value
- Items Sold

**Business Questions**

- Which month recorded the highest sales?
- What is the average order value?
- How does sales performance change over time?
- How do sales vary across product categories and locations?
- How do recorded sales compare between selected months?

### 3. Product Analysis

The Product Analysis module examines product and category performance.

**Key Performance Indicators**

- Product Sales
- Category Sales
- Items Sold
- Top Product Categories

**Business Questions**

- Which product categories generate the highest recorded sales?
- Which products have high sales but low ratings?
- Which products are purchased most frequently?
- How does product performance vary across categories?

### 4. Seller Analysis

The Seller Analysis module evaluates seller performance.

**Key Performance Indicators**

- Seller Sales
- Orders per Seller
- Items per Seller
- Top Sellers

**Business Questions**

- Which sellers contribute the most to recorded sales?
- Which sellers receive the highest number of orders?
- Which sellers handle the highest number of items?
- How does seller performance vary across locations?

### 5. Delivery & Fulfilment Analysis

The Delivery & Fulfilment module examines delivery operations and fulfilment performance.

**Key Performance Indicators**

- Average Delivery Days
- On-Time Delivery Rate
- Late Delivery Rate
- Delivery Delay Metrics

**Business Questions**

- What is the average delivery time?
- What percentage of orders were delivered on time?
- Which states have higher late-delivery rates?
- What is the average delay for late deliveries?
- Do late deliveries appear to be associated with customer review scores?

---

## 📊 Dashboard Features

The main application provides an executive overview of business performance, supported by interactive visualizations and analytical sections.

### 1. Executive Performance

Displays key business metrics:

- Total Recorded Sales
- Total Orders
- Total Customers
- Average Order Value

These KPIs provide a quick overview of the selected data.

### 2. Interactive Dashboard Filters

The dashboard includes date-based filtering through separate Start Date and End Date controls.

The main dashboard also supports state and product-category selection.

These filters allow users to explore selected periods and business dimensions. Filter behaviour depends on the relevant data and analysis section.

### 3. Business Snapshot

Provides an overview of:

- Total Products
- Total Sellers
- Average Delivery Time
- On-Time Delivery Percentage

### 4. What Needs Attention?

Highlights selected business indicators, including:

- Delivery performance status
- Top-performing seller
- Highest-selling product category

These indicators help users identify areas worth further investigation.

### 5. Monthly Sales Trend

Displays recorded sales over time through a monthly trend visualization.

This helps users examine changes in sales activity across the available historical period.

### 6. Sales Insights

Identifies:

- Highest active sales period
- Lowest active sales period

Periods with zero or negative sales are excluded from the active-period comparison.

These insights complement the monthly sales trend by highlighting notable periods.

### 7. What-If Business Simulator

Allows users to select a hypothetical percentage increase in orders and examine its proportional effect on recorded sales.

The simulator displays:

- Current Recorded Sales
- Estimated Additional Sales
- What-If Sales
- Current-versus-scenario comparison chart

The scenario assumes that recorded sales change proportionally with the selected hypothetical order increase. It is a scenario analysis, not a forecast of future performance.

### 8. Top Product Categories by Sales

Displays the top product categories by recorded sales using a horizontal bar chart.

Tooltips provide additional information about the categories and their sales values.

### 9. Top Sellers by Sales

Ranks sellers by recorded sales and displays the top sellers in a horizontal bar chart.

Seller identifiers are shortened for easier visualization.

### 10. Geographic Sales Analysis

Provides state-level analysis across Brazilian states.

The analysis includes:

- Recorded Sales
- Orders
- Unique Customers
- Average Order Value

A summary table and bar chart help users compare geographic performance.

### 11. Delivery Performance by State

Displays delivery performance indicators by state to support the identification of geographic differences in delivery operations.

### 12. Month-over-Month Sales Comparison

Allows users to select two months and compare their recorded sales.

The section displays:

- Sales for the first selected month
- Sales for the second selected month
- Percentage change
- Absolute sales difference
- Horizontal comparison chart

The percentage change is calculated relative to the first selected month's sales. When the starting value is zero, percentage change is not calculated.

The comparison is based on the currently filtered sales data.

---

## 🤖 GenAI Business Analyst

The project includes a Generative AI Business Analyst powered by Google's Gemini API.

The module uses calculated evidence from Python and Pandas to generate business explanations and recommendations.

### GenAI Workflow

**Business Question**

↓

**Identify Required Analysis**

↓

**Calculate Results Using Python and Pandas**

↓

**Prepare Data Evidence**

↓

**Send Evidence to Google Gemini**

↓

**Generate Business Explanation**

↓

**Provide Business Recommendations**

The numerical analysis is performed using the project's data-processing functions before the evidence is passed to Gemini. The AI component interprets the calculated results rather than replacing the underlying data analysis.

### Example Business Questions

The GenAI Business Analyst supports predefined questions such as:

- Who are our top customers by number of orders?
- Which month had the highest sales?
- Which products have high sales but low ratings?
- Which sellers generated the highest recorded sales?
- Which states have the highest late-delivery rates?
- Do late deliveries appear to be associated with lower review scores?

The application presents calculated evidence and provides an AI-generated business-oriented explanation.

AI-generated interpretations should be reviewed against the underlying data and should not be treated as proof of causation.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming and analysis |
| Pandas | Data cleaning, transformation, joining, and aggregation |
| NumPy | Numerical operations where required |
| Streamlit | Interactive dashboard and web application |
| Altair | Customized data visualizations |
| Google Gemini API | AI-generated business explanations |
| Git | Version control |
| GitHub | Repository hosting |
| Visual Studio Code | Development environment |
| CSV | Dataset storage and input |

---

## 🐍 Python and Pandas Analysis

Python and Pandas support the project's data-processing and analytical workflow.

The workflow includes:

1. Loading the Olist CSV datasets.
2. Cleaning and preparing the data.
3. Converting relevant date fields into datetime format.
4. Joining related datasets through relevant keys.
5. Creating a consolidated analytical sales dataset.
6. Calculating business KPIs.
7. Applying relevant filters.
8. Aggregating data for monthly and category-level analysis.
9. Generating tables and visualizations.
10. Preparing calculated evidence for the GenAI module.

Pandas operations such as `groupby()`, `sum()`, `mean()`, `nunique()`, and datetime-based grouping are used where appropriate.

---

## ❓ Business Questions Addressed

### Customer Questions

- Who are the top customers by number of orders?
- How many customers made repeat purchases?
- What is the repeat purchase rate?
- How does customer behaviour vary across locations?

### Sales & Orders Questions

- Which month recorded the highest sales?
- What is the total recorded sales value?
- What is the average order value?
- How many items were sold?
- How do sales compare between two selected months?

### Product Questions

- Which product categories generate the highest recorded sales?
- Which products have high sales but low ratings?
- Which products have the highest number of orders?

### Seller Questions

- Which sellers generated the highest recorded sales?
- Which sellers received the highest number of orders?
- Which sellers handled the highest number of items?

### Delivery & Fulfilment Questions

- Which states have the highest late-delivery rates?
- What is the average delivery time?
- What is the average delay for late deliveries?
- How does delivery performance vary across states?

### Cross-Analysis Question

- Do late deliveries appear to be associated with lower review scores?

---

## 🔐 GenAI API Security

The Gemini API key is configured through Streamlit secrets.

The configuration file is:

`.streamlit/secrets.toml`

Example configuration:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
```

The real API key should never be committed to a public GitHub repository.

The `.streamlit/secrets.toml` file should be excluded through `.gitignore`. For cloud deployment, configure the key through the deployment platform's secrets settings.

---

## 📁 Project Structure

```text
Olist_Business_Intelligence/
│
├── .streamlit/
│   └── secrets.toml
│
├── data/
│   ├── olist_customers_dataset.csv
│   ├── olist_geolocation_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_order_payments_dataset.csv
│   ├── olist_order_reviews_dataset.csv
│   ├── olist_orders_dataset.csv
│   ├── olist_products_dataset.csv
│   ├── olist_sellers_dataset.csv
│   └── product_category_name_translation.csv
│
├── docs/
│   ├── DFD_Level_0.png
│   ├── DFD_Level_1.png
│   ├── ER_Diagram.png
│   ├── FDD.png
│   └── Use_Case_Diagram.png
│
├── pages/
│   ├── 1_Customer.py
│   ├── 2_Sales_Order.py
│   ├── 3_Product.py
│   ├── 4_Seller.py
│   ├── 5_Delivery_Fulfilment.py
│   └── 6_AI_Analyst.py
│
├── src/
│   ├── ai_engine.py
│   ├── customer_analysis.py
│   ├── dashboard_filters.py
│   ├── data_cleaning.py
│   ├── data_loader.py
│   ├── data_model.py
│   ├── delivery_analysis.py
│   ├── product_analysis.py
│   ├── sales_analysis.py
│   └── seller_analysis.py
│
├── .gitignore
├── app.py
├── README.md
└── requirements.txt
```

*Note: This represents the intended project structure. Ensure that file names and folders match the actual repository before submitting.*

---

## 🗺️ System Diagrams

The project documentation includes diagrams describing the data model, system interactions, data flow, and functional structure.

### 1. Entity Relationship Diagram (ER Diagram)

Represents the relationships between Customers, Orders, Order Items, Products, Sellers, Payments, Reviews, Categories, and Geolocation.

File: `docs/ER_Diagram.png`

### 2. Use Case Diagram

Shows how business users interact with the dashboard and its analysis functions.

File: `docs/Use_Case_Diagram.png`

### 3. Data Flow Diagram — Level 0

Provides a high-level view of data movement between the user, the BI system, data sources, and the GenAI service.

File: `docs/DFD_Level_0.png`

### 4. Data Flow Diagram — Level 1

Provides a more detailed representation of the major analytical functions and dashboard workflow.

File: `docs/DFD_Level_1.png`

### 5. Functional Decomposition Diagram (FDD)

Represents the main functions of the Olist Business Intelligence & GenAI System, including the five business areas and the GenAI Business Analyst.

File: `docs/FDD.png`

---

## 📈 Results and Business Insights

The dashboard supports the analysis of:

- Customer purchasing behaviour and repeat purchases
- Monthly recorded sales trends
- Product category performance
- Seller performance
- State-level sales distribution
- Delivery and fulfilment performance
- Comparative sales performance between selected months
- Hypothetical sales scenarios
- AI-generated explanations based on calculated evidence

The insights depend on the available data and the filters selected by the user.

---

## ⚠️ Important Data Considerations

### Recorded Sales Versus Profit

The Olist dataset does not provide complete cost information such as product costs, operating costs, marketing expenses, and commissions.

Therefore, recorded sales and revenue-related metrics should not be interpreted as net profit.

### Product Quantity

The order-items dataset does not contain a direct product quantity field. Item records are used where appropriate to count items.

### Historical Data

The dataset represents historical e-commerce transactions. Results describe the available dataset and should not be interpreted as current market conditions.

### Delivery Metrics

Delivery metrics depend on the available purchase, estimated delivery, and actual delivery timestamps. Missing dates may affect calculations.

### Geographic Data

The geolocation dataset contains multiple records for geographic identifiers. It should not be treated as a simple one-row-per-postal-code lookup without appropriate aggregation.

### What-If Analysis

The What-If Business Simulator is based on a proportional scenario assumption. It is not a predictive model or a guarantee of future sales.

### GenAI Limitations

AI-generated explanations depend on the evidence supplied to the model and may require human review. They should not be treated as proof of causation.

---

## ⚙️ How to Run the Project

### Prerequisites

- Python
- Git (optional)
- A Google Gemini API key for the AI Analyst functionality

### Step 1: Clone the Repository

```bash
git clone https://github.com/sneha-ch099/Olist_Business_Intelligence.git
cd Olist_Business_Intelligence
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 3: Activate the Virtual Environment

On Windows:

```bash
.venv\Scripts\activate
```

### Step 4: Install Required Packages

```bash
pip install -r requirements.txt
```

### Step 5: Configure the Gemini API Key

Create `.streamlit/secrets.toml` and add your API key:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
```

Do not upload the real key to GitHub.

### Step 6: Run the Application

```bash
streamlit run app.py
```

Open the local URL shown in the terminal, usually:

`http://localhost:8501`

The dashboard will open in your browser.

---

## 🚀 Deployment

The application can be deployed using Streamlit Community Cloud or another compatible hosting service.

For a Streamlit Community Cloud deployment:

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Create an app using the repository and `app.py` as the main file.
4. Configure the Gemini API key in the app's secrets settings.
5. Deploy and test the application.

Ensure that the dataset files required by the application are available in the deployment environment and that secrets are configured securely.

Add the public application URL to the Live Demo section after confirming the deployed version works.

---

## 🔮 Future Enhancements

Potential future improvements include:

- Advanced customer segmentation
- Customer retention and cohort analysis
- Additional comparative business metrics
- Enhanced export and reporting options
- More advanced forecasting methods
- Expanded AI-assisted business analysis

These are potential extensions rather than claims about currently implemented features.

---

## 👩‍💻 Author

**Sneha Chaudhary**

Business Administration — Finance

**Project:** Olist Business Intelligence & GenAI System

---

*Developed as an academic Business Intelligence project using Python, Pandas, Streamlit, and Generative AI.*
