import folium
import json
import numpy as np
import polyline
import requests


# All available map colors
MAP_COLORS = (
    "black",
    "blue",
    "darkred",
    "purple",
    "red",
    "orange",
    "green",
    "pink",
    "darkblue",
    "beige",
    "gray",
    "lightgreen",
    "lightblue",
    "lightgray",
    "cadetblue",
)

with open("../../../SolucaoJson/cvrp-1-rj-11.json", "r") as data_file:
    json_data = data_file.read()
solution = json.loads(json_data)

origins_mean = np.mean(
    [
        (vehicle['origin']['lat'], vehicle['origin']['lng'])
        for vehicle in solution['vehicles']
    ],
    axis=0,
)
m = folium.Map(
    location=origins_mean,
    zoom_start=12,
    tiles="cartodbpositron",
)

route_indices_to_plot = None
num_vehicles = len(solution['vehicles'])
route_indices_to_plot = route_indices_to_plot or range(num_vehicles)
vehicles_subset = [solution['vehicles'] for i in route_indices_to_plot]

for i, vehicle in enumerate(solution['vehicles']):
    origin = (vehicle['origin']['lat'], vehicle['origin']['lng'])
    folium.CircleMarker(origin, color="red", radius=3, weight=5).add_to(m)
    vehicle_color = MAP_COLORS[i % len(MAP_COLORS)]
    vehicle_coords = [(point['point']['lat'], point['point']['lng']) for point in vehicle['deliveries']]
    folium.Polygon(
        vehicle_coords,
        popup=f"Vehicle {i}",
        color=vehicle_color,
        weight=1,
    ).add_to(m)

m.save("map.html")
