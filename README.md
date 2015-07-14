termplot
========
A quickly slapped together ASCII plotting library.  It can do line plots and histograms.  I created this to easily view plots of timeseries data when sshing into servers.

Usage
=====
```python
import math
from termplot import LINE, Plot
xvals, yvals = [], []
for i in range(0, 2000, 5):
    xx = i / 100.0
    xvals.append(xx)
    yvals.append(math.sin(xx) * float(i ** 0.5))
Plot(xvals, yvals, LINE)
```
![Line plot](/doc/line_plot.png?raw=true "Line plot")

```python
import random
from termplot import HISTOGRAM, Plot
xvals = []
for i in range(100000):
    xvals.append(random.gauss(0, 1.5))
Plot(xvals, plot_type=HISTOGRAM)
```
![Histogram plot](/doc/histogram_plot.png?raw=true "Histogram plot")

Bugs and Todo
=============
* The code is crazy ugly
* No axis titles
* No plot title
* Allow piping of data from stdin
