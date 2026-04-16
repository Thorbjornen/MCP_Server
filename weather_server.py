import sys
import json
import random
import datetime
from typing import List, Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ChronosWeatherSystem")

# Base de données simulée
WEATHER_DB = {
    "Paris": {"temp": 15, "condition": "Nuageux", "humidity": 75},
    "New York": {"temp": 22, "condition": "Ensoleillé", "humidity": 45},
    "Tokyo": {"temp": 18, "condition": "Pluvieux", "humidity": 85},
    "Lyon": {"temp": 14, "condition": "Vent violent", "humidity": 60},
    "London": {"temp": 12, "condition": "Brumeux", "humidity": 90},
    "Berlin": {"temp": 10, "condition": "Couvert", "humidity": 70}
}
DISTANCES = {
    ("Paris", "Lyon"): 465,
    ("Paris", "London"): 344,
    ("Paris", "Berlin"): 878,
    ("New York", "Tokyo"): 10838,
    ("London", "Berlin"): 932
}

# Statistiques d'utilisation
TOOL_STATS = {
    "get_available_cities": 0, "get_weather": 0, "calculate_travel_time": 0,
    "get_travel_recommendation": 0, "get_city_comparison": 0
}

def increment_stat(name):
    if name in TOOL_STATS: TOOL_STATS[name] += 1

class ErrorCodes:
    CITY_NOT_FOUND = "CITY_NOT_FOUND"
    EMPTY_PARAMETER = "EMPTY_PARAMETER"
    SAME_CITY = "SAME_CITY"

def create_response(data: Any = None, error_code: str = None, msg: str = None) -> str:
    if error_code:
        return json.dumps({"status": "error", "error": {"code": error_code, "message": msg}})
    return json.dumps(data)

# --- OUTILS & RESSOURCES ---

@mcp.resource("stats://tool-usage")
def get_tool_stats() -> str:
    return json.dumps(TOOL_STATS)

@mcp.tool()
def get_available_cities() -> List[str]:
    increment_stat("get_available_cities")
    return list(WEATHER_DB.keys())

@mcp.tool()
def get_weather(city: str) -> str:
    increment_stat("get_weather")
    if not city: return create_response(error_code=ErrorCodes.EMPTY_PARAMETER, msg="Ville requise")
    city = city.title()
    if city in WEATHER_DB:
        d = WEATHER_DB[city].copy()
        d["timestamp"] = datetime.datetime.now().isoformat()
        return create_response(data=d)
    return create_response(error_code=ErrorCodes.CITY_NOT_FOUND, msg=f"Ville {city} inconnue")

@mcp.tool()
def calculate_travel_time(origin: str, destination: str, speed_kmh: float = 100.0) -> str:
    increment_stat("calculate_travel_time")
    o, d = origin.title(), destination.title()
    if o == d: return create_response(error_code=ErrorCodes.SAME_CITY, msg="Même ville")
    dist = DISTANCES.get((o, d)) or DISTANCES.get((d, o)) or random.randint(100,1000)
    return create_response(data={"origin": o, "destination": d, "hours": dist/speed_kmh})

@mcp.tool()
def get_travel_recommendation(city: str) -> str:
    increment_stat("get_travel_recommendation")
    w_json = get_weather(city)
    if "error" in w_json: return w_json
    w_data = json.loads(w_json)
    # Note: Simplifié selon la tâche 6.3 du notebook
    return create_response(data={"city": city, "rec": f"Météo: {w_data.get('temp')}°C"})

@mcp.tool()
def get_city_comparison(city1: str, city2: str) -> str:
    increment_stat("get_city_comparison")
    c1, c2 = city1.title(), city2.title()
    if c1 not in WEATHER_DB or c2 not in WEATHER_DB:
        return create_response(error_code=ErrorCodes.CITY_NOT_FOUND, msg="Ville inconnue")
    diff = WEATHER_DB[c1]["temp"] - WEATHER_DB[c2]["temp"]
    return create_response(data={"comparison": f"{c1} vs {c2}", "diff": abs(diff)})

if __name__ == "__main__":
    mcp.run()