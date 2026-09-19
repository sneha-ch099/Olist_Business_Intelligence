# Olist Business Intelligence & GenAI System

## Project Overview

The Olist Business Intelligence & GenAI System is an interactive business analytics application developed using the Olist Brazilian e-commerce dataset.

The system transforms raw e-commerce data into meaningful business insights through data cleaning, data modelling, KPI analysis, interactive dashboards, and Generative AI.

The application is developed using Python and Streamlit. It provides analysis across five major business areas:

1. Customer
2. Sales & Orders
3. Product
4. Seller
5. Delivery & Fulfilment

In addition, the system includes a GenAI Business Analyst that allows managers and analysts to ask predefined business questions and receive data-driven explanations and business recommendations.

The overall objective is to transform Olist data into actionable business information that can support business analysis and decision-making.

---

## Problem Statement

The Olist e-commerce dataset contains information about customers, orders, products, sellers, payments, reviews, and delivery activities. However, the raw data is distributed across multiple datasets, making it difficult to obtain a consolidated view of business performance.

Business users need a system that can transform this raw data into clear and meaningful information about customers, sales and orders, products, sellers, and delivery fulfilment.

The project addresses this problem by developing an interactive Business Intelligence system that integrates and analyses the Olist datasets using Python, Pandas, and Streamlit.

The system also incorporates Generative AI to answer predefined business questions using calculated data evidence and provide simple business explanations and recommendations.

---

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

---

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

---

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

---

## Business Areas and KPIs

The system focuses on five business areas as required for the project.

### 1. Customer

The Customer Analysis module focuses on customer base and repeat purchasing behaviour.

Key Performance Indicators:

- Total Customers
- Repeat Customers
- Repeat Purchase Rate

Business Questions:

- How many customers are present in the dataset?
- How many customers made more than one purchase?
- What is the repeat purchase rate?
- How does customer behaviour vary across locations?

---

### 2. Sales & Orders

The Sales & Orders Analysis module evaluates overall sales and order performance.

Key Performance Indicators:

- Total Orders
- Total Sales
- Average Order Value
- Items Sold

Business Questions:

- Which month had the highest sales?
- What is the average order value?
- How many orders were completed?
- How does sales performance vary across categories and locations?

---

### 3. Product

The Product Analysis module evaluates product and category performance.

Key Performance Indicators:

- Product Sales
- Product Revenue
- Items Sold
- Top Products

Business Questions:

- Which product categories generate the highest sales?
- Which products have high sales but low ratings?
- Which products are purchased most frequently?
- How does product performance vary across categories?

---

### 4. Seller

The Seller Analysis module evaluates seller performance.

Key Performance Indicators:

- Seller Revenue
- Orders per Seller
- Items per Seller
- Top Sellers

Business Questions:

- Which sellers generated the highest revenue?
- Which sellers received the highest number of orders?
- Which sellers handled the highest number of items?
- How does seller performance vary across locations?

---

### 5. Delivery & Fulfilment

The Delivery & Fulfilment Analysis module evaluates order delivery performance.

Key Performance Indicators:

- Average Delivery Days
- On-Time Delivery Rate
- Late Delivery Rate
- Average Delay

Business Questions:

- What is the average delivery time?
- What percentage of orders were delivered on time?
- Which states have higher late delivery rates?
- What is the average delay for late deliveries?
- Does delivery performance appear to be associated with review scores?

---

## Technologies Used

The project uses the following technologies and tools:

- Python
- Pandas
- NumPy
- Streamlit
- Matplotlib
- Google Gemini API
- Git
- GitHub
- Visual Studio Code

---

## Python and Pandas Analysis

Python and Pandas are used for data loading, cleaning, transformation, joining, aggregation, and analysis.

The analytical workflow includes:

1. Loading the Olist CSV datasets.
2. Cleaning and preparing the data.
3. Converting relevant date fields into datetime format.
4. Joining related datasets using primary and foreign keys.
5. Creating a consolidated analytical sales dataset.
6. Calculating KPIs using Pandas.
7. Applying filters to the analytical data.
8. Generating tables and visualisations.
9. Passing calculated evidence to the GenAI module.

The project uses Pandas aggregation functions such as `groupby()`, `sum()`, `mean()`, `nunique()`, and time-based resampling for business analysis.

---

## Dashboard

The application is developed using Streamlit and provides an interactive Business Intelligence dashboard.

The main application contains:

- Executive Dashboard
- Customer Analysis
- Sales & Orders Analysis
- Product Analysis
- Seller Analysis
- Delivery & Fulfilment Analysis
- GenAI Business Analyst

Each analysis page follows a common structure:

**Title → Business Question → KPI Cards → Filters → Charts → Data Table → Business Interpretation**

The dashboard supports interactive filtering using relevant business dimensions such as:

- State
- City
- Product Category
- Seller
- Payment Type
- Order Status
- Review Score
- Date

Only relevant filters are provided for each business area.

---

## Business Questions

The system addresses business questions across the five selected business areas.

### Customer Questions

- Who are our top customers by number of orders?
- How many customers are repeat customers?
- What is the repeat purchase rate?

### Sales & Orders Questions

- Which month had the highest sales?
- What is the total sales value?
- What is the average order value?
- How many items were sold?

### Product Questions

- Which products have high sales but low ratings?
- Which product categories generate the highest sales?
- Which products have the highest number of orders?

### Seller Questions

- Which sellers generated the highest revenue?
- Which sellers received the highest number of orders?
- Which sellers handled the highest number of items?

### Delivery & Fulfilment Questions

- Which states have the highest late delivery rate?
- What is the average delivery time?
- What is the average delay for late deliveries?

### Cross-Analysis Question

- Do late deliveries appear to be associated with lower review scores?

---

## GenAI Business Analyst

The project includes a Generative AI Business Analyst that uses Google Gemini to provide business explanations based on calculated data evidence.

The GenAI workflow is:

**Manager Question**

↓

**Identify Required Analysis**

↓

**Pandas Calculation**

↓

**Actual Data Result**

↓

**Google Gemini**

↓

**Business Explanation**

↓

**Business Recommendation**

The GenAI module does not directly ask Gemini to calculate the raw dataset. Instead, the required analysis is first performed using Python and Pandas. The resulting evidence is then provided to Gemini for explanation.

This approach helps ensure that the numerical results shown to the user are based on the project data.

---

## GenAI Example Questions

The GenAI Business Analyst supports predefined questions such as:

- Who are our top customers by number of orders?
- Which month had the highest sales?
- Which products have high sales but low ratings?
- Which sellers generated the highest revenue?
- Which states have the highest late delivery rate?
- Do late deliveries appear to be associated with lower review scores?

The system displays the calculated data evidence and then generates a business-oriented explanation.

---

## GenAI API Security

The Gemini API key is stored securely using Streamlit secrets.

The API key is stored in:

`.streamlit/secrets.toml`

The key is not hardcoded directly into the Python source code.

The `.streamlit/secrets.toml` file is included in `.gitignore` so that the API key is not uploaded to GitHub.

---

## Project Structure

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

---

## Results and Analysis

The application provides interactive analysis of the Olist dataset across the five selected business areas.

The dashboard calculates business KPIs dynamically based on the available data and selected filters.

The main analysis areas include:

- Customer base and repeat customer analysis.
- Sales and order performance analysis.
- Monthly sales trends.
- Product and category performance.
- Seller revenue and order performance.
- Delivery time and fulfilment performance.
- State-level delivery analysis.
- Review and delivery relationship analysis.
- AI-generated explanations based on calculated evidence.

The dashboard allows users to change filters and observe how business metrics and visualisations change.

---

## Business Insights

The system supports business analysis by helping users:

- Understand customer purchasing behaviour.
- Identify repeat customer patterns.
- Monitor sales and order performance.
- Identify high-performing products and categories.
- Compare seller performance.
- Identify delivery and fulfilment issues.
- Examine geographical differences in delivery performance.
- Use Generative AI to interpret calculated results in simple business language.

The insights generated by the dashboard depend on the selected filters and the underlying Olist dataset.

---

## Important Data Considerations

The Olist dataset does not contain a direct quantity field for products. Therefore, item records are counted when calculating the number of items sold.

The project does not calculate actual business profit because the dataset does not provide all required cost information such as:

- Product cost
- Operating cost
- Marketing cost
- Commission cost

Therefore, sales and revenue-related metrics should not be interpreted as net profit.

Delivery metrics are calculated using the available purchase, delivery, and estimated delivery dates.

---

## Limitations

The project has the following limitations:

- The analysis is based on the available Olist dataset and therefore reflects the information contained in that dataset.
- The dataset represents historical e-commerce transactions and may not reflect current business conditions.
- Actual profit cannot be calculated because complete cost information is not available.
- Some orders may have missing delivery dates, which affects delivery calculations.
- The GenAI module depends on the availability of the Gemini API.
- AI-generated explanations are based only on the calculated evidence supplied to the model.
- The project uses predefined business questions rather than unrestricted natural-language analysis.
- The geographic dataset contains multiple records for location information and should not be treated as a simple one-row-per-ZIP-code lookup.

---

## How to Run the Project

Follow the steps below to run the Olist Business Intelligence & GenAI System locally.

### 1. Clone the Repository

Clone the project repository from GitHub and open the project folder in Visual Studio Code.

```bash
git clone https://github.com/sneha-ch099/Olist_Business_Intelligence.git
cd Olist_Business_Intelligence

### 2. Create the Virtual Environment

Create a Python virtual environment:

python -m venv .venv

### 3. Activate the Virtual Environment

On Windows, run:

.venv\Scripts\activate

### 4. Install Required Packages

Run:

pip install -r requirements.txt

### 5. Configure the Gemini API Key

Create the following file:

.streamlit/secrets.toml

Add the following line:

GEMINI_API_KEY = "YOUR_API_KEY"

Replace YOUR_API_KEY with a valid Gemini API key.

The API key is not hardcoded directly into the Python source code.

The .streamlit/secrets.toml file is included in .gitignore and should not be uploaded to GitHub.

### 6. Run the Streamlit Application

Run:

streamlit run app.py

The application will open in the web browser.

### 7. Application Pages

The application contains:

Executive Dashboard
Customer Analysis
Sales & Orders Analysis
Product Analysis
Seller Analysis
Delivery & Fulfilment Analysis
GenAI Business Analyst
```
