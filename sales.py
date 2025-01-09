#Importing Required Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import csv

# Title
st.title("Interactive Web Application for Sales Data Analysis on Demand Forecasting")
st.image("https://imgs.search.brave.com/HOpihCpa9JztvLehQDY6x4MDYzPxUSR1zLdvzGxvSZ4/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbWcu/ZnJlZXBpay5jb20v/ZnJlZS1waG90by9j/bG9zZS11cC1wZW4t/ZmluYW5jaWFsLWRv/Y3VtZW50c18xMjMy/LTE0MS5qcGc_c2Vt/dD1haXNfaHlicmlk",width=550)

# Exploring the Sales Dataset
st.title("Exploring the Sales Dataset")

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv("sales_dataset.csv")
data=load_data()

# Sidebar Menu
Menu = st.sidebar.radio("Menu", ["About Dataset","Sales Details of Product"])

if Menu == "About Dataset":
    st.image("https://imgs.search.brave.com/4xIg5HDlEfJHnrK810t3lrNiqN2pbq44cH_gGI8-szk/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90aHVt/YnMuZHJlYW1zdGlt/ZS5jb20vYi9kYXRh/LWNoYXJ0cy02MDA5/OTEzLmpwZw",width=550)
    st.header("Overview of Data")
    if st.checkbox("Shape of Dataset"):
     st.write(f"Shape of Dataset: {data.shape}")
    if st.checkbox("Tabular Data"):
     st.table(data.head(50))
    if st.checkbox("Statistical View Of Dataset"):
       st.table(data.describe())

    # Correlation Graph
    st.header("Correlation Graph")
    numeric_data = data.select_dtypes(include=['number'])
    fig, ax = plt.subplots(figsize=(7.7, 4))
    sns.heatmap(numeric_data.corr(), annot=True, cmap="coolwarm")
    st.pyplot(fig)

    # Graphical Analysis
    st.header("Graphical Analysis")

    graphs = st.selectbox("Choose the Graph",["Choose the Graph","Bar chart","Pie Chart","Line Chart","Scatter Plot","Donut Chart","Column Chart","Lollipop Chart","Dot Plot"])

    if graphs == "Bar chart":
        data['Order_Date'] = pd.to_datetime(data['Order_Date'])
        quarterly_data = data.resample('Q', on='Order_Date').sum()
        st.header("Grouping Data into Quarters")
        fig, ax = plt.subplots(figsize=(8, 3.5))
        sns.barplot(data=quarterly_data, x=quarterly_data.index, y='Units_Sold', color='blue', ax=ax)
        ax.set_title('Quarterly Units Sold')
        ax.set_xlabel('Quarter')
        ax.set_ylabel('Total Units Sold')
        ax.set_xticklabels(quarterly_data.index, rotation=45)
        st.pyplot(fig)

    if graphs == "Pie Chart":
        most_sold_category_units = data.groupby('Category')['Units_Sold'].sum()
        st.header("Distribution of Units Sold by Category")
        fig, ax = plt.subplots(figsize=(3,3))
        ax.pie(most_sold_category_units, labels=most_sold_category_units.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        ax.axis('equal') 
        st.pyplot(fig)

    if graphs == "Line Chart":
        data['Order_Date'] = pd.to_datetime(data['Order_Date'])
        units_sold_monthly = data.resample('M', on='Order_Date').sum()
        st.header("Monthly Units Sold Time Series")
        fig, ax = plt.subplots(figsize=(12, 6))
        units_sold_monthly['Units_Sold'].plot(ax=ax, title='Monthly Units Sold Time Series')
        ax.set_xlabel('Order_Date')
        ax.set_ylabel('Units Sold')
        st.pyplot(fig)

    if graphs == "Scatter Plot":
        # Plotting the scatter plot
        st.header("Comparision of Product Price vs Units Sold")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.scatter(data['Price'], data['Units_Sold'], alpha=0.5)
        ax.set_title('Product Price vs Units Sold')
        ax.set_xlabel('Price')
        ax.set_ylabel('Units Sold')
        st.pyplot(fig)        

    if graphs == "Donut Chart":
        units_sold_by_location = data.groupby('Location')['Units_Sold'].sum()
        st.header("Total Units Sold by Location")
        fig, ax = plt.subplots(figsize=(12, 6))
        wedges, texts, autotexts = ax.pie(units_sold_by_location.sort_values(ascending=False), 
                                        labels=units_sold_by_location.index, 
                                        autopct='%1.1f%%', startangle=90, 
                                        colors=sns.color_palette("Set3", n_colors=len(units_sold_by_location)))
        centre_circle = plt.Circle((0,0), 0.70, fc='white')
        ax.add_artist(centre_circle)
        ax.set_title('Total Units Sold by Location')
        plt.axis('equal')
        st.pyplot(fig)    

    if graphs == "Column Chart":
        revenue_by_location = data.groupby('Location')['Revenue'].sum().reset_index()
        revenue_by_location = revenue_by_location.sort_values(by='Revenue', ascending=False)
        st.header("Revenue By Location")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=revenue_by_location, x='Location', y='Revenue', ax=ax, color='red')
        ax.set_title('Revenue By Location (grouped)')
        ax.set_xlabel('Location')
        ax.set_ylabel('Total Revenue')
        ax.set_xticklabels(revenue_by_location['Location'], rotation=45)
        st.pyplot(fig)  

    if graphs == "Lollipop Chart":
        location_product_units_sold = data.groupby(['Location', 'Product_Name'])['Units_Sold'].sum()
        highest_units_products = location_product_units_sold.groupby('Location').idxmax().apply(lambda x: x[1])
        for location in data['Location'].unique():
            st.header("Highest Units Sold Products in location")
            fig, ax = plt.subplots(figsize=(8, 6))
            location_data = location_product_units_sold.loc[location]
            ax.scatter(location_data.index, location_data.values, color='blue', s=100, label='Units Sold')
            ax.plot(location_data.index, location_data.values, color='blue', alpha=0.7)
            ax.set_title(f'Highest Units Sold Products in {location}')
            ax.set_xlabel('Product Name')
            ax.set_ylabel('Units Sold')
            ax.set_xticklabels(location_data.index, rotation=90)
            ax.set_ylim(0, location_data.max() + 50)  
            ax.legend()
            st.pyplot(fig)
            print(f"In {location}, the product with the highest number of units sold is {highest_units_products[location]}")    

    if graphs == "Dot Plot":
        location_product_units_sold = data.groupby(['Location', 'Product_Name'])['Units_Sold'].sum()
        lowest_units_products = location_product_units_sold.groupby('Location').idxmin().apply(lambda x: x[1])
        for location in data['Location'].unique():
            fig, ax = plt.subplots(figsize=(8, 6))
            location_data = location_product_units_sold.loc[location]
            ax.scatter(location_data.index, location_data.values, color='red', s=100, label='Units Sold')
            ax.scatter(lowest_units_products[location], location_data[lowest_units_products[location]], color='green', s=150, zorder=5, label='Lowest Sales')
            ax.set_title(f'Lowest Units Sold Products in {location}')
            ax.set_xlabel('Product Name')
            ax.set_ylabel('Units Sold')
            ax.set_xticklabels(location_data.index, rotation=90)
            ax.legend()
            st.pyplot(fig)
            print(f"In {location}, the product with the lowest number of units sold is {lowest_units_products[location]}")

elif Menu == "Sales Details of Product":
    st.header("Choose the Product")
    # Defining product categories and their respective products
    product_categories = {
        "Camera": ['Canon EOS Rebel DSLR Camera', 'Sony Alpha Mirrorless Camera', 'Nikon DSLR Camera'],
        "Headphones": ['Sony WH-1000XM4 Wireless Headphones', 'JBL Quantum Gaming Headset', 'boAt Rockerz'],
        "Laptop": ['Dell XPS', 'Lenovo IdeaPad', 'HP Spectre x360'],
        "Smartphone": ['iPhone 12', 'Samsung Galaxy S21', 'OnePlus 9 Pro'],
        "Tv": ['LG OLED TV', 'Sony BRAVIA OLED TV', 'Samsung QLED TV']
    }
    # Select Product Category
    category = st.selectbox("Select Product Category", ["Choose Category"] + list(product_categories.keys()))
    if category != "Choose Category":
        #  Select Product Name
        product = st.selectbox("Select Product", ["Choose Product"] + product_categories[category])
        if product != "Choose Product":
            st.subheader(f"Details for {product}")
            # Filtering data for the selected product
            product_data = data[data['Product_Name'] == product]
            if not product_data.empty:
                #  Displaying product details
                # Highest and lowest sales in different locations
                sales_by_location = product_data.groupby('Location')['Units_Sold'].sum()
                highest_sales_location = sales_by_location.idxmax()
                lowest_sales_location = sales_by_location.idxmin()
                # Seasons in which the product was sold
                unique_seasons = product_data['Season'].unique()
                # Number of products sold per location and total
                total_units_sold = sales_by_location.sum()
                units_sold_by_location = sales_by_location.reset_index()
                # Price and Revenue
                price = product_data['Price'].iloc[0]
                total_revenue = product_data['Revenue'].sum()
                # Quality control
                quality_status = "Pass" if product_data['Quality_Control'].all() else "Fail"
                # Displaying details in tabular form
                st.table({
                    "Detail": ["Highest Sales Location", "Lowest Sales Location", "Seasons Sold", "Total Units Sold", "Product Price", "Total Revenue", "Quality Control"],
                    "Value": [highest_sales_location, lowest_sales_location, ", ".join(unique_seasons), total_units_sold, price, total_revenue, quality_status]
                })
                #  Graphical representation
                st.subheader("Graphical Representation")
                # Bar Chart: Sales by Location
                fig, ax = plt.subplots(figsize=(10, 3.5))
                sns.barplot(data=units_sold_by_location, x='Location', y='Units_Sold', palette='viridis', ax=ax)
                ax.set_title(f'Units Sold by Location for {product}')
                ax.set_xlabel('Location')
                ax.set_ylabel('Units Sold')
                st.pyplot(fig)
                # Pie Chart: Revenue Distribution by Location
                revenue_by_location = product_data.groupby('Location')['Revenue'].sum()
                fig, ax = plt.subplots(figsize=(9,3))
                ax.pie(revenue_by_location, labels=revenue_by_location.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
                ax.set_title(f'Revenue Distribution by Location for {product}')
                st.pyplot(fig)
            else:
                st.warning(f"No data found for the selected product: {product}")