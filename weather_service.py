import requests
import json
import os
import time
from typing import Dict, Any, List, Optional

class WeatherAPIError(Exception):
    """Custom exception for weather API errors"""
    pass

class WeatherService:
    """Service to fetch and cache weather data"""
    
    def __init__(self, api_key: Optional[str] = None, cache_dir: str = "cache", cache_expiry: int = 1800):
        """
        Initialize the weather service
        
        Args:
            api_key: OpenWeatherMap API key (defaults to hardcoded key or env var)
            cache_dir: Directory to store cached data
            cache_expiry: Cache expiry time in seconds (default: 30 minutes)
        """
        self.api_key = api_key or "5671370a74ba9809b4987e39c7238b04"  # your actual API key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.cache_dir = cache_dir
        self.cache_expiry = cache_expiry
        
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def get_weather(self, location: str, units: str = "metric") -> Dict[str, Any]:
        cached_data = self._get_cached_data(location, units)
        if cached_data:
            print(f"Using cached data for {location}")
            return cached_data
        
        try:
            print(f"Fetching fresh data for {location}")
            current_weather = self._fetch_current_weather(location, units)
            forecast = self._fetch_forecast(location, units)
            
            weather_data = {
                "temperature": round(current_weather["main"]["temp"], 1),
                "description": current_weather["weather"][0]["description"].capitalize(),
                "humidity": current_weather["main"]["humidity"],
                "wind_speed": current_weather["wind"]["speed"],
                "pressure": current_weather["main"]["pressure"],
                "feels_like": round(current_weather["main"]["feels_like"], 1),
                "weather_icon": current_weather["weather"][0]["icon"],
                "weather_condition": current_weather["weather"][0]["main"],
                "weather_description": current_weather["weather"][0]["description"].capitalize(),
                "country": current_weather["sys"]["country"],
                "forecast": self._format_forecast(forecast, units)
            }
            
            self._cache_data(location, weather_data, units)
            return weather_data
            
        except requests.RequestException as e:
            raise WeatherAPIError(f"Network error while fetching weather data: {str(e)}")
        except (KeyError, json.JSONDecodeError) as e:
            raise WeatherAPIError(f"Error parsing weather data: {str(e)}")
        except Exception as e:
            raise WeatherAPIError(f"Unexpected error: {str(e)}")
    
    def get_weather_for_comparison(self, location: str, units: str = "metric") -> Dict[str, Any]:
        try:
            current_weather = self._fetch_current_weather(location, units)
            return {
                "temperature": round(current_weather["main"]["temp"], 1),
                "feels_like": round(current_weather["main"]["feels_like"], 1),
                "humidity": current_weather["main"]["humidity"],
                "wind_speed": current_weather["wind"]["speed"],
                "pressure": current_weather["main"]["pressure"],
                "weather_icon": current_weather["weather"][0]["icon"],
                "weather_condition": current_weather["weather"][0]["main"],
                "weather_description": current_weather["weather"][0]["description"].capitalize(),
                "country": current_weather["sys"]["country"]
            }
        except requests.RequestException as e:
            raise WeatherAPIError(f"Network error while fetching weather data: {str(e)}")
        except (KeyError, json.JSONDecodeError) as e:
            raise WeatherAPIError(f"Error parsing weather data: {str(e)}")
        except Exception as e:
            raise WeatherAPIError(f"Unexpected error: {str(e)}")
    
    def _fetch_current_weather(self, location: str, units: str = "metric") -> Dict[str, Any]:
        url = f"{self.base_url}/weather"
        params = {
            "q": location,
            "appid": self.api_key,
            "units": units
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            error_info = response.json().get("message", "Unknown error")
            raise WeatherAPIError(f"API error ({response.status_code}): {error_info}")
        return response.json()
    
    def _fetch_forecast(self, location: str, units: str = "metric") -> Dict[str, Any]:
        url = f"{self.base_url}/forecast"
        params = {
            "q": location,
            "appid": self.api_key,
            "units": units
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            error_info = response.json().get("message", "Unknown error")
            raise WeatherAPIError(f"API error ({response.status_code}): {error_info}")
        return response.json()
    
    def _format_forecast(self, forecast_data: Dict[str, Any], units: str = "metric") -> List[Dict[str, Any]]:
        daily_forecasts = []
        for i in range(0, len(forecast_data["list"]), 8):
            if i + 4 < len(forecast_data["list"]):
                item = forecast_data["list"][i + 4]
                daily_forecasts.append({
                    "date": item["dt_txt"].split(" ")[0],
                    "temperature": round(item["main"]["temp"], 1),
                    "description": item["weather"][0]["description"].capitalize(),
                    "humidity": item["main"]["humidity"],
                    "wind_speed": item["wind"]["speed"]
                })
        return daily_forecasts
    
    def _get_cached_data(self, location: str, units: str = "metric") -> Optional[Dict[str, Any]]:
        cache_file = os.path.join(self.cache_dir, f"{location.lower().replace(' ', '_')}_{units}.json")
        if os.path.exists(cache_file):
            if time.time() - os.path.getmtime(cache_file) < self.cache_expiry:
                try:
                    with open(cache_file, "r") as f:
                        return json.load(f)
                except (json.JSONDecodeError, IOError):
                    return None
        return None
    
    def _cache_data(self, location: str, data: Dict[str, Any], units: str = "metric") -> None:
        cache_file = os.path.join(self.cache_dir, f"{location.lower().replace(' ', '_')}_{units}.json")
        try:
            with open(cache_file, "w") as f:
                json.dump(data, f)
        except IOError as e:
            print(f"Error caching weather data: {str(e)}")
    
    def clear_cache(self) -> None:
        print("Clearing weather cache...")
        for filename in os.listdir(self.cache_dir):
            if filename.endswith(".json"):
                os.remove(os.path.join(self.cache_dir, filename))
        print("Cache cleared successfully")