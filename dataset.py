import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import folium
from tqdm import tqdm



def load_plt_file(file_path):
    df = pd.read_csv(file_path, skiprows=6, header=None)
    df.columns = ['latitude', 'longitude', 'unused', 'altitude', 'date_days', 'date', 'time']
    df['timestamp'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    return df



def load_all_users(data_folder):
    all_data = []
    user_folders = os.listdir(data_folder)
    
    for user in tqdm(user_folders, desc="Loading Users"):
        user_path = os.path.join(data_folder, user, 'Trajectory')
        if not os.path.isdir(user_path):
            continue
        for file in os.listdir(user_path):
            if file.endswith('.plt'):
                file_path = os.path.join(user_path, file)
                df = load_plt_file(file_path)
                df['user'] = user  # Add user info
                all_data.append(df)
    
    if len(all_data) == 0:
        print("No data found!")
        return None
    
    combined_df = pd.concat(all_data, ignore_index=True)
    return combined_df



data_folder = 'add path here to ur dataset folder'
full_df = load_all_users(data_folder)

print("\n=== Data Summary ===")
print(full_df.head())
print(full_df.describe())



plt.figure(figsize=(10, 8))
plt.scatter(full_df['longitude'], full_df['latitude'], s=0.5, alpha=0.5)
plt.title('All Trajectories - Latitude vs Longitude')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)
plt.show()



def plot_folium(df):
    mid_lat = df['latitude'].mean()
    mid_lon = df['longitude'].mean()
    
    fmap = folium.Map(location=[mid_lat, mid_lon], zoom_start=5)
    

    for idx, row in df.head(10000).iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=1,
            color='blue',
            fill=True,
            fill_opacity=0.5
        ).add_to(fmap)
    
    return fmap

fmap = plot_folium(full_df)
fmap.save('all_trajectories_map.html')
print("Map saved to all_trajectories_map.html")

