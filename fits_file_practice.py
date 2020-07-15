#%% Initializing
import numpy as np
from astropy.io import fits
from astropy.table import Table
#from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt

#%% Opening file
#hdu_list = fits.open('/home/bruno/Documents/COSMOamautas/bootes_optIR_catalogue_science_ready_photoz.fits',memmap=True) #full galaxy catalogue
hdu_list = fits.open('/home/bruno/Documents/COSMOamautas/Data/bootes_catalogue_mass_median_107',memmap=True) #catalogue for log(M*)>10.7
hdu_list.info()
#print(hdu_list[1].columns)

#%% Reading data (this may take a while)
bootes_data = Table(hdu_list[1].data)

#%%
#some_row = bootes_data[1271740]
#print(some_row)

print(min(bootes_data['Z_BEST']))
print(max(bootes_data['Z_BEST']))
print(len(bootes_data['Z_BEST']))

#%% Filling missing values
bootes_data['u_rest'].filled(np.nan)
bootes_data['R_rest'].filled(np.nan)
bootes_data['J_rest'].filled(np.nan)

#%% Plotting two colors given by three filters
filter1 = 'u'
filter2 = 'R'
filter3 = 'J'
plt.clf()
plt.figure(figsize=(9,6))
plt.xlabel(f"${filter2}-{filter3}$",fontsize=10)
plt.ylabel(f"${filter1}-{filter2}$",fontsize=10)
plt.scatter(bootes_data[f'{filter2}_rest']-bootes_data[f'{filter3}_rest'],bootes_data[f'{filter1}_rest']-bootes_data[f'{filter2}_rest'],s=0.1)
#plt.scatter(some_row['u_rest']-some_row['R_rest'],some_row['R_rest']-some_row['J_rest'])
plt.plot([-10,0.7,10],[3.1,3.1,31],color='r')

#%% Plotting two filters
filter1 = 'u'
filter2 = 'R'
plt.clf()
plt.figure(figsize=(9,6))
plt.xlabel(f"{filter2} mag",fontsize=10)
plt.ylabel(f"{filter1} mag",fontsize=10)
plt.scatter(bootes_data[f'{filter2}_rest'],bootes_data[f'{filter1}_rest'],s=0.1)

#%% Masking inf values
#mask = (bootes_data['u_rest'] > -75) & (bootes_data['u_rest'] < 130)
#plt.clf()
#plt.hist(bootes_data['Z_BEST'],bins='auto')

#%% Plotting histograms
fig, ax = plt.subplots(figsize=(9,6))
ax.hist(bootes_data['Z_BEST'], 'auto')
ax.set_xlabel('Redshift z')
ax.set_ylabel('Galaxy count')
ax.set_title(r'Distribution of redshift for galaxies with log(M)>10.7')
#ax.set_ylim(ymax=25000)
fig.tight_layout()
plt.show()

#%% Closing file
hdu_list.close()
