# pypiplot

[![Python](https://img.shields.io/pypi/pyversions/pypiplot)](https://img.shields.io/pypi/pyversions/pypiplot)
[![PyPI Version](https://img.shields.io/pypi/v/pypiplot)](https://pypi.org/project/pypiplot/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/erdogant/pypiplot/blob/master/LICENSE)
[![Coffee](https://img.shields.io/badge/coffee-black-grey.svg)](https://erdogant.github.io/donate/?currency=USD&amount=5)
[![Github Forks](https://img.shields.io/github/forks/erdogant/pypiplot.svg)](https://github.com/erdogant/pypiplot/network)
[![GitHub Open Issues](https://img.shields.io/github/issues/erdogant/pypiplot.svg)](https://github.com/erdogant/pypiplot/issues)
[![Project Status](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)
[![Downloads](https://pepy.tech/badge/pypiplot/month)](https://pepy.tech/project/pypiplot/month)


* pypiplot is Python package to count and plot the number of downloads from Pypi.


### Installation
* Install pypiplot from PyPI (recommended). pypiplot is compatible with Python 3.6+ and runs on Linux, MacOS X and Windows. 

```bash
pip install pypiplot    # normal install
pip install -U pypiplot # or update if needed
```

#### Import pypiplot package
```python
import pypiplot as pypiplot
```

#### Example update repos to disk:
```python
from pypiplot import pypiplot

# Download all data for github user.
pp = pypiplot(username='erdogant')

# Update all repos
pp.update()

# Update single repo
pp.update(repo=['bnlearn','hnet'])

```

#### Example show repo download stats:
```python
from pypiplot import pypiplot

# Download all data for github user.
pp = pypiplot(username='erdogant')

# Get total stats across all repos
results = pp.stats()

# Get some stats
results = pp.stats(repo=['df2onehot','pca','bnlearn'])

print(results.keys())
# ['data', 'heatmap', 'n_libraries', 'repos']

# Print data
print(results['data'])

#             bnlearn  df2onehot    pca
# date                                 
# 2020-05-01    100.0       18.0  281.0
# 2020-05-02      6.0        4.0  260.0
# 2020-05-03     50.0       16.0  126.0
# 2020-05-04     82.0       64.0   86.0
# 2020-05-05     64.0      157.0   50.0
#             ...        ...    ...
# 2020-09-11    148.0      213.0   78.0
# 2020-09-12     96.0      102.0  144.0
# 2020-09-13     12.0       42.0  197.0
# 2020-09-14    156.0       92.0  244.0
# 2020-09-15     40.0       76.0  225.0

```

#### Example make plots

```python
pp.plot_year(title='pypiplot')
pp.plot(title='pypiplot')

```

<p align="center">
  <img src="https://github.com/erdogant/pypiplot/blob/master/docs/figs/plot_default.png" width="450" />
  <img src="https://github.com/erdogant/pypiplot/blob/master/docs/figs/plot_year_default.png" width="450" />
</p>


**Change some of the colors and the minimum cut-off value**

```python
pp.plot_year(vmin=100, cmap='interpolateYlOrRd')
pp.plot(vmin=100, cmap='interpolateYlOrRd')

```

<p align="center">
  <img src="https://github.com/erdogant/pypiplot/blob/master/docs/figs/plot_1.png" width="450" />
  <img src="https://github.com/erdogant/pypiplot/blob/master/docs/figs/plot_year_1.png" width="450" />
</p>


**Plot all repos for github username**

```python

# Download all data for github user.
pp = pypiplot(username='erdogant')

# Get total stats across all repos
results = pp.stats()

# Get some stats
results = pp.stats()

pp.plot_year(vmin=700, title='Total downloads across all repos')
pp.plot(vmin=100)

```

<p align="center">
  <img src="https://github.com/erdogant/pypiplot/blob/master/docs/figs/plot_year_total.png" width="450" />
  <img src="https://github.com/erdogant/pypiplot/blob/master/docs/figs/plot_total.png" width="450" />
</p>


#### Run pypiplot from terminal

Arguments:

    * "-u", "--username" : username github
    * "-l", "--library"  : library name(s)
    * "-p", "--path"     : path name to store plot.
    * "-v", "--vmin"     : minimun value of the figure.


```bash

> python pypiplot/pypiplot.py -u 'erdogant' -p 'C://pypi_heatmap.html' -v '700'

```

#### Citation
Please cite pypiplot in your publications if this is useful for your research. Here is an example BibTeX entry:
```BibTeX
@misc{erdogant2020pypiplot,
  title={pypiplot},
  author={Erdogan Taskesen},
  year={2020},
  howpublished={\url{https://github.com/erdogant/pypiplot}},
}
```

#### References
* https://github.com/erdogant/pypiplot

### Maintainer
* Erdogan Taskesen, github: [erdogant](https://github.com/erdogant)
* Contributions are welcome.
* If you wish to buy me a <a href="https://erdogant.github.io/donate/?currency=USD&amount=5">Coffee</a> for this work, it is very appreciated :)
	Star it if you like it!
