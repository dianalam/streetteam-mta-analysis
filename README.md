# streetteam-mta-analysis
Optimize a tech non-profit's street team placements by determining the ideal NYC subway station locations and days of the week
to deploy. Recommendations based on analysis of NYC MTA turnstile traffic data and philanthropic contributions by zip code. 

For more information, see my [blog post](http://dianalam.github.io/2016/01/16/munging-mta.html).

## in this repo
* `data-munge.py` parses MTA turnstile data and returns total traffic counts for each station in the given time period
* `analysis.py` integrates philanthropic data and determines optimal stations and days of the week; returns top stations
chart and traffic by day of week charts
* `data/` contains list of MTA data files used in `date-munge.py`
* `presentation/` contains pdf presentation of findings & recommendations

## installation
### clone this repo  
```bash
$ git clone https://github.com/dianalam/streetteam-mta-analysis.git
```

### dependencies
Scripts were written in Python 2.7. You'll need the following modules: 
```bash
matplotlib >= 1.5.1  
numpy >= 1.10.1  
pandas >= 0.17.1  
python-dateutil >= 2.4.2
```

To install modules, run:  
```bash
$ pip install <module>
```

### running
```bash
# parse data
$ python data-munge.py

# run analysis
$ python analysis.py
```
