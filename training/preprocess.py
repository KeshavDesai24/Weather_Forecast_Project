import pandas as pd
import os

input_folder = '../datafiles'
output_folder = '../datafiles/cleaned'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        path = os.path.join(input_folder, filename)

        # Avoid DtypeWarning
        df = pd.read_csv(path, low_memory=False)

        if {'YEAR', 'MN', 'DT'}.issubset(df.columns):
            df['MN'] = df['MN'].apply(lambda x: f"{int(x):02d}" if pd.notnull(x) else '01')
            df['DT'] = df['DT'].apply(lambda x: f"{int(x):02d}" if pd.notnull(x) else '01')

            # Use explicit format to avoid date warnings
            df['date'] = pd.to_datetime(df['YEAR'].astype(str) + '-' + df['MN'] + '-' + df['DT'],
                                        format='%Y-%m-%d', errors='coerce')

            temp_col = None
            possible_temp_cols = ['AA', 'T', 'T.1', 'MAX', 'MIN', 'TEMP', 'Temp', 'Temperature',
                'DBT', 'TC', 'WBT', 'DPT'  # Newly added based on your data
            ]


            for col in possible_temp_cols:
                if col in df.columns:
                    temp_col = col
                    break

            if temp_col:
                df = df[['date', temp_col]]
                df = df.rename(columns={temp_col: 'temperature'})
                df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
                df = df.sort_values('date')
                df['temperature'] = df['temperature'].interpolate(method='linear')

                output_path = os.path.join(output_folder, f'cleaned_{filename}')
                df.to_csv(output_path, index=False)
                print(f"✅ Saved: cleaned_{filename}")
            else:
                print(f"⚠️ No valid temperature column in {filename}")
                print(f"    → Columns found: {df.columns.tolist()}")
        else:
            print(f"⚠️ Missing YEAR/MN/DT columns in {filename}")
