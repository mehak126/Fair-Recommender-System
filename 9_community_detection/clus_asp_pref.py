import numpy as np 
import pandas as pd
import csv
from collections import Counter
import pickle
import seaborn as sn
import matplotlib.pyplot as plt


def pretty_graph(echo_mat):
	df_cm = pd.DataFrame(echo_mat)
	plt.figure(figsize = (10,7))
	sn.heatmap(df_cm, annot=True)	
	plt.savefig('echo.png')
	plt.show()


if __name__ == '__main__':
	num_aspects = 5
	num_clusters = 5

	asp_list = ["Basic awareness","Serial appreciation and feedback","general","Status of the women","Iron deficiency/ anemia"]
	
	asp_list = np.asarray(asp_list)

	pos_asp = np.zeros((num_aspects, num_clusters))
	neg_asp = np.zeros((num_aspects, num_clusters))
	num_items = np.zeros(num_aspects)

	with open('pos.pickle', 'rb') as handle:
		pos = pickle.load(handle)

	with open('neg.pickle', 'rb') as handle:
		neg = pickle.load(handle)

	with open('item_dict.pickle', 'rb') as handle:
		item_dict = pickle.load(handle)            #item gives index in pos/neg array

	with open('item_asp_map.pickle', 'rb') as handle:
		item_asp_map = pickle.load(handle)

	for item in item_asp_map:
		asp = item_asp_map[item]
		num_items[asp] += 1
		index = item_dict[item]
		pos_asp[asp,:] += pos[index,:]
		neg_asp[asp,:] += neg[index,:]

	pos_asp = pos_asp.astype(int)
	neg_asp = neg_asp.astype(int)
	tot = pos_asp+neg_asp
	# print(pos_asp/tot)
	# print("\n\n")
	# print(neg_asp/tot)
	# print("\n\n")
	# print(pos_asp/neg_asp)

	calc = pos_asp/neg_asp
	print(calc)
	calc[3:5,2] = 0
	pretty_graph(calc)
	

	exit()
	for i in range(num_clusters):
		asp = calc[:,i]
		print("Cluster "+str(i)+":")
		ind = np.argsort(-1*asp)
		# print(ind)
		print(asp_list[ind])

	# pretty_graph()

	# print(tot)
	# print(tot)
	# print(num_items)


