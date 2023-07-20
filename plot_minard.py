import pandas as pd
import numpy as np

import geopandas as gpd
import contextily as ctx

import matplotlib.pyplot as plt

# Create a DataFrame with columns for each type of data in Minard's visualization
data = pd.DataFrame(
    {
        "city": [
            "Kowno",
            "Wilna",
            "Smorgoni",
            "Molodexno",
            "Gloubokoe",
            "Minsk",
            "Smolensk",
            "Dorogobouge",
            "Wixma",
            "Mojaisk",
            "Moscou",
            "Tarantino",
            "Malo-jarosewii",
        ],
        "longitude": [
            54.91,
            54.68,
            54.78,
            54.51,
            55.20,
            53.90,
            54.78,
            54.85,
            55.03,
            55.59,
            55.75,
            55.73,
            55.82,
        ],
        "latitude": [
            23.90,
            25.32,
            26.48,
            26.85,
            31.00,
            27.56,
            32.04,
            34.90,
            36.49,
            37.36,
            37.62,
            37.52,
            37.65,
        ],
        "direction": [
            "Advance",
            "Advance",
            "Advance",
            "Advance",
            "Advance",
            "Advance",
            "Advance",
            "Advance",
            "Advance",
            "Advance",
            "Advance",
            "Retreat",
            "Retreat",
        ],
        "troops": [
            340000,
            320000,
            300000,
            280000,
            240000,
            200000,
            175000,
            145000,
            140000,
            127100,
            100000,
            98000,
            96000,
        ],
        "date": pd.to_datetime(
            [
                "1812-06-24",
                "1812-07-28",
                "1812-11-28",
                "1812-11-28",
                "1812-11-28",
                "1812-07-28",
                "1812-08-17",
                "1812-08-17",
                "1812-09-03",
                "1812-09-07",
                "1812-09-14",
                "1812-10-18",
                "1812-11-09",
            ]
        ),
        "temperature": [
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            -11,
            -21,
        ],
    }
)

print(data)


# %%
import pandas as pd
import numpy as np

# Define the column names
names = [
    "lonc",
    "latc",
    "city",
    "lont",
    "temp",
    "days",
    "month",
    "day",
    "lonp",
    "latp",
    "surviv",
    "direc",
    "division",
]

# Load the data
data_url = "https://www.cs.uic.edu/~wilkinson/TheGrammarOfGraphics/minard.txt"
data = pd.read_fwf(
    data_url, colspecs="infer", names=names, skiprows=6, skipfooter=3, engine="python"
)

# df_date = data.dropna(subset="month", axis=0).copy()
data["year"] = 1812
d_months = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}
data["month"] = data["month"].map(d_months)
data["date"] = pd.to_datetime(
    data[["year", "month", "day"]],
    errors="raise",
)

data = data.drop(["day", "month", "year"], axis=1)


# Display the first few rows
print(data.info())
print(data.head())

# %%
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx


def plot_troop_movements(df):
    # Create GeoDataFrames for cities and paths
    cities = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lonc, df.latc))
    paths = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lonp, df.latp))

    # Set coordinate reference system (CRS) for projections
    cities = cities.set_crs("EPSG:4326")
    paths = paths.set_crs("EPSG:4326")

    # Project to Web Mercator (EPSG:3857) for use with contextily
    cities = cities.to_crs("EPSG:3857")
    paths = paths.to_crs("EPSG:3857")

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 10))

    # Add the paths and cities to the plot
    paths.plot(ax=ax, color="blue", alpha=0.5)
    cities.plot(ax=ax, color="red")

    # Add basemap
    ctx.add_basemap(ax, source=ctx.providers.Stamen.TonerLite)

    # Set the plot title
    ax.set_title("Napoleon's Russian Campaign of 1812")

    # Show the plot
    plt.show()


# Call the function with your DataFrame
plot_troop_movements(data)
# %%

import matplotlib.pyplot as plt
import numpy as np

# Create a new figure
fig, ax = plt.subplots(figsize=(10, 5))
df = data.copy()
# Loop over the divisions
for division in df["division"].unique():
    # Filter the data for this division
    df_division = df[df["division"] == division]

    # Loop over the directions
    for direc in df_division["direc"].unique():
        # Filter the data for this direction
        df_direc = df_division[df_division["direc"] == direc]

        # Create a line plot for this division and direction
        ax.plot(
            df_direc["lonp"],
            df_direc["latp"],
            linewidth=df_direc["surviv"] / 50000,
            color="red" if direc == "A" else "blue",
        )

# Add labels for the cities
for i, row in df.dropna(subset=["city"]).iterrows():
    ax.text(row["lonc"], row["latc"], row["city"], fontsize=8)

# Set the title and labels
ax.set_title("Napoleon's Russian Campaign of 1812")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# Show the plot
plt.show()
# %%

import seaborn as sns

# Create a new figure
plt.figure(figsize=(10, 5))

# Create a line plot for the advance
sns.lineplot(
    x="lonp",
    y="latp",
    hue="division",
    size="surviv",
    data=df[df["direc"] == "A"],
    sizes=(0.5, 2),
    palette="Reds",
)

# Create a line plot for the retreat
sns.lineplot(
    x="lonp",
    y="latp",
    hue="division",
    size="surviv",
    data=df[df["direc"] == "R"],
    sizes=(0.5, 2),
    palette="Blues",
)

# Add labels for the cities
for i, row in df.dropna(subset=["city"]).iterrows():
    plt.text(row["lonc"], row["latc"], row["city"], fontsize=8)

# Set the title and labels
plt.title("Napoleon's Russian Campaign of 1812")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

# Show the plot
plt.show()
# %%
