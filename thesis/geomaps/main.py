import osmnx
import geopandas as gpd
import folium
import shapely
import warnings
from shapely.errors import ShapelyDeprecationWarning
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning) 

style = {'fillColor': '#f5f5f5'}

place = 'Copenhagen, Denmark'
districts = gpd.read_file('copenhagen_districts.geojson')


m = folium.Map([55.6867243, 12.5700724], zoom_start=10)
folium.TileLayer('cartodbpositron').add_to(m)


folium.GeoJson(districts, style_function = lambda x: style).add_to(m)

m.save('map.html')
