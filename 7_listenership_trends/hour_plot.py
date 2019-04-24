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
	plt.xlabel('hour', fontsize=14)
	plt.ylabel('no. of users at any hour', fontsize=14)
	plt.plot([i+1 for i in range(n)],hist)
	plt.savefig("hour_"+str(num)+".png")



def plotr(hist, num):
	# random.seed(1)
	plt.figure()
	n = len(hist)
	plt.xlabel('rank', fontsize=14)
	plt.ylabel('prob. of users raching a rank', fontsize=14)
	plt.plot([i+1 for i in range(n)],hist)
	plt.savefig("rank_"+str(num)+".png")



def main():

	# probab of users reching rank i 
	hour_r = int(sys.argv[1])
	# print(hour_r)
	r = 20
	r_file = "R_data.txt"
	R = np.zeros(r) #matrix of num users coming to rank i per minute
	sum_r = 0
	with open(r_file,'r') as fr:
		count = 0
		for line in fr:
			R[count] = float(line.strip())
			sum_r += R[count]
			count += 1
			if count == r:
				break
	R = R/R[0]
	plotr(R, r)


	# No. of users every hour 
	file_name = "hour.xlsx"
	dfs = pandas.read_excel(file_name, sheet_name=None).as_matrix()
	ti = 3 #time index
	cbi = 4 #call back index
	cci = 7 #call count index 
	hi = 6 #hour index
	l = [0 for i in range(24)]
	c = [0 for i in range(24)]
	l = np.asarray(l)
	c = np.asarray(c)
	time_dict = {}
	for i in range(dfs.shape[0]):
		if dfs[i,cbi] != "CALLBACK":
			continue
		h = int(dfs[i,hi])
		l[h] += int(dfs[i,cci])
		c[h] += 1
	l = l/c
	plot(l,'jja')
	# print( str(l[10]), str(l[12]), str(l[14]), str(l[19]))
	l = [int(l[i]) for i in range(len(l))]

	for i in range(R.shape[0]):
		print('{:.2f}'.format(R[i]*l[hour_r]))


	# exit()

if __name__ == "__main__":
	main()