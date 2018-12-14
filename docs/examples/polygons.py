import fieldmaps as fm
import matplotlib.pyplot as plt
import numpy as np
import requests

plt.style.use("ggplot")


# Fetch data.
src_url = (
    "https://raw.githubusercontent.com/HackFargo/Shapefiles-Archive/master/"
    "Footprints-Parcels/FargoParcels.geojson"
)
parcels = requests.get(src_url).json()
features = [
    feature
    for feature in parcels["features"]
    if feature["geometry"]["type"] == "Polygon"
]

# Extract measurements.
acres = [feature["properties"]["ACRES"] for feature in features]
school_districts = [feature["properties"]["SchoolDist"] for feature in features]

exteriors = [feature["geometry"]["coordinates"][0] for feature in features]
coords = np.array(exteriors)

# Make maps.
fig, (ax1, ax2) = plt.subplots(1, 2)
fig.subplots_adjust(wspace=.5)
ax1.set_title("Acres")
ax2.set_title("School District")

fm.poly_cont(acres, coords, ax=ax1, palette="Reds")
fm.poly_discrete(school_districts, coords, ax=ax2)
fm.apply_theme(ax1, ax2)

plt.show()
