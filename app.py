import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit as st
from fuzzywuzzy import process


shp_path = r"C:\Users\situm\Downloads\local_unit (1)\Local Unit\local_unit.shp"


def get_closest_match(user_input, choices):
    best_match, score = process.extractOne(user_input, choices)
    return best_match if score > 80 else None


def plot_district(district_name, shp_path, bg_color='lightgray', fig_size=(10, 6)):
    # Load shapefile
    gdf = gpd.read_file(shp_path)

    # Get the corrected district name
    corrected_name = get_closest_match(district_name, gdf['DISTRICT'].unique())
    if not corrected_name:
        st.error(f"District '{district_name}' not found in the data. Please check your input.")
        return

    # Filter for the selected district
    district_gdf = gdf[gdf['DISTRICT'] == corrected_name]

    # Compute centroids for labeling
    district_gdf["centroid"] = district_gdf.geometry.centroid

    # Plot the district with municipality borders
    fig, ax = plt.subplots(figsize=fig_size)
    district_gdf.plot(ax=ax, edgecolor='black', facecolor=bg_color)

    # Add municipality labels
    for _, row in district_gdf.iterrows():
        ax.annotate(text=row["GaPa_NaPa"], xy=(row["centroid"].x, row["centroid"].y),
                    ha="center", fontsize=8, color="darkred")

    ax.set_title(f"{corrected_name} District - Municipality Boundaries")
    ax.axis("off")  # Hide axes

    st.pyplot(fig)


# Streamlit app
st.title("Nepal District Map Viewer")

# Load shapefile data
st.write("Loading shapefile data...")
gdf = gpd.read_file(shp_path)

# Get unique district names
districts = sorted(gdf['DISTRICT'].unique())

# User input for district name
district_input = st.text_input("Enter district name:")

# Background color selection
bg_color = st.color_picker("Choose background color:", "#D3D3D3")

# Figure size selection
fig_width = st.slider("Figure width:", 5, 15, 10)
fig_height = st.slider("Figure height:", 5, 15, 6)

# Plot district when input is provided
if district_input:
    plot_district(district_input, shp_path, bg_color, (fig_width, fig_height))

