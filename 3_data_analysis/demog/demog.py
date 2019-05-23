import numpy as np 
import pandas
import csv
from collections import Counter
import pickle


def modify(d, val):
	for key in d:
		d[key] = round(d[key]/val, 2)

if __name__ == '__main__':


	# data = pandas.read_csv('thresh_2.5_5.csv', delimiter=',',  low_memory=False, header= None).as_matrix()
	demo1 = pandas.read_excel('SV1.xlsx').as_matrix()
	demo2 = pandas.read_excel('SV2.xlsx').as_matrix()

	with open('../../Data/cf/u_dict.pickle', 'rb') as handle:
		u_dict = pickle.load(handle)

	file = open('../../Data/cf/5_k_prototype.txt', 'r') 

	cluster = 0
	user_cluster = {}
	cluster_dict = {} #num users in each cluster
	summ = 0
	for line in file:
		users = line.split(" ")
		cluster_dict[cluster] = len(users)
		summ += len(users)
		# print(str(cluster)+" "+str(len(users)))
		for i in range(len(users)-1):
			user_cluster[int(users[i])] = cluster
		cluster += 1


	num_clusters = cluster
	gend = [Counter() for i in range(num_clusters)]
	aged = [Counter() for i in range(num_clusters)]
	locd = [Counter() for i in range(num_clusters)]


	count = 0
	for i in range(demo1.shape[0]):
		user = str(demo1[i,1]) #phone number
		if user not in u_dict:
			continue
		count += 1
		cluster = user_cluster[u_dict[user]]
		gender = demo1[i,3]
		age = demo1[i,4]
		loc = demo1[i,6] #location
		gend[cluster][gender] += 1
		aged[cluster][age] += 1
		locd[cluster][loc] += 1 

	print(count)
	print(summ)
	print(num_clusters)

	for i in range(len(gend)):
		print("-----------"+str(i)+"---------")
		modify(gend[i],sum(gend[i].values()))
		print(gend[i])


	print("\n\n")
	for i in range(len(aged)):
		print("-----------"+str(i)+"---------")
		modify(aged[i], sum(aged[i].values()))
		print(aged[i])

	print("\n\n")
	for i in range(len(locd)):
		print("-----------"+str(i)+"---------")
		modify(locd[i], sum(locd[i].values()))
		print(locd[i])
	# print(gend)
	# print(aged)


	pregd = [Counter() for i in range(num_clusters)]
	smalld = [Counter() for i in range(num_clusters)]
	childd = [Counter() for i in range(num_clusters)]

	count = 0
	for i in range(demo2.shape[0]):
		user = str(demo2[i,1]) #phone number
		if user not in u_dict:
			continue
		count += 1
		cluster = user_cluster[u_dict[user]]
		preg = demo2[i,3]
		small_kid = demo2[i,4]
		child = demo2[i,5] #location
		pregd[cluster][preg] += 1
		smalld[cluster][small_kid] += 1
		childd[cluster][child] += 1 

	print(count)
	print(summ)
	print("\n\n")
	for i in range(len(pregd)):
		print("-----------"+str(i)+"---------")
		modify(pregd[i], sum(pregd[i].values()))
		print(pregd[i])

	print("\n\n")
	for i in range(len(smalld)):
		print("-----------"+str(i)+"---------")
		modify(smalld[i], sum(smalld[i].values()))
		print(smalld[i])

	print("\n\n")
	for i in range(len(childd)):
		print("-----------"+str(i)+"---------")
		modify(childd[i], sum(childd[i].values()))
		print(childd[i])
