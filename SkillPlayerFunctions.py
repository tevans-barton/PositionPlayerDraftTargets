import pandas as pd
import numpy as np

def clean_position(df):
	df = df.dropna(subset = ['Pos'])
	df['Pos'] = [str.upper(x) for x in df['Pos']]
	df = df[(df['Pos'] == 'RB') | (df['Pos'] == 'WR') | (df['Pos'] == 'TE')]
	return df.reset_index(drop = True)

def drop_unnecessary_columns_rosters(df):
	unwanted_columns = ['No.', 'BirthDate', 'Yrs', 'AV', 'Salary']
	df = df.drop(unwanted_columns, axis = 1)
	return df

def clean_player_column(df):
	player_list = df['Player']
	player_list = [x.replace('*', '').replace('+', '') for x in player_list]
	player_list = [x.split('\\', 1)[0] for x in player_list]
	df['Player'] = player_list
	return df

def fix_column_names(df):
	rename_dict = { 'Att' : 'Rush Att',
					'Yds' : 'Rush Yds',
					'TD' : 'Rush TD',
					'Lng' : 'Rush Lng',
					'Y/A' : 'Rush Y/A',
					'Y/G' : 'Rush Y/G',
					'Yds.1' : 'Receiving Yds',
					'TD.1' : 'Receiving TD',
					'Lng.1' : 'Receiving Lng',
					'Y/G.1' : 'Receiving Y/G',
					'A/G' : 'Rush A/G',
					'Y/R' : 'Receiving Y/R'
					}
	df = df.rename(rename_dict, axis = 1)
	return df

def merge_stats_cols(dfa, dfb):
	to_drop = ['No.', 'Age', 'Pos', 'Rush Lng', 
				'Rush Y/A', 'Rush Y/G', 'Rush A/G', 
				'Receiving Y/R', 'Receiving Lng', 'R/G', 
				'Receiving Y/G', 'Fmb', 'Y/Tch', 'YScm', 'RRTD',
				'Ctch%']
	df1 = dfa.copy()
	df2 = dfb.copy()
	df1 = df1.drop(to_drop, axis = 1)
	df2 = df2.drop(to_drop, axis = 1)
	merged = df1.merge(df2, on = 'Player', how = 'outer', suffixes = (' 2017', ' 2018'))
	merged = merged.fillna(0)
	for i in range(1, 11):
		merged[merged.columns[i][0 : -5]] = merged[merged.columns[i]] + merged[merged.columns[i + 10]]
	cols_to_keep = [c for c in merged.columns if c[-4:] != '2017' and c[-4:] != '2018']
	merged = merged[cols_to_keep]
	merged['Catch Percentage'] = merged['Rec'] / merged['Tgt']
	return merged




