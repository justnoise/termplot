termplot
========
A quickly slapped together ascii plotting library.  It can do line plots and histograms.  I created this to quickly view plots of timeseries data when sshing into servers.

Usage
=====
```
import math
from termplot import Plot
xvals, yvals = [], []
for i in range(0, 2000, 5):
    xx = i / 100.0
    xvals.append(xx)
    yvals.append(math.sin(xx) * float(i ** 0.5))
Plot(xvals, yvals, LINE)
```
![Alt text](/doc/line_plot.jpg?raw=true "Line plot")

```
import random
xvals = []
for i in range(100000):
    xvals.append(random.gauss(0, 1.5))
Plot(xvals, plot_type=HISTOGRAM)
```
![Alt text](/doc/histogram_plot.jpg?raw=true "Histogram plot")

Bugs and Todo
=============
* The code is crazy ugly
* No axis titles
* No plot title