import current_market_scrape
import dateutil
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs
import time





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

    ax.set_title("Available National Stock Market Data\n(as of %s)" % date)
    plt.savefig('available_markets.pdf')



def market_change_map(country_market):
    """

    :rtype :
    """
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
            # facecolor is normalized to a 0,1 gradient assuming daily returns capped at -5,5
            ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                              facecolor=mpl.cm.bwr_r((country_market[name]+5)/10),
                              label=country.attributes['adm0_a3'])
        else:
            ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                              facecolor='0.75',
                              label=country.attributes['adm0_a3'])

    ## mm/dd/yyyy format
    date = time.strftime("%m/%d/%Y")
    hour = time.strftime("%H:%M")

    ax.set_title("Daily Change in National Stock Markets\n(Taken on %s at %s)" % (date, hour))
    plt.savefig('Daily_Change_%s.pdf' % time.strftime("%m_%d_%Y"))



if __name__ == '__main__':
    available_data_map(country_market)
    market_change_map(country_market)
