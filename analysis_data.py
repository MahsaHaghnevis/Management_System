import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to SQLite database
conn = sqlite3.connect('warehouse_management.db')

# Load data into pandas DataFrame
third_party_df = pd.read_sql_query('SELECT * FROM TPL', conn)
user_df = pd.read_sql_query('SELECT * FROM User', conn)
warehouse_df = pd.read_sql_query('SELECT * FROM Warehouse', conn)
catalog_df = pd.read_sql_query('SELECT * FROM Catalog', conn)
orders_df = pd.read_sql_query('SELECT * FROM Orders', conn)
location_df = pd.read_sql_query('SELECT * FROM Location', conn)

# Close the connection
conn.close()

# Descriptive Statistics
print("Descriptive Statistics for Users Age:")
print(user_df['Age'].describe())

print("\nDescriptive Statistics for Order Total Cost:")
print(orders_df['Total_cost'].describe())

# Frequency Distribution
print("\nFrequency Distribution for User Types:")
print(user_df['Type'].value_counts())

# Histogram for numerical data
plt.figure(figsize=(12, 6))
plt.hist(user_df['Age'], bins=20, alpha=0.7, label='Age')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.title('Histogram of User Ages')
plt.legend()
plt.show()

plt.figure(figsize=(12, 6))
plt.hist(orders_df['Total_cost'], bins=20, alpha=0.7, label='Total Cost')
plt.xlabel('Total Cost')
plt.ylabel('Frequency')
plt.title('Histogram of Order Total Costs')
plt.legend()
plt.show()

# Box Plot for numerical data
plt.figure(figsize=(12, 6))
sns.boxplot(x=user_df['Age'])
plt.title('Box Plot of User Ages')
plt.show()

plt.figure(figsize=(12, 6))
sns.boxplot(x=orders_df['Total_cost'])
plt.title('Box Plot of Order Total Costs')
plt.show()

# Distribution Plot
plt.figure(figsize=(12, 6))
sns.distplot(user_df['Age'], bins=20, kde=True)
plt.title('Distribution Plot of User Ages')
plt.show()

plt.figure(figsize=(12, 6))
sns.distplot(orders_df['Total_cost'], bins=20, kde=True)
plt.title('Distribution Plot of Order Total Costs')
plt.show()

# Cross-Tabulation for categorical data
print("\nCross-Tabulation for User Types and Third Party IDs:")
cross_tab = pd.crosstab(user_df['Type'], user_df['TP_ID'])
print(cross_tab)
