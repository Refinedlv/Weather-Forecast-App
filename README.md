# 🌤 Weather Forecast Application

A modern, responsive weather forecast application built with *FastAPI, **Python, and **vanilla HTML/CSS*. Get real-time weather data, compare cities, manage favorites, and enjoy a beautiful user interface without any JavaScript dependencies.

![Weather App Screenshot](https://drive.google.com/file/d/1ab0HSqLHEw0eza443POIklqKdXNupKEO/view?usp=drive_link)
![Weather App Screenshot](https://drive.google.com/file/d/1VI0ht6OMfuvKroM9t2o9_3gk1_ATayUz/view?usp=drive_link)

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Architecture](#-architecture)
- [Design System](#-design-system)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🌍 Core Weather Features
- *Real-time Weather Data*: Current conditions and 5-day forecasts
- *Location Search*: Search by city name with intelligent caching
- *Weather Metrics*: Temperature, humidity, wind speed, pressure, visibility
- *Weather Alerts*: Contextual alerts for severe weather conditions
- *Weather Quotes*: Inspirational quotes based on weather conditions

### 🔄 Comparison & Analysis
- *City Comparison*: Side-by-side weather comparison between two cities
- *Quick Comparisons*: Auto-generated comparisons from favorite locations
- *Popular Comparisons*: Pre-defined comparisons for major cities
- *Multiple Units*: Support for Celsius/Fahrenheit and metric/imperial

### ⭐ User Experience
- *Favorite Locations*: Save and manage favorite cities
- *User Preferences*: Customizable settings and default locations
- *Responsive Design*: Optimized for desktop, tablet, and mobile
- *Accessibility*: WCAG 2.1 compliant with keyboard navigation
- *Dark/Light Themes*: Automatic theme detection and manual toggle

### 🎨 Visual Features
- *Dynamic Styling*: Weather-condition-based card styling
- *CSS Animations*: Pure CSS weather animations (rain, snow, sun)
- *Modern UI*: Clean, modern design with smooth transitions
- *Interactive Elements*: Hover effects and micro-interactions

### ⚡ Performance
- *Smart Caching*: 30-minute cache for weather data
- *Fast Loading*: Optimized CSS and minimal HTTP requests
- *Offline-Ready*: Cached data available when offline
- *Progressive Enhancement*: Works without JavaScript

## 🛠 Technology Stack

### Backend
- *[FastAPI](https://fastapi.tiangolo.com/)* - Modern, fast web framework for Python
- *[Python 3.8+](https://python.org/)* - Programming language
- *[Uvicorn](https://www.uvicorn.org/)* - ASGI server implementation
- *[Requests](https://docs.python-requests.org/)* - HTTP library for API calls
- *[Jinja2](https://jinja.palletsprojects.com/)* - Template engine

### Frontend
- *HTML5* - Semantic markup
- *CSS3* - Modern styling with Grid, Flexbox, and Custom Properties

### External Services
- *[OpenWeatherMap API](https://openweathermap.org/api)* - Weather data provider


## 📁 Project Structure

\\\`
weather-forecast-app/
├── 📁 static/                      # Static assets
│   └── styles.css                  # Main stylesheet (enhanced)
├── 📁 templates/                   # Jinja2 HTML templates
│   ├── index.html                  # Homepage
│   ├── weather.html                # Weather display page
│   ├── comparison.html             # Weather comparison results
│   ├── comparison-form.html        # Comparison form
│   ├── preferences.html            # User preferences
│   ├── error.html                  # Error page
│   └── message.html                # Success/info messages
├── 📁 cache/                       # Weather data cache (auto-created)
├── 📄 main.py                      # FastAPI application entry point
├── 📄 weather_service.py           # Weather API integration
├── 📄 user_preferences.py          # User preferences management
├── 📄 weather_quotes.py            # Weather quotes system
├── 📄 requirements.txt             # Python dependencies
├── 📄 README.md                    # This file
\\\`

### 📁 Detailed File Structure

#### *Core Application Files*
\\\`
main.py                    # FastAPI app, routes, and business logic
├── Dependencies           # Weather service, preferences, quotes
├── Route Handlers         # GET/POST endpoints for all features
├── Template Rendering     # Jinja2 template responses
└── Error Handling         # Custom exception handling

weather_service.py         # Weather data management
├── WeatherService class   # Main service class
├── API Integration        # OpenWeatherMap API calls
├── Data Processing        # Weather data formatting
├── Caching System         # File-based caching
└── Error Handling         # WeatherAPIError exceptions

user_preferences.py        # User preferences system
├── UserPreferenceManager  # Preferences management class
├── JSON Storage           # File-based preference storage
├── Favorite Locations     # Location management
└── Settings Management    # User settings (units, intervals)
\\\`

#### *Frontend Templates*
\\\`
templates/
├── index.html             # Homepage with search and favorites
├── weather.html           # Weather display with forecast
├── comparison.html        # Weather comparison results
├── comparison-form.html   # City comparison form
├── preferences.html       # User settings and favorites
├── error.html             # Error page with friendly messages
└── message.html           # Success/confirmation messages
\\\`

#### *Styling System*
\\\`
static/styles.css          # Complete CSS system
├── CSS Custom Properties  # Design tokens and variables
├── Reset & Base Styles    # Normalize and base styles
├── Layout System          # Grid and flexbox layouts
├── Component Styles       # Cards, buttons, forms
├── Weather Animations     # Pure CSS weather effects
├── Responsive Design      # Mobile-first breakpoints
├── Theme System           # Light/dark mode support
└── Accessibility          # Focus states and a11y features
\\\`

## 🚀 Installation

### Prerequisites
- *Python 3.8+*
- *OpenWeatherMap API Key* (free at [openweathermap.org](https://openweathermap.org/api))

### Step-by-Step Setup

1. *Clone the repository*
   \\\`bash
   git clone https://github.com/Refinedlv/Weather-Forecast-App
   cd weather-forecast-app
   \\\`

2. *Create virtual environment*
   \\\`bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   \\\`

3. *Install dependencies*
   \\\`bash
   pip install -r requirements.txt
   \\\`

4. *Create cache directory*
   \\\`bash
   mkdir cache
   \\\`
   
   # Edit .env file with your API key
   OPENWEATHER_API_KEY=your_api_key_here
   \\\`

6. *Run the application*
   \\\`bash
   python3 main.py
   \\\`

7. *Access the application*
   Open your browser and navigate to http://localhost:4000

### Docker Installation (Optional)

\\\`bash

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| OPENWEATHER_API_KEY | OpenWeatherMap API key | None | ✅ Yes |
| CACHE_EXPIRY | Cache expiry time (seconds) | 1800 | ❌ No |
| HOST | Server host | 0.0.0.0 | ❌ No |
| PORT | Server port | 4000 | ❌ No |

### User Preferences Configuration

The application automatically creates a preferences.json file with the following structure:

\\\`json
{
  "default_location": "",
  "favorite_locations": [],
  "units": "metric",
  "refresh_interval": 30,
  "show_alerts": true,
  "map_default_layer": "temp"
}
\\\`

### Cache Configuration

- *Location*: ./cache/ directory
- *Format*: JSON files named by location and units
- *Expiry*: 30 minutes (configurable)
- *Automatic cleanup*: On application restart

## 📖 Usage

### Basic Weather Search

1. *Enter a city name* in the search box on the homepage
2. *Click "Get Weather"* to fetch current conditions
3. *View detailed information* including:
   - Current temperature and "feels like"
   - Weather description and conditions
   - Humidity, wind speed, and pressure
   - 5-day forecast with daily details

### Weather Comparison

1. *Navigate to "Compare Weather"* in the main menu
2. *Enter two city names* you want to compare
3. *Select temperature units* (Celsius or Fahrenheit)
4. *Click "Compare Weather"* to see side-by-side comparison
5. *Use quick comparisons* from your favorite locations

### Managing Favorites

1. *Add favorites* by checking "Add to favorites" when searching
2. *View favorites* on the homepage for quick access
3. *Remove favorites* from the preferences page
4. *Quick comparisons* are auto-generated from favorites

### Customizing Preferences

1. *Go to Preferences* from any page
2. *Set default location* for homepage pre-fill
3. *Choose temperature units* (Celsius/Fahrenheit)
4. *Configure cache refresh interval*
5. *Enable/disable weather alerts*
6. *Manage favorite locations*

## 🔌 API Endpoints

### Main Routes

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | / | Homepage | None |
| POST | /weather | Get weather data | location, save_preference, add_to_favorites |
| GET | /weather | Get weather (from favorites) | location |
| GET | /comparison | Comparison form | None |
| POST | /compare-weather | Compare cities | location1, location2, units |
| GET | /compare-weather | Compare cities (GET) | location1, location2, units |
| GET | /preferences | Preferences page | saved, error |
| POST | /save-preferences | Save user preferences | Various preference fields |
| POST | /add-favorite | Add favorite location | location |
| POST | /remove-favorite | Remove favorite | location |
| GET | /clear-cache | Clear weather cache | None |

### Response Formats

All endpoints return HTML responses using Jinja2 templates. No JSON APIs are exposed.

### Error Handling

- *Invalid locations*: User-friendly error messages
- *API failures*: Graceful degradation with cached data
- *Network issues*: Informative error pages
- *Rate limiting*: Automatic retry with exponential backoff

## 🏗 Architecture

### Application Architecture

\\\`
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │  External APIs  │
│                 │    │                 │    │                 │
│ HTML Templates  │◄──►│ FastAPI Routes  │◄──►│ OpenWeatherMap  │
│ CSS Styling     │    │                 │    │                 │
│ Form Handling   │    │ Data Processing │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Data Storage   │
                       │                 │
                       │ JSON Files      │
                       │ File Cache      │
                       │ User Prefs      │
                       └─────────────────┘
\\\`

### Service Layer Architecture

```python
# Service Classes
WeatherService          # Weather data management
├── API Integration     # External API calls
├── Data Caching        # Performance optimization
├── Data Formatting     # Response processing
└── Error Handling      # Exception management

UserPreferenceManager   # User data management
├── Preference Storage  # JSON file operations
├── Favorite Locations  # Location management
└── Settings Management # Configuration handling

#
