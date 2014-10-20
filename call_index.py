from __future__ import division
import os
import Quandl

__author__ = 'Patrick Howell'

def get_dt_ret(data):
    try:
        data['Return'] = ((data['Open'] - data['Close'])/data['Open']) * 100
        data['Date'] = data.index
    # Except for Japan's different labels
    except:
        data['Return'] = ((data['Open Price'] - data['Close Price'])/data['Open Price']) * 100
        data['Date'] = data.index

    data_dict = data.to_dict()
    dt_ret = {}
    for i in data_dict['Date']:
        dt_ret[data_dict['Date'][i].strftime("%Y-%m-%d")] = data_dict['Return'][i]
    return dt_ret

def quandl_apis(start_date, current_date):
    """
    Calling one "representative" index from each country available through Quandl's API, one at a time

    :param start_date/current_date: String in the form of 4digit year -- 2digit month -- 2digit day
    :return: Dictionary only in the form of {Country: {Dates: Returns}}
    """

    markets = {}

    # Argentina: MERVAL Index...start: 1996-10-08
    argentina = Quandl.get("YAHOO/INDEX_MERV", trim_start="%s" % start_date, trim_end="%s" % current_date,
               authtoken="SqjRioyWHL4APSzRUm_c")
    markets['Argentina'] = get_dt_ret(argentina)

    # Australia: All Ordinaries Index...start: 1984-08-03
    australia = Quandl.get("YAHOO/INDEX_AORD", trim_start="%s" % start_date, trim_end="%s" % current_date,
                           authtoken="SqjRioyWHL4APSzRUm_c")
    markets['Australia'] = get_dt_ret(australia)

    # Brazil: Bovespa Index...start: 1989-12-29
    #brazil = Quandl.get("BCB/7", trim_start="%s" % start_date, trim_end="%s" % current_date,
    #                    authtoken="SqjRioyWHL4APSzRUm_c")
    #markets['Brazil'] = get_dt_ret(brazil)

    # Canada: S&P TSX Composite Index...start: 1979-06-29
    canada = Quandl.get("YAHOO/INDEX_GSPTSE", trim_start="%s" % start_date, trim_end="%s" % current_date,
               authtoken="SqjRioyWHL4APSzRUm_c")
    markets['Canada'] = get_dt_ret(canada)

    # China: Hang Seng Index...start: 1986-12-31
    china = Quandl.get("YAHOO/INDEX_HSI", trim_start="%s" % start_date, trim_end="%s" % current_date,
                       authtoken="SqjRioyWHL4APSzRUm_c")
    markets['China'] = get_dt_ret(china)

    # France:  CAC 40 Index...start: 1990-03-01
    france = Quandl.get("YAHOO/INDEX_FCHI", trim_start="%s" % start_date, trim_end="%s" % current_date,
                        authtoken="SqjRioyWHL4APSzRUm_c")
    markets['France'] = get_dt_ret(france)

    # Germany: DAX Index...start: 1990-11-26
    germany = Quandl.get("YAHOO/INDEX_GDAXI", trim_start="%s" % start_date, trim_end="%s" % current_date,
                         authtoken="SqjRioyWHL4APSzRUm_c")
    markets['Germany'] = get_dt_ret(germany)

    # India: BSE 30 Sensitivity Index...start: 1997-07-01
    india = Quandl.get("YAHOO/INDEX_BSESN", trim_start="%s" % start_date, trim_end="%s" % current_date,
                       authtoken="SqjRioyWHL4APSzRUm_c")

    markets['India'] = get_dt_ret(india)

    # Indonesia: Jakarta Composite Index...start: 1997-07-01
    indonesia = Quandl.get("YAHOO/INDEX_JKSE", trim_start="%s" % start_date, trim_end="%s" % current_date,
                           authtoken="SqjRioyWHL4APSzRUm_c")
    markets['Indonesia'] = get_dt_ret(indonesia)

    # Japan: Nikkei Index...start: 1950-01-04
    japan = Quandl.get("NIKKEI/INDEX", trim_start="%s" % start_date, trim_end="%s" % current_date,
                       authtoken="SqjRioyWHL4APSzRUm_c")
    markets['Japan'] = get_dt_ret(japan)

    # Mexico: IPC Index...start: 1991-11-08
    mexico = Quandl.get("YAHOO/INDEX_MXX", trim_start="%s" % start_date, trim_end="%s" % current_date,
                        authtoken="SqjRioyWHL4APSzRUm_c")
    markets['Mexico'] = get_dt_ret(mexico)

    # Russia: RTSI Index...start: 1995-09-01
    russia = Quandl.get("YAHOO/INDEX_RTS_RS", trim_start="%s" % start_date, trim_end="%s" % current_date,
                        authtoken="SqjRioyWHL4APSzRUm_c")
    markets['Russia'] = get_dt_ret(russia)

    # South Korea: KOPSI Index...start: 1997-07-01
    skorea = Quandl.get("YAHOO/INDEX_KS11", trim_start="%s" % start_date, trim_end="%s" % current_date,
                        authtoken="SqjRioyWHL4APSzRUm_c")
    markets['South Korea'] = get_dt_ret(skorea)

    # Spain: IBEX 35 Index...start: 1993-02-15
    spain = Quandl.get("YAHOO/INDEX_IBEX", trim_start="%s" % start_date, trim_end="%s" % current_date,
                       authtoken="SqjRioyWHL4APSzRUm_c")
    markets['Spain'] = get_dt_ret(spain)

    # # UK: FTSE...no historical data available from Quandl
    # uk = Quandl.get("YAHOO/INDEX_FTSE", trim_start="%s" % start_date, trim_end="%s" % current_date,
    #                    authtoken="SqjRioyWHL4APSzRUm_c")
    # markets['United Kingdom'] = get_dt_ret(uk)

    # USA:  S&P 500 Index...start: 1950-01-03
    usa = Quandl.get("YAHOO/INDEX_GSPC", trim_start="%s" % start_date, trim_end="%s" % current_date,
                     authtoken="SqjRioyWHL4APSzRUm_c")
    markets['United States of America'] = get_dt_ret(usa)

    return markets


if __name__== '__main__':
    test = quandl_apis('2000-01-03', '2014-10-14')
    print "Dictionary finished!"