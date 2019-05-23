import numpy as np
import pandas as pd 
import pickle, sys
import math
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import fetch_20newsgroups_vectorized
from sklearn.feature_selection import chi2
import statsmodels.api as sm
from scipy import stats
from sklearn.metrics import f1_score
from imblearn.over_sampling import SMOTE
from sklearn.feature_selection import f_regression
import matplotlib.pyplot as plt



# from sklearn.cross_validation import train_test_split

def plotc(cluster, x, y):
	# fig_size = [100, 100]
	# plt.rcParams["figure.figsize"] = fig_size
	plt.bar(x, list(1-np.asarray(y)))
	plt.xticks(x, x,rotation=90)
	plt.xlabel('features')
	plt.ylabel('pvalues')
	plt.title('pvalues of features in cluster '+str(cluster))
	plt.savefig('./pvalues/'+str(j)+'.png')
	plt.close()

if __name__ == "__main__":

	num_clusters = int(sys.argv[1])

	# datax = pd.read_csv('regression_aspect_merge_new_metric.csv', low_memory=False, header = None).as_matrix()
	datax = pd.read_csv('../Data/met2_45_45/features_equal_rates.csv', low_memory=False, header = None).as_matrix()
	with open('skip_rate.pickle', 'rb') as handle:
		item_sr = pickle.load(handle)


	with open('item_dict.pickle', 'rb') as handle:
		sr_dict = pickle.load(handle)
	
	print(datax.shape)

	with open('../Data/met2_45_45/mdd_items.pickle', 'rb') as handle:
		mdd = pickle.load(handle)

	rev_dict = {}
	for item_id in mdd:
		rev_dict[mdd[item_id]] = item_id

	oy = []

	# feature_vector = ["Constant", "Rating", "Basic awareness", "In-depth knowledge", "Serial appreciation & feedback", "Factors influencing practice", "Existing practice", "general", "Livelihoods (employment included)", "Status of the women", "Entitlements (social and govt.)", "Positive change - In behaviour/ action", "Social issues", "Iron deficiency/ anemia", "Context Intensity"]
	# feature_vector = ["Constant", "Rating", "Basic awareness", "In-depth knowledge", "Serial appreciation & feedback", "Factors influencing practice", "Existing practice", "general", "Status of the women", "Entitlements (social and govt.)", "Positive change - In behaviour/ action", "Social issues", "Iron deficiency/ anemia", "Context Intensity"]
	feature_vector =  ["Constant","Rating","Basic awareness","Serial appreciation and feedback","general","Status of the women","Iron deficiency/ anemia","Context Intensity"]
	for j in range(num_clusters):
		num_attr = datax[0].shape[0]
		l = [i for i in range(0,num_attr-num_clusters)]+[num_attr-num_clusters+j]
		# print(l)
		# continue
		X = datax[:,l]
		y = []
		for i in range(len(mdd)):
			y.append(item_sr[sr_dict[rev_dict[i]], j])
		y = np.asarray(y)
		# oy.append(y.copy())
		
		######### distribution of data ############
		print("----- cluster "+str(j)+"------")
		print("nan: "+str(np.sum(np.isnan(y))))
		remove_nan = [not i for i in np.isnan(y)]
		# y[] = 0
		# print(len(remove_nan))
		# print(len(y))
		y_n = y[remove_nan]
		print("< 0: "+str(np.sum(y_n < 0)))
		print("> 0: "+str(np.sum(y_n > 0)))
		print("= 0: "+str(np.sum(y_n == 0)))

		X = X[remove_nan]
		y = y[remove_nan]

		
		# print("< 0: "+str(np.sum(y < 0)))
		# print("> 0: "+str(np.sum(y > 0)))
		# print("= 0: "+str(np.sum(y == 0)))
		y[y <= 0] = 0
		# y[y == 0] = 0
		y[y > 0] = 1 


		## SMOTE balancing 
		sm = SMOTE(random_state=42)
		X_res, y_res = sm.fit_resample(X, y)
		# print("<= 0: "+str(np.sum(y <= 0)))
		# print("> 0: "+str(np.sum(y > 0)))
		# print("<= 0: "+str(np.sum(y_res <= 0)))
		# print("> 0: "+str(np.sum(y_res > 0)))
		X, y = X_res, y_res
		# continue
		
		
		######### apply model ##############
		clf = LogisticRegression(random_state=0, solver='lbfgs',multi_class='multinomial', max_iter = 400).fit(X, y)
		# clf = LogisticRegression(random_state=0, multi_class='ovr').fit(X, y)
		pred_y = clf.predict(X[:, :])
		score = clf.score(X, y)
		# print("Mean Accuracy:"+str(score))
		print("F-score:"+str(f1_score(y, pred_y, average='macro')))
		
		# continue


		########## p values ############
		params = np.append(clf.intercept_,clf.coef_)
		predictions = clf.predict(X)

		myDF3 = pd.DataFrame()
		# print(len(params))
		# print(len(feature_vector))
		pd.set_option('display.width', 120)
		# myDF3["Feature"],myDF3["Coefficients"] = [feature_vector,params]
		# print(myDF3)
		# continue
		fval, pval = f_regression(X, y, center=True)
		plotc(j, feature_vector[1:], list(pval))
		# print(type(pval))
		# print(len(pval))
		# print(X.shape)
		# print(y.shape)
		# print(len(feature_vector))
		myDF3["Feature"],myDF3["Coefficients"],myDF3["pvals"] = [feature_vector,params,[0]+list(pval)]
		print(myDF3)
		continue
		# exit()
		'''	
		newX = np.append(np.ones((len(X),1)), X, axis=1)
		MSE = (sum((y-predictions)**2))/(len(newX)-len(newX[0]))

		var_b = MSE*(np.linalg.inv(np.dot(newX.T,newX)).diagonal())
		sd_b = np.sqrt(var_b)
		# print(sd_b.shape)
		# print(params.shape)
		ts_b = params/ sd_b

		p_values =[2*(1-stats.t.cdf(np.abs(i),(len(newX)-1))) for i in ts_b]

		sd_b = np.round(sd_b,3)
		ts_b = np.round(ts_b,3)
		p_values = np.round(p_values,3)
		params = np.round(params,4)

		myDF3 = pd.DataFrame()
		# print(len(params))
		# print(len(feature_vector))
		pd.set_option('display.width', 120)
		myDF3["Feature"],myDF3["Coefficients"],myDF3["Standard Errors"],myDF3["t values"],myDF3["Probabilites"] = [feature_vector,params,sd_b,ts_b,p_values]
		print(myDF3)
		'''

		

	
		

		########## chi square ############
		# scores, pvalues = chi2(X, y)
		# print(pvalues)
		

	# oy = np.asarray(oy)
	# print(oy[1, 0:10])
	# print(oy.shape)
	# with open("y.pickle", 'wb') as handle:
	# 	pickle.dump(oy, handle, protocol=pickle.HIGHEST_PROTOCOL)





# Meeting Discussion

# f1 score
# class balancing : smote
# change metric
# context intensity : retain
# start writing 

# genie coefficient on distribution of aspects
# compare income distributions
# how much pop. 

# -include new items
# compare genie coeff. across items


# COMBINE IN CF
# livelihood & agriculture -> put in general
# factors influencing practice & other factors & myths and misconceptions
# entertainment & general


