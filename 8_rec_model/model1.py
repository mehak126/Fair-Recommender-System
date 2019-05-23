# Inputs
# r : number of rank slots
# k : number of intervals
# T : total time duration
# min_exp : min % exposure to give to each aspect
# aspect_item_dict : pickled dictionary of aspects with items mapped to them which were positive
# r_file : file containing number of users coming to rank i per minute

# A time slot of time T is divided into k intervals. In each interval we rank r items

import numpy as np
import sys
from collections import Counter
import pickle



def hhi(exp):
	k = exp.shape[0]
	num_aspects = exp.shape[1]
	tot_exp = np.sum(exp, axis = 1) #tottal exposure in each interval
	x = exp.T/tot_exp
	x = x.T #dim = num intervals * aspects; contains percent of exp given to aspect in that interval
	hhi_var = np.sum(x*x, axis = 1)
	return hhi_var
	return np.sum(hhi_var)/len(hhi_var)


def main():
	r = int(sys.argv[1])
	k = int(sys.argv[2])
	T = float(sys.argv[3])
	min_exp = float(sys.argv[4])
	aspect_item_dict_file = sys.argv[5]
	r_file = sys.argv[6]

	R = np.zeros(r) #matrix of num users coming to rank i per minute
	sum_r = 0
	with open(r_file,'r') as fr:
		count = 0
		for line in fr:
			R[count] = float(line.strip())
			sum_r += R[count]
			count += 1
			if count == r:
				break


	with open(aspect_item_dict_file,'rb') as handle:
		aspect_item_dict_id = pickle.load(handle)[0]

	item_mapping = {}
	aspect_item_dict = {}
	item_counter = 0
	for key in aspect_item_dict_id.keys():
		aspect_item_dict[key] = []
		for item_id in aspect_item_dict_id[key]:
			item_mapping[item_counter] = item_id
			aspect_item_dict[key].append(item_counter)
			item_counter += 1

	total_exposure = sum_r * T
	print("total_exposure = " + str(total_exposure))

	num_aspects = len(aspect_item_dict)

	min_time_per_aspect = (min_exp*total_exposure)/100
	rem_time = total_exposure - (min_time_per_aspect*num_aspects)
	print("min_time_per_aspect = " + str(min_time_per_aspect))
	print("rem_time = " + str(rem_time))

	rem_time_ratio = np.zeros(num_aspects)
	total_items = 0
	for i in range(num_aspects):
		rem_time_ratio[i] = len(aspect_item_dict[i]) # remaining time to be divided in ratio of number of +ve items in that aspect
		# print(str(i) + ": " + str(len(aspect_item_dict[i])))
		total_items += len(aspect_item_dict[i])

	rem_time_div = np.zeros(num_aspects)
	for i in range(num_aspects):
		rem_time_div[i] = (rem_time*rem_time_ratio[i])/(r*k) #divide remaining time in remaining time ratio of aspects
		# rem_time_div[i] = (rem_time*rem_time_ratio[i])/total_items #divide remaining time in remaining time ratio of aspects
	
	print(rem_time_div)
	print(rem_time_ratio)
	# E_desired = np.array(total_items) #desired exposure for each item
	E_desired = Counter()
	E_remaining = Counter()
	item_aspect = np.zeros(total_items) #array where ith pos gives aspect of ith item
	for i in range(num_aspects):
		aspect_items = aspect_item_dict[i]
		num_items = len(aspect_items)
		min_asp_exp = min_time_per_aspect/num_items #minimum aspect exposure
		add_asp_exp = rem_time_div[i]/num_items #additional exposure to be given to that aspect
		for item in aspect_items:
			E_desired[item] = min_asp_exp + add_asp_exp
			E_remaining[item] = E_desired[item]
			item_aspect[item] = i

	# for key in E_desired.keys():
	# 	print(str(key) + " : " + str(E_desired[key]))

	#Elisa Algo with twist
	print("\n\n")
	# b -> the number of positions after which condition is to be checked
	b = 5 #???
	# b2 = 0.5
	print("E_desired of items of each aspect ")
	print(E_desired[0])
	print(E_desired[110])
	print(E_desired[150])
	print(E_desired[161])
	print(E_desired[165])
	print("\n\n")

	E_mila_aspect = np.zeros(num_aspects)
	E_mila_item = np.zeros(total_items)
	
	E_aspect_int = np.zeros((k, num_aspects))
	for i in range(k): #for each interval
		num_items_displayed = np.zeros(num_aspects) #number of items of each aspect displayed so far
		cur_constraint = b
		e_list = (E_remaining.most_common()) #list sorted by exposure
		# print(e_list)
		
		curr_index = 0
		items_shown = np.zeros(total_items)
		print("\nLIST " + str(i))
		for j in range(r): #the r items to be ranked	

			next_index = curr_index
			next_item = e_list[next_index][0]
			next_aspect = item_aspect[next_item]

			# print("RHS = " + str(int(cur_constraint * rem_time_div[int(next_aspect)])))
			# print("cur_constraint = " + str(int(cur_constraint * rem_time_ratio[int(next_aspect)]/(r*k))))
			constraint = (num_items_displayed[int(next_aspect)] <= int(cur_constraint * rem_time_ratio[int(next_aspect)]/(total_items)))
			# print(num_items_displayed[int(next_aspect)])
			# print(constraint)

			while ((not constraint) or (items_shown[next_item] == 1)) :

				next_index += 1
				if next_index >= total_items: #all items are violating constraint
					next_index = curr_index #just put current item
					next_item = e_list[next_index][0]
					next_aspect = item_aspect[next_item]
					break
				next_item = e_list[next_index][0]
				next_aspect = item_aspect[next_item]
				constraint = (num_items_displayed[int(next_aspect)] <= int(cur_constraint * rem_time_ratio[int(next_aspect)]/(total_items)))
				



			if ((j+b+1)%b == 0): #at every bth position, update cur_constraint
				#check constraint
				
				# constraint = (num_items_displayed[int(next_aspect)] <= int(j* rem_time_ratio[int(next_aspect)])) #confirm rhs
				# while not constraint:
				# 	# if i == 3:
				# 		# print("Here!!")
				# 	next_index += 1
				# 	if next_index >= total_items:
				# 		next_index = curr_index
				# 		break

				# 	next_item = e_list[next_index][0]
				# 	next_aspect = item_aspect[next_item]
				# 	constraint = (num_items_displayed[int(next_aspect)] <= int(j* rem_time_ratio[int(next_aspect)])) #confirm rhs
				# print("J = " + str(j+b))
				cur_constraint = j+b+1



			

			
			# print(str(item_mapping[next_item]) + " : Aspect : " + str(int(next_aspect)))
			print(str(next_item) + " : Aspect : " + str(int(next_aspect)))
			items_shown[next_item] = 1
			num_items_displayed[int(next_aspect)] += 1
			E_remaining[next_item] -= (R[j]*T)/k #e_mila seen from manish pranav's code
			# print(str(next_item) + " : Aspect : " + str(int(next_aspect)) + " : E_remaining : " + str(E_remaining[next_item]) + " : E Received = " + str((R[j]*T)/k))
			E_mila_aspect[int(next_aspect)] += (R[j]*T)/k
			E_aspect_int[i, int(next_aspect)] += (R[j]*T)/k
			E_mila_item[next_item] += (R[j]*T)/k
			if next_index != curr_index: #curr_index won't change
				continue
			else:
				curr_index += 1
				if curr_index >= total_items:
					curr_index = 0
				while(items_shown[curr_index] != 0):
					curr_index += 1
					if curr_index >= total_items:
						print("OMG WTF")
						exit()
						curr_index = 0
						items_shown = np.zeros(total_items)

			# print("\n")

	print("\n\nExposure Received by Different Aspects:")
	for i in range(len(E_mila_aspect)):
		print("Aspect " + str(i) + ": " + str(E_mila_aspect[i]))
	print("Num items of different aspects:")
	print(rem_time_ratio)
	print("ratio of exposure acheived:")
	min_ratio = min(E_mila_aspect)
	print([x/min_ratio for x in E_mila_aspect])

	print("\n\nExposure Received by Different items:")
	for i in range(len(E_mila_item)):
		print("item " + str(i) + ": " + str(E_mila_item[i]))

	#create file for aspect analysis
	with open("aspect_exp_1.txt",'w') as fw:
		for i in range(num_aspects):
			fw.write(str(E_mila_aspect[i]) + '\n')
	

	with open('res1.pickle', 'wb') as handle:
		pickle.dump(E_mila_item, handle, protocol=pickle.HIGHEST_PROTOCOL)

# 	print("{0:.3f}".format(hhi(E_aspect_int)))

	with open('hhi1.pickle', 'wb') as handle:
		pickle.dump(hhi(E_aspect_int), handle, protocol=pickle.HIGHEST_PROTOCOL)


	with open("item_exp_1.csv",'w') as fw:
		for i in range(total_items):
			fw.write(str(item_mapping[i]) + ',' + str(E_mila_item[i]) + '\n')







if __name__ == '__main__':
	main()

