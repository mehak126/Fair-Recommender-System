# args-
# 1 -> clustering_file
# 2 -> user_info
# 3 -> demography data
import numpy as np
import sys
import operator
from collections import Counter
from scipy import stats
import pickle


def main():

	# all sources and themes stored in order of dictionary created in thresh.py
	source_dict = ['SGC', 'ALL', 'FGC', 'UGC', 'RGC']
	theme_dict = ['others', 'Health', 'SHG', 'Education', 'Curated Local Updates', 'Social Welfare', 'Social Entertainment', 'Livelihoods', 'Agriculture', 'PFI', 'CF', 'Social Issues', 'MDD', 'Sanitation', 'KDKK', 'VHSND', 'ORS and diarrhea management', 'KITCHEN GARDENING', 'Social Entitlements', 'Family Planning']
	

	clustering_file = open(sys.argv[1],'r') #file containing clusters (output of 2_kprototype.py)
	inp_file = open(sys.argv[2],'r') #file containing user preference vectors (output of 1_entropy_heard.py)
	analysis_file = open( sys.argv[1] + '_analysis_total_new.txt','w') #output file
	

	all_clusters = clustering_file.read().split('\n')
	all_user_info = inp_file.read().split('\n')
	
	user_info = []
	for user in all_user_info:
		user = user.split(' ')
		user.pop()
		user_info.append(list(map(float,user[:100])))

	clusters = []
	for cluster in all_clusters:
		cluster = cluster.split(' ')
		cluster.pop()
		clusters.append(list(map(int,cluster)))
	clusters.pop()


	# num_items_to_display = 5

	for index_c, c in enumerate(clusters): #for each cluster,
		num_users = len(c)
		cluster_pref = np.zeros(len(user_info[0])) #to store average of user preferences for users belonging to that cluster
		
		for u_count, user in enumerate(c): #for each user,
			cluster_pref += user_info[user]
		cluster_pref /= num_users*1.0


		with open('cluster_' + str(index_c) + '.pickle', 'wb') as handle: #storing average cluster preference in a pickle file
			pickle.dump(cluster_pref, handle, protocol=pickle.HIGHEST_PROTOCOL)
		
		new_dict = {} #storing cluster preferences for each sourceXtheme pair in a dictionary
		for index,pref in enumerate(cluster_pref):
			new_dict[index] = pref

		sorted_dict = sorted(new_dict.items(), key=operator.itemgetter(1)) #sort from highest to lowest preference sourceXtheme pair for that cluster
		# print(sorted_dict)

		# print preference order in an analysis file
		analysis_file.write("Cluster " + str(index_c) + '\n')
		analysis_file.write("Num users: " + str(num_users) + '\n')
		for i in range(len(sorted_dict)):
			index = sorted_dict[i][0]
			row = int(index/len(theme_dict))
			col = int(index%len(theme_dict))
			analysis_file.write(str(i+1) + ' ' + source_dict[row] + ', ' + theme_dict[col] + '\n') 
		
		analysis_file.write('\n\n')




if __name__ == '__main__':
	main()