import random

def run_ransac(data, estimate, is_inlier, sample_size, goal_inliers, max_iterations, stop_at_goal=True, random_seed=None):
	dane = data #do pozniejszego usuwania
	for i in range(0,2):
		for j in range(0,512):
			if dane[j][i] == float('Inf') or dane[j][i] == -float('Inf'):
				dane[j][i] = None
		
	best_ic = 0
	best_model = None
	num = 0
	a=[]
	b=[]
	c=[]
	random.seed(random_seed)
	for i in xrange(max_iterations):
		s = random.sample(dane, int(sample_size))
		m = estimate(s)
		ic = 0
		for j in xrange(len(dane)):
			if is_inlier(m, dane[j]):
				ic += 1

		#print s
		#print 'estimate:', m,
		#print '# inliers:', ic

	#Dla jednej linii
	#	if ic > best_ic:
	#		best_ic = ic
	#		best_model = m
	#		if ic > goal_inliers and stop_at_goal:
	#			break
	#return best_model, best_ic

	#Dla wielu linii
		if ic > best_ic:
			best_ic = ic
			best_model = m
			if ic > goal_inliers:
				a.append(best_model[0])
				b.append(best_model[1])
				c.append(best_model[2])
				num += 1
				for j in xrange(len(dane)):
					if is_inlier(best_model, dane[j]):
						dane[j][0]=None
						dane[j][1]=None
				best_model = None
				best_ic = 0
	return a, b, c, num,dane
