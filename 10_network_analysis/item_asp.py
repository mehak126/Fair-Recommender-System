## calculates items aspects
import numpy as np
import random as rand
import pandas as pd
import pickle
from collections import Counter

if __name__ == "__main__":

	num_clusters = 5

	datax = pd.read_csv('../Data/met2_45_45/features_equal_rates.csv', low_memory=False, header = None).as_matrix()

	with open('../Data/met2_45_45/mdd_items.pickle', 'rb') as handle: #item_id -> index
		mdd = pickle.load(handle)

	rev_dict = {}
	for item_id in mdd:
		rev_dict[mdd[item_id]] = item_id

	res_pos = {}
	X = datax[:,1:-7]
	# print(X.shape[1])
	item_list = []

	for i in range(len(mdd)):
		item_list.append(rev_dict[i])

	item_list = np.asarray(item_list)


	# for asp in range(X.shape[1]):
	# 	res_pos[asp] = []
	count = 0
	dd = Counter()
	for i in range(X.shape[0]):
		asp = X[i,:]
		asp = np.where(asp==1)[0]
		if asp.shape[0] == 0: #ignoring items with no aspect(aspect wasnt imp enough to be considered)
			continue
		chosen_asp = rand.choice(asp)
		res_pos[item_list[i]] = chosen_asp
		dd[chosen_asp] += 1
		# count += 1

	print(res_pos)
	# print(dd)
	with open('item_asp_map.pickle', 'wb') as handle:
		pickle.dump(res_pos, handle, protocol=pickle.HIGHEST_PROTOCOL)

	# print(res_pos)
	# for i in res_pos:
	# 	print(type(i))

# if __name__ == "__main__":
# 	main()