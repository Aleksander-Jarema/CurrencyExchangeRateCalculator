import requests
import json
from datetime import datetime, timedelta

def get_exchange_rate(base, target):
    url = f"https://api.frankfurter.app/latest?from={base}&to={target}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("API call failed.")
    data = response.json()
    return data["rates"][target], data["date"]

def get_historical_rates(base, target, days=5):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    url = f"https://api.frankfurter.app/{start_date}..{end_date}?from={base}&to={target}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Historical API call failed.")
    return response.json()["rates"]

def save_to_log(log_data, filename="exchange_log.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(log_data)

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def main():
    print("💱 Currency Exchange Rate Tracker (Frankfurter API)")
    base = input("Enter base currency (e.g., EUR): ").upper()
    target = input("Enter target currency (e.g., USD): ").upper()

    try:
        rate, date = get_exchange_rate(base, target)
        print(f"\n📅 Date: {date}")
        print(f"💸 1 {base} = {rate} {target}")

        log = {
            "timestamp": datetime.now().isoformat(),
            "base": base,
            "target": target,
            "rate": rate,
            "date": date
        }
        save_to_log(log)

        show_history = input("\nShow last 5 days of historical rates? (y/n): ").lower()
        if show_history == "y":
            history = get_historical_rates(base, target)
            print("\n📈 Historical Rates:")
            for date, rate_data in sorted(history.items()):
                print(f"{date}: 1 {base} = {rate_data[target]} {target}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()