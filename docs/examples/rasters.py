import fieldmaps as fm
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("ggplot")


# Make measurements.
rs = np.random.RandomState(seed=13)
raster = rs.normal(size=(20, 20))
labels = np.zeros(raster.shape, dtype=np.dtype("<U8"))
labels[raster < 0] = "Negative"
labels[raster > 0] = "Positive"
labels[raster == 0] = "Zero"

# Make maps.
fig, (ax1, ax2) = plt.subplots(1, 2)
fig.subplots_adjust(wspace=.5)
ax1.set_title("Continuous")
ax2.set_title("Categorical")

fm.raster_cont(raster, ax=ax1)
fm.raster_discrete(labels, ax=ax2)
fm.apply_theme(ax1, ax2)

plt.show()
