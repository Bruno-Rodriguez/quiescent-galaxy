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
#To read the data directly without loading the file to memory:
#t = Table.read('/home/bruno/Documents/COSMOamautas/Data/bootes_catalogue_mass_median_107', hdu=1)
#print(hdu_list[1].columns)

#%% Reading data (this may take a while)
bootes_data = Table(hdu_list[1].data)
#Another method:
#t = Table.read(hdu_list[1])

#%% Trial commands
#some_row = bootes_data[1271740]
#print(some_row)
#print(min(bootes_data['Z_BEST']))
#print(max(bootes_data['Z_BEST']))
#print(len(bootes_data['Z_BEST']))

#%% Filling missing values
#bootes_data['u_rest'].filled(np.nan)
#bootes_data['R_rest'].filled(np.nan)
#bootes_data['J_rest'].filled(np.nan)

#%% Masking invalid ('inf') values
mask = np.isfinite(bootes_data['u_rest']) #& np.isfinite(bootes_data['R_rest'])
masked_table = bootes_data[mask]

#%% Plotting two colors given by three filters
filter1 = 'u'
filter2 = 'R'
filter3 = 'J'
plt.clf()
fig1, ax1 = plt.subplots(figsize=(9,6))
ax1.set_title('Color-color diagram for galaxies with log(M)>10.7')
ax1.set_xlabel(f"${filter2}-{filter3}$",fontsize=10)
ax1.set_ylabel(f"${filter1}-{filter2}$",fontsize=10)
ax1.scatter(masked_table[f'{filter2}_rest']-masked_table[f'{filter3}_rest'],masked_table[f'{filter1}_rest']-masked_table[f'{filter2}_rest'],s=0.1,label='Bootes field data')
ax1.plot([-10,0.7,10],[3.1,3.1,31],color='r',label='Color defining limit')
ax1.legend(numpoints=1, loc='best')
#ax1.set_ylim(ymax=25000)
fig1.tight_layout()
plt.show()

#%% Plotting two filters
filter1 = 'u'
filter2 = 'R'
plt.clf()
fig2, ax2 = plt.subplots(figsize=(9,6))
ax2.set_title('Magnitude-magnitude diagram for galaxies with log(M)>10.7')
ax2.set_xlabel(f"{filter2} mag",fontsize=10)
ax2.set_ylabel(f"{filter1} mag",fontsize=10)
ax2.scatter(masked_table[f'{filter2}_rest'],masked_table[f'{filter1}_rest'],s=0.1,label='Bootes field data')
ax2.legend(numpoints=1, loc='best')
fig2.tight_layout()
plt.show()

#%% Plotting Stellar mass vs Redshift
plt.clf()
fig3, ax3 = plt.subplots(figsize=(9,6))
ax3.set_title('Redshift and stellar mass distribution for galaxies with log(M)>10.7')
ax3.set_xlabel("Redshift z",fontsize=10)
ax3.set_ylabel("log(M [solar mass])",fontsize=10)
ax3.scatter(masked_table['Z_BEST'],masked_table['Mass_median'],s=0.1,label='Bootes field data')
ax3.legend(numpoints=1, loc='best')
fig3.tight_layout()
plt.show()

#%% Plotting Star formation rate vs Stellar mass
plt.clf()
fig3, ax3 = plt.subplots(figsize=(9,6))
ax3.set_title('Stellar mass and star formation rate distribution for galaxies with log(M)>10.7')
ax3.set_xlabel("log(M [solar masses])",fontsize=10)
ax3.set_ylabel("log(SFR [solar masses/yr])",fontsize=10)
ax3.scatter(masked_table['Mass_median'],masked_table['SFR_median'],s=0.1,label='Bootes field data')
ax3.plot([min(masked_table['Mass_median']),max(masked_table['Mass_median'])],[min(masked_table['Mass_median'])-11,max(masked_table['Mass_median'])-11],color='k',label='sSFR = -11')
ax3.set_ylim(ymin=0)
ax3.legend(numpoints=1, loc='best')
fig3.tight_layout()
plt.show()

#%% Plotting redshift histogram
fig, ax = plt.subplots(figsize=(9,6))
ax.set_title('Distribution of redshift for galaxies with log(M)>10.7')
ax.set_xlabel('Redshift z')
ax.set_ylabel('Galaxy count')
ax.hist(masked_table['Z_BEST'], 'auto')
#ax.set_ylim(ymax=25000)
fig.tight_layout()
plt.show()

#%% Plotting stellar mass histogram
fig, ax = plt.subplots(figsize=(9,6))
ax.set_title('Distribution of stellar mass for galaxies with log(M)>10.7')
ax.set_xlabel('log(M [solar masses])')
ax.set_ylabel('Galaxy count')
ax.hist(masked_table['Mass_median'], 'auto')
#ax.set_ylim(ymax=25000)
fig.tight_layout()
plt.show()

#%% Saving masked table to a new fits file
masked_table.write('/home/bruno/Documents/COSMOamautas/Data/new_table.fits')

#%% Closing original file
hdu_list.close()
