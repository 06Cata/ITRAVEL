import folium
from folium import IFrame

def get_map(list_of_dfs):
    taiwan_center = [23.69781, 120.960515]  # Latitude and Longitude of Taiwan center
    m = folium.Map(location=taiwan_center, zoom_start=8)

    colors = ['red', 'orange', 'green', 'blue', 'darkblue', 'purple', 'black', 'darkred', 'pink', 'lightblue', 'lightgreen', 'gray', 'black']
    
    for i, df in enumerate(list_of_dfs):
        for idx, row in df.iterrows():
            name = row['name'] if pd.notna(row['name']) else "No Name"
            address = row['address'] if pd.notna(row['address']) else "No Address"
            popup_content = f"Name: {name}<br>Address: {address}"
            iframe = IFrame(html=popup_content, width=200, height=80)
            popup = folium.Popup(iframe, max_width=2650)
            folium.Marker(
                location=[row['lat'], row['lng']],
                popup=popup,
                icon=folium.Icon(color=colors[i % len(colors)])
            ).add_to(m)

    # Fit the map to the bounds of Taiwan
    m.fit_bounds([[21.87, 119.32], [25.36, 122.04]])

    return m


import folium
import pandas as pd
from sklearn.cluster import KMeans
from geopy.distance import geodesic
import warnings
warnings.filterwarnings('ignore')

def cluster_and_centers(dfs, n_clusters, distance_threshold):
    # dfs: list of dataframes
    # n_clusters: 分幾群
    # distance_threshold: 要刪除的centerpoints周圍範圍
    
    all_data = pd.concat(list(dfs), ignore_index=True)

    # Convert DataFrame to a list of tuples with coordinates
    coords = list(zip(all_data['lat'], all_data['lng']))

    # Perform K-means clustering with the specified number of clusters
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(coords)

    # Get the center points of the clusters
    center_points = kmeans.cluster_centers_

    # Create a folium map centered at the first filtered center point
    m = folium.Map(location=[center_points[0][0], center_points[0][1]], zoom_start=14)

    color_palette = ['red', 'orange', 'green', 'blue', 'purple', ]
    color_idx = 0

    for df in dfs:
        # Add the points to the map
        for _, row in df.iterrows():
            color = color_palette[color_idx % len(color_palette)]
            folium.Marker([row['lat'], row['lng']], tooltip=row['name'], icon=folium.Icon(color=color)).add_to(m)

        color_idx += 1

    # Add the filtered center points and their circles to the map
    for center in center_points:
        folium.Marker([center[0], center[1]], icon=folium.Icon(color='gray')).add_to(m)
        folium.Circle(location=[center[0], center[1]], radius=distance_threshold, color='gray', fill=True, fill_color='gray', fill_opacity=0.2).add_to(m)

    return m, center_points

