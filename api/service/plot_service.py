#!/usr/bin/env python3

import json
import numpy as np
import plotly.express as px
import pandas as pd


def load_figs():
    """
        Loads the appropriate data and creates figures.
    """
    recent_df = pd.read_csv("data/listings.csv")
    recent_df = recent_df[
        (recent_df["price"].quantile(0.025) < recent_df["price"]) &
        (recent_df["price"] < recent_df["price"].quantile(0.975))
    ]

    with open("data/neighbourhoods.geojson", "r") as f:
        js = json.load(f)

    lat, lon = [], []
    for n in js["features"]:
        n["id"] = n["properties"]["neighbourhood"]
        for l1 in n["geometry"]["coordinates"]:
            for l2 in l1:
                for l3 in l2:
                    lat.append(l3[1])
                    lon.append(l3[0])
    center_lat = (max(lat) + min(lat)) / 2
    center_lon = (max(lon) + min(lon)) / 2

    listings_by_neighborhood = recent_df.pivot_table(
        index="neighbourhood",
        values=["price",],
        aggfunc="mean",
    ).reset_index()

    map_fig = px.choropleth_mapbox(
        listings_by_neighborhood,
        geojson=js,
        locations="neighbourhood",
        color="price",
        mapbox_style="carto-positron",
        opacity=0.5,
        color_continuous_scale="Viridis",
        center={"lat": center_lat, "lon": center_lon},
        zoom=10,
        #hover_data=["price_str",],
        labels={"price": "Price (€)", "neighbourhood": "Neighborhood"},
        title="Price of AirBnB in Berlin by Neighborhood"
    )

    scatter_df = recent_df.pivot_table(
            index=["neighbourhood_group", "room_type", "price"],
            values=["id"],
            aggfunc=len,
    ).reset_index()
    scatter_df["count"] = scatter_df["id"]

    scatter_fig = px.scatter(
        scatter_df,
        x="neighbourhood_group",
        y="price",
        color="room_type",
        size="count",
        labels={"neighbourhood_group": "Neighborhood", "price": "Price (€)", "room_type": "Room Type", "count": "Number of Listings"},
        title="Price of AirBnB Listings by Neighborhood and Room Type",
        marginal_x="histogram",
    )
    scatter_fig.update_xaxes(tickangle=30, title_text="Neighborhood", tickfont={"size": 14})
    scatter_fig.update_yaxes(range=(0, 150))

    return map_fig, scatter_fig


_map_fig, _scatter_fig = load_figs()


def random_plot():
    """
        Returns a random scatter plot.
    """
    df = pd.DataFrame({
        "x": np.random.randint(0, 100, 100),
        "y": np.random.randint(0, 100, 100),
        "size": np.random.randint(0, 10, 100),
        "color": np.random.randint(0, 4, 100),
    })
    return px.scatter(df, x="x", y="y", size="size", color="color")

def map_plot():
    """
        Returns a choropleth map of price vs neighborhood in Berlin.
    """
    return _map_fig

def scatter_plot():
    """
        Returns a scatter plot of price vs neighborhood and room type
    """
    return _scatter_fig
