import current_market_scrape
import dateutil
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs
import time
from call_index import quandl_apis





__author__ = 'Patrick Howell'


markets = current_market_scrape.get_markets_dict()
country_market = current_market_scrape.one_day_by_country(markets)

def available_data_map(country_market):
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.add_feature(cartopy.feature.OCEAN)
    ax.set_extent([-150, 60, -25, 60])
    shpfilename = shpreader.natural_earth(resolution='110m',
                                      category='cultural',
                                      name='admin_0_countries')
    reader = shpreader.Reader(shpfilename)
    countries = reader.records()

    for country in countries:
        name = country.attributes['sovereignt']
        if name in country_market:
            ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                              facecolor=(0,1,0),
                              label=country.attributes['adm0_a3'])
        else:
            ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                              facecolor='0.75',
                              label=country.attributes['adm0_a3'])

    ## mm/dd/yyyy format
    date = time.strftime("%m/%d/%Y")
    ax.annotate('Source: Quandl at https://www.quandl.com/c/markets/global-stock-markets', (0,0), (0, -20),
                 xycoords='axes fraction', textcoords='offset points', va='top')
    ax.set_title("Available National Stock Market Data\n(as of %s)" % date)
    plt.savefig('available_markets.pdf', bbox_inches='tight')



def market_change_map(country_market):
    """
    Takes a dictionary of format Country: Return and prints a color gradient map
    ranging from 5% to -5% as blue to red, respectively
    """
    # Getting the base figure set up
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
        if name in country_market:
            # facecolor is normalized to a 0,1 gradient assuming daily returns capped at -5,5
            ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                              facecolor=mpl.cm.bwr_r((country_market[name]+5)/10),
                              label=country.attributes['adm0_a3'])
        else:
            ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                              facecolor='0.75',
                              label=country.attributes['adm0_a3'])

    # mm/dd/yyyy format and hour:minute for time stamps to indicate when the map was created/what
    # data was used
    date = time.strftime("%m/%d/%Y")
    hour = time.strftime("%H:%M")

    # Add the color bar for a legend
    norm = mpl.colors.Normalize(vmin=-5, vmax=5)
    cax = fig.add_axes([0.95, 0.2, 0.02, 0.6])
    cb = mpl.colorbar.ColorbarBase(cax, cmap=mpl.cm.bwr_r, norm=norm, spacing='proportional')
    cb.set_label('One Day % Change', rotation=270, labelpad=16)
    cb.ax.yaxis.set_ticks_position('left')

    ax.set_title("Daily Change in National Stock Markets\n(Taken on %s at %s)" % (date, hour))
    ax.annotate('Source: Quandl at https://www.quandl.com/c/markets/global-stock-markets', (0,0), (0, -20),
                 xycoords='axes fraction', textcoords='offset points', va='top')


    plt.savefig('Daily_Change_%s.pdf' % time.strftime("%m_%d_%Y"), bbox_inches='tight')



if __name__ == '__main__':
    available_data_map(country_market)
    market_change_map(country_market)
