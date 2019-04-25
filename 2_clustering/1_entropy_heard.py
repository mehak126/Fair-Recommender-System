import numpy as np
from scipy.stats import entropy
from collections import Counter
import matplotlib.pyplot as plt
import pickle

def main():
	in_file = 'user_preferences.txt' #output file produced in 0_heard.py
	data_file = 'thresh_2.5_5_contr.csv' #data file of power users

	# num_demo_cols = 21 	
	# demo_info = [dict() for x in range(num_demo_cols)]
	# with open(data_file,'r') as fr:
	# 	for line in fr:
	# 		data = line.split(',')
	# 		if data[0] not in u_id:
	# 			u_id[data[0]] = user_count
	# 			for i in range(num_demo_cols):
	# 				demo_info[i][user_count] = data[i+8].rstrip().strip()
	# 			user_count += 1


	u_id = {}
	user_count = 0

	
	with open(in_file, 'r') as fr:
		content = fr.read().split('\n')

	input_data = [ np.array(list(map(float,x.strip().split(' ')))) for x in content]
	input_data = np.array(input_data)


	num_cols = 100 #only consider first 100 cols -> for calculating entropy, we only consider the preference vectors which are the first num_sourceXnum_theme entries, ignoring the categorical part of whether the user has heard that sourceXtheme pair or not

	overall_pref = np.zeros(num_cols) #for storing average preference, indicating global preference

	for i in range(num_cols):
		overall_pref[i] = np.sum( input_data[:,i] ) / (input_data.shape[0])



	c = 1.0 #for normalisation (to avoid 0)

	input_data = input_data + c
	overall_pref = overall_pref + c


	entropies = np.zeros(input_data.shape[0])
	for user in range(input_data.shape[0]):
		entropies[user] = entropy( input_data[user][:num_cols], overall_pref )



	log_entropies = list((10 * np.log(entropies)))


	dist = Counter(log_entropies) #distribution of entropies

	all_vals = sorted(dist.most_common())
	x_vals = [x[0] for x in all_vals]
	y_vals = [x[1] for x in all_vals]


	cdf = []
	sum = 0.0
	for x in all_vals:
		sum = sum + x[1]
		cdf.append(sum/len(input_data))
	ccdf = [1-x for x in cdf]


# Code for printing entropy distribution so that an appropriate cutoff can be chosen

	# # plt.plot((x_vals), (y_vals))
	# plt.plot((x_vals), ccdf)
	plt.plot((x_vals), cdf)
	plt.xlabel('10*log(k-l divergence scores)', fontsize = 14)
	plt.ylabel('Number of users (normalised)', fontsize = 14)
	# plt.title('Cumulative Distribution of users according to k-l divergence scores')
	# # plt.title('Distribution of users according to k-l divergence scores')
	plt.show()
	plt.close()
	# exit(1)


	# demo_file = open('user_demo_new.txt','w')
	with open('u_dict.pickle','rb') as handle: #user dictionary created in 0_heard.py
		u_dict = pickle.load(handle)

	rev_dict = {} #reverse of user_dictionary : here key = index, value = phone no.
	for ph_no in u_dict:
		rev_dict[u_dict[ph_no]] = ph_no



	new_user_dict = {} #new indices given to users extracted after setting entropy cutoff
	with open('cat_user_data_10_equal_rates.txt','w') as fw:
		for i in range(len(input_data)):
			if log_entropies[i] > -100: #put entropy cutoff here, after analysing from graph generated earlier
				ph_no = rev_dict[i]

				new_user_dict[ph_no] = len(new_user_dict)
				for j in range(len(input_data[i])):
					if j < num_cols:
						fw.write(str(input_data[i][j]) + ' ')
					else:
						fw.write(str(int(input_data[i][j]-1)) + ' ')
				fw.write('\n')
				# demo_file.write(age[i] + ' ' + gender[i])
				# for j in range(num_demo_cols):
					# demo_file.write(demo_info[j][i] + ' ')
				# demo_file.write('\n')

	# demo_file.close()
	with open('new_u_dict.pickle', 'wb') as handle: #store the new user dictionary in a pickle
		pickle.dump(new_user_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)



















if __name__ == '__main__':
	main()