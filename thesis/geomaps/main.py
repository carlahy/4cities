import osmnx
import geopandas as gpd
import geojson
import folium
import shapely
import warnings
from shapely.errors import ShapelyDeprecationWarning
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning) 

style = {'fillColor': '#f5f5f5'}
income_style = {'fillColor': '#ff8800'}

place = 'Copenhagen, Denmark'
districts = gpd.read_file('copenhagen_districts.geojson')

districts_dict = {}
with open('copenhagen_districts.geojson') as f:
  gj = geojson.load(f)

for feature in gj['features']:
  name = feature['properties']['name']
  districts_dict[name] = feature

print(districts_dict.keys())

osterbro_gdf = districts_dict['Osterbro']

ubs = gpd.read_file('ubs.geojson')

m = folium.Map([55.6867243, 12.5700724], zoom_start=10)
folium.TileLayer('cartodbpositron').add_to(m)
folium.GeoJson(osterbro_gdf, style_function = lambda x: 
income_style).add_to(m)

folium.GeoJson(districts, style_function = lambda x: style).add_to(m)
#folium.GeoJson(ubs).add_to(m)

m.save('map.html')
