from __future__ import division
import os
import Quandl as Q
import dateutil
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import animation
import cartopy
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs
import time
from call_index import quandl_apis

__author__ = 'Patrick Howell'

# General process: Calls the Quandl API to build a dictionary based on available dates
# Then that dictionary is used to create an individual .png map for every date
# which is stored in a subdirectory referred to by "Example Maps"



# Getting a small subset of data on possible G20 countries from Quandl
year2014 = quandl_apis('2014-10-15', '2014-10-19')

for date in sorted(year2014['United States of America']):
    # U.S. trading days used to standardize across all countries
    # starting the plot/figure, clearing the any old one
    plt.clf()
    fig, ax = plt.subplots(figsize=(12,6),
                       subplot_kw={'projection': ccrs.PlateCarree()})
    ax.add_feature(cartopy.feature.OCEAN)
    ax.set_extent([-150, 60, -25, 60])

    shpfilename = shpreader.natural_earth(resolution='110m',
                                      category='cultural',
                                      name='admin_0_countries')
    # Reader and countries both are "generator objects" which can be iterated
    reader = shpreader.Reader(shpfilename)
    countries = reader.records()

    for country in countries:
        # 'soverignt' is the attribute with full country names
        name = country.attributes['sovereignt']
        # So it is used to match the key of country name in the dictionary
        if name in year2014:
            # facecolor is normalized to a 0,1 gradient assuming daily returns capped at -5,5
            try:
                ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                                  facecolor=mpl.cm.bwr_r((year2014[name][date]+5)/10),
                                  label=country.attributes['adm0_a3'])
            # Except statement needed in case no corresponding date key exists for that country
            except:
                ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                  facecolor='0.75',
                  label=country.attributes['adm0_a3'])
        else:
            ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                              facecolor='0.75',
                              label=country.attributes['adm0_a3'])


    norm = mpl.colors.Normalize(vmin=-5, vmax=5)
    cax = fig.add_axes([0.95, 0.2, 0.02, 0.6])
    cb = mpl.colorbar.ColorbarBase(cax, cmap=mpl.cm.bwr_r, norm=norm, spacing='proportional')
    cb.set_label('One Day % Change', rotation=270, labelpad=16)
    cb.ax.yaxis.set_ticks_position('left')

    ax.set_title("Daily Change in National Stock Markets\n(Taken on %s)" % date)
    ax.annotate('Source: Quandl at https://www.quandl.com/c/markets/global-stock-markets', (0,0), (0, -20),
                 xycoords='axes fraction', textcoords='offset points', va='top')

    savepath = os.path.join('Example_Maps', 'G20_only_%s.png' % date)
    plt.savefig(savepath, bbox_inches='tight', dpi=50)

