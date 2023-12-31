# -*- coding: utf-8 -*-
"""Numpy_&_Pandas_Task_using transactions file and product file data cleaning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vd7U_TdQJoiAt0e0QhSOXPh5WSUivpvr
"""

import pandas as pd
import numpy as np

# reading the transactions csv file and take first five rows using head()
transactions_df=pd.read_csv("/content/project_transactions.csv")
transactions_df.head()

# Calculate the total discount
transactions_df["total_discount"] = transactions_df["RETAIL_DISC"] + transactions_df["COUPON_DISC"]

transactions_df.head()

# Calculate the percentage discount
transactions_df["percentage_discount"] = (transactions_df["total_discount"] / transactions_df["SALES_VALUE"]).abs()

transactions_df.head()

#If the percentage discount is greater than 1, set it equal to 1
transactions_df["percentage_discount"] = np.where(transactions_df["percentage_discount"] > 1, 1, transactions_df["percentage_discount"])
#If it is less than 0, set it to 0.
transactions_df["percentage_discount"] = np.where(transactions_df["percentage_discount"] < 0, 0, transactions_df["percentage_discount"])

transactions_df.head()

#Drop the individual discount columns (`RETAIL_DISC`, `COUPON_DISC`, `COUPON_MATCH_DISC`)
transactions_df=transactions_df.drop(["RETAIL_DISC","COUPON_DISC","COUPON_MATCH_DISC"], axis=1)

transactions_df.head()

#The total sales (sum of `SALES_VALUE`)
total_sales_value=transactions_df['SALES_VALUE'].sum()
print(total_sales_value)

#Total discount (sum of `total_discount`)
total_discount_value=transactions_df['total_discount'].sum()
print(total_discount_value)

#Overall percentage discount (sum of total_discount / sum of sales value)
overall_percentage_discount_value=total_discount_value/total_sales_value * 100
print(overall_percentage_discount_value)

#Total quantity sold (sum of `QUANTITY`)
total_quantity_sold_value=transactions_df['QUANTITY'].sum()
print(total_quantity_sold_value)

#Max quantity sold in a single row. Inspect the row as well. Does this have a high discount percentage?
max_quantity_sold_value = transactions_df["QUANTITY"].max()
max_quantity_row = transactions_df[transactions_df["QUANTITY"] == max_quantity_sold_value]
max_quantity_row.head()

#Total sales value per basket (sum of sales value / nunique basket_id).
total_sales_value_per_basket = total_sales_value / transactions_df["BASKET_ID"].nunique()
print(total_sales_value_per_basket)

# Total sales value per household (sum of sales value / nunique household_key)
total_sales_value_per_household = total_sales_value/ transactions_df["household_key"].nunique()
print(total_sales_value_per_household)

transactions_df.columns

# reading the product csv file
product_df=pd.read_csv("/content/product.csv")
product_df.head()

product_df.columns

join_df = pd.merge(transactions_df, product_df, how='inner', on='PRODUCT_ID')
print(join_df)

# Join the two DataFrames on the `Product ID` column
joined_df = transactions_df.merge(product_df, on="PRODUCT_ID")
joined_df.head()

"""Product Analysis

* Which products had the most sales by sales_value? Plot  a horizontal bar chart.
* Did the top 10 selling items have a higher than average discount rate?
* What was the most common `PRODUCT_ID` among rows with the households in our top 10 households by sales value?
* Look up the names of the  top 10 products by sales in the `products.csv` dataset.
* Look up the product name of the item that had the highest quantity sold in a single row.
"""

# Get the top 10 selling items by sales value
top_10_selling_items = joined_df.sort_values("QUANTITY", ascending=False).head(10)

import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Find products with the most sales by sales_value and plot a horizontal bar chart
top_selling_products = transactions_df.groupby('PRODUCT_ID')['SALES_VALUE'].sum().nlargest(10)
top_selling_products_info = product_df[product_df['PRODUCT_ID'].isin(top_selling_products.index)]
top_selling_products_info = top_selling_products_info.merge(top_selling_products, on='PRODUCT_ID')
top_selling_products_info.sort_values(by='SALES_VALUE', ascending=False, inplace=True)

plt.figure(figsize=(10, 6))
plt.barh(top_selling_products_info['PRODUCT_ID'], top_selling_products_info['SALES_VALUE'])
plt.xlabel('Sales Value')
plt.ylabel('Product ID')
plt.title('Top 10 Selling Products by Sales Value')
plt.show()

# Step 2: Check if the top 10 selling items had a higher than average discount rate
average_discount_rate = transactions_df['percentage_discount'].mean()
top_selling_items_discount_rate = transactions_df[transactions_df['PRODUCT_ID'].isin(top_selling_products.index)]['percentage_discount'].mean()
top_10_items_have_higher_discount = top_selling_items_discount_rate > average_discount_rate
print("Did the top 10 selling items have a higher than average discount rate?", top_10_items_have_higher_discount)

# Step 3: Find the most common PRODUCT_ID among rows with the households in the top 10 households by sales value
top_10_households = transactions_df.groupby('household_key')['SALES_VALUE'].sum().nlargest(10)
most_common_product_id_in_top_10_households = transactions_df[transactions_df['household_key'].isin(top_10_households.index)]['PRODUCT_ID'].mode().values[0]
print("Most common PRODUCT_ID among rows with the top 10 households by sales value:", most_common_product_id_in_top_10_households)

# Step 4: Look up the names of the top 10 products by sales in the products.csv dataset
top_selling_products_info = top_selling_products_info[['PRODUCT_ID', 'COMMODITY_DESC', 'SUB_COMMODITY_DESC', 'CURR_SIZE_OF_PRODUCT']]
print("Top 10 Selling Products:")
print(top_selling_products_info)

# Step 5: Find the product name of the item that had the highest quantity sold in a single row
max_quantity_product_id = transactions_df.loc[transactions_df['QUANTITY'].idxmax(), 'PRODUCT_ID']
product_name_highest_quantity = product_df.loc[product_df['PRODUCT_ID'] == max_quantity_product_id, 'COMMODITY_DESC'].values[0]
print("Product name of the item with the highest quantity sold in a single row:", product_name_highest_quantity)

