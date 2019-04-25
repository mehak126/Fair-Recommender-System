import numpy as np
from collections import Counter
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from sklearn.preprocessing import StandardScaler
from kmodes.kprototypes import KPrototypes
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)

def main():
	file_name = 'cat_user_data_10_equal_rates.txt' #output file produced in 1_entropy_heard.py
	n_clusters = 5 #set this after generating elbow curve first
	n_components = 60 #number of components of vector to be preserved in case dimensionality reduction (PCA) is applied

	# myfile = open(file_name)
	# all_data = myfile.read().split('\n')
	# myfile.close()

	# dim = all_data[0].split(' ') #first line of file contains dimensions of data
	# dim = list(map(int, dim))

	# matrix = []
	# for i in range(1, dim[0]+1):
	# 	all_data[i] = all_data[i].strip()
	# 	lis = list(map(float,all_data[i].split(' ')))
	# 	matrix.append(np.array(lis))

	matrix = []
	with open(file_name,'r') as fr:
		for line in fr:
			line = line.strip()
			lis = list(map(float,line.split(' ')))
			matrix.append(np.array(lis))


	

	matrix = np.array(matrix)
	num_rows = matrix.shape[0]
	num_cols = matrix.shape[1]

# normalise
	matrix = StandardScaler().fit_transform(matrix)

	# print(matrix.shape)

	# apply dimensionality reduction on first half
	pref_mat = matrix[:,  :int(num_cols/2) ]
	
	# with reduction
	# pca = PCA(n_components=n_components, random_state = 12).fit(matrix)
	# mat = pca.transform(matrix)
	# print(np.sum(pca.explained_variance_ratio_))
	# print(len(pca.explained_variance_ratio_))
	# final_matrix = np.concatenate( (mat, matrix[:, int(num_cols/2): ]) , axis = 1)

	# without reduction
	mat = pref_mat
	final_matrix = matrix

	
	categorical = np.arange(mat.shape[1] , final_matrix.shape[1] ,1) #categorical part of vector (wether user has heard that sourcextheme pair or not)
	
# Uncomment lines 62-79 for plotting elbow curve in range specified in variable K. After selecting suitable k, update variable n_clusters in line 18

	# cost = []
	# K = range(2,20)
	# for num_clusters in K:
	# 	test=KPrototypes(n_clusters=num_clusters, verbose = 1)
	# 	clusters = test.fit_predict(final_matrix, categorical= list(categorical))
	# 	clusters = np.array(clusters)
	# 	intra_dist = (test.cost_) / final_matrix.shape[0]
	# 	centroids = np.array(test.cluster_centroids_[0])
	# 	print(centroids.shape)
	# 	inter_dist = (np.sum(cdist(centroids, centroids, 'euclidean'))/(2*num_clusters))
	# 	cost.append(intra_dist / inter_dist)

	# plt.plot(K, cost, 'bx-')
	# plt.xlabel('k')
	# plt.ylabel('Cost')
	# plt.title('The Elbow Method showing the optimal k')
	# plt.show()
	# exit()

	test=KPrototypes(n_clusters=n_clusters, verbose = 1)
	clusters = test.fit_predict(final_matrix, categorical= list(categorical))
	clusters = np.array(clusters)
	tsne = TSNE(n_components=2, verbose=1, random_state = 12)
	tsne_results = tsne.fit_transform(pref_mat)
	plt.scatter(tsne_results[:,0], tsne_results[:,1])
	plt.show()
	plt.close()

	colours = get_cmap(n_clusters+1)

	coordinate_list = []
	for i in range(n_clusters):
		coordinate_list.append([])
	
	for i in range(len(clusters)):
		coordinate_list[clusters[i]].append(tsne_results[i])


	for i in range(n_clusters):
		X = []
		Y = []
		for j in range(len(coordinate_list[i])):
			X.append(coordinate_list[i][j][0])
			Y.append(coordinate_list[i][j][1])
		plt.scatter(X, Y, c = colours(i))
	plt.show()
	plt.close()
	
	f = open(str(n_clusters) + '_k_prototype_equal_rates.txt', 'w')
	for k in range(n_clusters):
		cluster = [i for i in range(matrix.shape[0]) if clusters[i] == k]
		for c in cluster:
			f.write(str(c) + " ")
		f.write('\n')
	f.close()
	count = Counter(clusters)
	print(count)








if __name__ == '__main__':
	main()