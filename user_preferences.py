import json
import os
from typing import Dict, Any, Optional, List

class UserPreferenceManager:
    """Manages user preferences for the weather app"""
    
    def __init__(self, file_path: str = "preferences.json"):
        """
        this will initialize the preference manager
        
        Args:
            file_path: Path to the preferences file
        """
        self.file_path = file_path
        self._ensure_preferences_file()
    
    def _ensure_preferences_file(self) -> None:
        """Create preferences file if it doesn't exist"""
        if not os.path.exists(self.file_path):
            default_preferences = {
                "default_location": "",
                "favorite_locations": [],
                "units": "metric",  # metric or imperial
                "refresh_interval": 30,  # minutes (1800 seconds)
                "show_alerts": True,
                "map_default_layer": "temp"  # temp, precipitation, wind, clouds
            }
            with open(self.file_path, "w") as f:
                json.dump(default_preferences, f, indent=2)
    
    def get_preferences(self) -> Dict[str, Any]:
        """
        Gets all saved preferences
            
        Returns:
            Dictionary of preferences
        """
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # If there's an error reading the file, return default preferences
            return {
                "default_location": "",
                "favorite_locations": [],
                "units": "metric",
                "refresh_interval": 30,
                "show_alerts": True,
                "map_default_layer": "temp"
            }
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """
        Get a specific preference value
        
        Args:
            key: Preference key
            default: Default value if preference doesn't exist
            
        Returns:
            Preference value or default
        """
        preferences = self.get_preferences()
        return preferences.get(key, default)
    
    def save_preference(self, key: str, value: Any) -> None:
        """
        Save a preference
        
        Args:
            key: Preference key
            value: Preference value
        """
        preferences = self.get_preferences()
        preferences[key] = value
        
        try:
            with open(self.file_path, "w") as f:
                json.dump(preferences, f, indent=2)
        except IOError as e:
            # Log error but don't raise an exception
            print(f"Error saving preference: {str(e)}")
    
    def add_favorite_location(self, location: str) -> None:
        """
        Add a location to favorites
        
        Args:
            location: Location name
        """
        preferences = self.get_preferences()
        favorites = preferences.get("favorite_locations", [])
        
        # Don't add duplicates
        if location not in favorites:
            favorites.append(location)
            preferences["favorite_locations"] = favorites
            
            try:
                with open(self.file_path, "w") as f:
                    json.dump(preferences, f, indent=2)
            except IOError as e:
                print(f"Error saving favorite location: {str(e)}")
    
    def remove_favorite_location(self, location: str) -> None:
        """
        Remove a location from favorites
        
        Args:
            location: Location name
        """
        preferences = self.get_preferences()
        favorites = preferences.get("favorite_locations", [])
        
        if location in favorites:
            favorites.remove(location)
            preferences["favorite_locations"] = favorites
            
            try:
                with open(self.file_path, "w") as f:
                    json.dump(preferences, f, indent=2)
            except IOError as e:
                print(f"Error removing favorite location: {str(e)}")
    
    def get_favorite_locations(self) -> List[str]:
        """
        Gets all favorite locations
        
        Returns:
            List of favorite locations
        """
        preferences = self.get_preferences()
        return preferences.get("favorite_locations", [])
    
    def clear_preferences(self) -> None:
        """will clear all preferences"""
        default_preferences = {
            "default_location": "",
            "favorite_locations": [],
            "units": "metric",
            "refresh_interval": 30,
            "show_alerts": True,
            "map_default_layer": "temp"
        }
        
        try:
            with open(self.file_path, "w") as f:
                json.dump(default_preferences, f, indent=2)
        except IOError as e:
            # Log error but don't raise an exception
            print(f"Error clearing preferences: {str(e)}")
