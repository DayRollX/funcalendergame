import random

# Define weather types with their properties
WEATHER_TYPES = {
    "Sunny": "☀️",
    "Cloudy": "☁️",
    "Rainy": "🌧️",
    "Snowy": "❄️",
    "Windy": "💨",
    "Foggy": "🌫️",
    "Thunderstorm": "⛈️",
    "Extreme Weather": "🌪️",
}

# Seasonal weather distribution
# Maps season index to a dictionary of weather type -> probability
SEASONAL_WEATHER = {
    "Winter": {  # December, January, February (months 11, 0, 1)
        "Snowy": 0.35,
        "Cloudy": 0.25,
        "Sunny": 0.15,
        "Windy": 0.15,
        "Foggy": 0.05,
        "Rainy": 0.03,
        "Thunderstorm": 0.01,
        "Extreme Weather": 0.01,
    },
    "Spring": {  # March, April, May (months 2, 3, 4)
        "Rainy": 0.30,
        "Cloudy": 0.25,
        "Sunny": 0.20,
        "Windy": 0.15,
        "Foggy": 0.05,
        "Snowy": 0.03,
        "Thunderstorm": 0.01,
        "Extreme Weather": 0.01,
    },
    "Summer": {  # June, July, August (months 5, 6, 7)
        "Sunny": 0.40,
        "Cloudy": 0.20,
        "Rainy": 0.15,
        "Thunderstorm": 0.12,
        "Windy": 0.08,
        "Foggy": 0.03,
        "Snowy": 0.01,
        "Extreme Weather": 0.01,
    },
    "Autumn": {  # September, October, November (months 8, 9, 10)
        "Cloudy": 0.25,
        "Rainy": 0.25,
        "Windy": 0.20,
        "Sunny": 0.15,
        "Foggy": 0.08,
        "Thunderstorm": 0.04,
        "Snowy": 0.02,
        "Extreme Weather": 0.01,
    },
}

def get_season(month_index):
    """Get the season for a given month index (0-11)."""
    if month_index in [11, 0, 1]:  # December, January, February
        return "Winter"
    elif month_index in [2, 3, 4]:  # March, April, May
        return "Spring"
    elif month_index in [5, 6, 7]:  # June, July, August
        return "Summer"
    else:  # September, October, November (8, 9, 10)
        return "Autumn"

def generate_weather_for_year():
    """Generate weather for every day of the year (all 12 months)."""
    from game_state import MONTHS
    
    weather_map = {}
    
    for month_idx, (_, days) in enumerate(MONTHS):
        season = get_season(month_idx)
        weather_chances = SEASONAL_WEATHER[season]
        
        month_weather = {}
        for day in range(1, days + 1):
            # Randomly select weather based on seasonal distribution
            weather_type = random.choices(
                list(weather_chances.keys()),
                weights=list(weather_chances.values()),
                k=1
            )[0]
            month_weather[day] = weather_type
        
        weather_map[month_idx] = month_weather
    
    return weather_map

def get_weather_emoji(weather_type):
    """Get the emoji for a weather type."""
    return WEATHER_TYPES.get(weather_type, "🌍")

def get_weather_description(weather_type):
    """Get a brief description of the weather."""
    descriptions = {
        "Sunny": "It's a beautiful sunny day!",
        "Cloudy": "The sky is overcast with clouds.",
        "Rainy": "It's raining outside.",
        "Snowy": "It's snowing heavily!",
        "Windy": "The wind is blowing strongly.",
        "Foggy": "Everything is shrouded in fog.",
        "Thunderstorm": "A violent thunderstorm is raging!",
        "Extreme Weather": "Extreme weather conditions are occurring!",
    }
    return descriptions.get(weather_type, "The weather is unpredictable.")
