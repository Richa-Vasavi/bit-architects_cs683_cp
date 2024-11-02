#!/usr/bin/python3

"""
__name__ = merge_champsim_data.py 
__author__ = Dimitrios Chasapis
__description = Computes stats for page accesses
"""

import argparse	
import pandas as pd
import numpy as np
import csv
import time

### Command Line Arguments ###
parser = argparse.ArgumentParser()
parser.add_argument('--input-file', dest='input_file', required=True, default=None, help="Input CSV file.")
parser.add_argument('--output-file', dest='output_file', required=False, default="data.csv", help="Output CSV file.")

args = parser.parse_args()

input_file = args.input_file

_df = pd.read_csv(input_file, sep=',')

#print(_df.head(100))

total_unique_pages = [0, 0]
total_accesses = [0, 0]
pages_access_90 = [0, 0]
pages_access_80 = [0, 0]
page_types = ['instr', 'data']
i = 0
for page_type in page_types:

	df = _df.loc[_df['type'] == page_type]

	#print(df.head(100))

	total_accesses[i] = df['accesses'].sum()
	total_unique_pages[i] = df[df.columns[0]].count() 

	df = df.sort_values('accesses', ascending=False)

	accesses_80 = total_accesses[i] * 0.8
	accesses_90 = total_accesses[i] * 0.9
	current_accesses = 0
	index = 0
	for _accesses in df['accesses'].values:
		current_accesses += _accesses
		#print("accesses:" + str(current_accesses))
		if accesses_80 <= current_accesses and pages_access_80[i] == 0:
			pages_access_80[i] = index
		elif accesses_90 <= current_accesses:
			pages_access_90[i] = index
			break;

		index += 1

	#print("total accesses:", current_accesses)
	#print("index 80%", pages_access_80)
	#print("index 90%", pages_access_90)

	i += 1




data = { 	'total_unique_pages': total_unique_pages, 'total_accesses': total_accesses, 
					'accesses_90': pages_access_90, 'accesses_80': pages_access_80, 'type': page_types}
new_df = pd.DataFrame(data)

#print(new_df)

new_df.to_csv(args.output_file, index=False)


