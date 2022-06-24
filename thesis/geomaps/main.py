import osmnx
import geopandas as gpd
import geojson
import folium
import shapely
import warnings
import csv
import colorsys
from shapely.errors import ShapelyDeprecationWarning
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning) 

def getIncomeStyle(income):
  degree = income/max(incomes)
  rgb = colorsys.hsv_to_rgb(245/360, 0.6*degree, 0.9)
  hex = "#" +  "".join("%02X" % round(i*255) for i in rgb)
  return {'fillColor': hex, 'color': hex, 'fillOpacity': 0.8}

# style = {'fillColor': '#f5f5f5', 'color': '#f5d742'}
income_style = {'fillColor': '#ff8800'}

place = 'Copenhagen, Denmark'
districts_geo = gpd.read_file('data/copenhagen_districts.geojson')

districts = ['Osterbro', 'Valby', 'Vesterbro/Kongens Enghave', 'Amager Ost', 
'Bronshoj-Husum', 'Norrebro', 'Indre By', 'Bispebjerg', 'Amager Vest', 'Vanlose'] 

districts_dict = {} 
for d in districts:
  districts_dict[d] = {}

with open('data/copenhagen_districts.geojson') as f:
  gj = geojson.load(f)

for feature in gj['features']:
  name = feature['properties']['name']
  districts_dict[name]['feature'] = feature

incomes = []
with open('data/income_taxable.csv') as f:
  reader = csv.reader(f, delimiter=',')
  for r in reader:
    name = r[2]
    income = r[3]
    districts_dict[name]['taxable_income'] = income
    incomes.append(int(income))

m = folium.Map([55.6867243, 12.5700724], zoom_start=12)
folium.TileLayer('cartodbpositron').add_to(m)

for d in districts_dict.keys():
  district = districts_dict[d]
  print(d)
  f = district['feature']
  i = int(district['taxable_income'])
  print(i)

  folium.GeoJson(f, style_function = lambda x: getIncomeStyle(i)).add_to(m)
#  folium.GeoJson(osterbro_gdf, style_function = lambda x: income_style).add_to(m)
  

ubs = gpd.read_file('data/ubs.geojson')
#folium.GeoJson(ubs).add_to(m)

m.save('map.html')
