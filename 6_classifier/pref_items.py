import numpy as np
import pandas as pd 
import pickle, sys
import math
import random 
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import fetch_20newsgroups_vectorized
from sklearn.feature_selection import chi2
import statsmodels.api as sm
from scipy import stats
from sklearn.metrics import f1_score
from imblearn.over_sampling import SMOTE
from sklearn.feature_selection import f_regression
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

import random as rand
from sklearn.svm import SVC

# from sklearn.cross_validation import train_test_split

def plotc(cluster, x, y):
	# fig_size = [100, 100]
	# plt.rcParams["figure.figsize"] = fig_size
	plt.bar(x, y)
	plt.xticks(x, x,rotation=90)
	plt.xlabel('features')
	plt.ylabel('importance')
	plt.title('Importance of fatures in cluster '+str(cluster))
	plt.savefig('../Data/met2_45_45/nskip/forest_imp/'+str(j)+'.png')
	plt.close()

if __name__ == "__main__":

	random.seed()

	num_clusters = int(sys.argv[1])

	# datax = pd.read_csv('regression_aspect_merge_new_metric.csv', low_memory=False, header = None).as_matrix()
	datax = pd.read_csv('../Data/met2_45_45/features_equal_rates.csv', low_memory=False, header = None).as_matrix()
	# datax = pd.read_csv('../Data/3ors/features_equal_rates_ors.csv', low_memory=False, header = None).as_matrix()

	with open('../Data/met2_45_45/mdd_items.pickle', 'rb') as handle: #item_id -> index
		mdd = pickle.load(handle)

	# print(datax.shape[0])
	# print(mdd)
	# exit()

	with open('../1 SKIP/skip_rate.pickle', 'rb') as handle:
		item_sr = pickle.load(handle)

	with open('../1 SKIP/neg.pickle', 'rb') as handle:
		pos = pickle.load(handle)

	with open('../1 SKIP/item_dict.pickle', 'rb') as handle:
		sr_dict = pickle.load(handle)
	

	rev_dict = {}
	for item_id in mdd:
		rev_dict[mdd[item_id]] = item_id


	# feature_vector = ["Constant", "Rating", "Basic awareness", "In-depth knowledge", "Serial appreciation & feedback", "Factors influencing practice", "Existing practice", "general", "Livelihoods (employment included)", "Status of the women", "Entitlements (social and govt.)", "Positive change - In behaviour/ action", "Social issues", "Iron deficiency/ anemia", "Context Intensity"]
	# feature_vector = ["Constant", "Rat+ing", "Basic awareness", "In-depth knowledge", "Serial appreciation & feedback", "Factors influencing practice", "Existing practice", "general", "Status of the women", "Entitlements (social and govt.)", "Positive change - In behaviour/ action", "Social issues", "Iron deficiency/ anemia", "Context Intensity"]
	feature_vector = ["Constant","Rating","Basic awareness","Serial appreciation and feedback","general","Status of the women","Iron deficiency/ anemia","Context Intensity"]
	imp_feature = {"feature":feature_vector[1:]}

	res_pos = [{} for i in range(num_clusters)]
	res_neg = [{} for i in range(num_clusters)]

	for j in range(num_clusters):
		num_attr = datax.shape[1]
		print(num_attr)
		print(type(datax))
		print(datax.shape)
		# exit()
		l = [i for i in range(0,num_attr-num_clusters)]+[num_attr-num_clusters+j]

		X = datax[:,l]
		y = []
		item_list = []
		for i in range(len(mdd)):
			y.append(item_sr[sr_dict[rev_dict[i]], j])
			item_list.append(rev_dict[i])

		item_list = np.asarray(item_list)
		y = np.asarray(y)

		
		# oy.append(y.copy())
		
		######### distribution of data ############
		print("----- cluster "+str(j)+"------")
		# print("nan: "+str(np.sum(y==0)))
		print("nan: "+str(np.sum(np.isnan(y))))
		remove_nan = [not i for i in np.isnan(y)]

		X = X[remove_nan]
		y = y[remove_nan]
		item_list = item_list[remove_nan]

		# print(len(y))
		# print("< 0: "+str(np.sum(y < 0)))
		# print("> 0: "+str(np.sum(y > 0)))
		# print("= 0: "+str(np.sum(y == 0)))
		
		# y[y == 0] = 0
		y[y <= 0] = 0
		y[y > 0] = 1 


		# print("<= 0: "+str(np.sum(y == 0)))
		# print("> 0: "+str(np.sum(y > 0)))

		
		#used for models
		res_it_list = item_list[y==1]
		res_det = X[y==1]        #result details
		bool_l = [True for i in range(res_det.shape[0])]

		for asp in range(X.shape[1]-2):
			res_pos[j][asp] = []
		count = 0
		for i in range(res_det.shape[0]):
			asp = res_det[i,1:-1]
			# print(asp)
			# print(rev_dict[i])

			asp = np.where(asp==1)[0]
			if asp.shape[0] == 0:
				continue
			chosen_asp = rand.choice(asp)
			res_pos[j][chosen_asp].append(item_list[i])
			count += 1
		


		res_it_list = item_list[y==0]
		res_det = X[y==0]        #result details
		bool_l = [True for i in range(res_det.shape[0])]
		# print(res_det)

		for asp in range(X.shape[1]-2):
			res_neg[j][asp] = []
		count = 0
		for i in range(res_det.shape[0]):
			asp = res_det[i,1:-1]

			asp = np.where(asp==1)[0]
			if asp.shape[0] == 0:
				continue
			chosen_asp = rand.choice(asp)
			res_neg[j][chosen_asp].append(item_list[i])
			count += 1
		
	

	with open('pos_res.pickle', 'wb') as handle:
		pickle.dump(res_pos, handle, protocol=pickle.HIGHEST_PROTOCOL)

	with open('neg_res.pickle', 'wb') as handle:
		pickle.dump(res_neg, handle, protocol=pickle.HIGHEST_PROTOCOL)
		
