from scraper import fetch_exchange_data
from storage import save_to_csv
from analyzer import (
    load_and_filter_data,
    plot_exchange_rates,
    plot_exchange_ratios,
    plot_percentage_changes,
    plot_interactive_rates,
    summarize_extremes
)
import pandas as pd
from colorama import init, Fore

init(autoreset=True)

def get_date_input(prompt):
    while True:
        date_str = input(prompt).strip()
        if not date_str:
            return None
        try:
            valid_date = pd.to_datetime(date_str)
            return valid_date.strftime("%Y-%m-%d")
        except ValueError:
            print(Fore.RED + "Invalid date format! Please enter the date in 'YYYY-MM-DD' format.")

# Pull the data
data = fetch_exchange_data()

# Save data
if data:
    print(Fore.CYAN + "Exchange Rates:")
    for key, value in data.items():
        print(f"{key}: {value}")
    save_to_csv(data)
    print(Fore.GREEN + "Data saved to CSV.")
else:
    print(Fore.RED + "No data retrieved.")

# Show available date range to user before asking input
df_all = pd.read_csv("data/exchange_rates.csv", parse_dates=["Timestamp"])
print(Fore.YELLOW + f"Available data range: {df_all['Timestamp'].min().date()} to {df_all['Timestamp'].max().date()}")

# Ask the user for the date range with validation
start_date = get_date_input("Enter start date (YYYY-MM-DD) or press Enter to use last 7 days: ")
end_date = get_date_input("Enter end date (YYYY-MM-DD) or press Enter to use today: ")

# Default to last 7 days if no input
today = pd.to_datetime("today").normalize()
if not start_date:
    start_date = (today - pd.Timedelta(days=7)).strftime("%Y-%m-%d")
if not end_date:
    end_date = today.strftime("%Y-%m-%d")

# Load and filter data
df = load_and_filter_data("data/exchange_rates.csv", start_date, end_date)

if df.empty:
    if start_date or end_date:
        print(Fore.RED + f"No data found for the given date range {start_date or 'beginning'} to {end_date or 'end'}.")
    else:
        print("No data found in the dataset.")
else:
    while True:
        print(Fore.MAGENTA + "\nSelect a visualization option:")
        print("1. Plot Exchange Rates")
        print("2. Plot Currency to Gold Ratios")
        print("3. Plot Percentage Changes")
        print("4. Plot Interactive Exchange Rates")
        print("5. Show Date Range Again")
        print("6. Export Filtered Data to CSV")
        print("7. Show Summary (High/Low/Change %)")
        print("0. Exit")

        choice = input("Enter your choice (0-7): ").strip()

        if choice == "1":
            plot_exchange_rates(df)
        elif choice == "2":
            plot_exchange_ratios(df)
        elif choice == "3":
            plot_percentage_changes(df)
        elif choice == "4":
            plot_interactive_rates(df)
        elif choice == "5":
            print(Fore.YELLOW + f"Filtered date range: {df['Timestamp'].min().date()} to {df['Timestamp'].max().date()}")
        elif choice == "6":
            output_path = f"data/filtered_rates_{start_date or 'start'}_to_{end_date or 'end'}.csv"
            df.to_csv(output_path, index=False)
            print(Fore.GREEN + f"Filtered data saved to: {output_path}")
        elif choice == "7":
            summarize_extremes(df)
        elif choice == "0":
            print(Fore.GREEN + "Exiting program.")
            break
        else:
            print(Fore.RED + "Invalid choice. Please select a valid option.")
