import numpy as np
import pickle
import pandas
import csv
from scipy.stats import entropy
from scipy.spatial import distance
from collections import Counter
from collections import defaultdict

def main():
	
	data = pandas.read_csv('merge_11col.csv', low_memory=False).as_matrix()
	item_dict = {}
	
	theme_list = ['others', 'Health', 'SHG', 'Education', 'Curated Local Updates', 'Social Welfare', 'Social Entertainment', 'Livelihoods', 'Agriculture', 'PFI', 'CF', 'Social Issues', 'MDD', 'Sanitation', 'KDKK', 'VHSND', 'ORS and diarrhea management', 'KITCHEN GARDENING', 'Social Entitlements', 'Family Planning']

# lines 20-144 are for creating a dictionary which maps each aspect for the required topic to a unique number. Aspects which have to be merged are mapped to the same number


	# mdd = ["Basic awareness","In-depth knowledge","Serial appreciation and feedback","Factors influencing practice","Existing practice","general","Livelihoods (employment included)","Status of the women","Entitlements (social and govt.)","Positive change - In behaviour/ action","Social issues","Iron deficiency/ anemia"]
	# cf = ["Basic awareness - Importance of breast-milk","Basic awareness - Importance","Basic awareness - Initiation (when to start)","Myths and misconceptions - Feeding biscuits and chips","general","In-depth knowledge on age-appropriate feeding - Diversity/Food groups","In-depth knowledge on age-appropriate feeding - Consistency of food","In-depth knowledge on age-appropriate feeding - Frequency/ intervals","In-depth knowledge on age-appropriate feeding - Importance of nutrition for children","Livelihoods (employment included)","Social issues","Serial appreciation and feedback","Factors influencing practice - role of health- workers","Positive change - In behaviour/ action","Positive change - In awareness","Other important factors - Hygiene while cooking","Other important factors - Separate utensils","Other important factors - kitchen garden","Other important factors - Feeding difficult and weak children"]
	# fp = ["Basic awareness: Importance of family planning- Better health of mother and children","Basic awareness: Importance of family planning - Socio-cultural well-being","Basic awareness: Importance of family planning -  Economic well-being","Basic awareness: Importance of family planning - Others","In-depth knowledge about elements of family planning - Delay in first pregnancy","In-depth knowledge about elements of family planning - Delay in first pregnancy","In-depth knowledge about elements of family planning - Gap between pregnancies","In-depth knowledge about elements of family planning - Limiting family size","Status of the women/ family - number of children","Status of the women/ family  - Number of pregnancies","Contraceptive measures - Pills for women","Contraceptive measures - Others","Contraceptive measures - Vasectomy/ nasbandi for men","Social issues","Initiatives","Discussion in SHG meeting - About importance of family planning","Serial appreciation and feedback - Positive"
# ,"entertainment"]
	# ors = ["In depth knowledge - symptoms of diarrhea","In depth knowledge - preparation","In depth knowledge - symptoms of diarrhea","In depth knowledge - dosage","In depth knowledge - importance of hygiene and hand wash","Basic awareness- importance","Basic awareness- importance","General 1 364"]
	# ed = ["Bal sansad/ Meena manch","Career counselling - teacher interview"]
	soc = ["Kanya Suraksha Yojana - grievance","Kanya Suraksha Yojana - information","Kanya Suraksha Yojana - others (experience sharing, etc)","Bridhdha pension - information","Bridhdha pension - grievance","Bridhdha pension - others","Vidhva pension - information","Vidhva pension - grievance","PHC-CHC - information","PHC-CHC - grievance","PHC-CHC - others","VHSND - information"]


	# print(mdd)
	# mdd_eff = ["Basic awareness","Serial appreciation and feedback","general","Status of the women","Iron deficiency/ anemia"]
	# cf_eff = ["Basic awareness - Importance of breast-milk", "Myths and misconceptions - Feeding biscuits and chips", "general", "In-depth knowledge on age-appropriate feeding - Diversity/Food groups", "Serial appreciation and feedback", "Other important factors - Hygiene while cooking"]
	# fp_eff = ["Basic awareness", "In-depth knowledge", "Status of the women", "Contraceptive measures"]#, "Initiatives", "Discussion in SHG meeting", "Serial appreciation and feedback", "entertainment"]
	# ors_eff = ["In depth knowledge", "Basic awareness", "Member- SHG"]
	# ed_eff = ed
	soc_eff = ['Kanya Suraksha Yojana', 'Bridhdha pension', 'Vidhva pension', 'PHC-CHC', 'VHSND']

	# print(len(cf_eff))
	# print(mdd_eff)
	# print(len(mdd))
	# print(len(mdd_eff))
	# exit()
	# num_aspects = len(mdd_eff) #for MDD
	# num_aspects = len(cf_eff)
	# num_aspects = len(fp_eff)
	num_aspects = len(soc_eff)

	print(num_aspects)

	# mdd_dict = {}
	# cf_dict = {}
	# fp_dict = {}
	# ors_dict = {}
	# ed_dict = {}
	soc_dict = {}

	# for count,aspect in enumerate(mdd_eff):
	# 	mdd_dict[aspect] = count
	
	# mdd_dict["In-depth knowledge"] = mdd_dict["Basic awareness"]
	# mdd_dict["Social issues"] = mdd_dict["Basic awareness"]

	# mdd_dict["Factors influencing practice"] = mdd_dict["general"]
	# mdd_dict["Existing practice"] = mdd_dict["Factors influencing practice"]
	# # mdd_dict["Livelihoods (employment included)"] = mdd_dict["general"]s
	# mdd_dict["Livelihoods (employment included)"] = mdd_dict["Factors influencing practice"]
	# mdd_dict["Entitlements (social and govt.)"] = mdd_dict["Factors influencing practice"]
	# mdd_dict["Positive change - In behaviour/ action"] = mdd_dict["Factors influencing practice"]


	# for count,aspect in enumerate(fp_eff):
	# 	fp_dict[aspect] = count
	
	# cf_dict["Basic awareness - Importance"] = cf_dict["Basic awareness - Importance of breast-milk"]
	# cf_dict["Basic awareness - Initiation (when to start)"] = cf_dict["Basic awareness - Importance of breast-milk"]
	# cf_dict["Social issues"] = cf_dict["Basic awareness - Importance of breast-milk"]

	# cf_dict["Factors influencing practice - role of health- workers"] = cf_dict["general"]
	# cf_dict["Positive change - In behaviour/ action"] = cf_dict["general"]
	# cf_dict["Positive change - In awareness"] = cf_dict["general"]
	# cf_dict["Livelihoods (employment included)"] = cf_dict["general"]


	# cf_dict["In-depth knowledge on age-appropriate feeding - Consistency of food"] = cf_dict["In-depth knowledge on age-appropriate feeding - Diversity/Food groups"]
	# cf_dict["In-depth knowledge on age-appropriate feeding - Frequency/ intervals"] = cf_dict["In-depth knowledge on age-appropriate feeding - Diversity/Food groups"]
	# cf_dict["In-depth knowledge on age-appropriate feeding - Importance of nutrition for children"] = cf_dict["In-depth knowledge on age-appropriate feeding - Diversity/Food groups"]


	# cf_dict["Other important factors - Separate utensils"] = cf_dict["Other important factors - Hygiene while cooking"]
	# cf_dict["Other important factors - kitchen garden"] = cf_dict["Other important factors - Hygiene while cooking"]
	# cf_dict["Other important factors - Feeding difficult and weak children"] = cf_dict["Other important factors - Hygiene while cooking"]

	# fp_dict["Basic awareness: Importance of family planning- Better health of mother and children"] = fp_dict["Basic awareness"]
	# fp_dict["Basic awareness: Importance of family planning - Socio-cultural well-being"] = fp_dict["Basic awareness"]
	# fp_dict["Basic awareness: Importance of family planning -  Economic well-being"] = fp_dict["Basic awareness"]
	# fp_dict["Basic awareness: Importance of family planning - Others"] = fp_dict["Basic awareness"]
	# fp_dict["Social issues"] = fp_dict["Basic awareness"]

	# fp_dict["In-depth knowledge about elements of family planning - Delay in first pregnancy"] = fp_dict["In-depth knowledge"]
	# fp_dict["In-depth knowledge about elements of family planning - Delay in first pregnancy"] = fp_dict["In-depth knowledge"]
	# fp_dict["In-depth knowledge about elements of family planning - Gap between pregnancies"] = fp_dict["In-depth knowledge"]
	# fp_dict["In-depth knowledge about elements of family planning - Limiting family size"] = fp_dict["In-depth knowledge"]

	# fp_dict["Status of the women/ family - number of children"] = fp_dict["Status of the women"]
	# fp_dict["Status of the women/ family  - Number of pregnancies"] = fp_dict["Status of the women"]

	# fp_dict["Contraceptive measures - Pills for women"] = fp_dict["Contraceptive measures"]
	# fp_dict["Contraceptive measures - Others"] = fp_dict["Contraceptive measures"]
	# fp_dict["Contraceptive measures - Vasectomy/ nasbandi for men"] = fp_dict["Contraceptive measures"]

	# # fp_dict["Discussion in SHG meeting - About importance of family planning"] = fp_dict["Discussion in SHG meeting"]

	# for count,aspect in enumerate(ors_eff):
	# 	ors_dict[aspect] = count

	# ors_dict["In depth knowledge - symptoms of diarrhea"] = ors_dict["In depth knowledge"]
	# ors_dict["In depth knowledge - preparation"] = ors_dict["In depth knowledge"]
	# ors_dict["In depth knowledge - symptoms of diarrhea"] = ors_dict["In depth knowledge"]
	# ors_dict["In depth knowledge - dosage"] = ors_dict["In depth knowledge"]
	# ors_dict["In depth knowledge - importance of hygiene and hand wash"] = ors_dict["In depth knowledge"]

	# ors_dict["Basic awareness- importance"] = ors_dict["Basic awareness"]	
	# ors_dict["Basic awareness- importance"] = ors_dict["Basic awareness"]	

	for count,aspect in enumerate(soc_eff):
		soc_dict[aspect] = count

	soc_dict["Kanya Suraksha Yojana - grievance"] = soc_dict["Kanya Suraksha Yojana"]
	soc_dict["Kanya Suraksha Yojana - grievance"] = soc_dict["Kanya Suraksha Yojana"]
	soc_dict["Kanya Suraksha Yojana - others (experience sharing, etc)"] = soc_dict["Kanya Suraksha Yojana"]


	soc_dict["Bridhdha pension - information"] = soc_dict["Bridhdha pension"]
	soc_dict["Bridhdha pension - grievance"] = soc_dict["Bridhdha pension"]
	soc_dict["Bridhdha pension - others"] = soc_dict["Bridhdha pension"]

	soc_dict["Vidhva pension - information"] = soc_dict["Vidhva pension"]
	soc_dict["Vidhva pension - grievance"] = soc_dict["Vidhva pension"]

	soc_dict["PHC-CHC - information"] = soc_dict["PHC-CHC"]
	soc_dict["PHC-CHC - grievance"] = soc_dict["PHC-CHC"]
	soc_dict["PHC-CHC - others"] = soc_dict["PHC-CHC"]

	soc_dict["VHSND - information"] = soc_dict["VHSND"]
















	theme_dict = {} #mapping each theme to a unique numbrt
	for i in range(len(theme_list)):
		theme_dict[theme_list[i]] = i
	
	clst_avg = [] #obtaining average cluster preferences for each cluster from the pickle files produced in the analysis code (analysis.py)
	with open('cluster_0.pickle', 'rb') as handle:
		clst_avg.append(pickle.load(handle))
	with open('cluster_1.pickle', 'rb') as handle:
		clst_avg.append(pickle.load(handle))
	with open('cluster_2.pickle', 'rb') as handle:
		clst_avg.append(pickle.load(handle))
	with open('cluster_3.pickle', 'rb') as handle:
		clst_avg.append(pickle.load(handle))
	with open('cluster_4.pickle', 'rb') as handle:
		clst_avg.append(pickle.load(handle))
	# with open('cluster_5.pickle', 'rb') as handle:
	# 	clst_avg.append(pickle.load(handle))
	# with open('cluster_6.pickle', 'rb') as handle:
	# 	clst_avg.append(pickle.load(handle))


	clst_avg = np.array(clst_avg)   #stores average cluster preferences for each cluster
	
	with open('new_u_dict_equal_rates.pickle', 'rb') as handle: #new user dictionary created in 1_entropy.py
		u_dict = pickle.load(handle)

	#print(u_dict)

	with open('user_preferences_equal_rates.txt', 'r') as fr: 
		content = fr.read().split('\n')

	input_data = [ np.array(list(map(float,x.strip().split(' ')))) for x in content]
	pref = np.array(input_data)


	print("CREATING ASPECT VECTOR")
	all_items = Counter(data[:,1]) #all unique items
	num_unique_items = len(all_items)
	# print(num_unique_items)
	aspect_vec = np.zeros((num_unique_items, num_aspects))

	# num_multiple_items = 0

	# for item_num,item in enumerate(all_items):
	# 	if item_num % 500 == 0:
	# 		print(item_num)
	# 	count = 0 # counting number of aspects each item is mapped to
	# 	entries = np.where(data[:,1] == item)
	# 	for entry in entries[0]:
	# 		theme = data[entry][6]
	# 		if theme != 'MDD':
	# 			continue
	# 		aspects = data[entry][10]
	# 		if type(aspects) != str:
	# 			continue
	# 		aspects = aspects.split(',')
	# 		for aspect in aspects:
				

	# 			if aspect_vec[item_num][mdd_dict[aspect]] == 0:
	# 				count += 1
	# 			aspect_vec[item_num][mdd_dict[aspect]] = 1

	# 	if count > 1:
	# 		num_multiple_items += 1
		
	# print(num_multiple_items)

	# print("Aspect mapping done.")




	##########FOR CONSIDERING MULTIPLE ASPECTS, UNCOMMENT THIS CODE (BELOW) #############

	num_multiple_items = 0
	i_d = {}
	for i in range(data.shape[0]):
		item = data[i][1]
		theme = data[i][6]
		# if theme != 'MDD':
		if theme != 'Social Entitlementst':
			continue
		if item not in i_d:
			i_d[item] = len(i_d)
		else:
			continue
		aspects = data[i][10]
		if type(aspects) != str:
			continue
		aspects = aspects.split(',')
		count = 0
		for aspect in aspects:
			# if aspect not in mdd:
			aspect = aspect.strip()
			# print(aspect)
			if aspect not in soc_dict.keys():
				continue
			print(soc_dict[aspect])
			
			count += 1

			# aspect_vec[i_d[item]][mdd_dict[aspect]] = 1
			aspect_vec[i_d[item]][soc_dict[aspect]] = 1
		if count > 1:
			num_multiple_items += 1
	print("Aspect mapping done")
	print("NUMBER OF ITEMS WITH MULTIPLE ASPECTS = " + str(num_multiple_items))

	# print(i_d)

	# with open('mdd_items.pickle', 'wb') as handle:
	with open('soc_items.pickle', 'wb') as handle:
		pickle.dump(i_d,handle)




	
	unknown_contr_items = 0
	items_done = 0
	
	with open('features_equal_rates_soc.csv', 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter=',', dialect="excel")
		for i in range(data.shape[0]):
			item = data[i,1]
			# if data[i,6] != 'MDD':
			if data[i,6] != 'Social Entitlements':
				continue
			if item not in item_dict:
				item_dict[item] = 1
				contr = str(data[i,8])
				if contr in u_dict:
					contr_pref = pref[u_dict[contr]][:100]
				else:
					unknown_contr_items += 1
					contr_pref = np.zeros((clst_avg.shape[1]))			# no unique preference

				entropies = np.zeros(clst_avg.shape[0])
				for c in range(clst_avg.shape[0]):
					entropies[c] = entropy( clst_avg[c]+1, contr_pref+1 )
					# entropies[c] = distance.euclidean(clst_avg[c], contr_pref)
					# entropies[c] = distance.cosine(clst_avg[c]+1, contr_pref+1)
				
				log_entropies = list((-1 * np.log(entropies)))
				# scaled_entropies = entropies * 10**5

				# context_intensity = clst_avg - contr_pref
				# writer.writerow([data[i,9], theme_dict[data[i,6].strip()]]+list(log_entropies))
				writer.writerow([data[i,9]] + list(map(int,aspect_vec[items_done])) + list(log_entropies))
				items_done += 1
	# print(unknown_contr_items)	


##########FOR CONSIDERING MULTIPLE ASPECTS, UNCOMMENT THIS CODE (ABOVE) #############



if __name__ == '__main__':
	main()