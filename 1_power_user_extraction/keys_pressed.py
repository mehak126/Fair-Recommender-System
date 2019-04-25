import sys
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from collections import defaultdict

def main():
	file_name = sys.argv[1] #data file. assumed col 0 -> caller id, col 3 -> duration heard, col 4 -> key pressed
	
	user_durations = Counter() #storing total call duration of each user
	user_keys_pressed = Counter() #storing total keys pressed by each user


	interaction = ['dtmf_*', 'dtmf_1', 'dtmf_2', 'dtmf_3', 'dtmf_4', 'dtmf_5', 'dtmf_6', 'dtmf_9']

	with open(file_name, 'r') as dat:
		for line in dat:
			info = line.split(',')
			if not int(info[3]) == 0: # if call duration is not 0
				user_durations[info[0]] += int(info[3])
				if info[4] in interaction:
					user_keys_pressed[info[0]] += 1
	
	all_kpm = [] #storing info of rate of pressing keys of all users in an array
	for k in user_keys_pressed:
		all_kpm.append( (-1 * np.log(float((user_keys_pressed[k]) / user_durations[k]) ))) #taking -log of fraction as values are very small

	kpm_variation = Counter(all_kpm) # x-> keys pressed per second, y-> how many users had that rate
	all_vals = sorted(kpm_variation.most_common()) 
	x_vals = [x[0] for x in all_vals]
	y_vals = [x[1] for x in all_vals]



	cdf = []
	cdf.append(y_vals[0])
	for i in range(1,len(y_vals)):
		cdf.append( float( float(cdf[i-1] + y_vals[i])) )

	cdf = [float(x/len(user_keys_pressed)) for x in cdf]
	ccdf = [float(1-x) for x in cdf]
	
	plt.plot(x_vals,cdf)
	plt.xlabel('Keys pressed per second (-log)', fontsize = 14)
	plt.ylabel('Number of users (Normalised)', fontsize = 14)
	# plt.title('Cumulative Distribution of users according to keys pressed per second')
	# plt.title('Distribution of users according to keys pressed per minute')
	plt.show()
	plt.close()









if __name__ == '__main__':
	main()