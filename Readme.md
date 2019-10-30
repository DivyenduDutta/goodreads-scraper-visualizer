# goodreads-scraper-visualizer          [![Documentation Status](https://readthedocs.org/projects/goodreads-scraper-visualizer/badge/?version=latest)](https://goodreads-scraper-visualizer.readthedocs.io/en/latest/?badge=latest) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/DivyenduDutta/goodreads-scraper-visualizer/blob/master/LICENSE.md) [![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Python 2 code which uses **beautiful soup 4** and **selenium** to scrape details of most popular books of a genre.
Also, once it has the individual book URLs, it scrapes the review details of each of those books and
visualizes this information.

Uses custom logger - [YALogger](https://github.com/DivyenduDutta/YALogger).

### Requirements 

As this is using Selenium to control the Chrome Browser,<br>
so you'll need to download its driver for your specific os from
[here](https://sites.google.com/a/chromium.org/chromedriver/downloads).


### Demo

need to do

### Documentation

Hosted on [Read The Docs](https://goodreads-scraper-visualizer.readthedocs.io/en/latest/).

Achieved via Sphinx (as the doc build tool), reStructuredText as the markup and hosted on Read The Docs website.

### Images

Couple of books review details visualized

![alt text](https://github.com/DivyenduDutta/goodreads-scraper-visualizer/blob/master/images/multiplebooks.PNG)

One book review details visualized

![alt text](https://github.com/DivyenduDutta/goodreads-scraper-visualizer/blob/master/images/375802_Ender_s_Game.png)

 
### Resources

> - [Selenium](http://www.seleniumhq.org/)
> - [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
> - [Matplotlib](https://matplotlib.org/)

### License

This is an open source tool licensed under GPL v3.0. Copy of the license can be found
[here](https://github.com/DivyenduDutta/goodreads-scraper-visualizer/blob/master/LICENSE.md).
