import numpy as np 
import pandas
import csv
from collections import Counter
import pickle

if __name__ == '__main__':

	data = pandas.read_csv('../Data/merge_11col.csv', low_memory=False).as_matrix()
	negative_interaction_list = ["dtmf_*","dtmf_0","dtmf_1","dtmf_4","hangup"]
	positive_interaction_list = ["dtmf_2","dtmf_3","dtmf_5","dtmf_6","completed"]


	#### UPDATE
	num_clusters = 5
	unique_items = len(Counter(data[:, 1]))

	count = 0
	item_dict = {}
	for i in range(data.shape[0]):
		if data[i, 1] not in item_dict:
			item_dict[data[i, 1]] = count
			count += 1
  
	# with open('new_u_dict_changed_metrics.pickle', 'rb') as handle:
	# 	u_dict = pickle.load(handle)
	with open('../Data/cf/u_dict.pickle', 'rb') as handle:
		u_dict = pickle.load(handle)
	
	file = open('../Data/cf/5_k_prototype.txt', 'r') 
	# file = open('../Data/cf/5_k_prototype.txt', 'r') 
	# file = open('6_k_prototype_2_changed_metric.txt', 'r') 
	cluster = 0
	user_cluster = {}
	cluster_dict = {} #num users in each cluster
	summ = 0
	for line in file:
		users = line.split(" ")
		cluster_dict[cluster] = len(users)
		summ += len(users)
		print(str(cluster)+" "+str(len(users)))
		for i in range(len(users)-1):
			# print(users[i])
			user_cluster[int(users[i])] = cluster
		cluster += 1

	print(summ)

	num_users = np.zeros((unique_items, num_clusters))
	for i in range(num_clusters):
		num_users[:,i] = cluster_dict[i]
	pos = np.zeros((unique_items, num_clusters))# positive array for pos interaction 
	neg = np.zeros((unique_items, num_clusters))# negative array for neg interaction
	
	heard_percentage = 45
	skipped_percentage = 45

	for i in range(data.shape[0]):
		percentage_heard = (float(data[i, 3])*100.0)/float(data[i, 2])
		if str(data[i, 0]) not in u_dict:		# if not power user -> dont consider  
			continue
		
		if (data[i,4] in positive_interaction_list):
			pos[item_dict[data[i,1]], user_cluster[u_dict[str(data[i, 0])]]] += 1
		elif (data[i,4] in negative_interaction_list):
			neg[item_dict[data[i,1]], user_cluster[u_dict[str(data[i, 0])]]] += 1
		else:
			if (percentage_heard >= heard_percentage):
				pos[item_dict[data[i,1]], user_cluster[u_dict[str(data[i, 0])]]] += 1
			elif (percentage_heard < skipped_percentage):
				neg[item_dict[data[i,1]], user_cluster[u_dict[str(data[i, 0])]]] += 1
		
		
		# if (percentage_heard >= heard_percentage) or (data[i,4] in positive_interaction_list):
		# 	pos[item_dict[data[i,1]], user_cluster[u_dict[str(data[i, 0])]]] += 1
		# elif (percentage_heard < skipped_percentage) or (data[i,4] in negative_interaction_list):
		# 	neg[item_dict[data[i,1]], user_cluster[u_dict[str(data[i, 0])]]] += 1
		

	skip_rate = (pos-neg)/(pos+neg)
	with open('skip_rate.pickle', 'wb') as handle:
		pickle.dump(skip_rate, handle, protocol=pickle.HIGHEST_PROTOCOL)

	with open('pos.pickle', 'wb') as handle:
		pickle.dump(pos, handle, protocol=pickle.HIGHEST_PROTOCOL)

	with open('neg.pickle', 'wb') as handle:
		pickle.dump(neg, handle, protocol=pickle.HIGHEST_PROTOCOL)	

	with open('item_dict.pickle', 'wb') as handle:
		pickle.dump(item_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

	# print(skip_rate[0:10, :])