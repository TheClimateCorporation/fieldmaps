from matplotlib import patches
import fieldmaps as fm
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("ggplot")


# Make data.
polygons = [
    patches.Circle([0, 0], radius=.5),
    patches.Circle([1, 1], radius=.5),
    patches.Circle([0, 2], radius=.5),
    patches.Circle([1, 3], radius=.5),
    patches.Circle([0, 4], radius=.5),
]
coords = np.array([circle.get_verts() for circle in polygons])

bound = .75
measure = np.linspace(0, 1, num=len(polygons))
masked = np.ma.MaskedArray(measure, measure >= bound)

# Make maps.
palette = fm.settings.alternate_palette

fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
fig.subplots_adjust(wspace=.7)
ax1.set_title("Original")
ax2.set_title("Masked")
ax3.set_title("Truncated")

fm.poly_cont(measure, coords, ax=ax1, palette=palette)
fm.poly_cont(masked, coords, ax=ax2, palette=palette)
fm.poly_cont(measure, coords, ax=ax3, palette=palette, upper=bound)

for ax in (ax1, ax2, ax3):
    fm.apply_theme(ax)
    xmin, xmax = ax.get_xbound()
    ax.set_xbound(xmin - .5, xmax + .5)
    ymin, ymax = ax.get_ybound()
    ax.set_ybound(ymin - .5, ymax + .5)

plt.show()
