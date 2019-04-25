# no change needed for incorporating demo
import numpy as np
import sys
from collections import Counter
import pickle

def main():
	in_file = sys.argv[1] #data file containing power users
	
	out_file = 'user_preferences.txt' #file containing array of users x (num_sources.num_themes.2), i.e.- the preference vector of each user for each sourceXtheme pair

	user_dict = {} #for assiging unique positions to each user
	items_heard = Counter() #for storing total items heard by each user
	user_preferences = Counter() #for storing preference vector of each user

	negative_interaction_list = ["dtmf_*","dtmf_0","dtmf_1","dtmf_4","hangup"] #keys indicating negative interaction with item
	positive_interaction_list = ["dtmf_2","dtmf_3","dtmf_5","dtmf_6","completed","dtmf_9"] #keys indicating positive interaction with item

	heard_percentage = 45 #percentage of duration heard above which item will be classified as 'liked' by user
	skipped_percentage = 45 #percentage of duration heard below which item will be classified as 'disliked' by user

	#actual sources and themes stored in order of ids created in thresh.py
	source_dict = ['SGC', 'ALL', 'FGC', 'UGC', 'RGC'] 
	theme_dict = ['others', 'Health', 'SHG', 'Education', 'Curated Local Updates', 'Social Welfare', 'Social Entertainment', 'Livelihoods', 'Agriculture', 'PFI', 'CF', 'Social Issues', 'MDD', 'Sanitation', 'KDKK', 'VHSND', 'ORS and diarrhea management', 'KITCHEN GARDENING', 'Social Entitlements', 'Family Planning']

	n_themes = len(theme_dict)
	n_sources = len(source_dict)



	none_count = 0
	with open(in_file,'r') as fr:
		for line in fr:
			line = line.rstrip().strip()
			data = line.split(',')
			user = data[0] #caller id
			if not user in user_dict: #if it's a new caller, assign him a position in the user_dict
				user_dict[user] = len(user_dict)

			theme = int(data[6])
			source = int(data[5])

			if int(data[2]) == 0: #item duration is 0
				continue

			items_heard[user_dict[user]] += 1

			user_preferences[(user_dict[user], n_sources*n_themes + source, n_themes*n_sources + theme) ] = 1 #putting 1 since that user has heard that sourceXtheme

			percentage_heard = float(data[3])*100.0/float(data[2])

			if (data[4] in positive_interaction_list): #if a positive interaction key was pressed
				user_preferences[(user_dict[user], source, theme)] += 1
			elif (data[4] in negative_interaction_list): #if a negative interaction key was pressed
				user_preferences[(user_dict[user], source, theme)] -= 1
			else:
				if (percentage_heard >= heard_percentage):
					user_preferences[(user_dict[user], source, theme)] += 1
				elif (percentage_heard < skipped_percentage):
					user_preferences[(user_dict[user], source, theme)] -= 1


	with open(out_file,'w') as fw:
		for i in range(len(user_dict)): #users
			for count in range(2): 
				for j in range(n_sources): #sources
					for k in range(n_themes): #themes
						if count == 0:
							fw.write(str(user_preferences[(i,j,k)]/items_heard[i]) + ' ')
						elif count == 1:
							fw.write(str(user_preferences[(i,n_sources*n_themes + j,n_sources*n_themes + k)] / items_heard[i] ) + ' ')
						# else:
						# 	fw.write(str(user_preferences[(i,n_sources*n_themes*2 + j,n_sources*n_themes*2 + k)]  ) + ' ')
			if i < len(user_dict)-1:
				fw.write('\n')
	print(n_themes)
	print(n_sources)


	with open('u_dict.pickle', 'wb') as handle: #storing the user dictionary (unique count given to each user) in a pickled file
		pickle.dump(user_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)












if __name__ == '__main__':
	main()