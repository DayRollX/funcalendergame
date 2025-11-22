
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

class GameState:
    def __init__(self):
        self.points = 0
        self.money = 0
        self.items = set()
        self.month_index = 11  # Start in December
        # Pre-generate events for every month/day at game start
        self.events = self.generate_events()

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


def trigger_event(state, day):
    """Deliver the pre-generated event for the current month/day."""
    print("\n===== EVENT TRIGGERED =====")

    month_idx = state.month_index
    try:
        event_type, payload = state.events[month_idx][day]
    except (IndexError, KeyError):
        print("Nothing happens today.")
        return

    if event_type == "story":
        # payload == (text, reward)
        story_event(state, payload)
    elif event_type == "store":
        store_event(state)
    else:  # "bad"
        bad_event(state, payload)


def story_event(state, payload):
    # payload: (text, reward)
    text, reward = payload
    print(f"\n📖 STORY EVENT: {text}")

    kind, value = reward

    if kind == "money":
        state.money += value
        print(f"💰 You received +{value} money!")
    elif kind == "points":
        state.points += value
        print(f"⭐ You received +{value} points!")
    elif kind == "item":
        state.add_item(value)
        print(f"🎒 You gained item: {value}")


def store_event(state):
    print("\n🛒 STORE EVENT — You may purchase an item.")

    store_items = {
        "1": ("+10 Points", 15),
        "2": ("See Mondays", 20),
        "3": ("Odd Bonus", 25),
        "0": ("Exit", 0),
    }

    for key, (name, price) in store_items.items():
        print(f"{key}. {name} — {price} gold")

    choice = input("Choose an item: ")

    if choice in store_items and choice != "0":
        item_name, cost = store_items[choice]
        if state.money >= cost:
            state.money -= cost
            # Immediate point purchases vs persistent items
            if item_name == "+10 Points":
                state.points += 10
                print(f"✅ Purchased {item_name}! +10 points granted.")
            else:
                state.add_item(item_name)
                print(f"✅ Purchased {item_name}!")
        else:
            print("❌ Not enough money.")

    print("Leaving store...")


def bad_event(state, penalty):
    # penalty is one of: "lose_points", "lose_money", "go_back_month"
    print("\n⚠️ BAD EVENT!")

    if penalty == "lose_points":
        loss = random.randint(5, 15)
        loss = min(loss, state.points)
        print(f"An unfortunate mishap! You lost {loss} points.")
        state.points -= loss

    elif penalty == "lose_money":
        loss = random.randint(5, 15)
        loss = min(loss, state.money)
        print(f"You dropped your wallet and lost {loss} money.")
        state.money -= loss

    elif penalty == "go_back_month":
        print("A time portal! You got sent back a month!")
        state.month_index += 1  # Move forward, since game moves backward
        if state.month_index > 11:
            state.month_index = 11


def play_game():
    state = GameState()

    while True:
        state.display_status()

        # Win condition
        if state.month_index < 0:
            print("\n🎉🎉 YOU WIN! You made it through the year! 🎉🎉")
            return

        month_name, days = MONTHS[state.month_index]
        print(f"\nPick a date in {month_name} (1–{days}):")

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
