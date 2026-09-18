# Olist Business Intelligence & GenAI System

## Project Overview

The Olist Business Intelligence & GenAI System is an interactive business analytics application developed using the Olist e-commerce dataset.

The system transforms raw e-commerce data into meaningful business insights through data cleaning, data modelling, KPI analysis, interactive dashboards, and Generative AI.

The application is developed using Python and Streamlit. It provides analysis across five major business areas:

1. Customer
2. Sales & Orders
3. Product
4. Seller
5. Delivery & Fulfilment

In addition, the system includes a GenAI Business Analyst that allows managers and analysts to ask predefined business questions and receive data-driven explanations and business recommendations.

The overall objective is to transform Olist data into actionable business information that can support business analysis and decision-making.

## Problem Statement

The Olist e-commerce dataset contains information about customers, orders, products, sellers, payments, reviews, and delivery activities. However, the raw data is distributed across multiple datasets, making it difficult to obtain a consolidated view of business performance.

Business users need a system that can transform this raw data into clear and meaningful information about customers, sales and orders, products, sellers, and delivery fulfilment.

The project addresses this problem by developing an interactive Business Intelligence system that integrates and analyses the Olist datasets using Python, Pandas, and Streamlit.

The system also incorporates Generative AI to answer predefined business questions using calculated data evidence and provide simple business explanations and recommendations.

## Project Objectives

The main objectives of the project are:

- To analyse customer behaviour and identify repeat customers.
- To analyse sales and order performance using relevant KPIs and trends.
- To evaluate product performance and identify high-performing products and categories.
- To analyse seller performance based on revenue, orders, and items sold.
- To evaluate delivery and fulfilment performance using delivery time, on-time delivery, late delivery, and delay metrics.
- To develop an interactive Streamlit dashboard with KPIs, filters, charts, and data tables.
- To integrate Generative AI for answering predefined business questions using actual data evidence.
- To provide business explanations and practical recommendations based on the analysed results.

## Dataset

The project uses the Olist Brazilian e-commerce dataset, which contains multiple CSV files covering different aspects of the e-commerce business.

The datasets used in the project include:

- `olist_customers_dataset.csv` — Customer information
- `olist_orders_dataset.csv` — Order information and order status
- `olist_order_items_dataset.csv` — Products included in each order
- `olist_products_dataset.csv` — Product information
- `olist_sellers_dataset.csv` — Seller information
- `olist_order_payments_dataset.csv` — Payment information
- `olist_order_reviews_dataset.csv` — Customer review information
- `product_category_name_translation.csv` — Product category translation
- `olist_geolocation_dataset.csv` — Geographic information

These datasets are loaded using Pandas and combined through relevant keys to create an analytical data model for the Business Intelligence dashboard.

The project uses the underlying customer, order, product, seller, payment, review, category, and geographic information to support the five selected business areas.

## Data Model

The project uses an integrated data model to connect the different Olist datasets and support business analysis.

The main relationships are:

- Customers are connected to Orders through `customer_id`.
- Orders are connected to Order Items through `order_id`.
- Order Items are connected to Products through `product_id`.
- Order Items are connected to Sellers through `seller_id`.
- Orders are connected to Payments through `order_id`.
- Orders are connected to Reviews through `order_id`.
- Products are connected to the Category Translation dataset through `product_category_name`.
- Customer and Seller geographic information is represented using their location attributes.

A consolidated analytical sales dataset is created by joining the relevant tables. This master dataset is used for sales, product, seller, and delivery analysis, while customer-level analysis also uses the customer and order datasets.

The data model allows information from multiple Olist datasets to be analysed together through Python and Pandas.

## Business Areas & KPIs

The Business Intelligence system focuses on five major business areas.

### 1. Customer

The Customer analysis focuses on understanding customer activity and repeat purchasing behaviour.

**KPIs:**
- Total Customers
- Repeat Customers
- Repeat Purchase Rate

### 2. Sales & Orders

The Sales & Orders analysis evaluates overall order and sales performance.

**KPIs:**
- Total Orders
- Total Sales
- Average Order Value
- Items Sold

### 3. Product

The Product analysis evaluates product and category performance.

**KPIs:**
- Product Sales
- Product Revenue
- Items Sold
- Top Products

### 4. Seller

The Seller analysis evaluates seller contribution and performance.

**KPIs:**
- Seller Revenue
- Orders per Seller
- Items per Seller
- Top Sellers

### 5. Delivery & Fulfilment

The Delivery & Fulfilment analysis evaluates the efficiency and timeliness of order delivery.

**KPIs:**
- Average Delivery Days
- On-Time Delivery Rate
- Late Delivery Rate
- Average Delay

The dashboard provides relevant filters, charts, KPI cards, and data tables for analysing these business areas.

## System Diagrams

The project includes the following diagrams to represent the system structure, users, data flow, and functional components:

### 1. Entity Relationship (ER) Diagram

The ER Diagram represents the relationships between the major Olist datasets, including customers, orders, order items, products, sellers, payments, reviews, categories, and geolocation.

**File:** `docs/ER_Diagram.png`

### 2. Use Case Diagram

The Use Case Diagram represents how business users and other system components interact with the Olist Business Intelligence and GenAI system.

**File:** `docs/Use_Case_Diagram.png`

### 3. Data Flow Diagram – Level 0

The Level 0 DFD provides a high-level view of the major processes, data stores, users, and external services involved in the system.

**File:** `docs/DFD_Level_0.png`

### 4. Data Flow Diagram – Level 1

The Level 1 DFD provides a detailed view of the dashboard analytics process and its five major business analysis areas.

**File:** `docs/DFD_Level_1.png`

### 5. Functional Decomposition Diagram (FDD)

The FDD represents the functional structure of the Olist Business Intelligence and GenAI system, including the five business analysis areas and the GenAI Business Analyst.

**File:** `docs/FDD.png`

## Technologies Used

The project uses the following technologies and tools:

- **Python** — Used for data processing, analysis, and application development.
- **Pandas** — Used for data cleaning, transformation, joining datasets, and KPI calculations.
- **Streamlit** — Used to develop the interactive Business Intelligence dashboard.
- **Google Gemini API** — Used to provide Generative AI-based business explanations and recommendations.
- **Google GenAI SDK** — Used to connect the Streamlit application with the Gemini API.
- **Matplotlib** — Used for data visualisation where required.
- **Git & GitHub** — Used for version control and project repository management.
- **Visual Studio Code** — Used as the development environment.
- **CSV Files** — Used as the source format for the Olist datasets.

## Dashboard & Application Features

The Streamlit application provides an interactive dashboard for analysing Olist business performance across the five selected business areas.

### Executive Dashboard

The main dashboard provides a consolidated overview of business performance through:

- Total Sales
- Total Orders
- Average Order Value
- Items Sold
- Monthly Sales Trend
- Top Product Categories
- Top Sellers
- Delivery Performance by State

Interactive filters allow users to explore the data based on relevant business dimensions.

### Customer Analysis

The Customer page provides:

- Total Customers
- Repeat Customers
- Repeat Purchase Rate
- State and city-based filtering
- Customer-related data visualisations and tables
- Business interpretation of customer behaviour

### Sales & Orders Analysis

The Sales & Orders page provides:

- Total Orders
- Total Sales
- Average Order Value
- Items Sold
- Sales trends
- Category-level sales analysis
- Relevant filters and data tables
- Business interpretation of sales performance

### Product Analysis

The Product page provides:

- Product Sales
- Product Revenue
- Items Sold
- Top-performing product categories
- Product and category performance analysis
- Interactive filters and data tables
- Business interpretation of product performance

### Seller Analysis

The Seller page provides:

- Seller Revenue
- Orders per Seller
- Items per Seller
- Top Sellers
- Seller location-based filtering
- Seller performance visualisations and tables
- Business interpretation of seller performance

### Delivery & Fulfilment Analysis

The Delivery & Fulfilment page provides:

- Average Delivery Days
- On-Time Delivery Rate
- Late Delivery Rate
- Average Delay
- Delivery performance by customer state
- Seller location-based delivery analysis
- Interactive filters and data tables
- Business interpretation of delivery performance

All analysis pages follow a consistent structure:

**Business Question → KPI Cards → Filters → Charts → Data Table → Business Interpretation**

## Business Questions

The system is designed to answer important business questions across the five selected business areas.

### Customer

- Who are our top customers by number of orders?
- What proportion of customers are repeat customers?
- How does customer activity vary across different locations?

### Sales & Orders

- Which month had the highest sales?
- What is the overall sales and order performance?
- Which product categories contribute the most to sales?
- What is the average order value?

### Product

- Which products or categories generate the highest sales?
- Which products have high sales but low ratings?
- How do product categories differ in terms of sales and orders?

### Seller

- Which sellers generated the highest revenue?
- Which sellers handled the highest number of orders?
- How does seller performance vary across locations?

### Delivery & Fulfilment

- Which states have the highest late delivery rate?
- What is the average delivery time?
- What proportion of orders are delivered on time?
- What is the average delivery delay?

### Cross-Business Analysis

- Do late deliveries appear to be associated with lower review scores?

These business questions are supported by calculated data evidence from the Olist dataset and are used by the dashboard and GenAI Business Analyst.

## GenAI Integration

The project includes a GenAI Business Analyst that uses Google Gemini to provide business explanations based on actual data calculated from the Olist dataset.

The GenAI workflow follows this architecture:

**Manager Question → Identify Required Analysis → Pandas Calculation → Actual Data Result → Gemini → Business Explanation → Business Recommendation**

### GenAI Process

1. The manager selects a predefined business question.
2. The system identifies the analysis required to answer the question.
3. Python and Pandas calculate the required results from the Olist data.
4. The calculated results are passed to the Gemini API as data evidence.
5. Gemini explains the results in simple business language.
6. The system provides a practical business recommendation based only on the calculated evidence.

### GenAI Business Questions

The GenAI Business Analyst supports questions related to:

- Top customers by number of orders
- Highest sales month
- Products with high sales but low ratings
- Top sellers by revenue
- States with the highest late delivery rate
- Relationship between late deliveries and review scores

### API Key Security

The Gemini API key is stored securely using Streamlit secrets and is not hardcoded in the application source code.

The secrets file is excluded from Git tracking through `.gitignore` to prevent accidental exposure of the API key.

## Results & Key Insights

The developed Business Intelligence system successfully integrates the Olist datasets and provides interactive analysis across the five selected business areas.

The dashboard allows users to identify important business patterns through KPI cards, filters, charts, and detailed data tables.

### Customer Insights

Customer analysis provides information about the total customer base, repeat customers, and repeat purchase rate. This helps in understanding customer purchasing behaviour and engagement.

### Sales & Orders Insights

Sales analysis provides information about total sales, total orders, average order value, items sold, and monthly sales trends. This helps identify changes in sales performance over time.

### Product Insights

Product analysis helps identify high-performing product categories and compare categories based on sales and order activity.

### Seller Insights

Seller analysis provides information about seller revenue, orders, items sold, and top-performing sellers. This helps understand seller contribution to the marketplace.

### Delivery & Fulfilment Insights

Delivery analysis evaluates average delivery time, on-time delivery, late delivery, and average delay. The analysis can help identify locations and patterns associated with delivery performance.

### GenAI Insights

The GenAI Business Analyst converts calculated data results into simple business explanations and recommendations. This allows managers and analysts to interpret the results without manually analysing every data table.

The results generated by the system are based on the available Olist dataset and the calculations implemented using Python and Pandas.

## Limitations

The project has the following limitations:

- The Olist dataset contains historical e-commerce data and may not represent current business conditions.
- The dataset does not contain complete information about product costs, operating costs, marketing costs, or seller commissions.
- Therefore, actual business profit or profit margin cannot be calculated reliably from the available data.
- The analysis depends on the quality and completeness of the original Olist datasets.
- Some orders may have missing delivery dates, review information, or other fields.
- The GenAI Business Analyst is limited to the predefined business questions implemented in the application.
- GenAI responses depend on the data evidence provided to the model and may be affected by temporary API availability or service limitations.
- The project is designed for business analysis and decision support and does not replace detailed financial, operational, or managerial analysis.

## How to Run the Project

Follow the steps below to run the Olist Business Intelligence & GenAI System locally.

### 1. Clone the Repository

Clone the project repository from GitHub and open the project folder in Visual Studio Code.

### 2. Create and Activate the Virtual Environment

Create a Python virtual environment:

```bash
python -m venv .venv


### 2.1 Activate the Virtual Environment

On Windows, run:

.venv\Scripts\activate


### 3. Install Required Packages

Run:

pip install -r requirements.txt



### 4. Configure the Gemini API Key

The Gemini API key is stored securely in:

.streamlit/secrets.toml

The API key is not included directly in the Python source code.


### 5. Run the Streamlit Application

Run:

streamlit run app.py


The application will open in the web browser.

### 6. Application Pages

The application contains:

Executive Dashboard
Customer Analysis
Sales & Orders Analysis
Product Analysis
Seller Analysis
Delivery & Fulfilment Analysis
GenAI Business Analyst

## Project Structure

The project is organized into separate folders and files for data processing, analysis, dashboard pages, documentation, and GenAI functionality.

```text
Olist_Business_Intelligence/
│
├── .streamlit/
│   └── secrets.toml
│
├── .venv/
│
├── data/
│   └── Olist CSV datasets
│
├── docs/
│   ├── ER_Diagram.png
│   ├── Use_Case_Diagram.png
│   ├── DFD_Level_0.png
│   ├── DFD_Level_1.png
│   └── FDD.png
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
