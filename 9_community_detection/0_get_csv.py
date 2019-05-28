import numpy as np
import pandas as pd
from collections import Counter


def main():
	negative_interaction_list = ["dtmf_*","dtmf_0","dtmf_1","dtmf_4","hangup"]
	positive_interaction_list = ["dtmf_2","dtmf_3","dtmf_5","completed"]

	data = pd.read_csv('thresh_2_5.5_contr.csv', low_memory=False, header = None).as_matrix() #data of power users

	graph = Counter() #this will store edge weights between listeners and items/themes/contributors
	num_heard = Counter()

	# contributers = Counter()
	# for i in range(data.shape[0]):
	# 	contr = data[i][8]
	# 	contributers[contr] = 1
	# print(len(contributers))


	d = {} #this is just for counting how many unique listeners there are 

	for i in range(data.shape[0]):
		user_id = data[i][0] #listener's id
		contr_id = data[i][8] #contributor's id

		# if contributers[user_id] == 0:
			# continue
		
		if user_id not in d: #if it's a new listener
			d[user_id] = 1
		
		item_id = data[i][1]
		key_pressed = data[i][4]
		source = data[i][5]
		theme = data[i][6]

		# num_heard[(user_id,source,theme)] += 1

		if key_pressed in positive_interaction_list: #uncomment according to the kind of graph you want to create (effect of positive interactions on weight)
			# graph[(user_id,item_id)] = 1
			# graph[(user_id,source,theme)] += 1
			graph[(user_id,contr_id)] += 1

		elif key_pressed in negative_interaction_list: #uncomment according to the kind of graph you want to create (effect of negative interactions on weight)
			# graph[(user_id,item_id)] = 0
			# graph[(user_id,source,theme)] -= 1
			continue
		else: #uncomment according to the kind of graph you want to create (effect of fraction heard on weight)
			total_duration = data[i][2]
			duration_heard = data[i][3]
			fraction_heard = float(duration_heard/total_duration)
			if fraction_heard > 0:
				# graph[(user_id,item_id)] = min(1, graph[(user_id,item_id)] + fraction_heard)
				if fraction_heard > 0.45:
					# graph[(user_id,source,theme)] += 1
					graph[(user_id,contr_id)] += 1
				# else:
					# graph[(user_id,source,theme)] -= 1
					# graph[(user_id,contr_id)] -= 1


	print(len(d)) #this will give the number of unique listeners


	with open('graph_nodes.ncol','w') as fr: #storing the graph in the format required by igraph
		for keys in graph.keys():
			u_id = keys[0]
			i_id = keys[1]
			if i_id == 911111111111: #ignoring this contributor
				continue
			# src = keys[1]
			# th = keys[2]
			# st_id = str(src) + '.' + str(th)
			val = graph[keys]
			# val = graph[keys]/num_heard[keys]
			fr.write(str(u_id) + ' ' + str(i_id) + ' ' + str(val) + '\n')








if __name__ == '__main__':
	main()