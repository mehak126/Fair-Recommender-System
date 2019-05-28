
import numpy as np
import pickle
import pandas
import csv
import seaborn as sn
import matplotlib.pyplot as plt
import pandas as pd

def main():
	
# for mdd
	main_theme = 'MDD'
	aspects = ["Basic awareness","In-depth knowledge","Serial appreciation and feedback","Factors influencing practice","Existing practice","general","Livelihoods (employment included)","Status of the women","Entitlements (social and govt.)","Positive change - In behaviour/ action","Social issues","Iron deficiency/ anemia"]
	eff_aspects = ["Basic awareness","Serial appreciation and feedback","general","Status of the women","Iron deficiency/ anemia"]

	aspect_dict = {}
	for count, aspect in enumerate(eff_aspects):
		aspect_dict[aspect] = count

	# for mdd
	aspect_dict["In-depth knowledge"] = aspect_dict["Basic awareness"]
	aspect_dict["Social issues"] = aspect_dict["Basic awareness"]
	aspect_dict["Factors influencing practice"] = aspect_dict["general"]
	aspect_dict["Existing practice"] = aspect_dict["Factors influencing practice"]
	aspect_dict["Livelihoods (employment included)"] = aspect_dict["Factors influencing practice"]
	aspect_dict["Entitlements (social and govt.)"] = aspect_dict["Factors influencing practice"]
	aspect_dict["Positive change - In behaviour/ action"] = aspect_dict["Factors influencing practice"]


#the code above creates a dictionary for the topic 'MDD', mapping each aspect to a unique number (similar to item mapping)


	with open('new_u_dict.pickle', 'rb') as handle: #created in 1_entropy_heard.py
		u_dict = pickle.load(handle)

	user_cluster_mapping = {} #mapping each user to her/his cluster
	with open('5_k_prototype.txt','r') as fr: #output of 2_k_prototype.py
		count = 0
		for line in fr:
			users = line.split()
			for user in users:
				user = user.strip()
				user_cluster_mapping[int(user)] = count
			count += 1

	num_aspects = len(eff_aspects)
	num_clusters = count

	production_map = np.zeros((num_clusters,num_aspects)) #this will map each cluster to how many items of each aspect were produced from it
	echo_mat = np.zeros((num_clusters,num_clusters)) #this will create a clusterxcluster echo chamberedness matrix

	data = pandas.read_csv('merge_11col.csv', low_memory=False).as_matrix()


	items_done = {} #counting unique items heard by power users
	power_list = {} #counting unique power listeners
	power_contr = {} #counting unique power contributors
	for i in range(data.shape[0]):
		theme = data[i][6]
		contr = str(data[i][8])
		listener = str(data[i][0])
		item = data[i][1]

		if listener not in power_list: #if it's a new listener, add to dict
				power_list[listener] = len(power_list)

		if contr not in power_contr: #if it's a new contributor, add to dict
			power_contr[contr] = len(power_contr)


		if item not in items_done: #if it's a new item, add to dict
			items_done[item] = len(items_done)

		if contr not in u_dict: #if the contributor is not a power contributor, continute (else we don't know his/her cluster)
			continue
		

		contr_id = u_dict[contr]
		cluster = user_cluster_mapping[contr_id]

		if listener in u_dict:
			listener_id = u_dict[listener]
			listener_cluster = user_cluster_mapping[listener_id]
			echo_mat[listener_cluster][cluster] += 1

		if theme != main_theme:
				continue
		
		aspects = data[i][10]
		if type(aspects) != str:
			continue
		aspects = aspects.split(',')
		for aspect in aspects:
			aspect = aspect.strip()
			if aspect not in aspect_dict.keys():
				continue
			aspect_num = aspect_dict[aspect]
			production_map[cluster][aspect_num] += 1




	# print(production_map)
	print(production_map)
	map_sum = np.sum(production_map,axis = 1)
	print(map_sum)
	final = []
	for i in range(production_map.shape[0]): #for each cluster
		div = map_sum[i]
		if div == 0:
			div = 1
		final.append(production_map[i]*100.0/div)
	final = np.array(final)
	print("Distribution of production of aspects in clusters\n")
	print(final)
	print("Cluster listenership")
	print(echo_mat)

	df_cm = pd.DataFrame(echo_mat)#, index = [i for i in "ABCDEFGHIJK"],columns = [i for i in "ABCDEFGHIJK"])
	plt.figure(figsize = (10,7))
	sn.heatmap(df_cm, annot=True)	
	plt.savefig('echo.png')
	plt.show()
	


	df_cm = pd.DataFrame(final)#, index = [i for i in "ABCDEFGHIJK"],columns = [i for i in "ABCDEFGHIJK"])
	plt.figure(figsize = (10,7))
	sn.heatmap(df_cm, annot=True)	
	plt.savefig('production.png')
	plt.show()

	print("total items : ")
	print(len(items_done))


	print(len(power_list))
	print(len(power_contr))
	
















if __name__ == '__main__':
	main()