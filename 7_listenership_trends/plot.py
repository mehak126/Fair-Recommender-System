import numpy as np
import sys
from collections import Counter
import pickle
import pandas, pickle, re, random, csv
import matplotlib.pyplot as plt

def plot(hist, num):
	# random.seed(1)
	plt.figure()
	n = len(hist)
	plt.xlabel('rank')
	plt.ylabel('users reaching rank i(%)')
	plt.plot([i+1 for i in range(n)],hist)
	# plt.savefig("rank_"+str(num)+".png")

def check(time):
	time = time.replace("-"," ")
	time = time.replace(":"," ")
	return time.split()[0:4]

def main():


	## probab of users reching rank i 
	# r = int(sys.argv[1])
	# r_file = sys.argv[2]
	# R = np.zeros(r) #matrix of num users coming to rank i per minute
	# sum_r = 0
	# with open(r_file,'r') as fr:
	# 	count = 0
	# 	for line in fr:
	# 		R[count] = float(line.strip())
	# 		sum_r += R[count]
	# 		count += 1
	# 		if count == r:
	# 			break
	# R = R/R[0]
	# plot(R, r)


	## number of users every hour


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

	ts = {}
	ts[10] = 0
	ts[12] = 1
	ts[14] = 2
	ts[19] = 3
	

	data1 = pandas.read_csv('mdd_time.csv', low_memory=False).as_matrix()

	dc = 1 #date column 
	ic = 8 #item_id column
	uc = 5
	# time = baby[0,ic]
	# y,m,d,h = check(time)	

	u_date = {}
	count = 0	
	ui = [{} for i in range(4)]
	avg = np.asarray([0, 0, 0, 0])
	l = []

	for i in range(data1.shape[0]):
		time = data1[i,dc]
		y,m,d,h = check(time)
		ym = y+'-'+m
		item = data1[i,ic]
		user = data1[i,uc]
		ymd = ym+'-'+d

		if ym in mdd_slots:
			if ymd not in u_date:
				# print(str(len(ui[0]))+" "+str(len(ui[1]))+" "+str(len(ui[2]))+" "+str(len(ui[3])))
				avg[0] += len(ui[0])
				avg[1] += len(ui[1])
				avg[2] += len(ui[2])
				avg[3] += len(ui[3])
				ui = [{} for i in range(4)]
				u_date[ymd] = 1
				count += 1
			if count == 70:
				print(len(l))
				print(avg/(count-2))
				exit()
			ind = ts[int(h)]
			if user not in ui[ind]:
				ui[ind][user] = 1
				if(count == 4 and ind == 1):
					# print(data1[i,:])
					l.append(data1[i,:])

	

if __name__ == '__main__':
	main()

