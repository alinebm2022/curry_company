# Restaurant Marketplace Analytics

> Exploratory data analysis and interactive dashboard for a restaurant marketplace, focusing on geographic distribution, restaurant performance, pricing, ratings, cuisine types, and customer-facing services.

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20Dashboard-red?logo=streamlit)](https://fomezero-alinebm.streamlit.app/)

# 1. Business Problem

Fome Zero is a restaurant marketplace that connects customers and restaurants through a digital platform.

Restaurants registered on the platform provide information such as location, cuisine type, ratings, pricing, delivery availability, online ordering, and reservations.

You were hired as a Data Scientist to analyze the company's data and provide insights that could support the CEO in understanding the business and making strategic decisions.

The analysis focuses on restaurant distribution, customer ratings, pricing, cuisine types, and the services offered by restaurants.

# 2. Business Challenge

The CEO needs a comprehensive view of the marketplace to better understand the company's current business landscape.

The analysis was structured into five main perspectives:

## General Overview

1. How many unique restaurants are registered?
2. How many unique countries are represented?
3. How many unique cities are represented?
4. What is the total number of ratings?
5. How many different cuisine types are registered?

## Country Analysis

1. Which country has the highest number of registered cities?
2. Which country has the highest number of registered restaurants?
3. Which country has the highest number of restaurants with a price level of 4?
4. Which country has the greatest number of distinct cuisine types?
5. Which country has the highest number of ratings?
6. Which country has the highest number of restaurants offering delivery?
7. Which country has the highest number of restaurants offering reservations?
8. Which country has the highest average number of ratings per restaurant?
9. Which country has the highest average restaurant rating?
10. Which country has the lowest average restaurant rating?
11. What is the average price for two people in each country?

## City Analysis

1. Which city has the highest number of registered restaurants?
2. Which city has the highest number of restaurants with an average rating above 4?
3. Which city has the highest number of restaurants with an average rating below 2.5?
4. Which city has the highest average price for two people?
5. Which city has the greatest number of distinct cuisine types?
6. Which city has the highest number of restaurants offering reservations?
7. Which city has the highest number of restaurants offering delivery?
8. Which city has the highest number of restaurants accepting online orders?

## Restaurant Analysis

1. Which restaurant has the highest number of ratings?
2. Which restaurant has the highest average rating?
3. Which restaurant has the highest price for two people?
4. Which Brazilian cuisine restaurant has the lowest average rating?
5. Which Brazilian cuisine restaurant in Brazil has the highest average rating?
6. Do restaurants accepting online orders also have, on average, more ratings?
7. Do restaurants offering reservations also have, on average, higher prices for two people?
8. Do Japanese restaurants in the United States have a higher average price for two people than American BBQ restaurants?

## Cuisine Analysis

1. Which Italian cuisine restaurant has the highest average rating?
2. Which Italian cuisine restaurant has the lowest average rating?
3. Which American cuisine restaurant has the highest average rating?
4. Which American cuisine restaurant has the lowest average rating?
5. Which Arabic cuisine restaurant has the highest average rating?
6. Which Arabic cuisine restaurant has the lowest average rating?
7. Which Japanese cuisine restaurant has the highest average rating?
8. Which Japanese cuisine restaurant has the lowest average rating?
9. Which Home-style cuisine restaurant has the highest average rating?
10. Which Home-style cuisine restaurant has the lowest average rating?
11. Which cuisine type has the highest average price for two people?
12. Which cuisine type has the highest average rating?
13. Which cuisine type has the highest number of restaurants accepting online orders and offering delivery?

# 3. Data

The analysis was conducted using restaurant marketplace data covering the period from **March 2025 to June 2025**.

The dataset was analyzed through five main business perspectives:

1. General Overview
2. Country
3. City
4. Restaurant
5. Cuisine

# 4. Key Insights

## 4.1 India has the largest number of registered restaurants

India has the highest number of registered restaurants in the analyzed dataset.

## 4.2 Indonesia has the highest average restaurant ratings

Indonesia has the highest restaurant ratings among the countries represented in the dataset.

## 4.3 Brazilian cities are represented among the top 10 cities

Three Brazilian cities are among the top 10 cities with the largest number of registered restaurants:

- São Paulo
- Rio de Janeiro
- Brasília

These results highlight the geographic diversity of the marketplace dataset.

# 5. Interactive Dashboard

The project includes an interactive dashboard developed with **Streamlit**.

The dashboard allows users to explore the main business metrics through different analytical perspectives, including countries, cities, restaurants, and cuisine types.

## Live Dashboard

[Access the Fome Zero Dashboard](https://fomezero-alinebm.streamlit.app/)

# 6. Technologies

- Python
- Pandas
- Streamlit
- Exploratory Data Analysis
- Data Visualization

# 7. Project Structure

```text
fome_zero/
│
├── Home.py
├── README.md
├── requirements.txt
├── zomato.csv
├── .gitignore
├── comida.jpg
│
└── pages/
    ├── 1_visao_pais.py
    ├── 2_visao_cidade.py
    └── 3_visao_culinaria.py
