from fastapi import FastAPI, Request, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from weather_service import WeatherService, WeatherAPIError
from user_preferences import UserPreferenceManager
from weather_quotes import WeatherQuotes
import os
from datetime import datetime
from typing import List, Optional

# Create FastAPI app
app = FastAPI(title="Weather Forecast App")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Create services
weather_service = WeatherService(cache_dir="cache")
preference_manager = UserPreferenceManager(file_path="preferences.json")
quote_service = WeatherQuotes()

def get_weather_styling(description: str) -> dict:
    """Determine weather card styling and icon based on description"""
    description_lower = description.lower()
    
    # Default values
    weather_style = "primary"
    weather_icon = "fas fa-cloud-sun"
    animation_class = ""
    
    if "clear" in description_lower or "sun" in description_lower:
        weather_style = "sunny"
        weather_icon = "fas fa-sun"
        animation_class = "sunny-animation"
        
        # Check if it's night time (simulated)
        current_hour = datetime.now().hour
        if current_hour < 6 or current_hour > 18:
            weather_style = "night"
            weather_icon = "fas fa-moon"
            animation_class = ""
    elif "cloud" in description_lower:
        weather_style = "cloudy"
        weather_icon = "fas fa-cloud"
        animation_class = "cloudy-animation"
    elif "rain" in description_lower or "drizzle" in description_lower:
        weather_style = "rainy"
        weather_icon = "fas fa-cloud-rain"
        animation_class = "rain-animation"
    elif "snow" in description_lower:
        weather_style = "snowy"
        weather_icon = "fas fa-snowflake"
        animation_class = "snow-animation"
    elif "storm" in description_lower or "thunder" in description_lower:
        weather_style = "stormy"
        weather_icon = "fas fa-bolt"
        animation_class = "storm-animation"
    elif "mist" in description_lower or "fog" in description_lower:
        weather_style = "cloudy"
        weather_icon = "fas fa-smog"
        animation_class = "cloudy-animation"
    
    return {
        "style": weather_style,
        "icon": weather_icon,
        "animation": animation_class
    }

def get_weather_alerts(description: str) -> list:
    """Generate weather alerts based on conditions"""
    alerts = []
    description_lower = description.lower()
    
    if "rain" in description_lower and "heavy" in description_lower:
        alerts.append({
            "title": "Heavy Rain Warning",
            "message": "Heavy rainfall expected. Potential for localized flooding in some areas.",
            "icon": "fas fa-exclamation-triangle"
        })
    elif "snow" in description_lower:
        alerts.append({
            "title": "Snow Advisory",
            "message": "Snowfall expected. Roads may be slippery, drive with caution.",
            "icon": "fas fa-snowflake"
        })
    elif "storm" in description_lower or "thunder" in description_lower:
        alerts.append({
            "title": "Severe Thunderstorm Warning",
            "message": "Thunderstorms with potential for lightning strikes and strong winds.",
            "icon": "fas fa-bolt"
        })
    
    return alerts

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page with saved preferences if available"""
    preferences = preference_manager.get_preferences()
    default_location = preferences.get("default_location", "")
    favorite_locations = preferences.get("favorite_locations", [])
    
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "default_location": default_location,
            "favorite_locations": favorite_locations,
            "preferences": preferences
        }
    )

@app.post("/weather", response_class=HTMLResponse)
async def get_weather(
    request: Request, 
    location: str = Form(...), 
    save_preference: bool = Form(False),
    add_to_favorites: bool = Form(False)
):
    """Get weather data for the specified location"""
    try:
        # Save preference if it is requested
        if save_preference:
            preference_manager.save_preference("default_location", location)
        
        # Add to favorites if requested
        if add_to_favorites:
            preference_manager.add_favorite_location(location)
        
        # Get weather data
        weather_data = weather_service.get_weather(location)
        
        # Get user preferences
        preferences = preference_manager.get_preferences()
        favorite_locations = preferences.get("favorite_locations", [])
        is_favorite = location in favorite_locations
        
        # Get weather styling
        current_styling = get_weather_styling(weather_data["description"])
        
        # Get weather quote
        weather_quote = quote_service.get_random_quote(weather_data["description"])
        
        # Get weather alerts
        weather_alerts = get_weather_alerts(weather_data["description"])
        
        # Add additional data for enhanced UI (simulated)
        current_time = datetime.now()
        
        # Add sunrise and sunset times (simulated)
        sunrise_time = current_time.replace(hour=6, minute=30, second=0).strftime("%H:%M")
        sunset_time = current_time.replace(hour=19, minute=45, second=0).strftime("%H:%M")
        
        # Add air quality (simulated)
        air_quality = {
            "index": 2,  # 1=Good, 2=Moderate, 3=Unhealthy for sensitive groups, 4=Unhealthy, 5=Very Unhealthy
            "description": "Moderate"
        }
        
        # Add "feels like" temperature (simulated)
        feels_like = round(weather_data["temperature"] + 2, 1)
        
        # Add pressure and visibility (simulated)
        pressure = 1013  # hPa
        visibility = 10  # km
        
        # Add UV index (simulated)
        uv_index = 4  # 0-2=Low, 3-5=Moderate, 6-7=High, 8-10=Very High, 11+=Extreme
        
        # Process forecast data with styling
        forecast_with_styling = []
        for day in weather_data.get("forecast", []):
            day_styling = get_weather_styling(day["description"])
            forecast_with_styling.append({
                **day,
                "styling": day_styling
            })
        
        # Render the template with enhanced weather data
        return templates.TemplateResponse(
            "weather.html", 
            {
                "request": request, 
                "location": location,
                "temperature": weather_data["temperature"],
                "description": weather_data["description"],
                "humidity": weather_data["humidity"],
                "wind_speed": weather_data["wind_speed"],
                "forecast": forecast_with_styling,
                # Styling information
                "current_styling": current_styling,
                "weather_quote": weather_quote,
                # Additional data for enhanced UI
                "feels_like": feels_like,
                "pressure": pressure,
                "visibility": visibility,
                "sunrise": sunrise_time,
                "sunset": sunset_time,
                "air_quality": air_quality,
                "uv_index": uv_index,
                "weather_alerts": weather_alerts,
                # Preferences
                "is_favorite": is_favorite,
                "favorite_locations": favorite_locations,
                "preferences": preferences
            }
        )
    except WeatherAPIError as e:
        return templates.TemplateResponse(
            "error.html", 
            {"request": request, "error_message": str(e)}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html", 
            {"request": request, "error_message": f"An unexpected error occurred: {str(e)}"}
        )

@app.get("/weather", response_class=HTMLResponse)
async def get_weather_get(request: Request, location: str = Query(...)):
    """Handle GET requests for weather (from favorite locations)"""
    return await get_weather(request, location, False, False)

@app.get("/clear-cache", response_class=HTMLResponse)
async def clear_cache(request: Request):
    """Clear the cached weather data"""
    try:
        weather_service.clear_cache()
        return templates.TemplateResponse(
            "message.html", 
            {"request": request, "message": "Cache cleared successfully! Fresh weather data will be fetched on your next search."}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html", 
            {"request": request, "error_message": f"Error clearing cache: {str(e)}"}
        )

@app.get("/preferences", response_class=HTMLResponse)
async def preferences_page(request: Request, saved: str = Query(None), error: str = Query(None)):
    """Render the preferences page"""
    preferences = preference_manager.get_preferences()
    return templates.TemplateResponse(
        "preferences.html", 
        {
            "request": request, 
            "preferences": preferences,
            "saved": saved,
            "error": error
        }
    )

@app.post("/save-preferences", response_class=RedirectResponse)
async def save_preferences(
    default_location: str = Form(""),
    units: str = Form("metric"),
    refresh_interval: int = Form(30),
    show_alerts: bool = Form(False),
    map_default_layer: str = Form("temp")
):
    """Save user preferences"""
    try:
        preference_manager.save_preference("default_location", default_location)
        preference_manager.save_preference("units", units)
        preference_manager.save_preference("refresh_interval", refresh_interval)
        preference_manager.save_preference("show_alerts", show_alerts)
        preference_manager.save_preference("map_default_layer", map_default_layer)
        
        return RedirectResponse(url="/preferences?saved=true", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/preferences?error={str(e)}", status_code=303)

@app.post("/add-favorite", response_class=RedirectResponse)
async def add_favorite(location: str = Form(...)):
    """Add a location to favorites"""
    preference_manager.add_favorite_location(location)
    return RedirectResponse(url=f"/weather?location={location}", status_code=303)

@app.post("/remove-favorite", response_class=RedirectResponse)
async def remove_favorite(location: str = Form(...)):
    """Remove a location from favorites"""
    preference_manager.remove_favorite_location(location)
    return RedirectResponse(url=f"/weather?location={location}", status_code=303)

@app.get("/comparison", response_class=HTMLResponse)
async def comparison_form(request: Request):
    """Render the weather comparison form"""
    preferences = preference_manager.get_preferences()
    favorite_locations = preferences.get("favorite_locations", [])
    units = preferences.get("units", "metric")
    
    return templates.TemplateResponse(
        "comparison-form.html", 
        {
            "request": request,
            "favorite_locations": favorite_locations,
            "units": units,
            "theme": "light"
        }
    )

@app.post("/compare-weather", response_class=HTMLResponse)
async def compare_weather_post(
    request: Request,
    location1: str = Form(...),
    location2: str = Form(...),
    units: str = Form("metric")
):
    """Compare weather between two locations (POST)"""
    return await compare_weather_logic(request, location1, location2, units)

@app.get("/compare-weather", response_class=HTMLResponse)
async def compare_weather_get(
    request: Request,
    location1: str = Query(...),
    location2: str = Query(...),
    units: str = Query("metric")
):
    """Compare weather between two locations (GET)"""
    return await compare_weather_logic(request, location1, location2, units)

async def compare_weather_logic(request: Request, location1: str, location2: str, units: str):
    """Common logic for weather comparison"""
    try:
        # Get weather data for both locations
        weather1 = weather_service.get_weather_for_comparison(location1, units)
        weather2 = weather_service.get_weather_for_comparison(location2, units)
        
        return templates.TemplateResponse(
            "comparison.html",
            {
                "request": request,
                "location1": location1,
                "location2": location2,
                "weather1": weather1,
                "weather2": weather2,
                "units": units,
                "theme": "light"
            }
        )
        
    except WeatherAPIError as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error_message": f"Error comparing weather: {str(e)}"}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error_message": f"An unexpected error occurred: {str(e)}"}
        )

if __name__ == "__main__":
    os.makedirs("cache", exist_ok=True)
    uvicorn.run("main:app", host="0.0.0.0", port=4000, reload=True)
