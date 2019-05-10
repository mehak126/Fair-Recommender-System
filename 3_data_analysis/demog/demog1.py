import numpy as np 
import pandas
import csv
from collections import Counter
import pickle
from statsmodels.stats.weightstats import ztest
import matplotlib.pyplot as plt


def modify(d, val):
	for key in d:
		d[key] = round(d[key]/val, 2)

def plot(x1, x2):
	x = [i for i in range(20)]
	plt.plot(x, x1,color='red')
	plt.plot(x, x2,color='blue')
	plt.scatter(x, x1,color='red')
	plt.scatter(x, x2,color='blue')
	plt.savefig("demog_topic_like.png")
	plt.show()


if __name__ == '__main__':

	# data = pandas.read_csv('thresh_2.5_5.csv', delimiter=',',  low_memory=False, header= None).as_matrix()
	data = pandas.read_csv('../../Data/merge_11col.csv', low_memory=False).as_matrix()
	demo1 = pandas.read_excel('SV1.xlsx').as_matrix()
	demo2 = pandas.read_excel('SV2.xlsx').as_matrix()

	negative_interaction_list = ["dtmf_*","dtmf_0","dtmf_1","dtmf_4","hangup"]
	positive_interaction_list = ["dtmf_2","dtmf_3","dtmf_5","dtmf_6","completed"]


	with open('item_asp_map.pickle', 'rb') as handle:
		item_asp_map = pickle.load(handle)

	with open('../../Data/cf/u_dict.pickle', 'rb') as handle:
		u_dict = pickle.load(handle)

	user_gend = {} #user gender dictionary
	count = 0
	for i in range(demo1.shape[0]):
		user = str(demo1[i,1]) #phone number
		gender = demo1[i,3]
		user_gend[user] = gender

	asp_list = ["Basic awareness","Serial appreciation and feedback","general","Status of the women","Iron deficiency/ anemia"]


	# aspect wise
	# female = np.zeros(len(asp_list))
	# male = np.zeros(len(asp_list))
	# for i in range(data.shape[0]):
	# 	user = str(data[i, 0])
	# 	if (user not in user_gend) or (user not in u_dict):		# if gender not known -> dont consider or not power user -> dont consider  
	# 		continue
	# 	item = data[i,1]
	# 	if item not in item_asp_map:		# if item is not o that particular topic ignore
	# 		continue
	# 	asp = item_asp_map[item]
	# 	gender = user_gend[user]
	# 	if gender == 'Mahila':
	# 		female[asp] += 1
	# 	elif gender.strip() == 'Purush':
	# 		male[asp] += 1

	# print(female)
	# print(male)
	# female /= np.sum(female)
	# male /= np.sum(male)
	# print(female)
	# print(male)

	# z = ztest(female, x2=male)
	# print(z)


	# topic wise
	heard_percentage = 45
	skipped_percentage = 45

	female = np.zeros(20)
	male = np.zeros(20)
	count = 0
	topic_dict = {}
	for i in range(data.shape[0]):
		user = str(data[i, 0])
		if (user not in user_gend) or (user not in u_dict):		# if gender not known -> dont consider or not power user -> dont consider  
			continue

		percentage_heard = (float(data[i, 3])*100.0)/float(data[i, 2])
		
		like = 0
		if (data[i,4] in positive_interaction_list):
			like += 1
		elif (data[i,4] in negative_interaction_list):
			like -= 1
		else:
			if (percentage_heard >= heard_percentage):
				like += 1
			elif (percentage_heard < skipped_percentage):
				like -= 1

		item = data[i,1]
		gender = user_gend[user]
		topic = data[i,6]
		if topic not in topic_dict:
			topic_dict[topic] = count
			count += 1
		topic = topic_dict[topic]
		if gender == 'Mahila':
			female[topic] += like
		elif gender.strip() == 'Purush':
			male[topic] += like

	print(topic_dict)
	print(female)
	print(male)
	female /= np.sum(female)
	male /= np.sum(male)
	print(female)
	print(male)

	z = ztest(female, x2=male)
	print(z)
	plot(female, male)





	
