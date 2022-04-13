import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math 

districts_map = {
  'København': 0,
  'Frederiksberg': 1, 
  'Hvidovre': 2, 
  'Tårnby': 3, 
  'Brøndby': 4, 
  'Rødovre': 5, 
  'Herlev': 6, 
  'Gladsaxe': 7, 
  'Gentofte': 8
}

lakes = [0] * 9
streams = [0] * 9

data = pd.read_csv('vand_oversigtskort.csv')
districts = list(dict.fromkeys(data['kommune']))
for i,r in data.iterrows():
  type = r['objekt_type']
  kommune = r['kommune']
  k = districts_map[kommune]
  if type == 'Hav':
    lakes[k] = lakes[k]+1
  elif type == 'Sø':
    streams[k] = streams[k]+1
  else:
    print('error ', type, kommune)

w = 0.35

plt.bar(districts, lakes, width=w, color='r')
plt.bar(districts, streams, width=w, bottom=lakes, color='b')
plt.ylabel('lakes and streams')
plt.xlabel('districts')
#ax.set_title('Lakes and streams per district in Copenhagen')
#ax.legend()

plt.show()
