import sys
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from collections import defaultdict
import math
import pandas
import csv

def main():

	file_name = sys.argv[1] #data file
	num_calls = Counter()


	# lines 18-55 are the same as num_calls.py and keys_pressed.py 

	# num_calls 
	cdr_id = {}
	with open(file_name, 'r') as dat:
		for line in dat:
			info = line.split(',')
			if(info[7] not in cdr_id):
				cdr_id[info[7]] = 1
				num_calls[info[0]] += 1



	# key_pressed
	user_durations = {}
	user_durations = defaultdict(lambda:0, user_durations)
	user_keys_pressed = Counter()

	interaction = ['dtmf_*', 'dtmf_1', 'dtmf_2', 'dtmf_3', 'dtmf_4', 'dtmf_5', 'dtmf_6', 'dtmf_9']

	with open(file_name, 'r') as dat:
		for line in dat:
			info = line.split(',')
			if not int(info[3]) == 0:
				user_durations[info[0]] += int(info[3])
				if info[4] in interaction:
					user_keys_pressed[info[0]] += 1


	
	


	all_kpm = []
	key_press_dict = {}
	key_press_dict = defaultdict(lambda:0, key_press_dict)
	for k in user_keys_pressed:
		all_kpm.append(int (-1 * np.log(float((user_keys_pressed[k]) / user_durations[k]) )))
		key_press_dict[k] =  (-1 * np.log(float((user_keys_pressed[k]) / user_durations[k]) ))
		

# not required (58-79)
	# avg_listenership
	# duration_heard = Counter()
	# item_durations = {}
	# item_durations = defaultdict(lambda:10, item_durations)

	# user_listenership = {}
	# user_listenership = defaultdict(lambda:10, user_listenership)
	# with open(file_name, 'r') as dat:
	# 	for line in dat:
	# 		info = line.split(',')
	# 		if not int(info[2]) == 0:			
	# 			if int(info[3]) >= int(info[2]):
	# 				duration_heard[info[0]] += int(info[2])
	# 				item_durations[info[0]] += int(info[2])
	# 			else:
	# 				duration_heard[info[0]] += int(info[3])
	# 				item_durations[info[0]] += int(info[2])

	# all_durations = []
	# for k in duration_heard:
	# 	all_durations.append(int( float(duration_heard[k])*100 / item_durations[k]))
	# 	user_listenership[k] = int( float(duration_heard[k])*100 / item_durations[k])



	th1 = 2 #cutoff chosen for num calls (log) (see from x axis of plot generated in num_calls.py)
	th2 = 5.5 #cutoff chosen for keys pressed per secong (-log) (see from x axis of plot generated in keys_pressed.py)
	
	print("CREATING DICTIONARIES") #assigning numerical ids to each source and theme
	src_map = {}
	theme_map = {}
	c1 = 0
	c2 = 0


	with open(file_name, 'r') as fr:
		for line in fr:
			data = line.split(',')
			if data[5].strip() not in src_map:
				src_map[data[5].strip()] = c1
				c1 += 1
			
			if data[6].strip() not in theme_map:
				theme_map[data[6].strip()] = c2
				c2 += 1






	print(src_map.keys())
	print(theme_map.keys())


	with open(file_name,'r') as fr: #for each entry in the data file,
		with open('thresh_'+str(th1)+'_'+ str(th2) + '.csv', 'w') as csvfile: #create a new file with given cutoffs
			writer = csv.writer(csvfile, delimiter=',', dialect="excel")
			for line in fr:
				line = line.rstrip()
				data = line.split(',')
				k = data[0]
				# print(k)
				if(np.log((num_calls[k])) >= th1) and (key_press_dict[k] <= th2 ): #if both thresholds are satisfied, write to file
					writer.writerow([data[0], data[1], data[2], data[3], data[4], src_map[data[5].strip()], theme_map[data[6].strip()], data[7], data[8].strip()]) # num_calls[k], key_press_dict[k], user_listenership[k]])
					# writer.writerow([data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]]) # num_calls[k], key_press_dict[k], user_listenership[k]])


if __name__ == '__main__':
	main()	