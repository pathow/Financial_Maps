from bs4 import BeautifulSoup
import urllib2
import sys


__author__ = 'Patrick Howell'

#API_key = 'SqjRioyWHL4APSzRUm_c'

def get_markets_dict():
    # Getting the most up to date information from Quandl's Global Markets Collection
    table_url = "https://www.quandl.com/c/markets/global-stock-markets"

    request = urllib2.Request(table_url)

    try:
        page = urllib2.urlopen(request)
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            print 'Failed to reach url'
            print 'Reason: ', e.reason
            sys.exit()
        elif hasattr(e, 'code'):
            if e.code == 404:
                print 'Error: ', e.code
                sys.exit()

    # Parsing the html into beautiful soup
    content = page.read()
    soup = BeautifulSoup(content)

    # Raw table data:
    raw_data = soup.find_all('tr')

    # Getting all table data entries and putting into list of lists format to separate rows
    full_data = []
    for entry in raw_data:
        row_data = [x.string for x in entry.find_all('td')]  # finding all table data by row
        if len(row_data) > 1:
            full_data.append(row_data)

    # Dictionary that will hold each index's information
    markets = {}

    for row in full_data:
        index = row[1].encode('ascii')
        # Need to check index not already in dictionary, since source page sometimes double lists
        # given different groupings like geography vs. G-20
        if index not in markets:
            # Converting the return entries to ascii to make check
            one_day = row[5].encode('ascii')
            mtd = row[6].encode('ascii')
            ytd = row[7].encode('ascii')
            # Check that none of the return data is missing
            # Then build each row by column entry
            if one_day != 'n.a.' and mtd != 'n.a.' and ytd != 'n.a.':
                markets[index] = {}
                markets[index]['Country'] = row[0].encode('ascii')
                markets[index]['Level'] = row[2].encode('ascii')
                markets[index]['Date'] = row[3].encode('ascii')
                markets[index]['Source'] = row[4].encode('ascii')

                # Stripping % signs and converting number strings to floats
                one_day = float(one_day[:-1])
                markets[index]['1 Day Change'] = one_day

                mtd = float(mtd[:-1])
                markets[index]['MTD Change'] = mtd

                ytd = float(ytd[:-1])
                markets[index]['YTD Change'] = ytd
        else:
            continue

    return markets

def one_day_by_country(markets):

    countries = {}

    for index in markets:
        current_country = markets[index]['Country']
        if current_country == 'UK':
            current_country = 'United Kingdom'
        elif current_country == 'USA':
            current_country = 'United States of America'
        if current_country not in countries:
            countries[current_country] = [markets[index]['1 Day Change']]
        else:
            countries[current_country].append(markets[index]['1 Day Change'])

    # Taking the average % change of all of a country's indices
    for country in countries:
        countries[country] = sum(countries[country])/len(countries[country])

    return countries

if __name__ == '__main__':
    markets = get_markets_dict()
    country = one_day_by_country(markets)
    for i in country:
        print "1 day change in %s: %.3f" % (i, country[i])
