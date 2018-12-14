import fieldmaps as fm
import matplotlib.pyplot as plt
import numpy as np
import requests

plt.style.use("ggplot")


# Fetch data.
src_url = (
    "https://raw.githubusercontent.com/HackFargo/Shapefiles-Archive/master/"
    "Water-Utilities/WaterHydrants.geojson"
)
hydrants = requests.get(src_url).json()
features = [
    feature
    for feature in hydrants["features"]
    if feature["geometry"]["type"] == "Point"
]

# Extract measurements.
status = [f["properties"]["Status"] for f in features]
elevation = np.array([
    f["properties"]["Elevation"] for f in features
], dtype=np.float)

xy = [feature["geometry"]["coordinates"] for feature in features]
coords = np.asarray(xy)

# Make maps.
fig, (ax1, ax2) = plt.subplots(1, 2)
fig.subplots_adjust(wspace=.5)
ax1.set_title("Elevation")
ax2.set_title("Status")

fm.point_cont(elevation, coords, ax=ax1, palette="Blues", upper=1000)
fm.point_discrete(status, coords, ax=ax2)
fm.apply_theme(ax1, ax2)

plt.show()
