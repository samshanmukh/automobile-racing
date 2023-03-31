import requests
import seaborn as sns
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
# Make a GET request to the webpage
url = 'https://speedwaycollective.com/drivers/stats'
response = requests.get(url)

# Parse the HTML content of the page using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the tables on the page
tables = soup.find_all('table')

# Assume that the table containing the driver stats is the first one
table = tables[0]

# Extract the data rows of the table
data_rows = table.find_all('tr')
driver_stats_list = []
for i, row in enumerate(data_rows):
    if i == 0:
        # This is the header row
        header_columns = [th.text.strip() for th in row.find_all('th')]
    else:
        # This is a data row
        data_cells = [td.text.strip() for td in row.find_all('td')]
        driver_stats = dict(zip(header_columns, data_cells))
        driver_stats_list.append(driver_stats)

# Create a DataFrame
df = pd.DataFrame(driver_stats_list)

# Clean up the data types
df = df.apply(pd.to_numeric, errors='ignore')
# df.head()

# ... (The rest of your code is the same until creating the DataFrame)

# Clean up the data types
# df = df.apply(pd.to_numeric, errors='ignore')

# Print the DataFrame
# print(df.head())

# Create a bar chart showing the distribution of top 5s by class
plt.figure()
sns.countplot(data=df, x='Class', hue='Top 5')
plt.title('Distribution of Top 5s by Class')
plt.xlabel('Class')
plt.ylabel('Top 5')
plt.savefig('static/many_fig1.png')
# plt.show()

# Create a bar chart showing the distribution of top 10s by class
plt.figure()
sns.countplot(data=df, x='Top 10', hue='Class')
plt.title('Distribution of Top 10s by Class')
plt.xlabel('Top 10')
plt.ylabel('Class')
plt.savefig('static/many_fig2.png')
# plt.show()

# Create a line chart showing the number of wins over time by driver
plt.figure()
sns.lineplot(data=df, x='Driver', y='Wins')
plt.title('Number of Wins Over Time')
plt.xlabel('Driver')
plt.ylabel('Wins')
plt.xticks(rotation=90)
plt.savefig('static/many_fig3.png')
# plt.show()

# Create a bar chart showing the number of wins by class
plt.figure()
sns.barplot(data=df, x='Class', y='Wins', estimator=sum, ci=None)
plt.title('Number of Wins by Class')
plt.xlabel('Class')
plt.ylabel('Wins')
plt.savefig('static/many_fig4.png')
# plt.show()

# Heatmap of Correlation Matrix
plt.figure(figsize=(12, 6))
sns.heatmap(df.corr(), annot=True, cmap='YlGnBu')
plt.title('Correlation Matrix')
plt.tight_layout()
plt.savefig('static/many_heatmap.png')
# plt.show()