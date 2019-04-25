import numpy as np
import sys


def get_clusters(file_name):
	clusters = []
	with open(file_name,'r') as fr:
		for index, line in enumerate(fr):
			if line.rstrip().strip() == '':
				continue
			clusters.append(line.rstrip().strip().split(' '))
	clusters = np.array(clusters)
	return clusters


def get_num_users(clusters):
	num = 0
	for c in clusters:
		num += len(c)
	return num

def get_cluster_dict(clusters):
	dict1 = {}
	for index, cluster in enumerate(clusters):
		for user in cluster:
			dict1[int(user)] = index
	return dict1



def main():
	clusters1 = get_clusters(sys.argv[1])
	clusters2 = get_clusters(sys.argv[2])
	num_users = get_num_users(clusters1)

	dict1 = get_cluster_dict(clusters1)
	dict2 = get_cluster_dict(clusters2)


	A = np.zeros((2,2))

	for i in range(num_users):
		for j in range(i+1, num_users):
			cond1 = (dict1[i] == dict1[j]) #i and j in same cluster in c1
			cond2 = (dict2[i] == dict2[j]) #i and j in same clusters in c2

			if (cond1 and cond2) : #same cluster in c1 and c2
				A[1][1] += 1
			elif (not cond1) and cond2:
				A[0][1] += 1
			elif cond1 and (not cond2):
				A[1][0] += 1
			elif (not cond1) and (not cond2):
				A[0][0] += 1

	jaccard = A[1][1]/(A[0][1] + A[1][0] + A[1][1])

	print("Similarity = " + str(jaccard))



	








if __name__ == '__main__':
	main()