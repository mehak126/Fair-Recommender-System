import sys
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from collections import defaultdict
import math
import pandas
import csv

def main():
	file_name = sys.argv[1] #data file. assumed column 0 -> listener id, column 7 -> call id
	num_calls = Counter() #Dictionary storing unique calls made by each user id

	cdr_id = {} #Dictionary to keep track of call ids already counted

	with open(file_name, 'r') as dat:
		for line in dat:
			info = line.split(',')
			if(info[7] not in cdr_id): #new call
				cdr_id[info[7]] = 1
				num_calls[info[0]] += 1

	
	all_calls = []
	for k in num_calls:
		all_calls.append(num_calls[k]) #storing all calls made by users in an array


	call_variation = Counter(all_calls) #x -> number of calls made, y -> how many users made those many calls
	all_vals = sorted(call_variation.most_common())
	x_vals = [x[0] for x in all_vals] #no. of calls made 
	y_vals = [x[1] for x in all_vals] #no. of users who made those many calls

 
	sum_user = 0
	cdf = []

	for y in y_vals:
		cdf.append(sum_user/len(num_calls))
		sum_user += y
		


	# plt.plot((x_vals), (y_vals))
	# plt.plot(np.log(x_vals),np.log(y_vals))
	plt.plot(np.log(x_vals), (cdf))
	plt.xlabel('Number of calls (log)', fontsize = 14)
	plt.ylabel('Number of users (normalised)', fontsize = 14)
	# plt.title(' Distribution of users according to number of calls')
	# plt.title('Cumulative Distribution of users according to number of calls')
	plt.show()
	plt.close()



if __name__ == '__main__':
	main()	