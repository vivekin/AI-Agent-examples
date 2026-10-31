from datetime import datetime
import requests

# -----------------------------
# TOOL 1: Weather
# -----------------------------
def get_weather(city: str) -> dict:
    """
    Get current weather information for a city.

    Args:
        city: Name of the city.

    Returns:
        Weather information including temperature and description.
    """

    api_key = "85c018992bbfa282a6ac3f25861ca336"

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        print("API request status code:", response.status_code)

        response.raise_for_status()

        weather_data = response.json()

        temp = weather_data["main"]["temp"]
        weather_desc = weather_data["weather"][0]["description"]

        return {
            "city": city,
            "temperature": temp,
            "description": weather_desc
        }

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}



# -----------------------------
# TOOL 2: Current Time
# -----------------------------

def get_current_time() -> str:
    """Get the current system date and time."""

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# -----------------------------
# TOOL 3: Random cat facts
# -----------------------------
def get_cat_facts() -> str:
    """
    Get random cat facts.

    """
    print("function called from llm -> get_cat_facts")

    url = "https://catfact.ninja/fact?max_length=100"

    try:
        response = requests.get(url, timeout=10)

        print("API request status code:", response.status_code)

        response.raise_for_status()
        data = response.json()
        return data["fact"]

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
