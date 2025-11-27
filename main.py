from game_state import GameState
from events import trigger_event, story_event, store_event, bad_event
from weather import get_season, get_weather_emoji

import random

# Months with days
MONTHS = [
    ("January", 31),
    ("February", 28),
    ("March", 31),
    ("April", 30),
    ("May", 31),
    ("June", 30),
    ("July", 31),
    ("August", 31),
    ("September", 30),
    ("October", 31),
    ("November", 30),
    ("December", 31),
]


def play_game():
    state = GameState()

    while True:
        state.display_status()

        # Win condition
        if state.month_index < 0:
            print("\n🎉🎉 YOU WIN! You made it through the year! 🎉🎉")
            return

        month_name, days = MONTHS[state.month_index]
        season = get_season(state.month_index)
        print(f"\nPick a date in {month_name} (1–{days}) — 🌍 Season: {season}")

        # Item effect: reveal Mondays
        if state.has_item("See Mondays"):
            print("📅 You can see which days are Mondays (not actual events):")
            mondays = [d for d in range(1, days + 1) if d % 7 == 1]
            print("Mondays:", mondays)

        # Input validation
        try:
            day = int(input("> "))
            if day < 1 or day > days:
                print("❌ Invalid day.")
                continue
        except:
            print("❌ Invalid input.")
            continue

        # Odd-day bonus (now point-based)
        if day % 2 == 1 and state.has_item("Odd Bonus"):
            print("🎁 Bonus! Odd day bonus: +10 points!")
            state.points += 10

        trigger_event(state, day)

        # Move backward a month
        state.month_index -= 1


if __name__ == "__main__":
    play_game()
