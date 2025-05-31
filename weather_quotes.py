import random
from typing import Dict, List

class WeatherQuotes:
    """Manages weather-related quotes based on weather conditions"""
    
    def __init__(self):
        self.quotes = {
            'clear': [
                "Sunshine is the best medicine.",
                "A sunny day is a happy day.",
                "Keep your face always toward the sunshine, and shadows will fall behind you.",
                "Wherever you go, no matter what the weather, always bring your own sunshine."
            ],
            'clouds': [
                "Clouds come floating into my life, no longer to carry rain or usher storm, but to add color to my sunset sky.",
                "Even the darkest clouds will eventually part to reveal the sun.",
                "Behind every cloud is another cloud.",
                "The clouds are the sky's imagination."
            ],
            'rain': [
                "Let the rain kiss you. Let the rain beat upon your head with silver liquid drops.",
                "Some people feel the rain. Others just get wet.",
                "The best thing one can do when it's raining is to let it rain.",
                "Rain is grace; rain is the sky descending to the earth."
            ],
            'snow': [
                "Snowflakes are one of nature's most fragile things, but just look what they can do when they stick together.",
                "When snow falls, nature listens.",
                "A snowball in the face is surely the perfect beginning to a lasting friendship.",
                "The first fall of snow is not only an event, it is a magical event."
            ],
            'thunderstorm': [
                "The sound of thunder reminds us of the power of nature.",
                "Thunderstorms are as much our friends as the sunshine.",
                "Life isn't about waiting for the storm to pass, it's about learning to dance in the rain.",
                "The storm starts when the drops start dropping. When the drops stop dropping then the storm starts stopping."
            ],
            'mist': [
                "In the mist, all of life becomes magical and mysterious.",
                "Mist makes everything more beautiful, more mysterious.",
                "The mist was so thick that the trees were completely hidden.",
                "The mist comes and goes, but the mountains remain."
            ],
            'default': [
                "Wherever you go, no matter what the weather, always bring your own sunshine.",
                "Climate is what we expect, weather is what we get.",
                "There's no such thing as bad weather, only inappropriate clothing.",
                "Weather forecast for tonight: dark."
            ]
        }
    
    def get_random_quote(self, weather_type: str) -> str:
        """
        Get a random quote based on weather type
        
        Args:
            weather_type: Weather description (e.g., "clear sky", "light rain")
            
        Returns:
            A random weather-related quote
        """
        # Convert to lowercase and simplify
        weather_type = weather_type.lower()
        
        # Find the appropriate category
        category = 'default'
        if 'clear' in weather_type or 'sun' in weather_type:
            category = 'clear'
        elif 'cloud' in weather_type:
            category = 'clouds'
        elif 'rain' in weather_type or 'drizzle' in weather_type:
            category = 'rain'
        elif 'snow' in weather_type:
            category = 'snow'
        elif 'thunder' in weather_type or 'storm' in weather_type:
            category = 'thunderstorm'
        elif 'mist' in weather_type or 'fog' in weather_type:
            category = 'mist'
        
        # Get quotes for the category
        quotes = self.quotes[category]
        
        # and then return a random quote (based on the weather)
        return random.choice(quotes)
    
    def get_all_quotes(self) -> Dict[str, List[str]]:
        """to get all quotes organized by category"""
        return self.quotes.copy()
    
    def add_quote(self, category: str, quote: str) -> None:
        """
        this is to add a new quote to a category
        
        Args:
            category: Weather category
            quote: Quote to add
        """
        if category not in self.quotes:
            self.quotes[category] = []
        self.quotes[category].append(quote)
