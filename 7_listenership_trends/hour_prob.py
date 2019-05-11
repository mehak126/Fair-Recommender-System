import numpy as np
import sys
from collections import Counter
import pickle
import pandas, pickle, re, random, csv
import matplotlib.pyplot as plt


def check(time):
	time = time.replace("-"," ")
	time = time.replace(":"," ")
	return time.split()[0:4]


def prob_bar(hist, avg, num):
	# random.seed(1)
	# Create a figure instance
	fig = plt.figure()
	n = len(hist)
	plt.xlabel('rank', fontsize=14)
	plt.ylabel('prob of users reaching a rank', fontsize=14)
	# plt.plot([i+1 for i in range(n)],avg)
	# plt.savefig("hour_"+str(num)+".png")

	# Create an axes instance
	ax = fig.add_subplot(111)
	# Create the boxplot
	bp = ax.boxplot(hist,showfliers=False)
	# Save the figure
	fig.savefig("new_prob_"+str(num)+".png")


def main():
	mdd_slots = {}
	mdd_slots['2017-06'] = 1 #june
	mdd_slots['2017-07'] = 1 #july
	mdd_slots['2017-08'] = 1 #aug

	'''
	2017---
	Mar, May, Apr (5-7)
	Sept, June, July, August (10-11, 12-1, 2-3, 7-8)
	Oct (10-11, 4-5)
	Nov (1-2)

	2018---
	Apr (10-11, 1-2, 2:30-4)
	'''
	# path = "../EDA/orig_data/bmgf/bmgf/data/"
	# d1 = pandas.read_csv(path+'bmgf_data_1.csv', low_memory=False).as_matrix()
	# d2 = pandas.read_csv(path+'bmgf_data_2.csv', low_memory=False).as_matrix()
	# d3 = pandas.read_csv(path+'bmgf_data_3.csv', low_memory=False).as_matrix()
	# d4 = pandas.read_csv(path+'bmgf_data_4.csv', low_memory=False).as_matrix()
	# d5 = pandas.read_csv(path+'bmgf_data_5.csv', low_memory=False).as_matrix()
	# d6 = pandas.read_csv(path+'bmgf_data_6_1.csv', low_memory=False).as_matrix()
	# d7 = pandas.read_csv(path+'bmgf_data_6_2.csv', low_memory=False).as_matrix()
	# d8 = pandas.read_csv(path+'bmgf_data_7_1.csv', low_memory=False).as_matrix()
	# d9 = pandas.read_csv(path+'bmgf_data_7_2.csv', low_memory=False).as_matrix()
	# d10 = pandas.read_csv(path+'bmgf_data_8.csv', low_memory=False).as_matrix()
	# # data2 = np.array(data2)
	# # print("done")
	
	# data1 = np.append(d1[:,:], d2[:,:], 0)
	# data1 = np.append(data1, d3[:,:], 0)
	# data1 = np.append(data1, d4[:,:], 0)
	# data1 = np.append(data1, d5[:,:], 0)
	# data1 = np.append(data1, d6[:,:], 0)
	# data1 = np.append(data1, d7[:,:], 0)
	# data1 = np.append(data1, d8[:,:], 0)
	# data1 = np.append(data1, d9[:,:], 0)
	# data1 = np.append(data1, d10[:,:], 0)

	data1 = pandas.read_csv('mdd_time.csv', low_memory=False).as_matrix()

	dc = 1 #date column 
	ic = 8 #item_id column
	uc = 5 #user column

	data_dict = {}
	date_ui_dict = {} #for a particular user item dict

	for i in range(data1.shape[0]):

		time = data1[i,dc]
		y,m,d,h = check(time)
		ym = y+'-'+m
		item = data1[i,ic]
		user = data1[i,uc]
		time = ym+' '+d+' '+h
		chosen_hr = 10

		if ym in mdd_slots:
			ind = mdd_slots[ym]
			if int(h) == chosen_hr:
				# print(str(time)+' '+str(user)+' '+str(item))
				if time not in date_ui_dict:
				 	date_ui_dict[time] = {}
				if user not in date_ui_dict[time]:
				 	date_ui_dict[time][user] = {}
				if item not in date_ui_dict[time][user]:
					date_ui_dict[time][user][item] = 1


	list_dict = {}
	for time in date_ui_dict:
		for user in date_ui_dict[time]:
			num_items_heard = len(date_ui_dict[time][user])
			if time not in list_dict:
				list_dict[time] = np.zeros(20)
			if num_items_heard >= 20:
				continue
			list_dict[time][num_items_heard] += 1

	plot_data = []
	avg = []
	for time in list_dict:
		for i in range(20):
			for j in range(i+1,20):
				list_dict[time][i] += list_dict[time][j] 
		list_dict[time] /= list_dict[time][0]
		plot_data.append(list(list_dict[time]))
		# print(list(list_dict[time]))
		avg.append(np.mean(list_dict[time]))
	# exit()

	plot_data = np.asarray(plot_data)
	print(plot_data.shape)
	# plot_data = plot_data.T
	avg = np.mean(plot_data, axis = 0)
	prob_bar(plot_data, avg, 0)




if __name__=="__main__":
	main()