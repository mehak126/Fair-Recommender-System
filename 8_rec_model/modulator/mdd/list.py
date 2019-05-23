from numpy import linalg as la
import numpy as np
import pandas, pickle, re, random, csv
import matplotlib.pyplot as plt
from collections import Counter

def check(time):
	time = time.replace("-"," ")
	time = time.replace(":"," ")
	return time.split()[0:4]

def plot(hist, num):
	# random.seed(1)
	plt.figure()
	n = len(hist)
	plt.plot([i for i in range(n)],hist)
	plt.savefig("hist_"+str(num)+".png")


def hhi(exp):
	k = exp.shape[0]
	num_aspects = exp.shape[1]
	tot_exp = np.sum(exp, axis = 1) #tottal exposure in each interval
	# print(exp)
	x = exp.T/tot_exp
	x = x.T #dim = num intervals * aspects; contains percent of exp given to aspect in that interval
	hhi_var = np.sum(x*x, axis = 1)
	return hhi_var
	return np.sum(hhi_var)/len(hhi_var)


def R_data(r_file, r):
	R = np.zeros(r) #matrix of num users coming to rank i per minute
	with open(r_file,'r') as fr:
		count = 0
		for line in fr:
			R[count] = float(line.strip())
			count += 1
			if count == r:
				break
	return R


def main():

	'''
	2017---
	Mar, May, Apr (5-7)
	Sept, June, July, August (10-11, 12-1, 2-3, 7-8)
	Oct (10-11, 4-5)
	Nov (1-2)

	2018---
	Apr (10-11, 1-2, 2:30-4)
	'''

	data1 = pandas.read_csv('mdd_data_jja.csv', low_memory=False).as_matrix()

	with open('item_asp_map.pickle', 'rb') as handle:
		item_asp = pickle.load(handle)

	with open('mdd_items.pickle', 'rb') as handle: #item_id -> index
		mdd = pickle.load(handle)

	r = 20
	r_file = ["R10.txt", "R12.txt", "R14.txt", "R19.txt"]
	# R = np.zeros((r,len(r_file)))
	# for i in range(len(r_file)):
	# 	R[:,i] = R_data(r_file[i], r)
	R = R_data(r_file[0], r)	
	# sum_R = np.sum(R)
	dc = 1 #date column 
	ic = 8 #item_id column
	k = 321 #actual 320 intervals

	ymdh_dict = {}
	count = 0
	ymdh_lists = []
	item_dict = {}
	
	exp_item = Counter()
	exp_aspect = Counter()

	for i in range(data1.shape[0]):
		time = data1[i,dc]
		y,m,d,h = check(time)
		ymdh = y+'-'+m+'-'+d+'-'+h
		item = data1[i,ic]

		if ymdh not in ymdh_dict:
			ymdh_dict[ymdh] = count
			item_dict = {}
			count += 1
			if count == k:
				break
			ymdh_lists.append([])

		yli = ymdh_dict[ymdh] #ymdh lists index
		if item not in item_dict:
			item_dict[item] = 1
			ymdh_lists[yli].append(item)

	

	# print(len(ymdh_lists))
	u_dict = {}
	total_items = 0
	k = k-1
	num_aspects = 5
	E_aspect_int = np.zeros((k, num_aspects))
	for i in range(len(ymdh_lists)):
		cl = ymdh_lists[i]#cl = current list
		for j in range(len(cl)):
			item = cl[j]
			if item not in item_asp:
				print(mdd[item])
				print(item)
				continue
			ia = item_asp[item]#item aspect
			# if ia == -1:
			if item not in u_dict:
				u_dict[item] = 1
				total_items += 1
			E_aspect_int[i,ia] += R[j]

			exp_item[item] += R[j]
			exp_aspect[ia] += R[j]


	with open('hhim.pickle', 'wb') as handle:
		pickle.dump(hhi(E_aspect_int), handle, protocol=pickle.HIGHEST_PROTOCOL)

	#create file for aspect analysis
	with open("aspect_exp_m.txt",'w') as fw:
		for i in range(num_aspects):
			fw.write(str(exp_aspect[i]) + '\n')

	with open("item_exp_m.csv",'w') as fw:
		item_count = 0
		for item in exp_item.keys():
			fw.write(str(item)+ ',' + str(exp_item[item]) + '\n')
			# print(item)


if __name__=='__main__':
	main()


# fairness - hhi
# diversity -  
# utility - one graph with std dev
# exp to diff ratings - 3 cdf for all models 

# utility per item basis - dont use original modulators 
# mean normalization rmse - whats the mean ?


# fairness, 
