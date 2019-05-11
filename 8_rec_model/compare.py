import numpy as np
import sys
from collections import Counter
import pickle
import matplotlib.pyplot as plt 



def rmse(base, res):
	mean_base = np.sum(base)/len(base)
	mean_res = np.sum(res)/len(res)

	er = res-base
	ser = er*er
	mser = np.sum(ser)/(mean_res * mean_base)
	rmser = np.sqrt(mser)/len(base)
	return  rmser


def plot_rmse(hist, num):
	# random.seed(1)
	plt.figure()
	n = len(hist)
	plt.xlabel('model index')
	plt.ylabel('rmse with model '+str(num))
	plt.plot([i+1 for i in range(n)],hist)
	plt.savefig("rmse_"+str(num)+".png")

def plot_hhi(data_to_plot):
	# Create a figure instance
	fig = plt.figure()
	# Create an axes instance
	ax = fig.add_subplot(111)
	# Create the boxplot
	bp = ax.boxplot(data_to_plot)
	# Save the figure
	fig.savefig('fig1.png', bbox_inches='tight')
	## Custom x-axis labels
	ax.set_xticklabels(['Sample1', 'Sample2', 'Sample3', 'Sample4'])
	## Remove top axes and right axes ticks
	ax.get_xaxis().tick_bottom()
	ax.get_yaxis().tick_left()



def main():

	with open('Model1/res1.pickle', 'rb') as handle:
		res1 = pickle.load(handle)

	with open('Model2/res2.pickle', 'rb') as handle:
		res2 = pickle.load(handle)

	with open('Model3/res3.pickle', 'rb') as handle:
		res3 = pickle.load(handle)

	with open('Model4/res4.pickle', 'rb') as handle:
		res4 = pickle.load(handle)

	with open('Model5/res5.pickle', 'rb') as handle:
		res5 = pickle.load(handle)

	with open('Model6/res6.pickle', 'rb') as handle:
		res6 = pickle.load(handle)


	base = res5
	e = np.zeros(4)
	e[0] = rmse(base, res1)
	e[1] = rmse(base, res2)
	e[2] = rmse(base, res3)
	e[3] = rmse(base, res4)
	# e[4] = rmse(base, res5)
	plot_rmse(e, 5) #5 is the base model



	### hhi_plots 

	with open('Model1/hhi1.pickle', 'rb') as handle:
		hhi1 = pickle.load(handle)

	with open('Model2/hhi2.pickle', 'rb') as handle:
		hhi2 = pickle.load(handle)

	with open('Model3/hhi3.pickle', 'rb') as handle:
		hhi3 = pickle.load(handle)

	with open('Model4/hhi4.pickle', 'rb') as handle:
		hhi4 = pickle.load(handle)

	with open('Model5/hhi5.pickle', 'rb') as handle:
		hhi5 = pickle.load(handle)

	with open('Model6/hhi6.pickle', 'rb') as handle:
		hhi6 = pickle.load(handle)

	data_to_plot = [hhi1, hhi2, hhi3, hhi4, hhi5]
	plot_hhi(data_to_plot, num)


if __name__ == "__main__":
	main()
