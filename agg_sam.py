import requests
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Make a GET request to the website
url = 'https://motomatters.com/results?page=1%2C0%2C0%2C0%2C0'
response = requests.get(url)

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing the results data
table = soup.find('table', {'class': 'resultsTable'})

# Extract the table headers
headers = []
for th in table.find_all('th'):
    headers.append(th.text.strip())

# Extract the table rows
rows = []
for tr in table.find_all('tr')[1:]:
    row = []
    for td in tr.find_all('td'):
        row.append(td.text.strip())
    rows.append(row)

# Create a DataFrame from the rows and headers
df = pd.DataFrame(rows, columns=['Pos', 'No.', 'Rider', 'Bike', 'Time', 'Gap', 'Speed'])

print("*******************************************************************************")
print("*******************************************************************************")
# Extract the title from the HTML code snippet
title = soup.find("h3", class_="node__title").find("span")
print(title.text)
print("*******************************************************************************")
print("*******************************************************************************")



print("*******************************************************************************")
print(df)

print("*******************************************************************************")

# # Summary and analysis
print(f"Total number of races: {len(df)}")

print("---------------------------------------")

# Print the fastest lap time
fastest_time = df.loc[0, "Time"]
print("Fastest lap time: ", fastest_time)

print("---------------------------------------")
# Get the top three positions
top_three = df.loc[:2, ["Pos", "Rider", "Bike"]]
print("Top three positions: \n", top_three)

print("---------------------------------------")
# Calculate the biggest time gap
biggest_gap = df.loc[19, "Gap"]
print("Biggest time gap: ", biggest_gap)

print("---------------------------------------")
# Count the number of each bike model
bike_counts = df["Bike"].value_counts()
print("Bike model counts: \n", bike_counts)

print("---------------------------------------")
# Get the rider with the highest speed
max_speed = df["Speed"].max()
max_speed_rider = df.loc[df["Speed"] == max_speed]
print("Rider with the highest speed: ", max_speed_rider)
print("Speed: ", max_speed, "km/h")

print("---------------------------------------")
# Get the slowest rider
slowest_rider = df.loc[19, "Rider"]
slowest_speed = df.loc[19, "Speed"]
print("Slowest rider: ", slowest_rider)
print("Speed: ", slowest_speed, "km/h")


print("*******************************************************************************")

# Set a color palette for the graphs
colors = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B2", "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"]

# Plot the distribution of bike models used
plt.figure(figsize=(8,6))
plt.bar(bike_counts.index, bike_counts.values, color=colors)
plt.title("Distribution of Bike Models", color="#333333")
plt.xlabel("Bike Model", color="#333333")
plt.ylabel("Count", color="#333333")
plt.xticks(rotation=45, color="#333333")
plt.yticks(color="#333333")
# plt.show()
plt.savefig("templates/sam_agg_plot.png")

# Plot the lap times for the top 10 riders
top_10 = df.head(10)
plt.figure(figsize=(8,6))
plt.plot(top_10["Rider"], top_10["Time"], marker="o", color=colors[0])
plt.title("Lap Times for Top 10 Riders", color="#333333")
plt.xlabel("Rider", color="#333333")
plt.ylabel("Time (s)", color="#333333")
plt.xticks(rotation=45, color="#333333")
plt.yticks(color="#333333")
# plt.show()
plt.savefig("templates/sam_agg_plot1.png")

# Plot the speeds of all riders
plt.figure(figsize=(8,6))
plt.hist(df["Speed"], bins=10, color=colors[1])
plt.title("Speed Distribution", color="#333333")
plt.xlabel("Speed (km/h)", color="#333333")
plt.ylabel("Count", color="#333333")
plt.xticks(color="#333333")
plt.yticks(color="#333333")
# plt.show()
plt.savefig("templates/sam_agg_plot2.png")

# Plot the position vs speed for all riders
plt.figure(figsize=(8,6))
plt.scatter(df["Pos"], df["Speed"], marker="x", color=colors[2])
plt.title("Position vs Speed", color="#333333")
plt.xlabel("Position", color="#333333")
plt.ylabel("Speed (km/h)", color="#333333")
plt.xticks(color="#333333")
plt.yticks(color="#333333")
# plt.show()
plt.savefig("templates/sam_agg_plot3.png")

# Plot 4: Scatter plot of Speed vs. Time
plt.figure(figsize=(10, 5))
sns.scatterplot(x='Time', y='Speed', data=df, color=colors[3])
plt.xlabel('Race Time', color="#333333")
plt.ylabel('Speed', color="#333333")
plt.title('Speed vs. Race Time', color="#333333")
plt.xticks(color="#333333")
plt.yticks(color="#333333")
# plt.show()
plt.savefig("templates/sam_agg_plot4.png")


print("""
Overall, the site seems to be a reliable and informative source for MotoGP and World Superbike fans, 
and I would recommend it for anyone looking for up-to-date race results and news.
""")

