import csv 
import glob
import pickle
from collections import defaultdict
import datetime
from dateutil import parser

### Script will save output as outfile below and parse all data in data/ subdir. Change as desired!
outfile = 'mta-data.pkl'
mta_files = glob.glob('data/*.txt')

def files_to_data(files_list):
    """Convert raw data into dict of traffic by hour by day for each turnstile.
    Args:
    files_list (list) -- list of paths of data files as str (e.g. ['data/turnstile_150530.txt'])

    Returns:
    tdict (dict) -- dict with keys = turnstile; values = date, hour, traffic 
    """
    tdict = defaultdict(list)
    for f in files_list:
        with open (f) as data:
            datadict = csv.DictReader(data)
            for row in datadict:
                ca = row[datadict.fieldnames[0]]
                unit = row[datadict.fieldnames[1]]
                scp = row[datadict.fieldnames[2]]
                station = row[datadict.fieldnames[3]]
                linename = row[datadict.fieldnames[4]]
                division = row[datadict.fieldnames[5]]
                date = row[datadict.fieldnames[6]]
                time = row[datadict.fieldnames[7]]
                desc = row[datadict.fieldnames[8]]
                entries = row[datadict.fieldnames[9]]
                exits = row[datadict.fieldnames[10]]
                tdict[(ca, unit, scp, station)].append([parser.parse(
                            date + " " + time), (int(entries) + int(exits))])
    return tdict                  

def get_traffic(dic):
    """Convert by hour traffic counts into by day counts. 
    Args:
    dic (dict) -- dict with counts by day and hour for each turnstile (output from files_to_data())

    Returns:
    tdict (dict) -- dict with keys = turnstile; values = date, traffic counts
    """
    tdict = defaultdict(list)

    for key in dic: 
        # create new dict with station identifier as key and all entry counts as list of values 
        tempdict = defaultdict(list) 
        for act in dic[key]: 
            timestamp = act[0] 
            traffic = act[1] 
            tempdict[timestamp.date()].append(traffic) 

        # iterate through tempdict and find difference between min and max values
        tempdict2 = defaultdict(list)
        for date in tempdict: 
            count = max(tempdict[date]) - min(tempdict[date])
            if 0 <= count <= 5000:
                tempdict2[date].append(count)

        tdict[key] = tempdict2
    return tdict

def get_traffic_by_unit(dic):
    """Combine traffic counts for turnstiles in the same control unit. 
    Args:
    dic (dict) -- dict with traffic counts by date for each turnstile (output from get_traffic())

    Returns:
    traffic_by_unit (dic) -- dict with keys = turnstile unit; values = date, traffic counts
    """
    traffic_byunit = defaultdict(list)
    
    # get ca, unit, station identifiers only
    for ca, unit, _, station in dic.keys():
        traffic_byunit[ca, unit, station].append(dic[(ca, unit, _, station)])

    # loop through dict for each station and combine counts from the same day 
    for key in traffic_byunit: 
        counts = traffic_byunit[key]
        summed_dict = defaultdict(list)
        for d in counts:
            for date, counts in d.iteritems():
                summed_dict[date] = summed_dict.get(date, 0) + counts[0] 

        traffic_byunit[key] = summed_dict
    return traffic_byunit

def get_traffic_by_station(dic):
    """Combine traffic counts for turnstiles in the same station.
    Args:
    dic (dict) -- dict with traffic counts by date for each control unit (output from get_traffic_by_unit())

    Returns:
    traffic_bystation (dict) -- dict with keys = station; values = date, traffic counts
    """
    traffic_bystation = defaultdict(list)
    
    # get stations only
    for ca, unit, station in dic.keys():
        traffic_bystation[station].append(dic[(ca, unit, station)])

    # loop through dict for each station and combine counts from the same day 
    for key in traffic_bystation: 
        counts = traffic_bystation[key]
        station_summed_dict = defaultdict(list)
        for d in counts:
            if type(d) != list:
                for date, counts in d.iteritems():
                    station_summed_dict[date] = station_summed_dict.get(date, 0) + counts

        traffic_bystation[key] = station_summed_dict
    return traffic_bystation

def get_total_counts(dic):
    """Compute total traffic counts by station within a given timeframe.
    Args:
    dic (dict) -- dict with counts by day and hour for each turnstile (output from files_to_data())

    Returns:
    total_by_station (dict) -- dict of total count by station for the given period of time 
    """
    data = get_traffic(dic)
    traffic_byunit = get_traffic_by_unit(data)
    traffic_bystation = get_traffic_by_station(traffic_byunit)
    total_by_station = defaultdict(list)

    for station in traffic_bystation:
        countsbyweek = traffic_bystation[station]
        for date, counts in countsbyweek.iteritems():
            total_by_station[station] = total_by_station.get(station, 0) + counts
    return total_by_station

def main():
	print 'Parsing in progress...'
	data = files_to_data(mta_files)
	total_by_station = get_total_counts(data)
	with open(outfile, 'w') as picklefile:
		pickle.dump(total_by_station, picklefile)
	print 'Parsing complete!'
	print 'Data saved to: ' + outfile

if __name__ == '__main__':
    main()
