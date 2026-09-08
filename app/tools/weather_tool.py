from langchain_core.tools import tool
from dotenv import load_dotenv
import os
import requests

load_dotenv()

api_key_weather=os.getenv("WEATHER_API_KEY")


@tool
def get_weather(city_name, api_key=api_key_weather):
    """get weather of any location ,city"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            weather = {
                "city": data["name"],
                "temperature": f"{data['main']['temp']}°C",
                "condition": data["weather"][0]["description"].title(),
                "humidity": f"{data['main']['humidity']}%",
                "wind_speed": f"{data['wind']['speed']} m/s"
            }
            return weather
        else:
            return {"error": data.get("message", "City not found")}
            
    except Exception as e:
        return {"error": str(e)}


