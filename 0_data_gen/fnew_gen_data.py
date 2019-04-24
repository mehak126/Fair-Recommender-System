import numpy as np 
import pandas
import csv
from collections import Counter

if __name__ == '__main__':
	# d1 = pandas.read_excel('item_listenership_new_part1(1).xlsx').as_matrix()
	# # print(d1[:])
	# d2 = pandas.read_excel('item_listenership_new_part2.xlsx').as_matrix()
	# d3 = pandas.read_excel('item_listenership_new_part3.xlsx').as_matrix()
	# d4_1 = pandas.read_excel('item_listenership_new_part4_1.xlsx').as_matrix()
	# d4_2 = pandas.read_excel('item_listenership_new_part4_2.xlsx').as_matrix()
	# d5 = pandas.read_excel('item_listenership_new_part5.xlsx').as_matrix()
	d1 = pandas.read_csv('bmgf_data_1.csv', low_memory=False).as_matrix()
	d2 = pandas.read_csv('bmgf_data_2.csv', low_memory=False).as_matrix()
	d3 = pandas.read_csv('bmgf_data_3.csv', low_memory=False).as_matrix()
	d4 = pandas.read_csv('bmgf_data_4.csv', low_memory=False).as_matrix()
	d5 = pandas.read_csv('bmgf_data_5.csv', low_memory=False).as_matrix()
	d6 = pandas.read_csv('bmgf_data_6_1.csv', low_memory=False).as_matrix()
	d7 = pandas.read_csv('bmgf_data_6_2.csv', low_memory=False).as_matrix()
	d8 = pandas.read_csv('bmgf_data_7_1.csv', low_memory=False).as_matrix()
	d9 = pandas.read_csv('bmgf_data_7_2.csv', low_memory=False).as_matrix()
	d10 = pandas.read_csv('bmgf_data_8.csv', low_memory=False).as_matrix()
	data2 = pandas.read_csv('bmgf_source_theme.csv', low_memory=False).as_matrix()
	
	# data2 = np.array(data2)
	
	data1 = np.append(d1[:,:], d2[:,:], 0);
	data1 = np.append(data1, d3[:,:], 0);
	data1 = np.append(data1, d4[:,:], 0);
	data1 = np.append(data1, d5[:,:], 0);
	data1 = np.append(data1, d6[:,:], 0);
	data1 = np.append(data1, d7[:,:], 0);
	data1 = np.append(data1, d8[:,:], 0);
	data1 = np.append(data1, d9[:,:], 0);
	data1 = np.append(data1, d10[:,:], 0);


	st = {}
	dt = []
	for i in range(data2.shape[0]):
		if(type(data2[i,2]) != str):
			st[data2[i,0]] = [data2[i,1].split(","), ["NA"]]
		elif(type(data2[i,1]) != str):
			st[data2[i,0]] = ["NA", data2[i,2].split(",")]
		else:
			st[data2[i,0]] = [data2[i,1].split(","), data2[i,2].split(",")]

		if(i == 2):
			print((st[data2[i,0]][1]))
	

	missing = open('missing_data_all', 'w')
	missing_writer = csv.writer(missing, delimiter=',', dialect="excel")

	with open('new_11col.csv', 'w') as csvfile:
		errors = Counter()
		writer = csv.writer(csvfile, delimiter=',', dialect="excel")
		for i in range(data1.shape[0]):
			# print(i)
			key = data1[i, 8]
			flag = 0
			if key in st:
				for theme in st[key][1]:
					for src in st[key][0]:
						cond1 = (src == "ALL" and len(st[key][0]) == 1) or (src != "ALL")
						cond2 = (theme == "SHG" and len(st[key][1]) == 1) or (theme != "SHG")
						cond3 = (theme != 'NA')
						cond4 = (src != 'NA')

						if(cond1 and cond2 and cond3 and cond4):
							if flag == 0:
								writer.writerow([data1[i,5], data1[i,8], data1[i,17], data1[i,21], data1[i,22], src, theme, data1[i, 0], data1[i, 11], data1[i, 12], data1[i, 19]])
								flag = 1
							else:
								writer.writerow([data1[i,5], data1[i,8], data1[i,17], data1[i,21], data1[i,22], src, theme, data1[i, 0], data1[i, 11], data1[i, 12], "NA"])
						else:
							if errors[data1[i,8]] == 0:
								errors[data1[i,8]] = 1
								if not cond1:
									missing_writer.writerow([data1[i,8], 'src = ALL'] )
								elif not cond2:
									missing_writer.writerow([data1[i,8], 'theme = SHG'] )
								elif not cond3:
									missing_writer.writerow([data1[i,8], 'theme = NA'] )
								else:
									missing_writer.writerow([data1[i,8], 'src = NA'] )



	    				# elif not cond1:
	    				# 	missing_writer.writerow([data1[i,8], 'src = ALL'] )
    					# elif not cond2:
    					# 	missing_writer.writerow([data1[i,8], 'theme = SHG'] )
    					# elif not cond3:
    					# 	missing_writer.writerow([data1[i,8], 'theme = NA'] )
    					# elif not cond4:
    					# 	missing_writer.writerow([data1[i,8], 'src = NA'] )


	    	# else:
	    	# 	writer.writerow([data1[i,5], data1[i,8], data1[i,17], data1[i,21], data1[i,22], "NA", "NA", data1[i, 0]])

	missing.close()
	# d5 = pandas.read_excel('final_7col.csv').as_matrix()
	# print(.shape)
	# with open('data_comb.csv', 'w') as csvfile:
	#     writer = csv.writer(csvfile, delimiter=',', dialect="excel")
	#     for i in range(data1.shape[0]):
	#     	writer.writerow(data1[i,:])

	    
	# print(dt)

	# 17 - item duration 
	# 21 - duration
	# 22 - key_pressed