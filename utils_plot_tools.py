# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 11:00:00 2023

@author: jhutchison

"""

# %% Packages
""" Third party and local imports """

import matplotlib.pyplot as plt
import pathlib

from mpl_toolkits.mplot3d import axes3d


# %% Functions
""" Define functions """


def plot_countour_profiles():
    """Project count profiles onto a graph"""
    # https://matplotlib.org/stable/gallery/mplot3d/contour3d_3.html

    ax = plt.figure().add_subplot(projection="3d")
    X, Y, Z = axes3d.get_test_data(0.05)

    # Plot the 3D surface
    ax.plot_surface(
        X, Y, Z, edgecolor="royalblue", lw=0.5, rstride=8, cstride=8, alpha=0.3
    )

    # Plot projections of the contours for each dimension.  By choosing offsets
    # that match the appropriate axes limits, the projected contours will sit on
    # the 'walls' of the graph.
    ax.contour(X, Y, Z, zdir="z", offset=-100, cmap="coolwarm")
    ax.contour(X, Y, Z, zdir="x", offset=-40, cmap="coolwarm")
    ax.contour(X, Y, Z, zdir="y", offset=40, cmap="coolwarm")

    ax.set(
        xlim=(-40, 40),
        ylim=(-40, 40),
        zlim=(-100, 100),
        xlabel="X",
        ylabel="Y",
        zlabel="Z",
    )

    plt.show()


def rotate_plot():
    """Rotating a 3D plot"""
    # https://matplotlib.org/stable/gallery/mplot3d/rotate_axes3d_sgskip.html

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    # Grab some example data and plot a basic wireframe.
    X, Y, Z = axes3d.get_test_data(0.05)
    ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)

    # Set the axis labels
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    # Rotate the axes and update
    for angle in range(0, 360 * 4 + 1):
        # Normalize the angle to the range [-180, 180] for display
        angle_norm = (angle + 180) % 360 - 180

        # Cycle through a full rotation of elevation, then azimuth, roll, and all
        elev = azim = roll = 0
        if angle <= 360:
            elev = angle_norm
        elif angle <= 360 * 2:
            azim = angle_norm
        elif angle <= 360 * 3:
            roll = angle_norm
        else:
            elev = azim = roll = angle_norm

        # Update the axis view and title
        ax.view_init(elev, azim, roll)
        plt.title("Elevation: %d°, Azimuth: %d°, Roll: %d°" % (elev, azim, roll))

        plt.draw()
        plt.pause(0.001)


# %% Variables
""" Set script (global) variables """

path_data = pathlib.Path("data/")


# %% Main
""" Display task data """

if __name__ == "__main__":
    print("plot contour profiles")
    plot_countour_profiles()

    print("rotate plot")
    # rotate_plot()

    print("main complete")


# %% Notes
""" Final thoughts """
