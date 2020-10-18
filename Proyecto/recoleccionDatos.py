import requests as req
from pymongo import MongoClient
import datetime

api_add='https://api.openweathermap.org/data/2.5/weather?lat=60.842946&lon=10.407098&appid=25033c9a977704fc141a3b4043acdb8c'
json_data = req.get(api_add).json()

try:
    conn = MongoClient("mongodb+srv://usr_json:881127Son@cluster0.exca8.mongodb.net/dataDB?retryWrites=true&w=majority")
    print('Connected succesfully')
except ValueError:
    print('Cloud not connect to MongoDB')

temp =json_data['main']['temp']
temp-=273.15
temp_max=json_data['main']['temp_max']
temp_max-=273.15
temp_min=json_data['main']['temp_min']
temp_min-=273.15
pressure=json_data['main']['pressure']
humidity=json_data['main']['humidity']
#seal_level=json_data['main']['sea_level']
#grnd_level=json_data['main']['grnd_level']
feels_like=json_data['main']['feels_like']
speed=json_data['wind']['speed']
deg=json_data['wind']['deg']
timezone=json_data['timezone']
name=json_data['name']
lon=json_data['coord']['lon']
lat=json_data['coord']['lat']

data_harvest={
    "temp":temp,
    "temp_max":temp_max,
    "temp_min":temp_min,
    "pressure":pressure,
    "humidity":humidity,
    #"seal_level":seal_level,
    #"grnd_level":grnd_level,
    "feels_like":feels_like,
    "speed":speed,
    "deg":deg,
    "timezone":timezone,
    "name":name,
    "lon":lon,
    "lat":lat,
    "date": datetime.datetime.now()
}

db = conn.dataDB
collection = db.gfg_collection

data_insert = collection.insert_one(data_harvest)
#print("Data inserted with record ids",data_insert)
cursor = collection.find()
#for record in cursor:
#    print(record)
