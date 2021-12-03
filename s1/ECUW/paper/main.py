import matplotlib.pyplot as plt
import numpy as np

fig, ax_eco = plt.subplots() # Create a figure containing a single axes.

years = list(range(2010,2021))
x_axis = years

y_wholesale=[413679.8,385185.4,585917.8,773798.6,907427.6,1005895.4,861263.1,961381.9,11098676,14504047,16030749]
y_financial=[np.nan,np.nan,np.nan,np.nan,172620.1,205329.5,246404.9,307653.7,3549828,3706838,3808144]
y_realestate=[254161.3,313559.8,344362.8,379357.2,445059.7,545164,602321.6,694936.7,9400666,10554757,8420941]
y_scientific=[np.nan,np.nan,np.nan,np.nan,411123.5,433203.1,523427.6,678035.4,766200,8151048,8120693]
y_administrative=[np.nan,np.nan,np.nan,np.nan,189463.5,206720.8,220055.8,332162.9,3433098,4259048,5263111]

ax_eco.plot(x_axis, y_wholesale, color='green')
ax_eco.plot(x_axis, y_realestate, color='blue')
ax_eco.plot(x_axis, y_scientific, color='pink')
ax_eco.plot(x_axis, y_administrative, color='black')
ax_eco.plot(x_axis, y_financial, color='red')

# ax_employ = ax_eco.twinx() # Instantiate second axis that shares same x-axis
# color = 'tab:blue'

plt.savefig('grp_vs_employment_by_sector.png')
