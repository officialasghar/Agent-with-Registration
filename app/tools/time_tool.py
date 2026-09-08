from langchain.tools import tool
from datetime import datetime
from zoneinfo import ZoneInfo
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import ssl
import certifi


ssl_context = ssl.create_default_context(
    cafile=certifi.where()
)

geolocator = Nominatim(
    user_agent="weather_agent",
    ssl_context=ssl_context
)

tf = TimezoneFinder()


@tool
def get_current_time(city: str) -> str:
    """
    Get the current local date and time for any city in the world.
    """

    location = geolocator.geocode(city)

    if not location:
        return f"Could not find the location: {city}"

    timezone = tf.timezone_at(
        lng=location.longitude,
        lat=location.latitude
    )

    if not timezone:
        return f"Could not determine timezone for {city}"

    current_time = datetime.now(ZoneInfo(timezone))

    return (
        f"Current time in {city}: "
        f"{current_time.strftime('%Y-%m-%d %I:%M:%S %p')} "
        f"({timezone})"
    )