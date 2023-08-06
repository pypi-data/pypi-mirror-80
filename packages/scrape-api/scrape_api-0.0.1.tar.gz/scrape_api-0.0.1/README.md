# Scrapeit

### scrape-api is sponsored by:	
<a href="https://www.developingnow.com/"><img src="https://github.com/alinisarhaider/ytkd_api/blob/master/developingco_logo.png?raw=true"/></a>

## Description
Python wrapper for REST API to scrape and retrieve data from Reddit for the given keyword.

## Installation

Download using pip via pypi.

```bash
$ pip install scrape-api
```

## Getting started

Import:

```python
>>> from scrape-api import Scrape
```


Create an object of Scrape.
```python
>>> scraper = Scrape(username='username', password='password')
```
Search for a new keyword.
```python
>>> search_results = scraper.new_search(keyword='zoro')
```
Retrieve results from previous searches.
```python
>>> previous_results = scraper.get_previous_results()
```