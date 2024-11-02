
import argparse
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.patches import Path
import seaborn as sns
#import scienceplots
import itertools
from matplotlib.colors import ListedColormap
import matplotlib.lines as mlines
from scipy.stats import gmean

#default plot parameters, user can overwrite them
plot_parameters = { 'ylabel': 'unset', 'xlabel': 'unset', 'fontsize': 11, 
					'legend_cols': 2, 'legend_yoffset': 0.5, 'legend_xoffset': 1.1,
					'alpha': 1.0 }

def load_df(input_data_files, input_tags, cache_type, op_type, sort = False, sorted_index = None):
		# create data dataframe
		df = pd.DataFrame()
		i = 0
		for input_file in input_data_files:
				tag = input_tags[i] #.pop(0) 
				new_df = pd.read_csv(input_file, sep=',', index_col='benchmarks')
				print(input_file + " size is " + str(len(new_df)))
				if (isinstance(cache_type, list)):
					new_df = new_df.loc[(new_df['CACHE'].isin(cache_type)) & (new_df['OP'] == op_type)]
				else:
					new_df = new_df.loc[(new_df['CACHE'] == cache_type) & (new_df['OP'] == op_type)]
				#new_df = new_df.add_suffix('_' + tag)
				# drop string columns, makes calculating gmean etc easier
				#new_df.drop(new_df.iloc[:, 0:2], axis=1, inplace=True)
				#new_df = new_df.astype(float)
				new_df['conf'] = tag
				new_df['MPKI'] = (new_df['MISS'] * 1000) / new_df['INSTRUCTIONS']
				new_df['iMPKI'] = (new_df['iMISS'] * 1000) / new_df['INSTRUCTIONS']
				new_df['dMPKI'] = (new_df['dMISS'] * 1000) / new_df['INSTRUCTIONS']
				new_df['itMPKI'] = (new_df['itMISS'] * 1000) / new_df['INSTRUCTIONS']
				new_df['dtMPKI'] = (new_df['dtMISS'] * 1000) / new_df['INSTRUCTIONS']

				if df.empty:
						if (sort):
							if (sorted_index is None):
								new_df = new_df.sort_values(by=['MPKI'], ascending=False)		
								sorted_index = new_df.index.values.tolist() 
							else:
								new_df = new_df.reindex(sorted_index)
						new_df['benchmarks'] = new_df.index
						df = new_df
				else:
						if (sort):
							new_df = new_df.reindex(sorted_index)
						new_df['benchmarks'] = new_df.index
						df = pd.concat([df, new_df])

				i += 1 # that's for tags' list
		#print(df.index)
		#df.to_csv('test2.csv')
		return df


def load_df2(	input_data_files, input_tags1, input_tags2, cache_type, op_type, 
				sort = False, sorted_index = None):
		# create data dataframe
		df = pd.DataFrame()
		i = 0
		j = 0
		#print("new dataframe")
		for input_file in input_data_files:
				tag1 = input_tags1[i] #.pop(0)
				tag2 = input_tags2[j]
				new_df = pd.read_csv(input_file, sep=',', index_col='benchmarks')
				#print(input_file + " size is " + str(len(new_df)))
				if (isinstance(cache_type, list)):
					new_df = new_df.loc[(new_df['CACHE'].isin(cache_type)) & (new_df['OP'] == op_type)]
				else:
					new_df = new_df.loc[(new_df['CACHE'] == cache_type) & (new_df['OP'] == op_type)]
				#new_df = new_df.add_suffix('_' + tag)
				# drop string columns, makes calculating gmean etc easier
				#new_df.drop(new_df.iloc[:, 0:2], axis=1, inplace=True)
				#new_df = new_df.astype(float)
				#print(tag1)
				new_df['conf1'] = tag1
				#print(tag2)
				new_df['conf2'] = tag2
				new_df['MPKI'] = (new_df['MISS'] * 1000) / new_df['INSTRUCTIONS']
				new_df['iMPKI'] = (new_df['iMISS'] * 1000) / new_df['INSTRUCTIONS']
				new_df['dMPKI'] = (new_df['dMISS'] * 1000) / new_df['INSTRUCTIONS']
				new_df['itMPKI'] = (new_df['itMISS'] * 1000) / new_df['INSTRUCTIONS']
				new_df['dtMPKI'] = (new_df['dtMISS'] * 1000) / new_df['INSTRUCTIONS']
				mean = new_df['MPKI'].mean()
				#print(tag1 + "_" + tag2 + " mean:" + str(mean))

				if df.empty:
						if (sort):
							if (sorted_index is None):
								new_df = new_df.sort_values(by=['MPKI'], ascending=False)		
								sorted_index = new_df.index.values.tolist() 
							else:
								new_df = new_df.reindex(sorted_index)
						new_df['benchmarks'] = new_df.index
						df = new_df
				else:
						if (sort):
							new_df = new_df.reindex(sorted_index)
						new_df['benchmarks'] = new_df.index
						df = pd.concat([df, new_df])
			
				#print("reset_factor:" + str(reset_factor))	
				#print("i:" + str(i))	
				if (i == (len(input_tags1)- 1)):
					i = 0
					j += 1
				else: 
					i += 1 # that's for tags' list

		#print(df.index)
		#df.to_csv('test2.csv')
		return df

def load_df3(	input_data_files, input_tags1, input_tags2, cache_type, op_type, 
				sort = False, sorted_index = None):
		# create data dataframe
		df = pd.DataFrame()
		i = 0
		j = 0
		#print("new dataframe")
		for input_file in input_data_files:
				tag1 = input_tags1[i] #.pop(0)
				tag2 = input_tags2[i]
				new_df = pd.read_csv(input_file, sep=',', index_col='benchmarks')
				#print(input_file + " size is " + str(len(new_df)))
				if (isinstance(cache_type, list)):
					new_df = new_df.loc[(new_df['CACHE'].isin(cache_type)) & (new_df['OP'] == op_type)]
				else:
					new_df = new_df.loc[(new_df['CACHE'] == cache_type) & (new_df['OP'] == op_type)]
				#new_df = new_df.add_suffix('_' + tag)
				# drop string columns, makes calculating gmean etc easier
				#new_df.drop(new_df.iloc[:, 0:2], axis=1, inplace=True)
				#new_df = new_df.astype(float)
				#print(tag1)
				new_df['conf1'] = tag1
				#print(tag2)
				new_df['conf2'] = tag2
				new_df['MPKI'] = (new_df['MISS'] * 1000) / new_df['INSTRUCTIONS']
				new_df['iMPKI'] = (new_df['iMISS'] * 1000) / new_df['INSTRUCTIONS']
				new_df['dMPKI'] = (new_df['dMISS'] * 1000) / new_df['INSTRUCTIONS']
				new_df['itMPKI'] = (new_df['itMISS'] * 1000) / new_df['INSTRUCTIONS']
				new_df['dtMPKI'] = (new_df['dtMISS'] * 1000) / new_df['INSTRUCTIONS']
				mean = new_df['MPKI'].mean()
				#print(tag1 + "_" + tag2 + " mean:" + str(mean))

				if df.empty:
						if (sort):
							if (sorted_index is None):
								new_df = new_df.sort_values(by=['MPKI'], ascending=False)		
								sorted_index = new_df.index.values.tolist() 
							else:
								new_df = new_df.reindex(sorted_index)
						new_df['benchmarks'] = new_df.index
						df = new_df
				else:
						if (sort):
							new_df = new_df.reindex(sorted_index)
						new_df['benchmarks'] = new_df.index
						df = pd.concat([df, new_df])
			
				#print("reset_factor:" + str(reset_factor))	
				#print("i:" + str(i))	
				i += 1 # that's for tags' list

		#print(df.index)
		#df.to_csv('test3.csv')
		return df



def compute_variation(baseline_df, df, col_name, new_col_name, input_tags, revert=False): 
	# scale baseline_df is smaller than df
	#print(len(baseline_df.index))
	#print(len(df.index))
	if (len(df.index) > len(baseline_df.index)):
		scale_by = int(len(df.index) / len(baseline_df.index))
		baseline_orig_df = baseline_df
		#print(scale_by)
		for i in range(1, scale_by):
			baseline_df['conf1'] = input_tags[i]
			baseline_df = pd.concat([baseline_df, baseline_orig_df])
	# compue improvement
	#print(baseline_df)
	if (revert):
		df[new_col_name] = ((baseline_df[col_name] - df[col_name]) * 100 / df[col_name])
	else:
		df[new_col_name] = ((df[col_name] - baseline_df[col_name]) * 100 / baseline_df[col_name])
	#print(df[col_name])
	#print(df[new_col_name])
	#df.to_csv("test.csv")	
	return df

def compute_variation2(baseline_df, df, col_name, new_col_name, input_tags1, input_tags2): 
	# scale baseline_df is smaller than df
	print(len(baseline_df.index))
	print(len(df.index))
	if (len(df.index) > len(baseline_df.index)):
		scale_by = int(len(df.index) / len(baseline_df.index))
		baseline_orig_df = baseline_df
		print(scale_by)
		for i in range(1, scale_by):
			baseline_df['conf1'] = input_tags1[i]
			baseline_df['conf2'] = input_tags2[i]
			baseline_df = pd.concat([baseline_df, baseline_orig_df])
	# compue improvement
	#print(baseline_df)
	df[new_col_name] = ((df[col_name] - baseline_df[col_name]) * 100 / baseline_df[col_name])
	#print(df[col_name])
	#print(df[new_col_name])
	df.to_csv("test.csv")	
	return df


def compute_miss_cycles(baseline_df, df, input_tags1, input_tags2): 
	# scale baseline_df is smaller than df
	print(len(baseline_df.index))
	print(len(df.index))
	if (len(df.index) > len(baseline_df.index)):
		scale_by = int(len(df.index) / len(baseline_df.index))
		baseline_orig_df = baseline_df
		print(scale_by)
		for i in range(1, scale_by):
			baseline_df['conf1'] = input_tags1[i]
			baseline_df['conf2'] = input_tags2[i]
			baseline_df = pd.concat([baseline_df, baseline_orig_df])
	# compue improvement
	#print(baseline_df)
	df[new_col_name] = ((df[col_name] - baseline_df[col_name]) * 100 / baseline_df[col_name])
	speedup = 1.00 + (df["IPC_IMPROVEMENT"] / 100)
	print(speedup)
	df[new_col_name] = (1 - (1/speedup))
	#print(df[col_name])
	#print(df[new_col_name])
	df.to_csv("test.csv")	
	return df



def compute_stat(df, stat_name):
	if stat_name == "MPKI":
		return df
	elif stat_name == "MISS_CYCLES_":
		df['MISS_CYCLES'] = (df['MISS'] * df['AVERAGE_MISS_LATENCY'].fillna(1))
		#df['MISS_CYCLES'] = (df['HIT'] * 1) + (df['MISS'] * df['AVERAGE_MISS_LATENCY'].fillna(1))
		df['MISS_CYCLES'] = df['MISS_CYCLES'] / ( df['CYCLES'])
		df['MISS_CYCLES'] = df['MISS_CYCLES'] * 100
		#TODO: this is only valid for ITLB
		#TODO: 6 is hardcoded value for fetch width
	elif stat_name == "MISS_CYCLES":
		speedup = 1.00 + (df["IPC_IMPROVEMENT"] / 100)
		print(speedup)
		df["MISS_CYCLES"] = (1 - (1/speedup)) * 100


	return df

def filter_df(df, col, thrshld):
	return df[df[col] >= thrshld]


def sort_df(df, orig_tags, col, order):
	print(df['conf'])
	df = df.sort_values(by=['IPC_IMPROVEMENT'], ascending=order)
	print(df['conf'])
	new_df = pd.DataFrame()
	for tag in orig_tags:	
		filtered_df = df.loc[df['conf'] == tag]
		#filtered_df = filtered_df.sort_values(by=['IPC_IMPROVEMENT'], ascending=order)
		new_df = new_df.append(filtered_df, ignore_index=False)

	df = new_df
	print(df['conf'])

	#df = df.sort_values(by=['IPC_IMPROVEMENT'], ascending=order)

	#print("Sort is yet uniplemented!")
	return df

def create_plot(nrows, ncols, plot_width, plot_height, plot_extra_height):

		fig, axes = plt.subplots(	nrows=nrows, ncols=ncols, 
									figsize=(plot_width, plot_height+plot_extra_height),
									gridspec_kw={	'width_ratios': [plot_width-2, 2], 
													'height_ratios': [plot_extra_height, plot_height]})

		if (plot_extra_height > 0):
			axes[0][0].remove()
			axes[0][1].remove()

		return fig, axes


def plot(data, x, y, hue, axes, plot_type, plot_params, show_xlabel = False, show_xticks = False, show_legend = False,
					switch_yaxis = False):
	## find_plot ##
	#sns.set_style("dark")
	if (plot_type == 'histogram'):
		ax = sns.histplot(	data=data, xz=x, y=y, hue=hue, linestyles='', 
							kde=True, ax=axes)
	elif (plot_type == 'violin'):
		ax = sns.violinplot(data=data, y=y, x=hue, linewidth=1, scale='count', ax=axes, color='#aeaeae')
		i = 0
		while (i < len(ax.collections)):
			if (i % 2 == 0):
				ax.collections[i].set_edgecolor('black')
			else:
				ax.collections[i].set_edgecolor('black')
				ax.collections[i].set_linewidth(4)
			i = i + 1
		#ax = sns.swarmplot(data=data, y=y, x=hue, size=1.5, legend=False, ax=axes, color='black')
	elif (plot_type == 'boxplot'):
		PROPS = {
			'boxprops':{'facecolor':'#aeaeae', 'edgecolor':'black'},
			'medianprops':{'color':'black'},
			'whiskerprops':{'color':'black'},
			'capprops':{'color':'black'}
		}
		ax = sns.boxplot(data=data, y=y, x=hue, linewidth=1, showfliers=False, ax=axes, color='#aeaeae', **PROPS)
	elif (plot_type == 'swarmplot'):
		ax = sns.swarmplot(data=data, y=y, x=hue, size=1.5, legend=False, ax=axes, color='#aeaeae')

	elif (plot_type == 'barplot'):
		ax = sns.barplot(	data=data, x=x, y=y, hue=hue, width=0.8,
							linewidth=1, edgecolor='black', ax=axes)
	else:
		#marker_styles = ['o', 'x', '1', '+', '*', 'v', '<', '>', 'D', '.', '1']
		#marker_styles = ['o', 'x', '+', '*']
		marker_styles = ['s', 'v', 'o', '^', 'P', 'X']
		#marker_styles = ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']
		#marker_styles = ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
		ax = sns.scatterplot( data=data, x=x, y=y, hue=hue, style=hue, 
							markers=marker_styles, edgecolor='black', alpha=plot_params['alpha'], ax=axes)
		#ax = sns.pointplot( data=data, x=x, y=y, hue=hue, linestyles='', 
		#					scale=0.5, ax=axes)
					
	#ax.legend(loc='best', ncol=1, bbox_to_anchor=(0,0), frameon=False)
	if (show_legend):
		ax.legend(	loc='center', ncol=plot_params['legend_cols'], 
					bbox_to_anchor=(plot_params['legend_yoffset'], plot_params['legend_xoffset']), frameon=False)
	else:
		if (ax.get_legend() != None):
			ax.get_legend().remove()
	#ax.legend(loc='lower left', frameon=False)
	#ax.tick_params(axis="y", pad=2)
	fontsize=plot_params['fontsize']
	ax.set_ylabel(plot_params['ylabel'], fontsize=fontsize)
	ax.set_xlabel(plot_params['xlabel'], fontsize=fontsize)

	if switch_yaxis:
		ax.yaxis.set_label_position("right")
		ax.yaxis.tick_right()
	if plot_type != 'violin' and plot_type != 'barplot':
		ax.set_xticks([])
	plt.yticks(fontsize=fontsize)
	plt.xticks(fontsize=fontsize)

	ax.set_axisbelow(True)
	ax.grid(visible=True, axis='y', color='grey', alpha=0.5, linestyle='--', linewidth=1.5)

	return ax


def plot_mean_barplot(data, x, y, hue, axes, show_xlabel = False, show_legend = False):

		#ax.set_yscale('symlog')
	#ax.set_xticks([])
	#ax.set_xlabel(plot_conf['xlabel'])
	#ax.set_ylabel('IPC improvement (%)')
	ax = sns.barplot(data=data, x=x, y=y, hue=hue, ax=axes)

	ax.set_axisbelow(True)
	ax.grid(visible=True, color='grey', alpha=0.5, which='major', linestyle='--', linewidth=1.5)


	if (show_legend):
		ax.legend(loc='upper center', ncol=4, bbox_to_anchor=(-2.2,1.17))
	else:
		ax.get_legend().remove()

	if (show_xlabel):
		ax.set_xlabel('')
	else:
		ax.set_xlabel('geomean')

	ax.set_xticks([])
	ax.set_ylabel('')

	return ax


def plot_single_stat(	input_baseline_files, input_data_files, input_tags, cache_type,
											op_type, stat_name, plot_conf, output_file):

		baseline_df = load_df(input_baseline_files, input_tags, cache_type, op_type, False)
		df = load_df(input_data_files, input_tags, cache_type, op_type, False)
		df = compute_variation(baseline_df, df, 'IPC', 'IPC_IMPROVEMENT', input_tags)

		df.to_csv('data.csv')

		print(df.head(10).loc[:, stat_name])	

		#fig, axes = create_plot(2, 2, plot_conf['plot_width'], plot_conf['plot_height'], 0)
		plot_width = plot_conf['plot_width']
		plot_height = plot_conf['plot_height']
		fig, axes = plt.subplots(	nrows=1, ncols=1, 
									figsize=(plot_width, plot_height))

		# compute means
		means = []
		for conf in input_tags:
				mean = gmean(abs(df.loc[(df['conf'] == conf)][stat_name]))
				mean = df.loc[(df['conf'] == conf)][stat_name].median()
				means.append(mean)
		
		means_df = pd.DataFrame({'benchmarks':'geomean', 'conf':input_tags, 'geomean':means})
		#means_df = means_df.loc[(means_df['conf'] != input_tags[0])]
		print(means_df)

		sns.set_style("white")
		axes.set_xticklabels(	axes.get_xticklabels(), rotation=plot_conf['rotation'], 
													horizontalalignment='right')

		plot_parameters['xlabel'] = ''
		plot_parameters['ylabel'] = stat_name
		plot_parameters['fontsize'] = plot_conf['fontsize']
		ax = plot(df, 'benchmarks',stat_name, 'conf', axes, 
							plot_conf['plot_type'], plot_parameters)

		#plt.yticks(range(-10, 20))
		#ax.set_ylim([0, 30])
		#ax.set_xticklabels(ax.get_xticklabels(), minor=True)
		#vertical line for our stuff
		if plot_conf['add_seperator']:
			plt.axvline(x=4.5, ymin=0, ymax=1, color='black', axes=axes)

		fig.savefig(output_file, dpi=220, bbox_inches='tight')



def plot_ipc_improvement_single(	input_baseline_files, input_data_files, input_tags, cache_type,
									op_type, plot_conf, output_file):

		baseline_df = load_df(input_baseline_files, input_tags, cache_type, op_type, False)
		df = load_df(input_data_files, input_tags, cache_type, op_type, False)
		df = compute_variation(baseline_df, df, 'IPC', 'IPC_IMPROVEMENT', input_tags)

		#fig, axes = create_plot(2, 2, plot_conf['plot_width'], plot_conf['plot_height'], 0)
		plot_width = plot_conf['plot_width']
		plot_height = plot_conf['plot_height']
		fig, axes = plt.subplots(	nrows=1, ncols=1, 
									figsize=(plot_width, plot_height))

		df.to_csv("data.csv")


		print(df.head(100))
		print(df['IPC'])
		#matplotlib.rc('axes', edgecolor='black')
		# compute means
		means = []
		for conf in input_tags:
				mean = gmean(abs(df.loc[(df['conf'] == conf)]['IPC_IMPROVEMENT']))
				mean = df.loc[(df['conf'] == conf)]['IPC_IMPROVEMENT'].median()
				means.append(mean)
		
		means_df = pd.DataFrame({'benchmarks':'geomean', 'conf':input_tags, 'geomean':means})
		#means_df = means_df.loc[(means_df['conf'] != input_tags[0])]
		print(means_df)

		sns.set_style("white")
		axes.set_xticklabels(	axes.get_xticklabels(), rotation=plot_conf['rotation'], 
													horizontalalignment='right')

		plot_parameters['xlabel'] = ''
		plot_parameters['ylabel'] = 'IPC improvement (%)'
		plot_parameters['fontsize'] = plot_conf['fontsize']
		ax = plot(df, 'benchmarks','IPC_IMPROVEMENT', 'conf', axes, 
							plot_conf['plot_type'], plot_parameters)

		#plt.yticks(range(-10, 20))
		#ax.set_ylim([0, 30])
		#ax.set_xticklabels(ax.get_xticklabels(), minor=True)
		#vertical line for our stuff
		if plot_conf['add_seperator']:
			plt.axvline(x=4.5, ymin=0, ymax=1, color='black', axes=axes)

		fig.savefig(output_file, dpi=220, bbox_inches='tight')


def plot_stat_w_mean(	input_data_file, stat_name, page_type, 
												cache_type, op_type, plot_conf, output_file):

		df = pd.read_csv(input_data_file, sep=',', index_col='benchmarks')

		df = df.loc[df['type'] == page_type]

		_min = df[stat_name].min()
		_max = df[stat_name].max()
		print(stat_name + "_min:" + str(_min))
		print(stat_name + "_max:" + str(_max))
		#means_df = pd.DataFrame({'benchmarks':'average', 'average':mean}, index=[1])
		#print(means_df)

		#fig, axes = create_plot(2, 2, plot_conf['plot_width'], plot_conf['plot_height'], 0)
		plot_width = plot_conf['plot_width']
		plot_height = plot_conf['plot_height']
		fig, axes = plt.subplots(	nrows=1, ncols=2, 
									figsize=(plot_width, plot_height+.1),
									gridspec_kw={	'width_ratios': [plot_width-2, 2], 
													'height_ratios': [plot_height]})

		#sns.set_palette(sns.color_palette(['#929292', '#424242']))
		sns.set_palette(sns.color_palette(['#999999', '#777777', '#555555', '#333333']))
		#sns.set_palette(sns.color_palette(['cyan', 'blue', "green", "orange", "magenta", "red"]))
		#sns.color_palette("tab10")
		plot_parameters['xlabel'] = plot_conf['xlabel']
		plot_parameters['ylabel'] = 'IPC Improvment (%)'
		plot_parameters['legend_cols'] = 4
		plot_parameters['legend_xoffset'] = 1.2
		plot_parameters['legend_yoffset'] = 0.8

		#ax = df.plot.bar(	x='total_unique_pages', y=stat_name)
	
		#ax.set_ylabel(plot_conf['ylabel'])
		#ax.set_xlabel(plot_conf['xlabel'])

		#ax.set_axisbelow(True)
		#ax.grid(visible=True, axis='y', color='grey', alpha=0.5, linestyle='--', linewidth=1.5)




		#plot_parameters['xlabel'] = 'average'
		#lot_parameters['ylabel'] = ''
		#ax = means_df.plot.bar( x='benchmakrs', y='average', axes=axes[1])
		
		#ax.set_ylim([-3, 5])
		#ax.collections[0].set_sizes([15])
		#ax.set_yticks([-2.5, 0, 2.5, 5])
		#ax.set_ylim([-3, 5])
		#ax.set_ylim([means_df['geomean'].min()-0.5, means_df['geomean'].max()+1])
		#plt.subplots_adjust(wspace=0.25,hspace=0.001)

		#fig.savefig(output_file, bbox_inches='tight')
		#matplotlib.pyplot.close()


def plot_ipc_improvement_w_means(	input_baseline_files, input_data_files, input_tags, cache_type,
									op_type, plot_conf, output_file):

		baseline_df = load_df(input_baseline_files, input_tags, cache_type, op_type)
		df = load_df(input_data_files, input_tags, cache_type, op_type)
		df = compute_variation(baseline_df, df, 'IPC', 'IPC_IMPROVEMENT', input_tags)
		#df = filter_df(df, 'MPKI', 1.0)
		#df.to_csv('test.csv')

		df = sort_df(df, input_tags, 'IPC_IMPROVEMENT', False)
		#df = df.sort_values(by=['IPC_IMPROVEMENT'], ascending=False)	


		# compute means
		means = []
		for conf in input_tags:
				mean = df.loc[(df['conf'] == conf)]['IPC_IMPROVEMENT'].mean()
				#print(mean)
				means.append(mean)
		
		means_df = pd.DataFrame({'benchmarks':'geomean', 'conf':input_tags, 'geomean':means})
		print(means_df)

		#fig, axes = create_plot(2, 2, plot_conf['plot_width'], plot_conf['plot_height'], 0)
		plot_width = plot_conf['plot_width']
		plot_height = plot_conf['plot_height']
		fig, axes = plt.subplots(	nrows=1, ncols=2, 
									figsize=(plot_width, plot_height+.1),
									gridspec_kw={	'width_ratios': [plot_width-2, 2], 
													'height_ratios': [plot_height]})

		#sns.set_palette(sns.color_palette(['#929292', '#424242']))
		sns.set_palette(sns.color_palette(['#999999', '#777777', '#555555', '#333333']))
		#sns.set_palette(sns.color_palette(['cyan', 'blue', "green", "orange", "magenta", "red"]))
		#sns.color_palette("tab10")
		plot_parameters['xlabel'] = plot_conf['xlabel']
		plot_parameters['ylabel'] = 'IPC Improvment (%)'
		plot_parameters['legend_cols'] = 4
		plot_parameters['legend_xoffset'] = 1.2
		plot_parameters['legend_yoffset'] = 0.8
		ax = plot(df, 'benchmarks','IPC_IMPROVEMENT', 'conf', axes[0], plot_conf['plot_type'], 
							plot_parameters, show_legend=True)


		ax.collections[0].set_sizes([15])
		ax.set_yticks([-2.5, 0, 2.5, 5])
		ax.set_ylim([-3, 5])

		# Get the legend handles
		handles, labels = ax.get_legend_handles_labels()

		# Iterate through the handles and call `set_edgecolor` on each
		for ha in handles:
			ha.set_edgecolor("black")
			
		ax.legend(	handles, labels, loc='center', ncol=plot_parameters['legend_cols'], 
					bbox_to_anchor=(plot_parameters['legend_yoffset'], plot_parameters['legend_xoffset']), frameon=False)

		#plt.yticks(np.arange(means_df['geomean'].min(), means_df['geomean'].max()+1, 1.0))
		plot_parameters['xlabel'] = 'Geomean'
		plot_parameters['ylabel'] = ''
		ax = plot(means_df, 'benchmarks','geomean', 'conf', axes[1], 'barplot', 
							plot_parameters)
		
		#ax.set_ylim([-3, 5])
		#ax.collections[0].set_sizes([15])
		ax.set_yticks([-2.5, 0, 2.5, 5])
		ax.set_ylim([-3, 5])
		#ax.set_ylim([means_df['geomean'].min()-0.5, means_df['geomean'].max()+1])
		plt.subplots_adjust(wspace=0.25,hspace=0.001)

		fig.savefig(output_file, bbox_inches='tight')
		#matplotlib.pyplot.close()


def plot_latency_w_means(	input_data_files, input_tags, cache_type,
							op_type, plot_conf, output_file):

		df = load_df(input_data_files, input_tags, cache_type, op_type)
		#df = df.sort_values(by=['IPC_IMPROVEMENT'], ascending=False)		
		df.to_csv('test.csv')
		# compute means
		imiss_latency_means = []
		dmiss_latency_means = []
		for conf in input_tags:
				imiss_latency_mean = df.loc[(df['conf'] == conf)]['AVERAGE_iMISS_LATENCY'].mean()
				dmiss_latency_mean = df.loc[(df['conf'] == conf)]['AVERAGE_dMISS_LATENCY'].mean()
				#print(mean)
				imiss_latency_means.append(imiss_latency_mean)
				dmiss_latency_means.append(dmiss_latency_mean)
		
		means_df = pd.DataFrame({'benchmarks':'mean', 'AVERAGE_iMISS_LATENCY': imiss_latency_means, 'AVERAGE_dMISS_LATENCY': dmiss_latency_means})
		means_dfm = means_df.melt('benchmarks', var_name='cols', value_name='vals')

		df['benchmarks'] = df.index
		df = df[['benchmarks', 'AVERAGE_iMISS_LATENCY', 'AVERAGE_dMISS_LATENCY']]
		dfm = df.melt('benchmarks', var_name='cols', value_name='vals')
		# plots
		fig, axes = plt.subplots(		nrows=1, ncols=2, figsize=(6, 2),
																gridspec_kw={'width_ratios': [4, 2], 'height_ratios': [2]})

		plot_type = plot_conf['plot_type']
		sns.set_palette(sns.color_palette(['#929292', '#424242']))

		#sns.set_style("dark")
		sns.set_style("white")

		marker_styles = ['o', 'x', '^', '+', '*', '8', 's', 'p', 'd', 'v']
		ax = sns.pointplot( data=dfm, x='benchmarks', y='vals', hue='cols', linestyles='', 
														markers=marker_styles, scale=0.6, ax=axes[0])

		ax.legend(loc='upper center', ncol=6, frameon=False, bbox_to_anchor=(0.5,1.2))
		ax.set_ylabel('MPKI increase (%)')
		ax.set_xlabel(plot_conf['xlabel'])
		ax.set_xticks([])


		ax.set_axisbelow(True)
		ax.grid(visible=True, color='grey', alpha=0.5, which='major', linestyle='--', linewidth=1.5)
		#ax.set_yscale('symlog')
		#ax.set_xticks([])
		#ax.set_xlabel(plot_conf['xlabel'])
		#ax.set_ylabel('IPC improvement (%)')
		print(means_dfm)
		ax = sns.barplot(data=means_dfm, x='benchmarks', y='vals', hue='cols', ax=axes[1])

		ax.set_axisbelow(True)
		ax.grid(visible=True, color='grey', alpha=0.5, which='major', linestyle='--', linewidth=1.5)

		if (plot_type == 'violin'):
				ax.legend(loc='upper center', ncol=6, bbox_to_anchor=(-3.5,1.17))
		else:
				ax.get_legend().remove()

		ax.set_xticks([])
		ax.set_xlabel('mean')
		#ax.set_ylabel('IPC improvement (%)')
		ax.set_ylabel('')
		#ax.set_title(plot_conf['xlabel'])
		#plt.text(-1.5, -0.1, plot_conf['xlabel'], ha='center', va='center', transform=plt.gca().transAxes)

		fig.savefig(output_file)
		matplotlib.pyplot.close()


def plot_average_multiple_caches(	input_baseline_files, input_data_files, input_tags, cache_types, 
																	op_type, stat_name, plot_conf, output_file):

		baseline_df = load_df(input_baseline_files, input_tags, cache_types, op_type, False)
		df = load_df(input_data_files, input_tags, cache_types, op_type, False)
 
		#df = compute_variation(baseline_df, df, 'MPKI', 'MPKI_REDUCTION')
		# compute means
		means = []
		caches = []
		confs = []
		for cache in cache_types:
			for conf in input_tags:
				mean = gmean(df.loc[(df['conf'] == conf) & (df['CACHE'] == cache)][stat_name])
				means.append(mean)
				caches.append(cache)
				confs.append(conf)
		

		means_df = pd.DataFrame({'benchmarks':'geomean', 'cache':caches, 'conf': confs, 'geomean':means})
		print(means_df)

		#fig, axes = create_plot(2, 2, plot_conf['plot_width'], plot_conf['plot_height'], 0)
		plot_width = plot_conf['plot_width']
		plot_height = plot_conf['plot_height']
		fig, axes = plt.subplots(	nrows=2, ncols=4, 
									figsize=(plot_width, plot_height+2),
									gridspec_kw={	'width_ratios': [plot_width/4, plot_width/4, plot_width/4, plot_width/4], 
													'height_ratios': [2, plot_height]})

		axes[0][0].remove()
		axes[0][1].remove()
		axes[0][2].remove()
		axes[0][3].remove()

		sns.set_style('white')
		#sns.set_palette('Greys')
		#sns.set_context("paper")
		i = 0
#		plt.yticks(fontsize=5)
		plt.xticks(fontsize=5)

		for cache in cache_types:
			plot_parameters['xlabel'] = cache
			plot_parameters['ylabel'] = plot_conf['ylabel']
			#plot(	means_df.loc[means_df['cache'] == cache], 'cache', 'geomean', 'conf', axes[i], plot_conf['plot_type'], 
			#		plot_parameters)
			ax = sns.barplot(	data=means_df.loc[means_df['cache'] == cache],
								x='cache', y='geomean', hue='conf', width=0.8, color='grey',
								linewidth=.5, edgecolor='black', ax=axes[1][i])
			#ax.legend(loc='best', ncol=1, bbox_to_anchor=(0,0), frameon=False)

			#hatches = itertools.cycle(['/', '//', '+', '-', 'x', '\\', '*', 'o', 'O', '.'])
			for j, bar in enumerate(ax.patches):
				if (j == 10):
					bar.set_hatch('////')
				elif j == 9:
					bar.set_hatch('...')
				elif j == 8:
					bar.set_hatch('xxx')
				elif j == 7:
					bar.set_hatch('OO')
				elif j == 6:
					bar.set_hatch('\\\\\\')
			#	hatch = next(hatches)
	
			if (i == 0):
				ax.set_ylabel(plot_conf['ylabel'])
				#ax.legend(loc='center', frameon=False)
				ax.legend(loc='center', ncol=3, frameon=False, bbox_to_anchor=(1.6, 1.3))
			else:
				ax.set_ylabel('')
				ax.get_legend().remove()

			if (cache == "cpu0_L1D"):
				ax.set_xlabel("L1D")
			elif (cache == "cpu0_L2C"):
				ax.set_xlabel("L2C")
			elif (cache == "cpu0_DTLB"):
				ax.set_xlabel("DTLB")
			elif (cache == "cpu0_STLB"):
				ax.set_xlabel("STLB")
			else:
				ax.set_xlabel("LLC")

			ax.set_xticks([])
			ax.tick_params(axis='y', labelsize=11, pad=-3)
			#ax.set_ylabel('ylabel', fontsize=5)


			ax.set_axisbelow(True)
			ax.grid(visible=True, axis='y', color='grey', alpha=0.5, linestyle='--', linewidth=1.5)
			sns.despine(top=True, left=False)

			i += 1		

		fig.savefig(output_file, bbox_inches='tight')
		matplotlib.pyplot.close()


def plot_average_multiple_caches_single_fig(	input_st_data_files, input_smt_data_files, input_tags, 
																							cache_types, op_type, stat_name, plot_conf, output_file):

		#fig, axes = create_plot(2, 2, plot_conf['plot_width'], plot_conf['plot_height'], 0)
		plot_width = plot_conf['plot_width']
		plot_height = plot_conf['plot_height']
		fig, axes = plt.subplots(	nrows=3, ncols=7, 
									figsize=(plot_width+1, plot_height+2),
									gridspec_kw={	'width_ratios':	[	plot_width/8, plot_width/8, plot_width/8, 
																		0.5, # some extra space for seperation 
																		plot_width/8, plot_width/8, plot_width/8],
																'height_ratios': [1, plot_height, 1]})
		#fig.subplots_adjust(bottom=0.5)
		for i in range(0, 7):
			axes[0][i].remove()
			axes[2][i].remove()

		axes[1][3].remove()

		sns.set_style('white')
#		plt.yticks(fontsize=5)
#		plt.xticks(fontsize=5)

		fig_num = 0
		for input_data_files in [input_st_data_files, input_smt_data_files]:
			# load data
			df = load_df(input_data_files, input_tags, cache_types, op_type, False)
			# compute means
			means = []
			caches = []
			confs = []
			for cache in cache_types:
				for conf in input_tags:
					mean = gmean(df.loc[(df['conf'] == conf) & (df['CACHE'] == cache)][stat_name])
					means.append(mean)
					caches.append(cache)
					confs.append(conf)
		

			means_df = pd.DataFrame({'benchmarks':'geomean', 'cache':caches, 'conf': confs, 'geomean':means})
			print(means_df)

			i = 0
			for cache in cache_types:
				plot_parameters['xlabel'] = cache
				plot_parameters['ylabel'] = plot_conf['ylabel']
				ax = sns.barplot(	data=means_df.loc[means_df['cache'] == cache],
													x='cache', y='geomean', hue='conf', width=0.8, color='grey',
													linewidth=.5, edgecolor='black', ax=axes[1][i + fig_num])

				#hatches = itertools.cycle(['/', '//', '+', '-', 'x', '\\', '*', 'o', 'O', '.'])
				for j, bar in enumerate(ax.patches):
					if (j == 9):
						bar.set_hatch('////')
					elif j == 10:
						bar.set_hatch('...')
					elif j == 8:
						bar.set_hatch('xxx')
					elif j == 7:
						bar.set_hatch('OO')
					elif j == 6:
						bar.set_hatch('\\\\\\')
				#	hatch = next(hatches)

				fontsize = plot_conf['fontsize']
				if i == 0:
					#print('setting label -> ' + plot_conf['ylabel'])
					ax.set_ylabel(plot_conf['ylabel'], fontsize=fontsize)
				else:
					ax.set_ylabel('')

				#ax.yaxis.set_label_coords(-.3, .35)
	
				if (i + fig_num) == 0 and plot_conf['show_legend']:
					ax.legend(loc='center', ncol=11, frameon=False, bbox_to_anchor=(3.5, 1.1))
				else:
					ax.get_legend().remove()

				if (cache == "cpu0_L1D"):
					ax.set_xlabel("L1D", fontsize=fontsize)
				elif (cache == "cpu0_L2C"):
					ax.set_xlabel("L2C", fontsize=fontsize)
				elif (cache == "cpu0_STLB"):
					ax.set_xlabel("STLB", fontsize=fontsize)
				else:
					ax.set_xlabel("LLC", fontsize=fontsize)

				ax.set_xticks([])
				#ax.tick_params(axis='y', labelsize=fontsize, pad=-1)
#				plt.yticks(fontsize=fontsize+4)
				plt.xticks(fontsize=fontsize)

				ax.set_axisbelow(True)
				ax.grid(visible=True, axis='y', color='grey', alpha=0.5, linestyle='--', linewidth=1.5)
				sns.despine(top=True, left=False)

				i += 1		
				# fisrst fig end
			fig_num += 4
		
		if plot_conf['extra_xlabels']:
			plt.text(1,-.4, 'Single Hardware Thread', transform=axes[1][0].transAxes, fontsize=fontsize)	
			plt.text(1, -.4, 'Two Hardware Threads', transform=axes[1][4].transAxes, fontsize=fontsize)	

		fig.savefig(output_file, bbox_inches='tight')



def plot_single_column_figure(	input_baseline_files, input_data_files, input_tags, 
								cache_type, op_type, stat_name, plot_conf, output_file):

		baseline_df = load_df(input_baseline_files, input_tags, cache_type, op_type, False)
		df = load_df(input_data_files, input_tags, cache_type, op_type)
		df = compute_variation(baseline_df, df, 'IPC', 'IPC_IMPROVEMENT', input_tags)
		print(df)
		# plot		
		plot_width=plot_conf['plot_width']
		plot_height=plot_conf['plot_height']
		fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(plot_width, plot_height))

		plot_type = plot_conf['plot_type']

		sns.set_style("white")
		
		# compute means
		means = []
		for conf in input_tags:
			#mean = gmean(df.loc[(df['conf'] == conf)][stat_name])
			mean = df.loc[(df['conf'] == conf)][stat_name].mean()
			means.append(mean)
		
		means_df = pd.DataFrame({'benchmarks':'geomean', 'conf':input_tags, 'geomean':means})
		plot_parameters['ylabel'] = "IPC Improvement (%)"
		plot_parameters['xlabel'] = "Workloads"
		plot_parameters['fontsize'] = plot_conf['fontsize']
		ax = plot(	df, 'benchmarks', stat_name, 'conf', axes, plot_type, 
					plot_parameters, show_xticks=True, show_legend=True)

		ax.set_xticklabels(ax.get_xticklabels(), rotation=30, size=9, horizontalalignment='right')
		fig.savefig(output_file, bbox_inches='tight')


def plot_mpki_variation_all(input_data_files, input_tags_01, input_tags_02, 
														cache_type, op_type, plot_conf, output_file):

		input_tags = []
		for tag1 in input_tags_01:
			for tag2 in input_tags_02:
				input_tags.append(tag1 + "#" + tag2)
		
		#baseline_df = load_df(input_baseline_files, input_tags, cache_type, op_type, False)
		df = load_df(input_data_files, input_tags, cache_type, op_type, False)

		#df = compute_variation(baseline_df, df, 'iMPKI', 'iMPKI_INCREASE')
		#df = compute_variation(baseline_df, df, 'dMPKI', 'dMPKI_INCREASE')

		# compute means
		impki_means = []
		dmpki_means = []
		confs = []
		cores = []
		for conf in input_tags:
				impki_mean = df.loc[(df['conf'] == conf)]['iMPKI'].mean()
				dmpki_mean = df.loc[(df['conf'] == conf)]['dMPKI'].mean()
				#print(mean)
				_conf = conf.split('#')
				impki_means.append(impki_mean)
				dmpki_means.append(dmpki_mean)
				confs.append(_conf[0])
				cores.append(_conf[1])
		
		means_df = pd.DataFrame({'conf': confs, 'core': cores, 'iMPKI': impki_means, 'dMPKI': dmpki_means})
		means_dfm = means_df.melt(['conf', 'core'], var_name='cols', value_name='vals')
		#means_df = means_df.loc[(means_df['conf'] != input_tags[0])]
		means_dfm.set_index(['conf', 'core'], inplace=True)
		means_dfm['MPKI'] = means_dfm.groupby(level=['conf', 'core']).cumsum()
		means_dfm.reset_index(inplace=True)
		# plots
		plot_width = plot_conf['plot_width']
		plot_height = plot_conf['plot_height']
		fig, axes = plt.subplots(		nrows=1, ncols=2, figsize=(plot_width, plot_height),
																gridspec_kw={'width_ratios': [plot_width/2, plot_width/2], 'height_ratios': [plot_height]})

		sns.set_palette(sns.color_palette(['#929292', '#424242']))

		sns.set_style("white")
		print(means_df)
		print(means_dfm)

		ax = means_df.loc[means_df['core'] == "Single Hardware Thread"][['iMPKI', 'dMPKI']].plot(kind='bar', stacked=True, ax=axes[0], linewidth=0) 
		ax.set_xlabel('Single Hardware Thread', fontsize=12)
		ax.set_xticks([])
		ax.get_legend().remove()
		ax.set_ylabel('MPKI')

		for j, rect in enumerate(ax.patches):
			if (j == 0):
				height = rect.get_height()
				ax.text(rect.get_x() + rect.get_width() / 2., 2, "LRU",
								ha='center', rotation=0, color='black')
			elif (j == 1):
				height = rect.get_height()
				ax.text(rect.get_x() + rect.get_width() / 2., 1.8, "iTP",
								ha='center', rotation=0, color='black')

		ax.set_ylim([0,2])

		ax = means_df.loc[means_df['core'] == "Two Hardware Threads"][['iMPKI', 'dMPKI']].plot(kind='bar', stacked=True, ax=axes[1], linewidth=0) 
		ax.set_xlabel('Two Hardware Threads', fontsize=12)
		ax.set_xticks([])
		ax.legend(loc='center', ncol=1, frameon=False, bbox_to_anchor=(1.1,0.5))
		sns.despine(top=True, left=False)

		for j, rect in enumerate(ax.patches):
			if (j == 0):
				height = rect.get_height()
				ax.text(rect.get_x() + rect.get_width() / 2., 3.8, "LRU",
								ha='center', rotation=0, color='black')
			elif (j == 1):
				height = rect.get_height()
				ax.text(rect.get_x() + rect.get_width() / 2., 3.8, "iTP",
								ha='center', rotation=0, color='black')

		ax.set_ylim([0,4])

		fig.savefig(output_file, bbox_inches='tight')


def plot_impact_on_llc(	input_baseline_files, input_data_files, input_tags, cache_type,
												op_type, plot_conf, output_file):

		baseline_df = load_df(input_baseline_files, input_tags, cache_type, op_type, False)
		df = load_df(input_data_files, input_tags, cache_type, op_type, False)

		df = compute_variation(baseline_df, df, 'IPC', 'IPC_IMPROVEMENT', input_tags)
		df = compute_variation(baseline_df, df, 'MPKI', 'MPKI_VARIATION', input_tags)
		# compute means
		mpki_means = []
		ipc_means = []
		confs = []
		for conf in input_tags:
			mpki_mean = df.loc[(df['conf'] == conf)]['MPKI_VARIATION'].mean()
			ipc_mean = df.loc[(df['conf'] == conf)]['IPC_IMPROVEMENT'].mean()
			mpki_means.append(-mpki_mean)
			ipc_means.append(ipc_mean)
			confs.append(conf)
		
		mpki_df = pd.DataFrame({'benchmark': 'geomean', 'conf': confs, 'MPKI_VARIATION': mpki_means})
		ipc_df = pd.DataFrame({'benchmark': 'geomean', 'conf': confs, 'IPC_IMPROVEMENT': ipc_means})
		print(mpki_df)
		print(ipc_df)
		#sns.set_palette(sns.color_palette(['#929292', '#727272', '#424242']))
		sns.set_palette(sns.color_palette(['#424242', '#424242', '#424242']))
		# plots
		plot_width = plot_conf['plot_width']
		plot_height = plot_conf['plot_height']
		fig, axes = plt.subplots(		nrows=1, ncols=2, figsize=(plot_width, plot_height),
																gridspec_kw={'width_ratios': [plot_width/2, plot_width/2], 'height_ratios': [plot_height]})

		sns.set_style("white")

		ax = sns.barplot(		data=mpki_df, x='conf', y='MPKI_VARIATION', width=0.8,
												ax=axes[0], linewidth=0)
		#ax.legend(loc='upper center', ncol=2, frameon=0, bbox_to_anchor=(0.5,1.2))
		ax.set_ylabel('MPKI reduction (%)')
		ax.set_xlabel('')
		ax.set_axisbelow(True)
		ax.grid(visible=True, color='grey', alpha=0.5, which='major', linestyle='--', linewidth=1.5)

		ax = sns.barplot(		data=ipc_df, x='conf', y='IPC_IMPROVEMENT', width=0.8,
												ax=axes[1], edgecolor='k', linewidth=0)

#		ax = sns.lineplot(		data=ipc_df, x='conf', y='IPC_IMPROVEMENT',
#												ax=axes[1])


		ax.yaxis.tick_right()
		ax.yaxis.set_label_position('right')
		ax.set_ylabel('IPC improvement (%)')
		ax.set_xlabel('')
		ax.set_axisbelow(True)
		ax.grid(visible=True, color='grey', alpha=0.5, which='major', linestyle='--', linewidth=1.5)

		fig.savefig(output_file)
		matplotlib.pyplot.close()


def plot_dtmpki_variation(input_baseline_files, input_data_files, input_tags, cache_types,
													op_type, plot_conf, output_file):

		baseline_df = load_df(input_baseline_files, input_tags, cache_types, op_type, False)
		df = load_df(input_data_files, input_tags, cache_types, op_type, False)

		df = compute_variation(baseline_df, df, 'dtMPKI', 'dtMPKI_INCREASE', input_tags)

		# compute means
		dtmpki_means = []
		confs = []
		caches = []
		for conf in input_tags:
			for cache in cache_types:
				dtmpki_mean = df.loc[(df['CACHE'] == cache) & (df['conf'] == conf)]['dtMPKI_INCREASE'].mean()
				#print(mean)
				dtmpki_means.append(dtmpki_mean)
				confs.append(conf)
				if (cache == "cpu0_L1D"):
					cache = "L1D"
				elif (cache == "cpu0_L2C"):
					cache = "L2C"
				
				caches.append(cache)
		
		means_df = pd.DataFrame({'conf': confs, 'cache': caches, 'dtMPKI_INCREASE': dtmpki_means})
		#means_df = means_df.loc[(means_df['conf'] != input_tags[0])]
		df['benchmarks'] = df.index
		df = df[['benchmarks', 'CACHE', 'dtMPKI_INCREASE']]
		
		sns.set_palette(sns.color_palette(['#929292', '#424242']))
		# plots
		plot_width = plot_conf['plot_width']
		plot_height = plot_conf['plot_height']
		fig, axes = plt.subplots(		nrows=1, ncols=1, figsize=(plot_width, plot_height),
																gridspec_kw={'width_ratios': [plot_width], 'height_ratios': [plot_height]})

		sns.set_style("white")

		print(means_df)
		ax = sns.barplot(		data=means_df, x='cache', y='dtMPKI_INCREASE', hue='conf', width=0.8,
												ax=axes, edgecolor='k', linewidth=0)
		ax.legend(loc='upper center', ncol=2, frameon=0, bbox_to_anchor=(0.5,1.2))
		ax.set_ylabel('MPKI increase (%)')
		#ax.set_xticks()
		#ax.set_xlabel('')
		#ax.set_xticklabels(ax.get_xticklabels(), rotation=30, size=9, horizontalalignment='right')

		ax.set_axisbelow(True)
		ax.grid(visible=True, color='grey', alpha=0.5, which='major', linestyle='--', linewidth=1.5)

		fig.savefig(output_file)


def plot_dtmpki_variation_abs_(input_data_files, input_tags, cache_types,
													op_type, plot_conf, output_file):

		#baseline_df = load_df(input_baseline_files, input_tags, cache_types, op_type, False)
		#df = load_df(input_data_files, input_tags, cache_types, op_type, False)

		#df = compute_variation(baseline_df, df, 'dtMPKI', 'dtMPKI_INCREASE')

		sns.set_palette(sns.color_palette(['#626262','#929292','#626262','#929292']))
		# plots
		plot_width = plot_conf['plot_width']
		plot_height = plot_conf['plot_height']
		fig, axes = plt.subplots(		nrows=2, ncols=1, figsize=(plot_width, plot_height+.2),
																gridspec_kw={'width_ratios': [plot_width], 'height_ratios': [.2, plot_height]})

		axes[0].remove()
		sns.set_style("white")
		matplotlib.rcParams['axes.grid'] = True
		matplotlib.rcParams['savefig.transparent'] = True	

		#metrics = ['MPKI', 'iMPKI', 'dMPKI', 'itMPKI', 'dtMPKI']
		metrics = ['dMPKI', 'iMPKI', 'dtMPKI', 'itMPKI']
		hatch_idx = 0
		mpki_legend_handle = [None, None, None, None]
		rep_pol_legend_handle = [None, None]
		for metric in metrics: 
			df = load_df(input_data_files, input_tags, cache_types, op_type, False)
			# compute means
			mpki_means = []
			confs = []
			caches = []
			for conf in input_tags:
				for cache in cache_types:
					if (metric == 'dMPKI'):
						dmpki_mean = df.loc[(df['CACHE'] == cache) & (df['conf'] == conf)]['dMPKI'].mean()
						impki_mean = df.loc[(df['CACHE'] == cache) & (df['conf'] == conf)]['iMPKI'].mean()
						dtmpki_mean = df.loc[(df['CACHE'] == cache) & (df['conf'] == conf)]['dtMPKI'].mean()
						itmpki_mean = df.loc[(df['CACHE'] == cache) & (df['conf'] == conf)]['itMPKI'].mean()
						mpki_mean = dmpki_mean + impki_mean + dtmpki_mean + itmpki_mean
					elif (metric == 'iMPKI'):
						impki_mean = df.loc[(df['CACHE'] == cache) & (df['conf'] == conf)]['iMPKI'].mean()
						dtmpki_mean = df.loc[(df['CACHE'] == cache) & (df['conf'] == conf)]['dtMPKI'].mean()
						itmpki_mean = df.loc[(df['CACHE'] == cache) & (df['conf'] == conf)]['dtMPKI'].mean()
						#print(cache)
						#print(impki_mean)
						if cache == "cpu0_L1D":
							mpki_mean = impki_mean
						else:
							mpki_mean = impki_mean + dtmpki_mean + itmpki_mean
					elif (metric == 'dtMPKI'):
						dtmpki_mean = df.loc[(df['CACHE'] == cache) & (df['conf'] == conf)]['dtMPKI'].mean()
						itmpki_mean = df.loc[(df['CACHE'] == cache) & (df['conf'] == conf)]['itMPKI'].mean()
						mpki_mean = dtmpki_mean + itmpki_mean
					elif (metric == 'itMPKI'):
						mpki_mean = df.loc[(df['CACHE'] == cache) & (df['conf'] == conf)]['itMPKI'].mean()
					#print(mean)
					mpki_means.append(mpki_mean)
					confs.append(conf)
					if (cache == "cpu0_L1D"):
						cache = "L1D"
					elif (cache == "cpu0_L2C"):
						cache = "L2C"
				
					caches.append(cache)
		
			means_df = pd.DataFrame({'conf': confs, 'cache': caches, metric: mpki_means})
			#means_df = means_df.loc[(means_df['conf'] != input_tags[0])]
			df['benchmarks'] = df.index
			df = df[['benchmarks', 'CACHE', metric]]
			
			#print(means_df)
			ax = sns.barplot(	data=means_df, x='cache', y=metric, hue='conf', width=0.92,
												ax=axes[1], edgecolor='black', linewidth=1)
			#ax.set_yscale('symlog', linthreshy=0.01)
			## cannot set translarency or other properties of hactes, need to create custom one ###
			hatches = ['', '///', 'xx', '\\\\\\']
			#print("hatch_idx: " + str(hatch_idx*11))
			for j, bar in enumerate(ax.patches):
				# Define a custom hatch pattern
				#custom_hatch = PathPatch(Path([(0, 0), (1, 1)], [Path.MOVETO, Path.LINETO]), hatch='xx', alpha=0.5, color='gray')

				if ((j == 0) and (hatch_idx == 0)):
					rep_pol_legend_handle[0] = bar
				if ((j == 3) and (hatch_idx == 0)):
					rep_pol_legend_handle[1] = bar

				if (j == (hatch_idx*12 + 3)):
					#print(j)
					mpki_legend_handle[hatch_idx] = bar

				if (j >= 12*(hatch_idx)):
					#print("bar[" + str(j) + "] -> " + hatches[hatch_idx])
					bar.set_hatch(hatches[hatch_idx])
					#bar.set_hatch(custom_hatch)
					#bar.set_edgecolor('grey')


			for j, container in enumerate(ax.containers):
				#print(container)
				#print(len(container))
				if j == 0:
					ax.bar_label(container, labels=['         Single\n         HW Thread', '       Single\n         HW Thread', '         Single\n         HW Thread'], fontsize=9)
				if j == 2:
					ax.bar_label(container, labels=['         Two\n          HW Threads', '         Two\n        HW Theads', '         Two\n         HW Threads'], fontsize=9)


			ax.get_legend().remove()
			#ax.legend(loc='upper center', ncol=2, frameon=0, bbox_to_anchor=(0.5,1.3))
			ax.set_ylabel('MPKI (log)')
			#ax.set_xticks()
			ax.set_xlabel('')
			#ax.set_xticklabels(ax.get_xticklabels(), rotation=30, size=9, horizontalalignment='right')
			ax.set_yscale('symlog')
			ax.set_ylim([None, 400])

			ax.set_axisbelow(True)
			ax.grid(visible=True, color='grey', alpha=0.5, which='major', linestyle='--', linewidth=1.5)
			hatch_idx += 1
			
		mpki_breakdown_legend = ax.legend(handles = [mpki_legend_handle[0], mpki_legend_handle[1], mpki_legend_handle[2], mpki_legend_handle[3]], 
																				labels = ['dMPKI', 'iMPKI', 'dtMPKI', 'itMPKI'], loc='upper center', 
																				ncol=2, frameon=0, bbox_to_anchor=(0.8,1.45), title = "MPKI Breakdown")
		ax.legend(handles = [rep_pol_legend_handle[0], rep_pol_legend_handle[1]], 
								labels = ['LRU', 'KiT'], loc='upper center', 
								ncol=1, frameon=0, bbox_to_anchor=(0.2,1.45), title = "Replacement Policy")
		plt.gca().add_artist(mpki_breakdown_legend)
		mpki_breakdown_legend.legendHandles[0].set_facecolor('white')
		mpki_breakdown_legend.legendHandles[1].set_facecolor('white')
		mpki_breakdown_legend.legendHandles[2].set_facecolor('white')
		mpki_breakdown_legend.legendHandles[3].set_facecolor('white')

		fig.savefig(output_file, bbox_inches='tight')


def plot_kit_mpki_breakdown( 	input_data_files, input_tags, cache_types,
								op_type, plot_conf, output_file):

		#baseline_df = load_df(input_baseline_files, input_tags, cache_types, op_type, False)
		#df = load_df(input_data_files, input_tags, cache_types, op_type, False)

		#df = compute_variation(baseline_df, df, 'dtMPKI', 'dtMPKI_INCREASE')

		sns.set_palette(sns.color_palette(['#626262','#929292','#626262','#929292']))
		# plots
		plot_width = plot_conf['plot_width']
		plot_height = plot_conf['plot_height']
		fig, axes = plt.subplots(		nrows=2, ncols=1, figsize=(plot_width, plot_height+.2),
																gridspec_kw={'width_ratios': [plot_width], 'height_ratios': [.2, plot_height]})

		axes[0].remove()
		sns.set_style("white")
		matplotlib.rcParams['axes.grid'] = True
		matplotlib.rcParams['savefig.transparent'] = True	

		#metrics = ['MPKI', 'iMPKI', 'dMPKI', 'itMPKI', 'dtMPKI']
		metrics = ['dMPKI', 'iMPKI', 'dtMPKI', 'itMPKI']
		hatch_idx = 0
		mpki_legend_handle = [None, None, None, None]
		rep_pol_legend_handle = [None, None]
		for metric in metrics: 
			df = load_df(input_data_files, input_tags, cache_types, op_type, False)
			# compute means
			mpki_means = []
			confs = []
			caches = []
			for conf in input_tags:
				for cache in cache_types:
					if (metric == 'dMPKI'):
						dmpki_mean = df.loc[(df['CACHE'] == cache) & (df['conf'] == conf)]['dMPKI'].mean()
						impki_mean = df.loc[(df['CACHE'] == cache) & (df['conf'] == conf)]['iMPKI'].mean()
						dtmpki_mean = df.loc[(df['CACHE'] == cache) & (df['conf'] == conf)]['dtMPKI'].mean()
						itmpki_mean = df.loc[(df['CACHE'] == cache) & (df['conf'] == conf)]['itMPKI'].mean()
						mpki_mean = dmpki_mean + impki_mean + dtmpki_mean + itmpki_mean
					elif (metric == 'iMPKI'):
						impki_mean = df.loc[(df['CACHE'] == cache) & (df['conf'] == conf)]['iMPKI'].mean()
						dtmpki_mean = df.loc[(df['CACHE'] == cache) & (df['conf'] == conf)]['dtMPKI'].mean()
						itmpki_mean = df.loc[(df['CACHE'] == cache) & (df['conf'] == conf)]['dtMPKI'].mean()
						#print(cache)
						#print(impki_mean)
						if cache == "cpu0_L1D":
							mpki_mean = impki_mean
						else:
							mpki_mean = impki_mean + dtmpki_mean + itmpki_mean
					elif (metric == 'dtMPKI'):
						dtmpki_mean = df.loc[(df['CACHE'] == cache) & (df['conf'] == conf)]['dtMPKI'].mean()
						itmpki_mean = df.loc[(df['CACHE'] == cache) & (df['conf'] == conf)]['itMPKI'].mean()
						mpki_mean = dtmpki_mean + itmpki_mean
					elif (metric == 'itMPKI'):
						mpki_mean = df.loc[(df['CACHE'] == cache) & (df['conf'] == conf)]['dtMPKI'].mean()
					#print(mean)
					mpki_means.append(mpki_mean)
					confs.append(conf)
					if (cache == "cpu0_L1D"):
						cache = "L1D"
					elif (cache == "cpu0_L2C"):
						cache = "L2C"
				
					caches.append(cache)
	
			print(mpki_means)	
			means_df = pd.DataFrame({'conf': confs, 'cache': caches, metric: mpki_means})
			#means_df = means_df.loc[(means_df['conf'] != input_tags[0])]
			df['benchmarks'] = df.index
			df = df[['benchmarks', 'CACHE', metric]]
			
			print(means_df)
			ax = sns.barplot(	data=means_df, x='cache', y=metric, hue='conf', width=0.7,
												ax=axes[1], edgecolor='black', linewidth=1)
			#ax.set_yscale('symlog', linthreshy=0.01)
			## cannot set translarency or other properties of hactes, need to create custom one ###
			hatches = ['', '///', 'xx', '\\\\\\']
			#print("hatch_idx: " + str(hatch_idx*11))
			for j, bar in enumerate(ax.patches):
				# Define a custom hatch pattern
				#custom_hatch = PathPatch(Path([(0, 0), (1, 1)], [Path.MOVETO, Path.LINETO]), hatch='xx', alpha=0.5, color='gray')

				print(j)
				if ((j == 0) and (hatch_idx == 0)):
					rep_pol_legend_handle[0] = bar
				if ((j == 2) and (hatch_idx == 0)):
					rep_pol_legend_handle[1] = bar

				if (j == (hatch_idx*4 + 1)):
					#print(j)
					mpki_legend_handle[hatch_idx] = bar

				if (j >= 4*(hatch_idx)):
					print("bar[" + str(j) + "] -> " + hatches[hatch_idx])
					bar.set_hatch(hatches[hatch_idx])
					#bar.set_hatch(custom_hatch)
					#bar.set_edgecolor('grey')


#			for j, container in enumerate(ax.containers):
				#print(container)
				#print(len(container))
#				if j == 0:
#					ax.bar_label(container, labels=['         Single\n         HW Thread', '       Single\n         HW Thread', '         Single\n         HW Thread'], fontsize=9)
#				if j == 2:
#					ax.bar_label(container, labels=['         Two\n          HW Threads', '         Two\n        HW Theads', '         Two\n         HW Threads'], fontsize=9)


			ax.get_legend().remove()
			#ax.legend(loc='upper center', ncol=2, frameon=0, bbox_to_anchor=(0.5,1.3))
			ax.set_ylabel('MPKI (log)')
			#ax.set_xticks()
			ax.set_xlabel('')
			#ax.set_xticklabels(ax.get_xticklabels(), rotation=30, size=9, horizontalalignment='right')
			ax.set_yscale('symlog')
			ax.set_ylim([None, 400])

			ax.set_axisbelow(True)
			ax.grid(visible=True, color='grey', alpha=0.5, which='major', linestyle='--', linewidth=1.5)
			hatch_idx += 1
			
		mpki_breakdown_legend = ax.legend(handles = [ 	mpki_legend_handle[0], mpki_legend_handle[1],
														mpki_legend_handle[2], mpki_legend_handle[3] ], 
													labels = ['dMPKI', 'iMPKI', 'dtMPKI', 'itMPKI'], loc='upper center', 
													ncol=2, frameon=0, bbox_to_anchor=(0.75,1.5), title = "MPKI Breakdown")
		ax.legend(handles = [rep_pol_legend_handle[0], rep_pol_legend_handle[1]], 
								labels = ['LRU', 'Keep Instructions (P=0.8)'], loc='upper center', 
								ncol=1, frameon=0, bbox_to_anchor=(0.25,1.5), title = "Replacement Policy")
		plt.gca().add_artist(mpki_breakdown_legend)
		mpki_breakdown_legend.legendHandles[0].set_facecolor('white')
		mpki_breakdown_legend.legendHandles[1].set_facecolor('white')
		mpki_breakdown_legend.legendHandles[2].set_facecolor('white')
		mpki_breakdown_legend.legendHandles[3].set_facecolor('white')

		fig.savefig(output_file, bbox_inches='tight')


'''
 input_baseline_files: 	List of files to be used as baseline.  
						If more than 1, they need to pair with input_data_files
 input_data_files: List of files containing the data to plot
 input_tags: 	Tags matching the input_data_files cache_type: Which CACHE data to keep 
				(e.g. cpu0_L1D, LLC, etc)
 op_type: Which OP data to keep (e.g. ACCESS, MISS, HIT, etc)
 plot_conf: Special dictionary that keeps plot specific configurations
 output_file: Name for the output figure
'''
def plot_ipc_improvement(	input_baseline_files, input_data_files, input_tags, cache_type,
							op_type, plot_conf, output_file):

		baseline_df = load_df(input_baseline_files, input_tags, cache_type, op_type, False)
		df = load_df(input_data_files, input_tags, cache_type, op_type, False)

		df = compute_variation(baseline_df, df, 'IPC', 'IPC_IMPROVEMENT', input_tags)
 
		# compute means
		means = []
		for conf in input_tags:
				mean = df.loc[(df['conf'] == conf)]['IPC_IMPROVEMENT'].mean()
				#print(mean)
				means.append(mean)
		
		means_df = pd.DataFrame({'benchmarks':'geomean', 'conf':input_tags, 'geomean':means})


		fig, axes = create_plot(2, 2, plot_conf['plot_width'], plot_conf['plot_height'], 0.3)


		plot_parameters['xlabel'] = plot_conf['xlabel']
		plot_parameters['ylabel'] = 'IPC improvement (%)'
		plot(	df, 'benchmarks','IPC_IMPROVEMENT', 'conf', axes[1][0], plot_conf['plot_type'], 
				plot_parameters)

		plot_mean_barplot(means_df, 'benchmarks', 'geomean', 'conf', axes[1][1])

		fig.savefig(output_file)
		matplotlib.pyplot.close()


def plot_breakdown_comparison(input_data_files, input_tags, cache_type,
															op_type, stat_names, plot_conf, output_file):

		df = load_df(input_data_files, input_tags, cache_type, op_type, True)

		# plots
		plot_height = 3
		fig_height = plot_height * len(stat_names)
		height_ratios = [ 3 for x in stat_names ] 
		fig, axes = plt.subplots(		nrows=len(stat_names), ncols=2, figsize=(7, fig_height),
																gridspec_kw={'width_ratios': [5, 2], 'height_ratios': height_ratios})

		plot_type = plot_conf['plot_type']

		#sns.set_style("dark")
		sns.set_style("white")

		i = 0
		for stat_name in stat_names:

			if (len(stat_names) > 1):
				_axes = axes[i][0]
			else:
				_axes = axes[0]

			# compute means
			means = []
			for conf in input_tags:
					mean = df.loc[(df['conf'] == conf)][stat_name].mean()
					#print(mean)
					means.append(mean)
		
			means_df = pd.DataFrame({'benchmarks':'geomean', 'conf':input_tags, 'geomean':means})
			#means_df = means_df.loc[(means_df['conf'] != input_tags[0])]

			if (plot_type == 'histogram'):
					ax = sns.histplot(	data=df, xz='benchmarks', y=stat_name, hue='conf', linestyles='', 
															kde=True, ax=_axes)
					ax.set_xlabel('MPKI')


			elif (plot_type == 'violin'):
					ax = sns.violinplot(data=df, y='IPC_IMPROVEMENT', x='conf', linestyles='', ax=axes[i])
					ax.set_ylabel('MPKI')
					ax.set_xticks([])
					ax.set_xlabel('replacement policies configuration')
					#ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
					#plt.xticks(rotation=45)


			elif (plot_type == 'barplot'):
					#sns.set_style("whitegrid")
#					ax = sns.barplot(		data=df, x='benchmarks', y='dMPKI', hue='conf', width=0.8,
 #													 linewidth=0,
#														 ax=axes[0])

					ax = sns.barplot(		data=df, x='benchmarks', y=stat_name, hue='conf', width=0.8,
															linewidth=0,
															ax=_axes)
					ax.legend(loc='upper center', ncol=4, bbox_to_anchor=(0.5,1.15))
					ax.set_ylabel('MPKI')
					ax.set_xticks([])

			else:
					marker_styles = ['o', 'x', '^', '+', '*', 'v', '<', '>', 'D', '.', '1']
					ax = sns.pointplot( data=df, x='benchmarks', y=stat_name, hue='conf', linestyles='', 
															markers=marker_styles, scale=0.5, ax=_axes)
					
					if (i == 0):
						ax.legend(loc='center', ncol=8, bbox_to_anchor=(0.75,1.1))
						plt.setp(ax.get_legend().get_texts(), fontsize=8);
					else:
						ax.get_legend().remove()
					ax.set_ylabel('MPKI')
					ax.set_xticks([])


					if (i < (len(stat_names) - 1)):
						ax.set_xlabel('')
					else:
						ax.set_xlabel(plot_conf['xlabel'])


			ax.set_axisbelow(True)
			ax.grid(visible=True, color='grey', alpha=0.5, which='major', linestyle='--', linewidth=1.5)
			#ax.set_yscale('symlog')
			#ax.set_xticks([])
			#ax.set_xlabel(plot_conf['xlabel'])
			#ax.set_ylabel('IPC improvement (%)')
			if (len(stat_names) > 1):
				_axes = axes[i][1]
			else:
				_axes = axes[1]

			ax = sns.barplot(data=means_df, x='benchmarks', y='geomean', hue='conf', ax=_axes)

			ax.set_axisbelow(True)
			ax.grid(visible=True, color='grey', alpha=0.5, which='major', linestyle='--', linewidth=1.5)


			if (plot_type == 'violin'):
					ax.legend(loc='upper center', ncol=4, bbox_to_anchor=(-2.2,1.17))
			else:
					ax.get_legend().remove()

			if (i < (len(stat_names) - 1)):
					ax.set_xlabel('')
			else:
					ax.set_xlabel('geomean')

			ax.set_xticks([])
			ax.set_ylabel('')
			#ax.set_title(stat_name)
			#plt.text(-1.5, -0.1, plot_conf['xlabel'], ha='center', va='center', transform=plt.gca().transAxes)
			i += 1

		fig.savefig(output_file)
		matplotlib.pyplot.close()



def plot_policy_comparison( input_files, input_tags, cache_type, op_type, plot_conf,
														output_file):
		df = pd.DataFrame()
		i = 0
		for input_file in input_files:

				tag = input_tags[i] #.pop(0) 
				new_df = pd.read_csv(input_file, sep=',')
				new_df = new_df.loc[(new_df['CACHE'] == cache_type) & (new_df['OP'] == op_type)]
				#new_df = new_df.add_suffix('_' + tag)
				# drop string columns, makes calculating gmean etc easier
				#new_df.drop(new_df.iloc[:, 0:2], axis=1, inplace=True)
				#new_df = new_df.astype(float)
				new_df['conf'] = tag
				new_df['MPKI'] = (new_df['MISS'] * 1000) / new_df['INSTRUCTIONS']
				new_df['iMPKI'] = (new_df['iMISS'] * 1000) / new_df['INSTRUCTIONS']
				new_df['dMPKI'] = (new_df['dMISS'] * 1000) / new_df['INSTRUCTIONS']
				new_df['itMPKI'] = (new_df['itMISS'] * 1000) / new_df['INSTRUCTIONS']
				new_df['dtMPKI'] = (new_df['dtMISS'] * 1000) / new_df['INSTRUCTIONS']

				if df.empty:
						new_df['IPC_IMPROVEMENT'] = 0
						baseline_df = new_df
						df = new_df
				else:
						new_df['IPC_IMPROVEMENT'] = ((new_df['IPC'] - baseline_df['IPC']) * 100) / baseline_df['IPC']
						df = pd.concat([df, new_df])

				i += 1 # that's for tags' list

		#df.to_csv("test.csv")

		# drop baseline
		df = df.loc[(df['conf'] != input_tags[0])]

		# compute means
		means = []
		for conf in input_tags:
				mean = df.loc[(df['conf'] == conf)]['IPC_IMPROVEMENT'].mean()
				#print(mean)
				means.append(mean)
		
		means_df = pd.DataFrame({'benchmarks':'geomean', 'conf':input_tags, 'geomean':means})
		means_df = means_df.loc[(means_df['conf'] != input_tags[0])]


		# plots
		fig, axes = plt.subplots(		nrows=1, ncols=2, figsize=(18, 6),
																gridspec_kw={'width_ratios': [14, 4], 'height_ratios': [6]})

		plot_type = plot_conf['plot_type']

		#sns.set_style("dark")
		sns.set_style("white")

		if (plot_type == 'histogram'):
				ax = sns.histplot(	data=df, x='IPC_IMPROVEMENT', hue='conf', linestyles='', kde=True, 
														ax=axes[0])
				ax.set_xlabel('IPC improvement (%)')


		elif (plot_type == 'violin'):
				ax = sns.violinplot(data=df, y='IPC_IMPROVEMENT', x='conf', linestyles='', ax=axes[0])
				ax.set_ylabel('IPC improvement (%)')
				ax.set_xticks([])
				ax.set_xlabel('replacement policies configuration')
				#ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
				#plt.xticks(rotation=45)


		elif (plot_type == 'barplot'):
				ax = sns.barplot(		data=df, x='benchmarks', y='IPC_IMPROVEMENT', hue='conf', width=0.8,
														ax=axes[0])
				ax.legend(loc='upper center', ncol=4, bbox_to_anchor=(0.5,1.15))
				ax.set_ylabel('IPC improvement (%)')
				ax.set_xticks([])

		else:
				marker_styles = ['o', 'x', '^', '+', '*', '8', 's', 'p', 'd', 'v']
				ax = sns.pointplot( data=df, x='benchmarks', y='IPC_IMPROVEMENT', hue='conf', linestyles='', 
														markers=marker_styles, scale=0.6, ax=axes[0])

				ax.legend(loc='upper center', ncol=4, bbox_to_anchor=(0.5,1.15))
				ax.set_ylabel('IPC improvement (%)')
				ax.set_xticks([])


		ax.set_axisbelow(True)
		ax.grid(visible=True, color='grey', alpha=0.5, which='major', linestyle='--', linewidth=1.5)
		#ax.set_yscale('symlog')
		#ax.set_xticks([])
		#ax.set_xlabel(plot_conf['xlabel'])
		#ax.set_ylabel('IPC improvement (%)')

		ax = sns.barplot(data=means_df, x='benchmarks', y='geomean', hue='conf', ax=axes[1])

		ax.set_axisbelow(True)
		ax.grid(visible=True, color='grey', alpha=0.5, which='major', linestyle='--', linewidth=1.5)
		
		if (plot_type == 'violin'):
				ax.legend(loc='upper center', ncol=4, bbox_to_anchor=(-2.2,1.17))
		else:
				ax.get_legend().remove()

		ax.set_xticks([])
		ax.set_xlabel('geomean')
		ax.set_ylabel('IPC improvement (%)')
		ax.set_title(plot_conf['xlabel'])
		#plt.text(-1.5, -0.1, plot_conf['xlabel'], ha='center', va='center', transform=plt.gca().transAxes)

		fig.savefig(output_file)



def plot_recall_dist_hist(input_files, input_tags, output_file):

		df = pd.DataFrame()
		i = 0
		for input_file in input_files:
				tag = input_tags[i] #.pop(0) 
				new_df = pd.read_csv(input_file, sep=',')
				# compute frequency percentages
				new_df['percentage'] = (new_df['frequency'] / new_df['frequency'].sum(axis=0)) * 100
				# create bins
				bins = [ 0, 16, 32, 64, 128, 512, 1024, 2048, 4096, 8192, 16384, 32768 ]
				new_df['bins'] = pd.cut(new_df['reuse_distance'], bins)
				new_df = new_df.groupby(['bins'], axis=0).sum()
				# remove columns we don't need for plot
				new_df = new_df.drop(columns='frequency')
				new_df = new_df.drop(columns='reuse_distance')
				# add suffix
				new_df = new_df.add_suffix('_' + tag)
				# drop string columns, makes calculating gmean etc easier
				#new_df.drop(new_df.iloc[:, 0:2], axis=1, inplace=True)
				#new_df = new_df.astype(float)
				if df.empty:
						df = new_df
				else:
						df = pd.merge(df, new_df, on="bins", suffixes=('', '_' + tag))
						df = df.drop_duplicates()

				i += 1 # that's for tags' list



		df = df.transpose()
		#print(df)
		#print(df_perc)		 
		#ax = 
		# Define a custom color palette with 20 colors
		colors = ['#004c6d', '#c2c700', '#f79a00', '#be1e2d', '#5c6f7c', '#cc8e00', '#d0743c', '#6b3e26', '#848482', '#6ba4a4', '#009edb', '#008aac', '#82c6e2', '#0079c2', '#d9b43a', '#cf4a9b']
		 # Create a colormap with the custom color palette
		cmap = ListedColormap(colors)

		ax = df.plot.bar(stacked=True, figsize=(18, 8), legend=True, width=.8, cmap = cmap)

		ax.set_axisbelow(True)
		ax.grid(visible=True, color='grey', alpha=0.5, which='major', linestyle='--', linewidth=1.5)
		#		ax.get_legend().remove()
		#ax.legend(tags, loc='center left', bbox_to_anchor=(1.0, 0.5))
		#ax.set_yscale('symlog')
		ax.set_xticks([])
		ax.set_xlabel('SMT Qualcomm Workloads')
	 # ax.set_ylabel('IPC improvement (%)')

		#percentages = ax[0][0].get_yticks() * 100
		#ax[0][0].set_yticklabels(['{:.0f}%'.format(x) for x in percentages])
		#ax[0][0].plot()

		# Set the x-axis label
		#ax.set_xlabel('Bins')
		#ax.set_ylim(0, 100)
		# Set the y-axis label
		#ax.set_ylabel('Percentage')

		plt.savefig(output_file)


def plot_qualcom_vs_spec(	input_data_files, input_tags, cache_type,
													op_type, stat_name, plot_conf, output_file):

		df = load_df(input_data_files, input_tags, cache_type, op_type)

		#df = filter_df(df, 'MPKI', 1.0)
		
		#for bench in df['benchmarks']:
		#	print(bench + ".champsimtrace.xz")
		# plot settings
		plot_width = plot_conf['plot_width']
		plot_height = plot_conf['plot_height']
		fig, axes = plt.subplots(	nrows=1, ncols=2, 
									figsize=(plot_width, plot_height+.1),
									gridspec_kw={	'width_ratios': [plot_width-2, 2], 
													'height_ratios': [plot_height]})

		plot_type = plot_conf['plot_type']

		sns.set_style("white")
		sns.set_palette(sns.color_palette(['#929292', '#424242']))

		df = compute_stat(df, stat_name)	
		df_qualcomm = df.loc[(df['benchmarks'].str.contains("srv_")), ].sort_values(by=[stat_name], ascending=False)
		df_spec = df.loc[(df['benchmarks'].str.contains("srv_") == False), ].sort_values(by=[stat_name], ascending=False)
		df = pd.concat([df_qualcomm, df_spec], axis=0)

		# print some stats
		print(df_qualcomm[stat_name].max())
		print(df_qualcomm[stat_name].min())

		# compute means
		means = []
		input_tags.reverse()
		for conf in input_tags:
			mean = df.loc[(df['conf'] == conf)][stat_name].mean()
			print(conf + ":" + str(mean))
			means.append(mean)
		
		means_df = pd.DataFrame({'benchmarks':'geomean', 'conf':input_tags, 'geomean':means})
		input_tags.reverse()

		# plot point graph
		marker_styles = ['o', 'x']
		ax = sns.pointplot( data=df, x='benchmarks', y=stat_name, hue='conf', linestyles='', 
												markers=marker_styles, scale=0.6, ax=axes[0])

		ax.legend()
						
		ax.legend(loc='center', ncol=4, bbox_to_anchor=(.8,1.15), frameon=False)
		ax.set_ylabel('cycles spent\non instruction\naddress translation (%)')
		ax.set_ylabel(plot_conf['ylabel'], fontsize=11)
		ax.set_xlabel(plot_conf['xlabel'], fontsize=11)
		ax.set_xticks([])
		if plot_conf['ylim1'] != None:
			ax.set_ylim([0, plot_conf['ylim1']])

		ax.set_axisbelow(True)
		ax.grid(visible=True, color='grey', alpha=0.5, which='major', linestyle='--', linewidth=1.5)

		ax = sns.barplot(	data=means_df, x='benchmarks', y='geomean', hue='conf', width=0.8,
											linewidth=1, edgecolor='black', ax=axes[1])
		
		ax.get_legend().remove()
		ax.set_ylabel('')
		ax.set_xlabel('Mean', fontsize=11)
		ax.set_xticks([])
		if plot_conf['ylim2'] != None:
			ax.set_ylim([0, plot_conf['ylim2']])

		ax.set_axisbelow(True)
		ax.grid(visible=True, axis='y', color='grey', alpha=0.5, linestyle='--', linewidth=1.5)

		fig.savefig(output_file, bbox_inches='tight')


def plot_itp_vs_mockingjay(	input_baseline_files, input_data_files, input_tags, cache_type,
														op_type, plot_conf, output_file):

		baseline_df = load_df(input_baseline_files, input_tags, cache_type, op_type)
		df = load_df(input_data_files, input_tags, cache_type, op_type)

		df = compute_variation(baseline_df, df, 'IPC', 'IPC_IMPROVEMENT', input_tags)
		#df = filter_df(df, 'MPKI', 1.0)
		#df.to_csv('test.csv')
		#df = df.sort_values(by=['IPC_IMPROVEMENT'], ascending=False)		

		# compute means
		means = []
		means_mpki = []
		for conf in input_tags:
				mean = df.loc[(df['conf'] == conf)]['IPC_IMPROVEMENT'].mean()
				mean_mpki = df.loc[(df['conf'] == conf)]['MPKI'].mean()
				#print(mean)
				means.append(mean)
				means_mpki.append(mean_mpki)
		
		means_df = pd.DataFrame({'benchmarks':'geomean', 'conf':input_tags, 'geomean':means, 'mean_mpki': means_mpki})

		print(means_df)
		#fig, axes = create_plot(2, 2, plot_conf['plot_width'], plot_conf['plot_height'], 0)
		plot_width = plot_conf['plot_width']
		plot_height = plot_conf['plot_height']
		fig, axes = plt.subplots(	nrows=1, ncols=2, 
									figsize=(plot_width, plot_height+.1),
									gridspec_kw={	'width_ratios': [plot_width/2, plot_width/2], 
													'height_ratios': [plot_height]})

		#matplotlib.rcParams.update({'font.size': 13})

		#sns.set_style("whitegrid")
		sns.set_palette(sns.color_palette(['#929292', '#424242']))

		plot_parameters['xlabel'] = plot_conf['xlabel']
		plot_parameters['ylabel'] = 'LLC MPKI'
		ax = plot(	means_df, 'benchmarks','mean_mpki', 'conf', axes[0], 'barplot', 
								plot_parameters, show_legend=True)

		ax.legend(loc='center', ncol=2, bbox_to_anchor=(.5, 1.1), frameon=False)
		plot_parameters['xlabel'] = 'Geomean'
		plot_parameters['ylabel'] = 'IPC Improvement (%)'
		plot(	means_df, 'benchmarks','geomean', 'conf', axes[1], 'barplot', 
					plot_parameters, show_legend=False, switch_yaxis=True)

		fig.savefig(output_file)


def plot_mockingjay_vs_itp_ipc(	input_st_baseline_files, input_smt_baseline_files, 
																input_st_data_files, input_smt_data_files, 
																input_tags, cache_type, op_type, plot_conf, output_file):
		
		plot_width = plot_conf['plot_width']
		plot_height = plot_conf['plot_height']
		fig, axes = plt.subplots(	nrows=1, ncols=2, 
									figsize=(plot_width, plot_height+.1),
									gridspec_kw={	'width_ratios': [plot_width/2, plot_width/2], 
													'height_ratios': [plot_height]})

		plt.subplots_adjust(wspace=0.02, hspace=0.01)

		#sns.set_palette(sns.color_palette(['#d2d2d2', '#d2d2d2', '#929292', '#929292']))
		sns.set_style("whitegrid")

		plot_parameters['xlabel'] = ''
		plot_parameters['ylabel'] = 'IPC improvement (%)'
	
		subplot_title = ['Single Hardware Thread', 'Two Hardware Threads']
		input_baseline_files_l = [input_st_baseline_files, input_smt_baseline_files] 
		input_data_files_l = [input_st_data_files, input_smt_data_files] 
		i = 0
		for input_baseline_files, input_data_files in zip(input_baseline_files_l, input_data_files_l):
			#print(input_baseline_files)
			#print(input_data_files)
			baseline_df = load_df(input_baseline_files, input_tags, cache_type, op_type, False)
			df = load_df(input_data_files, input_tags, cache_type, op_type, False)
			#print(baseline_df)
			#print(df)
			df = compute_variation(baseline_df, df, 'IPC', 'IPC_IMPROVEMENT', input_tags)
			print(df['IPC_IMPROVEMENT'].head(50))


			ax = sns.violinplot(data=df, y='IPC_IMPROVEMENT', x='conf', linewidth=.6, scale='count', 
													color='#aeaeae', ax=axes[i])

			ax.set_axisbelow(True)
			ax.grid(visible=True, axis='y', color='grey', alpha=0.5, linestyle='--', linewidth=1.5)

			j = 0
			while (j < len(ax.collections)):
				if (j % 2 == 0):
					ax.collections[j].set_edgecolor('black')
				else:
					ax.collections[j].set_edgecolor('black')
					ax.collections[j].set_linewidth(3)
				j = j + 1

			#ax.set_xticklabels(	["Mockingjay", "$iTP\oplus{xPTP}$", "Mockingjay", "$iTP\oplus{xPTP}$"], 
			#										rotation=10, horizontalalignment='right')

			means = []
			for conf in input_tags:
				mean = df.loc[(df['conf'] == conf)]['IPC_IMPROVEMENT'].mean()
				print(conf + ":" + str(mean))
				means.append(mean)

			#means_df = pd.DataFrame({'benchmarks':'geomean', 'conf':input_tags, 'geomean':means})
			ax.set_xticklabels(	ax.get_xticklabels(), 
													rotation=15, horizontalalignment='right', fontsize=7)
			ax.set_title(subplot_title[i], fontsize=7)
			ax.set_ylabel(plot_parameters['ylabel'], fontsize=7)
			ax.set_xlabel(plot_parameters['xlabel'], fontsize=7)
			plt.xticks(fontsize=7)
			plt.yticks(fontsize=7)

			if i == 0:
				#ax.spines[['right']].set_visible(False)			
				print('')
			else:
				ax.set_ylabel('')
				ax.axes.yaxis.set_ticklabels([], fontsize=9)


			#ax = sns.swarmplot(data=df, y='IPC_IMPROVEMENT', x='conf', size=1, legend=False, ax=axes, color='k', zorder=100)
#			ax.set_ylim([-50,50])
			#ax.set_ylim([None,25])
			ax.set_ylim([-10,20])

			#square1 = mlines.Line2D([], [], color='#d2d2d2', marker='None', linestyle='None', 
			#											markeredgecolor='black', markersize=0, label='SPEC CPU 2006/17')
			#square2 = mlines.Line2D([], [], color='#929292', marker='None', linestyle='None',
			#											markeredgecolor='black', markersize=0, label='Qualcomm Server')
			#ax.legend(handles=[square1, square2], loc='center', ncol=2, bbox_to_anchor=(0.48, 1.1), 
			#					frameon=False, fontsize=9, handletextpad=-.5)

			#plt.axvline(x=1.48, ymin=0, ymax=1, color='black', axes=axes[i], linewidth=.8)
			#plt.axvline(x=1.52, ymin=0, ymax=1, color='black', axes=axes[i], linewidth=.8)
			i += 1

		fig.savefig(output_file, dpi=220, bbox_inches='tight')


def plot_mpki_breakdown(input_data_files, input_tags, cache_types, 
						op_type, plot_conf, output_file):
			
		#fig, axes = create_plot(2, 2, plot_conf['plot_width'], plot_conf['plot_height'], 0)
		plot_width = plot_conf['plot_width']
		plot_height = plot_conf['plot_height']
		fig, axes = plt.subplots(	nrows=2, ncols=3, 
									figsize=(plot_width, plot_height+2),
									gridspec_kw={	'width_ratios': [plot_width/3, plot_width/3, 
																	 plot_width/3], 
													'height_ratios': [2, plot_height]})

		axes[0][0].remove()
		axes[0][1].remove()
		axes[0][2].remove()

		#sns.set_palette(sns.color_palette(['#929292', '#424242']))
		sns.set_style("white")
		sns.set_palette(sns.color_palette(['#333333', '#555555', '#888888', '#AAAAAA']))


		i = 0
		for cache_type in cache_types:
	
			#baseline_df = load_df(input_baseline_files, input_tags, cache_type, op_type, False)
			df = load_df(input_data_files, input_tags, cache_type, op_type, False)

			#df = compute_variation(baseline_df, df, 'iMPKI', 'iMPKI_INCREASE')
			#df = compute_variation(baseline_df, df, 'dMPKI', 'dMPKI_INCREASE')
			#print(df)
			#print(df[['conf', 'iMPKI']])
			# compute means
			impki_means = []
			dmpki_means = []
			itmpki_means = []
			dtmpki_means = []
			policies = []
			types = []
			for conf in input_tags:
				impki_mean = df.loc[(df['conf'] == conf)]['iMPKI'].mean()
				dmpki_mean = df.loc[(df['conf'] == conf)]['dMPKI'].mean()
				itmpki_mean = df.loc[(df['conf'] == conf)]['itMPKI'].mean()
				dtmpki_mean = df.loc[(df['conf'] == conf)]['dtMPKI'].mean()
				#print(mean)
				#_conf = conf.split('#')
				impki_means.append(impki_mean)
				dmpki_means.append(dmpki_mean)
				itmpki_means.append(itmpki_mean)
				dtmpki_means.append(dtmpki_mean)
				policies.append(conf)
				#policies.append(_conf[0])
				#types.append(_conf[1])
		
			means_df = pd.DataFrame({'policy': policies, 'instructions': impki_means, 'data': dmpki_means, "PTE (instr.)": itmpki_mean, "PTE (data)": dtmpki_means})
			means_dfm = means_df.melt(['policy'], var_name='cols', value_name='vals')
			#means_df = means_df.loc[(means_df['conf'] != input_tags[0])]
			means_dfm.set_index(['policy'], inplace=True)
			means_dfm['MPKI'] = means_dfm.groupby(level=['policy']).cumsum()
			means_dfm.reset_index(inplace=True)

			#sns.set_palette(sns.color_palette(['#929292', '#424242']))

			sns.set_style("white")
			#print(means_df)
			print(cache_type)
			print(means_dfm)

			#ax = sns.barplot(	data=means_dfm, x='policy', y='vals', hue='cols', 
			#					linewidth=.5, edgecolor='black',ax=axes[1][i])

			ax = means_df.set_index('policy').plot(	kind = 'bar', stacked = True, 
													edgecolor='black', linewidth=0, ax=axes[1][i])

			cache_name_split = cache_type.split('_')
			if len(cache_name_split) > 1: 
				ax.set_xlabel(cache_name_split[1], fontsize=12)
			else:
				ax.set_xlabel(cache_name_split[0], fontsize=12)
				
		#ax.set_xticks([])
			if i == 0:
				ax.legend(loc='center', ncol=4, frameon=False, bbox_to_anchor=(1.6,1.1))
				ax.set_ylabel('MPKI')
			else:
				ax.get_legend().remove()
				ax.set_ylabel('')

			ax.set_xticklabels(	ax.get_xticklabels(), rotation=plot_conf['rotation'], 
								horizontalalignment='center')


			ax.set_axisbelow(True)
			ax.grid(visible=True, axis='y', color='grey', alpha=0.5, linestyle='--', linewidth=1.5)
			sns.despine(top=True, left=False)

#		ax.set_ylim([0,2])
			i += 1		
	
		fig.savefig(output_file, bbox_inches='tight')


def plot_llc_pol_comparison(input_baseline_files, input_data_files, 
							l2c_tags, llc_tags, cache_type, op_type, plot_conf, output_file):

	plot_width = plot_conf['plot_width']
	plot_height = plot_conf['plot_height']
#	fig, axes = plt.subplots(	nrows=1, ncols=2, 
#								figsize=(plot_width, plot_height+.1),
#								gridspec_kw={	'width_ratios': [plot_width/2, plot_width/2], 
#													'height_ratios': [plot_height]})
	fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(plot_width, plot_height))

	#plt.subplots_adjust(wspace=0.02, hspace=0.01)

	#sns.set_palette(sns.color_palette(['#d2d2d2', '#d2d2d2', '#929292', '#929292']))
	#sns.set_style("whitegrid")

	plot_parameters['xlabel'] = 'LLC Replacement Policies'
	plot_parameters['ylabel'] = 'IPC improvement (%)'
	
	baseline_df = load_df3(input_baseline_files, l2c_tags, llc_tags, cache_type, op_type, False)
	df = load_df3(input_data_files, l2c_tags, llc_tags, cache_type, op_type, False)

	#print(len(baseline_df.index))
	#print(len(df.index))

	df = compute_variation2(baseline_df, df, 'IPC', 'IPC_IMPROVEMENT', l2c_tags, llc_tags)
	#print(df['IPC_IMPROVEMENT'].head(50))
	#df.to_csv("test.csv")

	ax = sns.violinplot(data=df, y='IPC_IMPROVEMENT', x='conf2', hue='conf1', linewidth=1, scale='count', 
													color='#aeaeae', ax=axes)
		
	i = 0
	while (i < len(ax.collections)):
		if (i % 2 == 0):
			ax.collections[i].set_edgecolor('black')
		else:
			ax.collections[i].set_edgecolor('black')
			ax.collections[i].set_linewidth(1)
		i = i + 1

	ax.set_yticks([-10, 0, 12.5, 25])
	ax.set_ylim([-10, 25])

	ax.set_axisbelow(True)
	ax.grid(visible=True, axis='y', color='grey', alpha=0.5, linestyle='--', linewidth=1.5)

	#j = 0
	#while (j < len(ax.collections)):
	#	if (j % 2 == 0):
	#		ax.collections[j].set_edgecolor('black')
	#	else:
	#		ax.collections[j].set_edgecolor('black')
	#		ax.collections[j].set_linewidth(3)
	#	j = j + 1

	#ax.set_xticklabels(	["Mockingjay", "$iTP\oplus{xPTP}$", "Mockingjay", "$iTP\oplus{xPTP}$"], 
	#										rotation=10, horizontalalignment='right')

	means = []
	i = 0
	for conf1 in l2c_tags:
		conf2 = llc_tags[i]
		mean = df.loc[(df['conf1'] == conf1) & (df['conf2'] == conf2)]['IPC_IMPROVEMENT'].mean()
		print(conf1 + " - " + conf2 + ":" + str(mean))
		means.append(mean)
		i += 1

	ax.legend(loc='center', ncol=3, bbox_to_anchor=(.5, 1.2), frameon=False, fontsize=7)
	#means_df = pd.DataFrame({'benchmarks':'geomean', 'conf':input_tags, 'geomean':means})
	#ax.set_xticklabels(ax.get_xticklabels(), rotation=15, horizontalalignment='right', fontsize=7)
	#ax.set_title(subplot_title[i], fontsize=7)
	ax.set_ylabel(plot_parameters['ylabel'], fontsize=7)
	ax.set_xlabel(plot_parameters['xlabel'], fontsize=7)
	plt.xticks(fontsize=7)
	plt.yticks(fontsize=7)

	#if i == 0:
	#	#ax.spines[['right']].set_visible(False)			
	#	print('')
	#else:
	#	ax.set_ylabel('')
	#	ax.axes.yaxis.set_ticklabels([], fontsize=9)


	#ax.set_ylim([-10,20])

	fig.savefig(output_file, dpi=220, bbox_inches='tight')



def plot_mlt_instr_pages(	input_st_baseline_files, input_smt_baseline_files, 
							input_st_data_files, input_smt_data_files, 
							input_tags1, input_tags2,
							cache_type, op_type, plot_conf, output_file):
		
		sns.set_style("white")
		plot_width = plot_conf['plot_width']
		plot_height = plot_conf['plot_height']
		fig, axes = plt.subplots(	nrows=1, ncols=2, 
									figsize=(plot_width, plot_height+.1),
									gridspec_kw={	'width_ratios': [plot_width/2, plot_width/2], 
													'height_ratios': [plot_height]})

		plt.subplots_adjust(wspace=0.1, hspace=0.01)

		sns.set_palette(sns.color_palette(['#333333', '#555555', '#888888', 'red']))

		plot_parameters['xlabel'] = ''
		plot_parameters['ylabel'] = 'IPC improvement (%)'
	
		subplot_title = ['Single Hardware Thread', 'Two Hardware Threads']
		input_baseline_files_l = [input_st_baseline_files, input_smt_baseline_files] 
		input_data_files_l = [input_st_data_files, input_smt_data_files] 
		i = 0
		for input_baseline_files, input_data_files in zip(input_baseline_files_l, input_data_files_l):
			#print(input_baseline_files)
			#print(input_data_files)
			baseline_df = load_df2(input_baseline_files, input_tags1, input_tags2, cache_type, op_type, False)
			df = load_df2(input_data_files, input_tags1, input_tags2, cache_type, op_type, False)
			#print(baseline_df)
			#print(df)
			df = compute_variation(baseline_df, df, 'IPC', 'IPC_IMPROVEMENT', input_tags1)
			#print(df['IPC_IMPROVEMENT'].head(50))


			means = []
			confs1 = []
			confs2 = []
			for conf1 in input_tags1:
				for conf2 in input_tags2:
					mean = df.loc[(df['conf1'] == conf1) & (df['conf2'] == conf2)]['IPC_IMPROVEMENT'].mean()
					#mean = gmean((df.loc[(df['conf1'] == conf1) & (df['conf2'] == conf2)]['IPC_IMPROVEMENT']))
					#mean = gmean(abs(df.loc[(df['conf'] == conf)]['IPC_IMPROVEMENT']))
					#print(conf1 + "_" + conf2 + ":" + str(mean))
					confs1.append(conf1)
					confs2.append(conf2)
					means.append(mean)

			means_df = pd.DataFrame({'benchmarks':'geomean', 'conf1':confs1, 'conf2':confs2, 'geomean':means})

			print(means_df)
			
			#markerprops = dict(markeredgecolor='white')

			ax = sns.lineplot(	data=means_df, y='geomean', x='conf1', 
								hue="conf2", style='conf2', 
								markers=True, ax=axes[i])

			ax.set_axisbelow(True)
			ax.grid(visible=True, axis='both', color='grey', alpha=0.3, linestyle='-', linewidth=.5)

			j = 0

			plt.draw() # need this to populate xticklabels
			ax.set_xticklabels(	ax.get_xticklabels(), fontsize=7)

			ax.set_title(subplot_title[i], fontsize=7)
			ax.set_ylabel(plot_parameters['ylabel'], fontsize=7)
			#if i == 0:
			#	ax.set_xlabel('Single Hardware Thread', fontsize=7)
			#else:
			#	ax.set_xlabel('Two Hardware Threads', fontsize=7)
			ax.set_xlabel('')

			if i == 0:
				#ax.spines[['right']].set_visible(False)			
				#ax.set_ylim([-5,5])
				ax.yaxis.tick_left()
				ax.set_yticks([-10, 0, 10, 20])
				ax.set_yticklabels( [-10, 0, 10, 20], size = 7)

				ax.text(0.1, -22, 'Portion of code and data footprint allocated by 2MB pages', fontsize=7)

			else:
				ax.set_ylabel('')
				#ax.set_ylim([0,20])
				ax.yaxis.set_label_position("right")	
				ax.set_yticks([-10, 0, 10, 20])
				ax.yaxis.tick_left()
				ax.axes.yaxis.set_ticklabels([], fontsize=9)

			ax.set_ylim([-10, 20])

			#ax.set_yticklabels( ax.get_yticks().astype(int), size = 7)
					
			if (i == 0):
				handles, labels = ax.get_legend_handles_labels()
				for h in handles:
					#h.set(**markerprops)
					#h.set_markersize(5)
					h.set_markeredgecolor('white')

				ax.legend(handles, labels, handlelength=1.5, loc='center', ncol=4, bbox_to_anchor=(1,1.3), frameon=False)
				#ax.legend(loc='center', ncol=4, bbox_to_anchor=(1,1.15), frameon=False)
				plt.setp(ax.get_legend().get_texts(), fontsize=7);
				#ax.get_legend().remove()
			else:
				ax.get_legend().remove()

			i += 1



		fig.savefig(output_file, dpi=220, bbox_inches='tight')


def plot_spec_eval_manual(output_file, plot_conf):
	
		#fig, axes = create_plot(2, 2, plot_conf['plot_width'], plot_conf['plot_height'], 0)
		plot_width = plot_conf['plot_width']
		plot_height = plot_conf['plot_height']
		fig, axes = plt.subplots(	nrows=1, ncols=1, 
									figsize=(plot_width, plot_height))

	
		benchmarks = [ 
						"403.gcc", "433.milc", "462.libquantum", "482.sphinx3", "627.cam4", "450.soplex", "470.lbm",
						"403.gcc", "433.milc", "462.libquantum", "482.sphinx3", "627.cam4", "450.soplex", "470.lbm",
						"403.gcc", "433.milc", "462.libquantum", "482.sphinx3", "627.cam4", "450.soplex", "470.lbm"
					 ]

		policies =	[
						"SHiP", "SHiP", "SHiP", "SHiP", "SHiP", "SHiP", "SHiP",
						"Mockingjay-orig", "Mockingjay-orig", "Mockingjay-orig",
						"Mockingjay-orig", "Mockingjay-orig", "Mockingjay-orig", "Mockingjay-orig",
						"Mockingjay", "Mockingjay", "Mockingjay",
						"Mockingjay", "Mockingjay", "Mockingjay", "Mockingjay"
					]

		ship = [ 0.04, -2.2, -2.6, 0.2, -2.2, 0.4, -1.0 ]
		mock_new = [ 1.9, 1.7, 9.8, 31.0, 2.4 , -11.8, -0.5 ]
		mock_orig = [ 1.0, 0.5, 5.0, 24, 1.0, 10.0, 16.0 ]
	
		values = ship + mock_orig + mock_new

		df = pd.DataFrame({'benchmarks':benchmarks, 'policy':policies, 'speedup':values})
		#means_df = means_df.loc[(means_df['conf'] != input_tags[0])]
		print(df)

		sns.set_style("white")
		axes.set_xticklabels(	axes.get_xticklabels(), rotation=plot_conf['rotation'], 
													horizontalalignment='right')

		plot_parameters['xlabel'] = ''
		plot_parameters['ylabel'] = 'IPC improvement (%)'
		plot_parameters['fontsize'] = plot_conf['fontsize']
		ax = plot(df, 'benchmarks','speedup', 'policy', axes, 
							plot_conf['plot_type'], plot_parameters, show_legend=False)

		ax.legend(	loc='center', ncol=3, 
					bbox_to_anchor=(0.5, 1.05), 
					frameon=False)

		#plt.yticks(range(-10, 20))
		#ax.set_ylim([0, 30])
		#ax.set_xticklabels(ax.get_xticklabels(), minor=True)
		#vertical line for our stuff
		plt.axvline(x=4.5, ymin=0, ymax=1, color='black', axes=axes)

		fig.savefig(output_file, dpi=220, bbox_inches='tight')



def plot_itlb_sensitivity(	input_qualcomm_baseline_files, input_qualcomm_data_files, 
														input_spec_baseline_files, input_spec_data_files,
														input_tags, cache_type, op_type, stat_name, plot_conf, output_file):

		qualcomm_baseline_df = load_df(input_qualcomm_baseline_files, input_tags, cache_type, op_type)
		qualcomm_df = load_df(input_qualcomm_data_files, input_tags, cache_type, op_type)

		spec_baseline_df = load_df(input_spec_baseline_files, input_tags, cache_type, op_type)
		spec_df = load_df(input_spec_data_files, input_tags, cache_type, op_type)

		# plot settings
		plot_width = plot_conf['plot_width']
		plot_height = plot_conf['plot_height']
		fig, axes = plt.subplots(	nrows=1, ncols=2, 
									figsize=(plot_width, plot_height+.1),
									gridspec_kw={	'width_ratios': [plot_width-2, 2], 
																'height_ratios': [plot_height]})

		plt.subplots_adjust(left=0.1,
                    		bottom=0.1, 
                    		right=1, 
                    		top=0.9, 
                    		wspace=0.4, 
                    		hspace=0.4)

		plot_type = plot_conf['plot_type']

		sns.set_style("white")
		sns.set_palette(sns.color_palette(['#DDDDDD', '#CCCCCC', '#AAAAAA', '#777777', '#666666', '#555555', '#444444', '#333333']))

		qualcomm_df = compute_variation(qualcomm_baseline_df, qualcomm_df, 'IPC', 'IPC_IMPROVEMENT', input_tags, True)
		qualcomm_df = compute_stat(qualcomm_df, stat_name)	
		qualcomm_df = qualcomm_df.sort_values(by=['MISS_CYCLES'], ascending=False)# key=lambda x: x.map(custom_dict))
		
		spec_df = compute_variation(spec_baseline_df, spec_df, 'IPC', 'IPC_IMPROVEMENT', input_tags, True)
		spec_df = compute_stat(spec_df, stat_name)	
		spec_df = spec_df.sort_values(by=['MISS_CYCLES'], ascending=False)# key=lambda x: x.map(custom_dict))
		
		#df = df.sort_values(by=['conf'], ascending=True, key=lambda x: x.map(custom_dict))
		#df_qualcomm = df.loc[(df['benchmarks'].str.contains("srv_")), ].sort_values(by=[stat_name], ascending=False)
		#df_spec = df.loc[(df['benchmarks'].str.contains("srv_") == False), ].sort_values(by=[stat_name], ascending=False)
		df = pd.concat([qualcomm_df, spec_df], axis=0)

		# compute means
		input_tags.reverse()	
		means = []
		for conf in qualcomm_df['conf'].unique():
			mean = qualcomm_df.loc[(qualcomm_df['conf'] == conf)][stat_name].mean()
			print(conf + ":" + str(mean))
			means.append(mean)

		qualcomm_means_df = pd.DataFrame({'benchmarks':'geomean', 'workload': 'qualcomm', 'conf':input_tags, 'geomean':means})

		print(qualcomm_means_df)

		means = []
		for conf in spec_df['conf'].unique():
			mean = spec_df.loc[(spec_df['conf'] == conf)][stat_name].mean()
			print(conf + ":" + str(mean))
			means.append(abs(mean))
		
		spec_means_df = pd.DataFrame({'benchmarks':'geomean', 'workload': 'spec', 'conf':input_tags, 'geomean':means})

		print(spec_means_df)

		means_df = pd.concat([qualcomm_means_df, spec_means_df], axis=0)

		# plot point graph
		plot_conf['legend_yoffset'] = .8
		plot_conf['legend_xoffset'] = 1.25
		plot_conf['fontsize'] = 14
		plot_conf['alpha'] = .9
		plot_conf['xlabel'] = ''
		ax = plot(df, 'benchmarks', stat_name, 'conf', axes[0], 'point', plot_conf, False, False, True, False)
	
			
		#plt.axvline(x=180, ymin=0, ymax=1, color='black', axes=axes[0])
		#ax.vlines(100,0,20)
		ax.axvline(98, color='black', zorder=0)
			
		ax.text(25, -6, 'Qualcomm\n   Server', fontsize=plot_conf['fontsize'])
		ax.text(115, -3.25, 'SPEC', fontsize=plot_conf['fontsize'])

		# Get the legend handles
		handles, labels = ax.get_legend_handles_labels()

		# Iterate through the handles and call `set_edgecolor` on each
		for ha in handles:
			ha.set_edgecolor("black")
			
		ax.legend(handles, labels, loc='center', ncol=plot_conf['legend_cols'], bbox_to_anchor=(.8,1.25), frameon=False, fontsize=plot_conf['fontsize'])

		if plot_conf['ylim1'] != None:
			ax.set_ylim([0, plot_conf['ylim1']])

		ax.set_axisbelow(True)
		ax.grid(visible=True, color='grey', alpha=0.5, which='major', linestyle='--', linewidth=1.5)

		ax = sns.barplot(	data=means_df, x='workload', y='geomean', hue='conf', width=0.8,
											linewidth=1, edgecolor='black', ax=axes[1])
	
		ax.text(-0.9, -4.5, 'Qualcomm\n   Server', fontsize=plot_conf['fontsize'])
		ax.text(0.7, -2.5, 'SPEC', fontsize=plot_conf['fontsize'])

		ax.axvline(0.5, color='black', zorder=0)
	
		ax.get_legend().remove()
		ax.set_ylabel('')
		ax.set_xlabel('', fontsize=plot_conf['fontsize'])
		ax.set_xticks([])
		ax.set_ylabel('AVG Cycles Spent on\nInstruction Address\nTranslation (%)', fontsize=plot_conf['fontsize'])
		plt.yticks(fontsize=11)

		if plot_conf['ylim2'] != None:
			ax.set_ylim([0, plot_conf['ylim2']])

		ax.set_axisbelow(True)
		ax.grid(visible=True, axis='y', color='grey', alpha=0.5, linestyle='--', linewidth=1.5)

		fig.savefig(output_file, bbox_inches='tight')



