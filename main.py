from typing import Union, Optional

from fastapi import FastAPI, status, Request, Response, Depends, Query
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from fastapi.staticfiles import StaticFiles
import builtins

import requests

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

templates = Jinja2Templates(directory="templates")

# Redirect the root URL to the home endpoint
@app.get("/")
async def root():
    return RedirectResponse(url="/motogp")

@app.get("/list-data")
async def read_json_data(request: Request):
    response = requests.get(motogp_url)
    json_data = response.json()
    return templates.TemplateResponse("list.html", {"request": request, "items": json_data})

motogp_url = 'https://raw.githubusercontent.com/samshanmukh/automobile-racing/master/motogp.json'
nascar_url = 'https://raw.githubusercontent.com/samshanmukh/automobile-racing/master/NASCARChampionHistoryDataset.json'
formula1_url = 'https://raw.githubusercontent.com/samshanmukh/automobile-racing/master/formula1.json'

#### Sanmukh Sain Karri ####
@app.get("/motogp")
async def read_json_data(request: Request):
    response = requests.get(motogp_url)
    json_data = response.json()
    return templates.TemplateResponse("motogp.html", {"request": request, "items": json_data})

@app.get("/motogp-json")
async def read_json_data():
    response = requests.get(motogp_url)
    json_data = response.json()
    return json_data

@app.get("/motogp-position-json")
async def read_json_data(position: int = Query(None)):
    response = requests.get(motogp_url)
    json_data = response.json()
    
    # Filter the JSON data based on the position query parameter
    if position is not None:
        filtered_data = [item for item in json_data if item['position'] == position]
        return filtered_data
    
    return json_data

@app.get("/motogp-bikes-json")
async def read_json_data(bike_name: Optional[str] = None):
    response = requests.get(motogp_url)
    json_data = response.json()
    
    if bike_name:
        json_data = [item for item in json_data if item["bike_name"].lower() == bike_name.lower()]
    
    return json_data


#### Manideep Reddy ####
@app.get("/nascar")
async def read_json_data(request: Request):
    response = requests.get(nascar_url)
    json_data = response.json()
    return templates.TemplateResponse("nascar.html", {"request": request, "items": json_data})

@app.get("/nascar-json")
async def read_json_data():
    response = requests.get(nascar_url)
    json_data = response.json()
    return json_data

@app.get("/nascar-wins-json")
async def read_json_data(wins: int = None):
    response = requests.get(nascar_url)
    json_data = response.json()
    if wins is not None:
        filtered_data = [item for item in json_data if item.get("Wins") == wins]
        return filtered_data
    return json_data

@app.get("/nascar-menufacturer-json")
async def read_json_data(manufacturer: str = None):
    response = requests.get(nascar_url)
    json_data = response.json()

    if manufacturer:
        json_data = [item for item in json_data if item.get('Car Manufacturer') == manufacturer]

    return json_data



#### Adarsh Bayya ####
@app.get("/formula1")
async def read_json_data(request: Request):
    response = requests.get(formula1_url)
    json_data = response.json()
    return templates.TemplateResponse("formula1.html", {"request": request, "items": json_data})

@app.get("/formula1-json")
async def read_json_data():
    response = requests.get(formula1_url)
    json_data = response.json()
    return json_data

@app.get("/formula1-championship-json")
async def read_json_data(world_championships: Optional[int] = None):
    response = requests.get(formula1_url)
    json_data = response.json()

    if world_championships:
        json_data = [entry for entry in json_data if entry['World Championships'] == world_championships]

    return json_data

@app.get("/formula1-team-json")
async def read_json_data(team: str = None):
    response = requests.get(formula1_url)
    json_data = response.json()

    if team:
        json_data = [entry for entry in json_data if entry['Team'] == team]

    return json_data

@app.get("/sam_agg", response_class=HTMLResponse)
async def read_item(request: Request):
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
    fastest_time = df.loc[0, "Time"]

    # Get the top three positions
    top_three = df.loc[:2, ["Pos", "Rider", "Bike"]]

    # Calculate the biggest time gap
    biggest_gap = df.loc[19, "Gap"]

    # Count the number of each bike model
    bike_counts = df["Bike"].value_counts()

    # Get the rider with the highest speed
    max_speed = df["Speed"].max()
    max_speed_rider = df.loc[df["Speed"] == max_speed]

    # Get the slowest rider
    slowest_rider = df.loc[19, "Rider"]
    slowest_speed = df.loc[19, "Speed"]
    return templates.TemplateResponse("sam_agg_results.html", {
        "request": request, 
        "df": df, 
        "total_races": len(df),
        "fastest_time": fastest_time, 
        "top_three": top_three, 
        "biggest_gap": biggest_gap, 
        "bike_counts": bike_counts, 
        "max_speed_rider": max_speed_rider, 
        "max_speed": max_speed, 
        "slowest_rider": slowest_rider, 
        "slowest_speed": slowest_speed,
        "len": builtins.len  # pass the len function to the template context
    })
    # Put the code you want to execute here
    # return templates.TemplateResponse("sam_agg_results.html", {"request": request, "df": df})
