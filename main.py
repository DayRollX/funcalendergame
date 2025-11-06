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
        self.jumps = 5
        self.money = 0
        self.items = set()
        self.month_index = 11  # Start in December

    def has_item(self, item):
        return item in self.items

    def add_item(self, item):
        self.items.add(item)

    def display_status(self):
        print(f"\n🗓  Current Month: {MONTHS[self.month_index][0]}")
        print(f"✨ Jumps: {self.jumps} | 💰 Money: {self.money}")
        print(f"🎒 Items: {', '.join(self.items) if self.items else 'None'}")


def trigger_event(state, day):
    """Select a random event."""
    event_type = random.choice(["story", "store", "bad"])

    print("\n===== EVENT TRIGGERED =====")

    if event_type == "story":
        story_event(state)
    elif event_type == "store":
        store_event(state)
    else:
        bad_event(state, day)


def story_event(state):
    rewards = [
        ("You found a shiny coin!", ("money", 10)),
        ("You discovered an energy drink!", ("jump", 1)),
        ("You met a friendly guide!", ("item", "See Mondays")),
        ("You found a mysterious charm!", ("item", "Odd Bonus")),
    ]
    text, reward = random.choice(rewards)

    print(f"\n📖 STORY EVENT: {text}")

    kind, value = reward

    if kind == "money":
        state.money += value
        print(f"💰 You received +{value} money!")
    elif kind == "jump":
        state.jumps += value
        print(f"✨ You received +{value} jump!")
    elif kind == "item":
        state.add_item(value)
        print(f"🎒 You gained item: {value}")


def store_event(state):
    print("\n🛒 STORE EVENT — You may purchase an item.")

    store_items = {
        "1": ("+1 Jump", 15),
        "2": ("See Mondays", 20),
        "3": ("Odd Bonus", 25),
        "0": ("Exit", 0),
    }

    for key, (name, price) in store_items.items():
        print(f"{key}. {name} — {price} gold")

    choice = input("Choose an item: ")

    if choice in store_items and choice != "0":
        item, cost = store_items[choice]
        if state.money >= cost:
            state.money -= cost
            state.add_item(item)
            print(f"✅ Purchased {item}!")
        else:
            print("❌ Not enough money.")

    print("Leaving store...")


def bad_event(state, day):
    penalties = ["lose_jump", "lose_money", "go_back_month"]

    # Don't allow "go back month" in December
    if state.month_index == 11:
        penalties.remove("go_back_month")

    penalty = random.choice(penalties)

    print("\n⚠️ BAD EVENT!")

    if penalty == "lose_jump":
        print("You slipped and fell. Lost 1 jump.")
        state.jumps -= 1

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

        # Lose condition
        if state.jumps <= 0:
            print("\n💀 You have no jumps left... Game Over.")
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

        # Jump used
        state.jumps -= 1

        # Odd-day bonus
        if day % 2 == 1 and state.has_item("Odd Bonus"):
            print("🎁 Bonus! Odd day bonus: +10 money!")
            state.money += 10

        trigger_event(state, day)

        # Move backward a month
        state.month_index -= 1


if __name__ == "__main__":
    play_game()
