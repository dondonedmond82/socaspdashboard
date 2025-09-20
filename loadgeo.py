import pandas as pd
from geopy.geocoders import Nominatim
import geopandas as gpd
import hvplot.pandas

# Example cities
df = pd.DataFrame({'city': ['Bangui', 'Paris', 'Nairobi']})

# Geocoder
geolocator = Nominatim(user_agent="city_locator")

# Get coordinates for each city
df[['lat', 'lon']] = df['city'].apply(
    lambda city: pd.Series(
        (lambda loc: (loc.latitude, loc.longitude))(
            geolocator.geocode(city)
        )
    )
)

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df.lon, df.lat),
    crs="EPSG:4326"
)

# Plot
gdf.hvplot.points(
    x='lon', y='lat',
    geo=True,
    tiles='CartoLight',
    color='blue',
    hover_cols=['city']
)


import geopandas as gpd
import hvplot.pandas

# Load shapefile with city polygons/points
cities = gpd.read_file("cities.geojson")

# Filter for one city
city_gdf = cities[cities['NAME'] == 'Bangui']

# Plot
city_gdf.hvplot(geo=True, tiles='CartoLight')
    