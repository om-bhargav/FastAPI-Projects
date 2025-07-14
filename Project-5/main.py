from fastapi import FastAPI
import requests as r

app = FastAPI()




@app.get("/search/{city_name}")
def get_Weather(city_name):
      data = r.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={your_API_KEY}")
      return data.json()
