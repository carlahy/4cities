import osmnx
import geopandas as gpd
import geojson
import folium
import shapely
import warnings
import csv
import colorsys
from shapely.errors import ShapelyDeprecationWarning
import branca.colormap as cm
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning) 

hues = ['#DEEDCF', '#BFE1B0', '#99D492', '#74C67A', '#56B870', '#39A96B', '#1D9A6C', '#188977', '#137177', '#0E4D64', '#0A2F51']

plain_style = {'color': '#0A2F51', 'fillOpacity': 0}
marker_style = marker = {'fillColor': '#000000'}

def getIncomeStyle(i):
  degree = round(i/max(incomes) * 10)
  c = hues[degree-1]
  return {'fillColor': c, 'color': c, 'fillOpacity': 0.65}

def getEduStyle(e):
  degree = int(e/max(edus) * 10) 
  c = hues[degree-1]
  return {'fillColor': c, 'color': c, 'fillOpacity': 0.65}

districts = ['Osterbro', 'Valby', 'Vesterbro', 'Kongens Enghave', 'Amager Ost', 
'Bronshoj-Husum', 'Norrebro', 'Indre By', 'Bispebjerg', 'Amager Vest', 'Vanlose', 'Christianshavn'] 
districts_dict = {} 
for d in districts:
  districts_dict[d] = {}

with open('data/copenhagen_districts_committees.geojson') as f:
  gj = geojson.load(f)

for feature in gj['features']:
  name = feature['properties']['name']
  if name == 'Fredriksberg': continue
  districts_dict[name]['feature'] = feature

incomes = []
with open('data/income_taxable_committee.csv') as f:
  reader = csv.reader(f, delimiter=',')
  for r in reader:
    name = r[2]
    income = int(r[3])
    districts_dict[name]['taxable_income'] = income
    incomes.append(int(income))

populations = []
with open('data/population.csv') as f:
  reader = csv.reader(f, delimiter=',')
  for r in reader:
    name = r[0]
    p = int(r[1])
    districts_dict[name]['population'] = p
    populations.append(p)

edus = []
with open('data/edu_uni.csv') as f:
  reader = csv.reader(f, delimiter=',')
  for r in reader:
    name = r[1]
    edu = int(r[2]) + int(r[3]) + int(r[4])
    population = districts_dict[name]['population']
    e = edu/population
    districts_dict[name]['edu_uni'] = e
    edus.append(e)

print(max(edus))
print(min(edus))

m = folium.Map([55.6867243, 12.5700724], zoom_start=12)
folium.TileLayer('cartodbpositron').add_to(m)

def getFeatureStyle(feature):
  name = feature['properties']['name']
  i = int(districts_dict[name]['taxable_income'])
  return getIncomeStyle(i)

def getEduStyleFromFeature(feature):
  name = feature['properties']['name']
  e = districts_dict[name]['edu_uni']
  return getEduStyle(e)

for d in districts_dict.keys():
  district = districts_dict[d]
  f = district['feature']
  i = int(district['taxable_income'])

  folium.GeoJson(f, style_function = getFeatureStyle).add_to(m)
  # folium.GeoJson(f, style_function = getEduStyleFromFeature).add_to(m)  
  # folium.GeoJson(f, style_function = lambda x: plain_style).add_to(m)  

ubs = gpd.read_file('data/ubs.geojson')
# folium.GeoJson(ubs,
#                     marker = folium.CircleMarker(radius = 13, # Radius in metres
#                                            weight = 0, #outline weight
#                                            fill_color = '#E74C3C', 
#                                            fill_opacity = 1)
#                     # tooltip = folium.GeoJsonTooltip(fields = ['name'],
#                                                     # aliases=[''],
#                                                     # style = ("background-color: white; color: #E74C3C; font-family: arial; font-size: 12px; padding: 10px;"),
#                                                     # permanent = True,
#                                                     # sticky = True
#                     ).add_to(m)


# colormap = cm.linear.scale(0, 35).to_step(10)

colormap = cm.LinearColormap(['#DEEDCF', '#BFE1B0', '#99D492', '#74C67A', '#56B870', '#39A96B', '#1D9A6C', '#188977', '#137177', '#0E4D64', '#0A2F51'],
                           vmin=3000000, vmax=20000000)
                          #  vmin=15, vmax=35)
colormap.caption = 'taxable income 1000 DKK'
# colormap.caption = '% population with university degrees'
m.add_child(colormap)

m.save('map.html')
