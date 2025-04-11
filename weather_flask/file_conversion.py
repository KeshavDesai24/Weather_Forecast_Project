import xarray as xr
import os

ds_max_temp = xr.open_dataset("weather-nc\_2018\max_temperature.nc")
ds_mean_temp = xr.open_dataset("weather-nc\_2018\mean_temperature.nc")
ds_max_preci = xr.open_dataset("weather-nc\_2018\max_precipitation.nc")
ds_mean_preci = xr.open_dataset("weather-nc\_2018\mean_precipitation.nc")
ds_mslp = xr.open_dataset("weather-nc\_2018\mslp.nc")

# Convert to Pandas DataFrame
df_max_temp = ds_max_temp.to_dataframe().reset_index()
df_mean_temp = ds_mean_temp.to_dataframe().reset_index()
df_max_preci = ds_max_preci.to_dataframe().reset_index()
df_mean_preci = ds_mean_preci.to_dataframe().reset_index()
df_mslp = ds_mslp.to_dataframe().reset_index()

# Save as CSV
if os.path.exists("notebook\data\_2018\_attributes\max_temperature.csv"):
    print("Max Tempreture File already exists")
else:
    df_max_temp.to_csv("notebook\data\_2018\_attributes\max_temperature.csv", index= False)
    print("Max Tempreture File created")

if os.path.exists("notebook\data\_2018\_attributes\mean_temperature.csv"):
    print("Mean Tempreture File already exists")
else:
    df_mean_temp.to_csv("notebook\data\_2018\_attributes\mean_temperature.csv", index= False)
    print("Mean Tempreture File created")

if os.path.exists("notebook\data\_2018\_attributes\max_precipitation.csv"):
    print("Max Precipitation File already exists")
else:
    df_max_preci.to_csv("notebook\data\_2018\_attributes\max_precipitation.csv", index=False)
    print("Max Precipitation File created")

if os.path.exists("notebook\data\_2018\_attributes\mean_precipitation.csv"):
    print("Mean Precipitation File already exists")
else:
    df_mean_preci.to_csv("notebook\data\_2018\_attributes\mean_precipitation.csv", index=False)
    print("Mean Precipitation File created")

if os.path.exists("notebook\data\_2018\_attributes\mslp.csv"):
    print("Mslp File already exists")
else:   
    df_mslp.to_csv("notebook\data\_2018\_attributes\mslp.csv", index=False)
    print("Mslp File created")

