from typing import Union, Optional

from fastapi import FastAPI, status, Request, Response, Depends, Query
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

import requests

app = FastAPI()

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