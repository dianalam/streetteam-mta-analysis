# streetteam-mta-analysis
Optimize a tech non-profit's street team placements by determining the ideal NYC subway station locations at which
to deploy. Recommendations based on analysis of NYC MTA turnstile traffic data and philanthropic contributions by zip code. 

For more information, see my [blog post](http://dianalam.github.io/2016/01/16/munging-mta.html).

## in this repo
* `datamunge.py` parses MTA turnstile data and returns total traffic counts for each station in the given time period
* `analysis.py` integrates philanthropic data and determines optimal stations; returns top stations
charts
* `data/` contains list of MTA data files used in `datamunge.py`
* `contributions.csv` contains contributions data by zip and station name for top stations
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
$ python datamunge.py

# run analysis
$ python analysis.py
```

Note that repo comes with default MTA turnstile data for the period between April and May of 2015. To use data 
from a different time frame, download the `.txt` files from the [MTA website](http://web.mta.info/developers/turnstile.html) and save in `data/` directory. The 
script will run on all files in that directory. 

To obtain additional contributions data, visit [The Chronicle of Philanthropy](https://philanthropy.com/interactives/how-america-gives) and input zip code information for your
station. 

## data sources
Thanks to: 
* [The NYC MTA](http://web.mta.info/developers/turnstile.html)
* [The Chronicle of Philanthropy](https://philanthropy.com)

