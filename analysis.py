import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

### Change infile name if you changed it from the default in data-munge.py
infile = 'mta-data.pkl'
contributions = 'contributions.csv'

def get_df(pickled):
	"""Convert data output from data-munge.py into a dataframe.
	Args:
	pickled (pickle object) -- object containing dict of stations and total traffic counts

	Returns:
	df (pandas dataframe) -- dataframe of stations and traffic counts, sorted by top stations
	"""
	with open(pickled, 'r') as picklefile:
		data = pickle.load(picklefile)
	stations, counts = zip(*data.items())
	df = pd.DataFrame({'station': list(stations), 'counts': list(counts)})
	df.set_index('station', inplace = True)
	df.sort_values('counts', ascending = False, inplace = True)
	return df

def plot_top25_stations(df):
	"""Plot top 25 stations by traffic count."""
	# need to resort in ascending and take tail b/c of pyplot barh idiosyncracies
	top25 = df.sort_values(by = 'counts').tail(25)
	top25.plot(
		kind = 'barh', 
		y = 'counts', 
		figsize = (20, 12), 
		fontsize = 20, 
		alpha = 0.5, 
		legend = False,
		color = 'black')
	plt.title('Top 25 MTA Stations by Traffic', fontsize = 24)
	plt.xlabel('Total Entries and Exits (10-millions)', fontsize = 20)
	plt.ylabel('Station', fontsize = 20)
	plt.show()

def drop_stations(station_list, df):
	"""Drop stations that have multiple stations represented in the same name.
	Args:
	station_list (list) -- list of station names to drop_stations
	Returns:
	df (df) -- data frame with remaining stations 
	"""
	df = df.head(25).drop(station_list, axis=0)
	return df

def add_contr_data(data, df):
	"""Determine top 25 stations by total potential contribution (traffic * median cont pp).
	Note that csv only contains zip and contribution information for the top 25 stations
	in the April - May 2015 analysis (excluding dropped stations). For additional stations, 
	visit https://philanthropy.com/interactives/how-america-gives and input station zip to 
	collect contribution data. 
	Args:
	data (str) -- filename of csv file with contributions data
	df (df) -- top stations dataframe excluding repeated stations
	"""
	data = pd.read_csv(data).set_index('station')
	merged = pd.merge(df, data, how = 'left', left_index = True, right_index = True)
	merged['total_potential_contr'] = merged['med_contribution_2012'] * merged['counts']
	merged.sort_values(by = 'total_potential_contr', ascending = False, inplace = True)
	return merged

def plot_top10_stations(df):
	"""Plot top 10 stations by total potential contribution.
	Args:
	df (df) -- dataframe with top stations sorted by total potential contribution.
	"""
	forplot = df.sort_values(by = 'total_potential_contr').tail(10)
	forplot.plot(
		kind = 'barh', 
		y = 'total_potential_contr', 
		figsize = (20, 12), 
		fontsize = 20, 
		alpha = 0.5, 
		legend = False,
		color = 'black')
	plt.title('Top 10 MTA Stations by Potential Contribution Size', fontsize = 24)
	plt.xlabel('Total Potential Contributions ($B)', fontsize = 20)
	plt.ylabel('Station', fontsize = 20)
	plt.show()

def main():
	print 'Analysis in progress...'
	top_stations = get_df(infile)
	print 'Returning top 25 stations by traffic chart'
	plot_top25_stations(top_stations)
	to_drop = to_drop = ['86 ST', '125 ST', '96 ST', 'CANAL ST', 'CHURCH AVE', 
	'96 ST', '50 ST', '59 ST', '28 ST', '23 ST']
	top_stations = drop_stations(to_drop, top_stations)
	with_contr = add_contr_data(contributions, top_stations)
	print 'Returning top 10 stations by potential contributions chart'
	plot_top10_stations(with_contr)

if __name__ == '__main__':
    main()

