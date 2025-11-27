import random
from weather import generate_weather_for_year

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

class GameState:
    def __init__(self):
        self.points = 0
        self.money = 0
        self.items = set()
        self.month_index = 11  # Start in December
        # Pre-generate events for every month/day at game start
        self.events = self.generate_events()
        # Pre-generate weather for every month/day at game start
        self.weather = generate_weather_for_year()

    def has_item(self, item):
        return item in self.items

    def add_item(self, item):
        self.items.add(item)

    def display_status(self):
        print(f"\n🗓  Current Month: {MONTHS[self.month_index][0]}")
        print(f"⭐ Points: {self.points} | 💰 Money: {self.money}")
        print(f"🎒 Items: {', '.join(self.items) if self.items else 'None'}")

    def generate_events(self):
        """Generate a map of events for every month and day."""
        rewards = [
            ("You found a shiny coin!", ("money", 10)),
            ("You discovered a point token!", ("points", 5)),
            ("You met a friendly guide!", ("item", "See Mondays")),
            ("You found a mysterious charm!", ("item", "Odd Bonus")),
        ]

        all_events = []
        for m_idx, (_, days) in enumerate(MONTHS):
            month_events = {}
            for day in range(1, days + 1):
                event_type = random.choice(["story", "store", "bad"])

                if event_type == "story":
                    text, reward = random.choice(rewards)
                    month_events[day] = ("story", (text, reward))

                elif event_type == "store":
                    month_events[day] = ("store", None)

                else:  # bad
                    penalties = ["lose_points", "lose_money", "go_back_month"]
                    # Don't allow "go_back_month" in December
                    if m_idx == 11 and "go_back_month" in penalties:
                        penalties.remove("go_back_month")
                    penalty = random.choice(penalties)
                    month_events[day] = ("bad", penalty)

            all_events.append(month_events)
        return all_events