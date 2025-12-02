"""Weather effects mapping and helper to apply them.

Edit the `WEATHER_EFFECTS` dict to add or tweak effects.

Each weather key maps to a dict that can contain:
 - 'points': int  -> points to add (can be negative)
 - 'money': int   -> coins to add (can be negative)
 - 'message': str -> optional message printed when applied
 - 'func': callable(state) -> optional custom function to run instead

The `apply_weather_effect` helper applies numeric changes and prints a message.

Example: Sunny gives +5 points and +5 coins by default.
"""

from typing import Dict, Any, Optional

# Easy-to-update mapping. Add new weather types or change values here.
WEATHER_EFFECTS: Dict[str, Dict[str, Any]] = {
    "Sunny": {
        "points": 5,
        "money": 5,
        "message": "☀️ It's a sunny day! You feel energized (+5 points, +5 coins).",
    },
    # Example placeholders for other weather types; tweak as desired.
    "Rainy": {
        "points": 0,
        "money": 0,
        "message": "☔ Rainy day — nothing special happens by default.",
    },
    "Cloudy": {
        "points": 0,
        "money": 0,
        "message": "☁️ Cloudy day — calm and steady.",
    },
    "Snowy": {
        "points": 2,
        "money": 0,
        "message": "❄️ Snowy day — chilly but inspiring (+2 points).",
    },
}


def apply_weather_effect(state, weather: str) -> Optional[Dict[str, int]]:
    """Apply the configured effect for `weather` to the `state`.

    Returns a dict with the applied numeric changes (keys: 'points', 'money'),
    or None if there was no configured effect.
    """
    if not weather:
        return None

    effect = WEATHER_EFFECTS.get(weather)
    if not effect:
        return None

    # If a custom function is provided, call it for complex behavior.
    func = effect.get("func")
    if callable(func):
        try:
            func(state)
        except Exception:
            # Do not let a custom effect crash the game; fail silently.
            pass
        return None

    points = int(effect.get("points", 0))
    money = int(effect.get("money", 0))

    if points:
        state.points += points
    if money:
        state.money += money

    # Prefer a custom message if present
    message = effect.get("message")
    if message:
        print(message)
    else:
        parts = []
        if points:
            parts.append(f"+{points} points")
        if money:
            parts.append(f"+{money} coins")
        if parts:
            print("Weather effect:", ", ".join(parts))

    return {"points": points, "money": money}


def register_custom(weather: str, func) -> None:
    """Register a custom callable for a specific weather type.

    The callable will receive the `state` and may perform arbitrary changes.
    Example usage:
        def windy_boost(state):
            state.points += 3
        register_custom('Windy', windy_boost)
    """
    WEATHER_EFFECTS.setdefault(weather, {})["func"] = func
