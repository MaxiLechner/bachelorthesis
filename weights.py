from clusters import *
from ED import *
import numpy as np


def cluster(n,m):
	y = [[i,j] for i in range(n) for j in range(m)]
	#g = np.zeros((n,m))
	#y = []
	#it = np.nditer(g, flags=['multi_index'])
	#while not it.finished:
	#	y.append(it.multi_index)
	#	it.iternext()
	for i in range(n*m):
		y[i] = map(lambda x: x+1,y[i])

	for i in range(n*m):
		y[i] = y[i] + [y[i][0]*y[i][1]]

	y = sorted(y, key = lambda a: a[2])
	for i in range(n*m):
		y[i] = [y[i][0],y[i][1]]
	return y

def subclusters(a,b):
	l = cluster(a,b)
	if len(l)==1:
		return 0
	else:
		b = [[(l[-1][0]-(i[0]-1))*(l[-1][1]-(i[1]-1)), i] for i in l[:-1]]
		b = list(reversed(b))
		#list_of_lists = []
		#for i in b:
		#	list_of_lists.append(i[0]*[i[1]])
		#flattened = [val for sublist in list_of_lists for val in sublist]
		
		#return flattened
		return b

a = cluster(2,2)

b = []
for i in range(len(a)):
	if a[i][0]==a[i][1]:
		b.append([a[i],1])
	else:
		b.append([a[i],1])

for i in b:
	print i
for i in cluster(1,3):
	print i, ':', subclusters(i[0],i[1])

for i in subclusters(1,3):
	print i,':', i[0], subclusters(i[1][0],i[1][1])


'''

graph = cluster(k,l)

o = [str(i) for i in range(len(graph))]

#print map(tuple,graph)

howoften = [i[0] for i in subclusters(k,l)]
sub = [i[1] for i in subclusters(k,l)]

dic = {str(i):sub[i] for i in range(len(sub))}
'''