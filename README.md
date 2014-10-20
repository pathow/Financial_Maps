Financial_Maps
==============

Mapping international financial data by country

Scrapes Quandl's page of international stock indices with one module, at this point mostly just to obtain the one day performance of each index. The index is then matched with its home country, and the result is printed as a gradient of degree of change to a map of the world.

The other option makes use of Quandl's API to query a representative stock index from every available G20 country. The Python code itself only creates a series of .png files in the Example_Maps folder, but does not animate the maps into a single .gif itself.

In order to animate, once all .pngs are obtained, run the following code in Terminal:
    convert -delay 50 -loop 100 *.png g20.gif


DISCLAIMER: These maps make zero claim to convey actionable financial information. This is more an exercise in how to plot data to a map using Python.
