import numpy as np 
import pandas
import csv
import matplotlib.pyplot as plt


if __name__ == '__main__':
	data = pandas.read_csv('thresh_2.5_5.csv', delimiter=',',header = None, low_memory=False).as_matrix()

	theme_item = {}
	n_themes = 21
	unique = {}
	y = []
	print("num users per theme count")
	for  i in range(n_themes):
		print(i, np.sum(data[:, 6] == i)/data.shape[0])
		y.append(np.sum(data[:, 6] == i)/data.shape[0])

	x = [i for i in range(n_themes)]
	themes_list = ['NA', 'others', 'Health', 'SHG', 'Education', 'Curated Local Updates', 'Social Welfare', 'Social Entertainment', 'Livelihoods', 'Agriculture', 'PFI', 'CF', 'Social Issues', 'MDD', 'Sanitation', 'KDKK', 'VHSND', 'ORS and diarrhea management', 'KITCHEN GARDENING', 'Social Entitlements', 'Family Planning']
	fig_size = [200, 200]
	plt.rcParams["figure.figsize"] = fig_size
	plt.bar(x, y)
	plt.xticks(x, themes_list,rotation=90)
	plt.xlabel('Themes')
	plt.ylabel('Number of users')
	plt.title('Distribution of users according to themes')
	plt.show()
	plt.close()

	for i in range(data.shape[0]):
		if data[i, 6] in theme_item:
			if data[i, 1] not in theme_item[data[i, 6]]:
				theme_item[data[i, 6]][data[i, 1]] = 1
			else:
				theme_item[data[i, 6]][data[i, 1]] += 1
		else:
			theme_item[data[i, 6]] = {}
			theme_item[data[i, 6]][data[i, 1]] = 1

		if data[i, 1] not in unique:
			unique[data[i, 1]] = 1



	print("\n")
	print("items per theme count ", len(unique.keys())) 
	tot_items = 0
	for th in theme_item:
		tot_items += len(theme_item[th].keys())
		print(th, len(theme_item[th].keys()))

	print("\n")
	print("items per theme percentage ", tot_items)
	y = []
	for th in theme_item:
		print(th, len(theme_item[th].keys())/tot_items)
		y.append(len(theme_item[th].keys())/tot_items)

	plt.bar(x, y)
	plt.xlabel('Themes')
	plt.ylabel('items%')
	plt.title('Distribution of items according to themes')
	plt.xticks(x, themes_list, rotation=90)
	plt.show()
	plt.close()