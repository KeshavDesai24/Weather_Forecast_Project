import os
import pandas as pd

folder_path = r'Weather_Forecast_Project(DMBI)\datafiles'  

# Loop through all Excel files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv') or file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        try:
            # Read the first sheet of the Excel file
            df = pd.read_excel(file_path)
            print(f"\n📄 Columns in {file_name}:")
            print(list(df.columns))
        except Exception as e:
            print(f"\n⚠️ Could not read {file_name}: {e}")
