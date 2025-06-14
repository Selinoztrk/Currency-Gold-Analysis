import csv
from datetime import datetime
import os
import pandas as pd

def save_to_csv(data, filename="data/exchange_rates.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Add data with DataFrame
    df = pd.DataFrame([data])
    df["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df.to_csv(filename, mode='a', header=not os.path.exists(filename), index=False)
