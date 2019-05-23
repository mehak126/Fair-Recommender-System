# import numpy as np 
# import pandas
# from collections import Counter

# if __name__ == '__main__':
# 	data = pandas.read_csv('merge_11col.csv', low_memory=False).as_matrix()

# 	theme_list = ['others', 'Health', 'SHG', 'Education', 'Curated Local Updates', 'Social Welfare', 'Social Entertainment', 'Livelihoods', 'Agriculture', 'PFI', 'CF', 'Social Issues', 'MDD', 'Sanitation', 'KDKK', 'VHSND', 'ORS and diarrhea management', 'KITCHEN GARDENING', 'Social Entitlements', 'Family Planning']

# 	## translator to remove ""
# 	tr = str.maketrans("", "", "\"")

# 	themed = {}
# 	camp_item = {}
# 	camp_user = {}
# 	for i in range(data.shape[0]):
		
# 		curr_theme = data[i, 6]
# 		curr_camp = data[i, 10]
# 		curr_item = data[i, 1]
# 		curr_user = data[i, 0]

# 		if type(curr_camp) != str:
# 			continue

# 		if curr_theme not in themed:
# 			themed[curr_theme] = Counter()

# 		# print(curr_camp)
# 		# print(data[i, :])
# 		clist = curr_camp.split(",")

# 		for camp in clist:
# 			camp = camp.translate(tr)
# 			camp = str(curr_theme) + camp
# 			if camp != "NA":
# 				themed[curr_theme][camp] += 1
# 				if camp not in camp_item:
# 					camp_item[camp] = Counter()
# 				camp_item[camp][curr_item] += 1

# 				if camp not in camp_user:
# 					camp_user[camp] = Counter()
# 				camp_user[camp][curr_user] += 1				


# 	for theme in themed:
# 		print(theme_list[theme]+" "+ str(len(themed[theme])))

# 	print("\n\n\n\n")

# 	for theme in themed:
# 		print(theme_list[theme]+" "+str(len(themed[theme])))
# 		item_sum = 0
# 		user_sum = 0
# 		for camp in themed[theme]:
# 			if theme>9:
# 				print(camp[2:]+" "+str(len(camp_item[camp]))+" "+str(len(camp_user[camp])))
# 			else:
# 				print(camp[1:]+" "+str(len(camp_item[camp]))+" "+str(len(camp_user[camp])))
# 			# item_sum += len(camp_item[camp])
# 			# user_sum += len(camp_user[camp])
# 		# print(theme+" "+str(item_sum)+" "+str(user_sum))
# 		print("----------------------------------------")
# 	# for camp in camp_item:
# 	# 	print(camp+": "+str(len(camp_item[camp]))+" "+camp_user[camp])








## new_11col

import numpy as np 
import pandas
from collections import Counter

if __name__ == '__main__':
	data = pandas.read_csv('../data/new_11col.csv', low_memory=False).as_matrix()

	theme_list = ['others', 'Health', 'SHG', 'Education', 'Curated Local Updates', 'Social Welfare', 'Social Entertainment', 'Livelihoods', 'Agriculture', 'PFI', 'CF', 'Social Issues', 'MDD', 'Sanitation', 'KDKK', 'VHSND', 'ORS and diarrhea management', 'KITCHEN GARDENING', 'Social Entitlements', 'Family Planning']

	## translator to remove ""
	tr = str.maketrans("", "", "\"")

	themed = {}
	camp_item = {}
	camp_user = {}
	for i in range(data.shape[0]):
		
		curr_theme = data[i, 6]
		curr_camp = data[i, 10]
		curr_item = data[i, 1]
		curr_user = data[i, 0]

		if type(curr_camp) != str:
			continue

		if curr_theme not in themed:
			themed[curr_theme] = Counter()

		# print(curr_camp)
		# print(data[i, :])
		clist = curr_camp.split(",")

		for camp in clist:
			camp = camp.translate(tr)
			# if curr_theme == "MDD" and camp.startswith("In-depth knowledge on age-appropriate"):
			# 	print(data[i, :])
			# 	exit()
			camp = str(curr_theme) + "_"+camp
			if camp != "NA":
				themed[curr_theme][camp] += 1
				if camp not in camp_item:
					camp_item[camp] = Counter()
				camp_item[camp][curr_item] += 1

				if camp not in camp_user:
					camp_user[camp] = Counter()
				camp_user[camp][curr_user] += 1				


	for theme in themed:
		print(theme+" "+ str(len(themed[theme])))

	print("\n\n\n\n")

	for theme in themed:
		print(theme+" "+str(len(themed[theme])))
		item_sum = 0
		user_sum = 0
		for camp in themed[theme]:
				print(camp+" "+str(len(camp_item[camp]))+" "+str(len(camp_user[camp])))
			# item_sum += len(camp_item[camp])
			# user_sum += len(camp_user[camp])
		# print(theme+" "+str(item_sum)+" "+str(user_sum))
		print("----------------------------------------")
	# for camp in camp_item:
	# 	print(camp+": "+str(len(camp_item[camp]))+" "+camp_user[camp])

		
