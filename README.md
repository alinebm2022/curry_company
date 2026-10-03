# Food Delivery Marketplace Analytics

> Exploratory data analysis and interactive dashboard for a food delivery marketplace, focusing on business growth, restaurant performance, delivery operations, and driver performance.

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20Dashboard-red?logo=streamlit)](https://projects-aline-curry-company.streamlit.app/)

# 1. Business Problem

Cury Company is a technology company that operates a food delivery marketplace connecting restaurants, delivery drivers, and customers.

Through the application, customers can order meals from registered restaurants and receive their orders through delivery drivers registered on the platform.

The company generates a large amount of data related to orders, delivery operations, restaurants, delivery drivers, traffic conditions, weather conditions, vehicle conditions, and customer ratings.

Although the number of deliveries is growing, the CEO does not have a consolidated view of the company's main growth and operational KPIs.

You were hired as a Data Scientist to develop data-driven solutions for the delivery business. Before implementing predictive algorithms, the company's first need is to organize its main strategic KPIs into a single analytical tool that allows the CEO to monitor the business and support day-to-day decision-making.

Cury Company operates under a **Marketplace business model**, connecting three main groups:

- Restaurants
- Delivery drivers
- Customers

# 2. Business Challenge

The CEO needs a consolidated view of the company's main operational and growth indicators.

The analysis was structured into three main business perspectives:

## Company Perspective

1. Number of orders per day
2. Number of orders per week
3. Distribution of orders by traffic conditions
4. Order volume by city and traffic conditions
5. Number of orders per delivery driver per week
6. Central location of each city by traffic condition

## Delivery Driver Perspective

1. Youngest and oldest delivery drivers
2. Best and worst vehicle conditions
3. Average rating per delivery driver
4. Average rating and standard deviation by traffic conditions
5. Average rating and standard deviation by weather conditions
6. Top 10 fastest delivery drivers by city
7. Top 10 slowest delivery drivers by city

## Restaurant Perspective

1. Number of unique delivery drivers
2. Average distance between restaurants and delivery locations
3. Average delivery time and standard deviation by city
4. Average delivery time and standard deviation by city and order type
5. Average delivery time and standard deviation by city and traffic condition
6. Average delivery time during festivals

# 3. Data

The analysis was conducted using food delivery marketplace data covering the period from **January 2025 to March 2025**.

The dataset contains information related to:

- Orders
- Restaurants
- Delivery drivers
- Delivery locations
- Traffic conditions
- Weather conditions
- Vehicle conditions
- Delivery times
- Customer ratings
- Festivals

The analysis was organized into three main business perspectives:

1. **Company**
2. **Restaurants**
3. **Delivery Drivers**

# 4. Analytical Strategy

The dashboard was designed around the three main perspectives of the marketplace business model.

## 4.1 Company Growth

The company perspective focuses on understanding order volume and its relationship with traffic and city characteristics.

Key metrics include:

- Orders per day
- Orders per week
- Orders by traffic condition
- Orders by city
- Orders by delivery type
- Orders by traffic condition and city type
- Orders per delivery driver

## 4.2 Restaurant Performance

The restaurant perspective focuses on delivery operations and the factors associated with delivery time.

Key metrics include:

- Number of unique orders
- Average delivery distance
- Average delivery time
- Delivery time variability
- Delivery time by city
- Delivery time by order type
- Delivery time during festivals

## 4.3 Delivery Driver Performance

The delivery driver perspective focuses on driver characteristics, ratings, and delivery performance.

Key metrics include:

- Driver age
- Vehicle condition
- Average driver rating
- Rating by traffic condition
- Rating by weather condition
- Fastest delivery drivers
- Delivery performance by city

# 5. Key Insights

## 5.1 Daily order seasonality

The number of orders presents a daily variation, with approximately **10% variation between consecutive days** in the analyzed period.

## 5.2 Traffic conditions in Semi-Urban cities

Semi-Urban cities do not have records classified as low traffic conditions in the analyzed dataset.

## 5.3 Delivery time variation and weather

The largest variations in delivery time occur under **Sunny weather conditions**.

These findings provide an initial view of operational patterns that can be further investigated to understand the factors influencing delivery performance.

# 6. Interactive Dashboard

The project includes an interactive dashboard developed with **Streamlit**.

The dashboard organizes the main business KPIs into three analytical views:

- Company
- Restaurants
- Delivery Drivers

## Live Dashboard

[Access the Cury Company Dashboard](https://projects-aline-curry-company.streamlit.app/)

# 7. Technologies

- Python
- Pandas
- Streamlit
- Exploratory Data Analysis
- Data Visualization

# 8. Project Structure

```text
curry_company/
│
├── Home.py
├── README.md
├── requirements.txt
├── train.csv
├── .gitignore
├── eu.jpeg
│
└── pages/
    ├── 1_visao_empresa_module.py
    ├── 2_visao_entregador_module.py
    └── 3_visao_restaurante_module.py
