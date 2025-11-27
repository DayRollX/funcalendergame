import random
from weather import get_weather_emoji, get_weather_description

def trigger_event(state, day):
    """Deliver the pre-generated event for the current month/day."""
    print("\n===== EVENT TRIGGERED =====")

    month_idx = state.month_index
    
    # Display weather for the day
    try:
        weather = state.weather[month_idx][day]
        emoji = get_weather_emoji(weather)
        description = get_weather_description(weather)
        print(f"{emoji} Weather: {description}")
        
        # Apply weather-based item effects
        if weather == "Rainy" and state.has_item("Umbrella"):
            state.money += 10
            print(f"☔ Umbrella triggered! You gained 10 coins!")
        
        if weather == "Sunny" and state.has_item("Sunny Orb"):
            state.points += 5
            print(f"☀️ Sunny Orb triggered! You gained 5 points!")
    except (IndexError, KeyError):
        pass
    
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
        "4": ("Umbrella", 30),
        "5": ("Sunny Orb", 35),
        "6": ("Rain Stick", 40),
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
                if item_name == "Umbrella":
                    print(f"✅ Purchased {item_name}! Get 10 coins on rainy days.")
                elif item_name == "Sunny Orb":
                    print(f"✅ Purchased {item_name}! Get 5 points on sunny days.")
                elif item_name == "Rain Stick":
                    print(f"✅ Purchased {item_name}! Shows all rainy days in the month.")
                else:
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