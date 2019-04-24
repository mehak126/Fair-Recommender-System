import numpy as np 
import pandas
import csv
from collections import Counter

if __name__ == '__main__':
	
	data = pandas.read_csv('new_11col.csv', low_memory=False).as_matrix()
	# data = data[0:15101, :]
	theme_list = ['others', 'Health', 'SHG', 'Education', 'Curated Local Updates', 'Social Welfare', 'Social Entertainment', 'Livelihoods', 'Agriculture', 'PFI', 'CF', 'Social Issues', 'MDD', 'Sanitation', 'KDKK', 'VHSND', 'ORS and diarrhea management', 'KITCHEN GARDENING', 'Social Entitlements', 'Family Planning']
	mdd = ["Basic awareness", "In-depth knowledge", "Factors influencing practice", "Existing practice", "Iron deficiency/ anemia", "Status of the women"]
	mdd_dict = Counter(mdd)

	## translator to remove ""
	tr = str.maketrans("", "", "\"")

	with open('merge_11col.csv', 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter=',', dialect="excel")
		for i in range(data.shape[0]):
			theme = data[i, 6]
			theme = theme.strip(" ")
			camp = data[i, 10]
					
			
			if theme == "MDD":		
				if type(camp) != str:
					writer.writerow(list(data[i,:]))
					continue
				
				clist = camp.split(",")
				new_camp_list = ""
				camp_dict = {}
				for camp_i in clist:
					camp_i = camp_i.translate(tr)
					match = False
					for j in range(len(mdd)):
						if camp_i.startswith(mdd[j]):
							if (mdd[j] not in camp_dict):
								new_camp_list += mdd[j]+","
								camp_dict[mdd[j]] = 1
							match = True #mdd[j] already added so to prevent line 44(that adds camp as it is)
							break
					if camp_i.startswith("In depth knowledge"):
						if (mdd[1] not in camp_dict):
							new_camp_list += mdd[1]+","
							camp_dict[mdd[1]] = 1
						match = True #mdd[j] already added so to prevent line 44(that adds camp as it is)
						# break
					if camp_i.startswith("Livelihoods"):
						if "general" not in camp_dict:
							new_camp_list += "general"+","
							camp_dict["general"] = 1
						match = True
					if not match: #one of the camp matched our list, no further lookup in other camps for that item
						if camp_i not in camp_dict:
							new_camp_list += camp_i+","
				
				writer.writerow(list(data[i,:-1])+[new_camp_list[:-1]])
			else:
				writer.writerow(list(data[i,:]))