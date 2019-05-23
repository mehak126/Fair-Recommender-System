from numpy import linalg as la
import numpy as np
import pandas, pickle, re, random, csv
import matplotlib.pyplot as plt

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

def corr_hour(ind, h, ym):
	if ind == 0:
		if h == 17:
			return True
	elif ind == 1:
		if h == 10 or h == 12 or h == 14 or h == 19:
			return True
	elif ind == 2:
		if ym == '2017-09': #sep special
			if h == 10 or h == 12 or h == 14 or h == 19:
				return True
		elif ym == '2017-10': #oct
			if h == 10 or h == 16:
				return True
		else:				  #nov
			if h == 13:
				return True
	else:
		if h == 10 or h == 13 or h == 14 or h == 15:
			return True
	return False



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

	u1 = {}
	u2 = {}
	u3 = {}
	u4 = {}

	mdd_slots = {}
	# mdd_slots['2017-03'] = 0 #mar
	# mdd_slots['2017-04'] = 0 #apr
	# mdd_slots['2017-05'] = 0 #may

	mdd_slots['2017-06'] = 1 #june
	mdd_slots['2017-07'] = 1 #july
	mdd_slots['2017-08'] = 1 #aug

	# mdd_slots['2017-09'] = 2 #sep
	# mdd_slots['2017-10'] = 2 #oct
	# mdd_slots['2017-11'] = 2 #nov

	# mdd_slots['2018-04'] = 3 #apr 2018

	x = [[] for i in range(5)]
	udict = [{} for i in range(5)] #unique items dict 
	c = [0]*5
	dates = [{} for i in range(5)] #unique dates dict 
	bad = [{} for i in range(5)]


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
	# print("done")
	
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

	# baby = data1[0:10,:]

	# with open('baby.pickle', 'wb') as handle:
	# 	pickle.dump(baby, handle, protocol=pickle.HIGHEST_PROTOCOL)

	# with open('baby.pickle', 'rb') as handle:
	# 	baby = pickle.load(handle)

	with open('mdd_items.pickle', 'rb') as handle:
		mdd_dict = pickle.load(handle)

	# if 1229996 in mdd_dict:
	# 	print("YES")
	dc = 1 #date column 
	ic = 8 #item_id column
	# time = baby[0,ic]
	# y,m,d,h = check(time)	

	with open('mdd_data_jja.csv', 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter=',', dialect="excel")

		for i in range(data1.shape[0]):

			time = data1[i,dc]
			y,m,d,h = check(time)
			ym = y+'-'+m
			item = data1[i,ic]

			if ym in mdd_slots:
				ind = mdd_slots[ym]
				if corr_hour(ind, int(h), ym):
					
					if item in mdd_dict:
						writer.writerow(list(data1[i,:]))
						if item not in udict[ind]:
							udict[ind][item] = 1
							c[ind] += 1
						ymd = ym+'-'+d
						if ymd not in dates[ind]:
							dates[ind][ymd] = 1
							x[ind].append(c[ind])

						# if item not in udict[4]:
						# 	udict[4][item] = 1
						# 	c[4] += 1
						# ymd = ym+'-'+d
						# if ymd not in dates[4]:
						# 	dates[4][ymd] = 1
						# 	x[4].append(c[4])
					else:
						if item not in bad[ind]:
							bad[ind][item] = 1



	for i in range(4):
		x[i].append(c[i])
		plot(x[i],i)
		b = len(bad[i])
		g = c[i]
		print(b)
		# print(str(i)+':'+str(b/g))


		# print(dates[i])


if __name__=='__main__':
	main()