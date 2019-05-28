import numpy as np
import igraph as ig
from igraph import *
import louvain
import matplotlib.pyplot as plt


def is_number(label):
	return len(label) == 12

def main():
	g = Graph.Read_Ncol("graph_nodes.ncol", weights = True, directed = True)


	# partition = louvain.find_partition(g, louvain.ModularityVertexPartition)
	
	# g.vs["type"] = [is_number(name) for name in g.vs["name"]] #this is to seperate users from items in case the graph is a bipartite graph between listeners and items. Since listener ids are 12 digits long, they can be distinguished from item ids.
	# user_part = g.bipartite_projection(which = True) #project the bipartite graph into a unipartite and extract the users
	user_part = g
	
	
	cutoff_wt = 0 #set this as the minimum weight you would like for each edge. remaining will be deleted
	rem_edges = [] #for storing edges whose weight is less than the minimum cutoff

	
	for e in user_part.es():
		# print(e.index)
		# print("source: %s target: %d" % (e.source, e.target))
	# 	# print("multiplicity %d" % (g.count_multiple(e)))
	# 	# print("weight %f\n" % e['weight'])
		# if e['weight'] < min_wt:
		# 	min_wt = e['weight']
		# if e['weight'] > max_wt:
		# 	max_wt = e['weight']
		# edge_weight_dist[e['weight']] += 1
	
		if e['weight'] < cutoff_wt:
			rem_edges.append(e.index)


	user_part.delete_edges(rem_edges) #delete those edges which had weight less than cutoff weight


	# x = [i for i in range(1609)]
	# cum = [edge_weight_dist[0]]
	# for i in range(1,1609):
	# 	cum.append(cum[i-1] + edge_weight_dist[i])


	

	# print(edge_weight_dist[100])
	# plt.plot(x,edge_weight_dist)
	# plt.plot(x,cum)
	# plt.show()

	# print(min_wt)
	# print(max_wt)

	partition = louvain.find_partition(user_part, louvain.ModularityVertexPartition)
	print("PARTITION MADE")

	modularity = partition.modularity
	print(modularity) 

	

	






if __name__ == '__main__':
	main()