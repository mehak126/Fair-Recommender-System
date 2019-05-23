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
		if h == 10 or h == 12 or h == 13 or h == 16 or h == 19:
			return True
	return False



def main():

	'''
	FAMILY PLANNING  

	2017---

	2018---
	May,Jun,Jul  (12-1, 6:30-7)
	8,9,10 Aug,Sept,Oct,Nov (10-11, 12-2, 4-5, 6:30-8)
	Dec (10-11, 12-1, 7-8)

	2019--
	Feb (10-11, 1-2)
	Jan (10-11, 7-8)
	'''

	fp_slots = {}
	# fp_slots['2017-03'] = 0 #mar
	# fp_slots['2017-04'] = 0 #apr
	# fp_slots['2017-05'] = 0 #may

	fp_slots['2018-08'] = 0 #june
	fp_slots['2018-09'] = 0 #july
	fp_slots['2018-10'] = 0 #aug

	# fp_slots['2017-09'] = 2 #sep
	# fp_slots['2017-10'] = 2 #oct
	# fp_slots['2017-11'] = 2 #nov

	# fp_slots['2018-04'] = 3 #apr 2018

	x = [[] for i in range(1)]
	udict = [{} for i in range(1)] #unique items dict 
	c = [0]*1
	dates = [{} for i in range(1)] #unique dates dict 
	bad = [{} for i in range(1)]


	path = "../EDA/orig_data/bmgf/bmgf/data/"
	d1 = pandas.read_csv(path+'bmgf_data_1.csv', low_memory=False).as_matrix()
	d2 = pandas.read_csv(path+'bmgf_data_2.csv', low_memory=False).as_matrix()
	d3 = pandas.read_csv(path+'bmgf_data_3.csv', low_memory=False).as_matrix()
	d4 = pandas.read_csv(path+'bmgf_data_4.csv', low_memory=False).as_matrix()
	d5 = pandas.read_csv(path+'bmgf_data_5.csv', low_memory=False).as_matrix()
	d6 = pandas.read_csv(path+'bmgf_data_6_1.csv', low_memory=False).as_matrix()
	d7 = pandas.read_csv(path+'bmgf_data_6_2.csv', low_memory=False).as_matrix()
	d8 = pandas.read_csv(path+'bmgf_data_7_1.csv', low_memory=False).as_matrix()
	d9 = pandas.read_csv(path+'bmgf_data_7_2.csv', low_memory=False).as_matrix()
	d10 = pandas.read_csv(path+'bmgf_data_8.csv', low_memory=False).as_matrix()
	# data2 = np.array(data2)
	print("done")
	
	data1 = np.append(d1[:,:], d2[:,:], 0)
	data1 = np.append(data1, d3[:,:], 0)
	data1 = np.append(data1, d4[:,:], 0)
	data1 = np.append(data1, d5[:,:], 0)
	data1 = np.append(data1, d6[:,:], 0)
	data1 = np.append(data1, d7[:,:], 0)
	data1 = np.append(data1, d8[:,:], 0)
	data1 = np.append(data1, d9[:,:], 0)
	data1 = np.append(data1, d10[:,:], 0)


	# data1 = pandas.read_csv('fp_time.csv', low_memory=False).as_matrix()

	# baby = data1[0:10,:]

	# with open('baby.pickle', 'wb') as handle:
	# 	pickle.dump(baby, handle, protocol=pickle.HIGHEST_PROTOCOL)

	# with open('baby.pickle', 'rb') as handle:
	# 	baby = pickle.load(handle)

	with open('fp_items.pickle', 'rb') as handle:
		fp_dict = pickle.load(handle)

	# if 1229996 in fp_dict:
	# 	print("YES")
	dc = 1 #date column 
	ic = 8 #item_id column
	# time = baby[0,ic]
	# y,m,d,h = check(time)	

	with open('fp_data_jja.csv', 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter=',', dialect="excel")

		for i in range(data1.shape[0]):

			time = data1[i,dc]
			y,m,d,h = check(time)
			ym = y+'-'+m
			item = data1[i,ic]

			if ym in fp_slots:
				ind = fp_slots[ym]
				if corr_hour(ind, int(h), ym):
					
					if item in fp_dict:
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



	for i in range(1):
		x[i].append(c[i])
		plot(x[i],i)
		b = len(bad[i])
		g = c[i]
		print(b)
		# print(str(i)+':'+str(b/g))


		# print(dates[i])


if __name__=='__main__':
	main()