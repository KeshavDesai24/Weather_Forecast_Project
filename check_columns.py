import os
import pandas as pd

DATA_DIR = "./training/cleaned"

for filename in os.listdir(DATA_DIR):
    if filename.endswith(".csv"):
        path = os.path.join(DATA_DIR, filename)
        df = pd.read_csv(path)
        print(f"\n📁 {filename}")
        print("🔍 Columns:", list(df.columns))
