import folium
import json
import numpy as np
import polyline
import requests


def _route_wiring(points):

    coords_uri = ";".join(
        f"{point['point']['lng']},{point['point']['lat']}" for point in points)

    response = requests.get(
        f"http://localhost:5000/route/v1/driving/{coords_uri}?overview=simplified",
        timeout=10000
    )

    data = response.json()
    line = data["routes"][0]["geometry"]

    return [(lat, lng) for lat, lng in polyline.decode(line)]


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
    vehicle_color = MAP_COLORS[i % len(MAP_COLORS)]

    # Plot origin
    origin = (vehicle['origin']['lat'], vehicle['origin']['lng'])
    folium.CircleMarker(origin, color="red", radius=3, weight=5).add_to(m)

    # Plot street outlines
    wiring = _route_wiring(vehicle['deliveries'])
    folium.PolyLine(
        wiring, color=vehicle_color, weight=1.0, popup=f"Vehicle {i}"
    ).add_to(m)

    # Plot the deliveries as regular points
    for delivery in vehicle['deliveries']:
        folium.Circle(
            location=(delivery['point']['lat'], delivery['point']['lng']),
            radius=10,
            fill=True,
            color=vehicle_color,
            popup=(
                f"Vehicle {i} ({delivery['point']['lat']}, {delivery['point']['lng']})"
            ),
        ).add_to(m)

m.save("map.html")
