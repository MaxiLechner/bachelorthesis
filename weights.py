from clusters import *
from ED import *
import numpy as np
import string as string

def traverse(item):
    try:
        for i in iter(item):
            for j in traverse(i):
                yield j
    except TypeError:
        yield item

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
	m = a
	n = b
	l = cluster(a,b)
	if len(l)==1:
		#return "P(%d,%d)"%(1,1)
		return "W(%d,%d)=P(%d,%d)"%(1,1,1,1)
		#return (1,1)
	else:
		b = [[(l[-1][0]-(i[0]-1))*(l[-1][1]-(i[1]-1)), i] for i in l[:-1]]
		b = list(reversed(b))
		#list_of_lists = []
		#for i in b:
		#	list_of_lists.append(i[0]*[i[1]])
		#flattened = [val for sublist in list_of_lists for val in sublist]
		#return flattened
		

		prop = "W(%d,%d)=P(%d,%d)"%(m,n,m,n)
		#prop = "P(%d,%d)"%(m,n)
		for i in b:
			#print i[0],'+',i[1]
			prop += "%+d*W(%d,%d)"%(-i[0],i[1][0],i[1][1])
		return prop
		#return b

#split W(1,1) = P(1,1) in two lists

a = []
for i in cluster(2,2):
	a.append(str(subclusters(i[0],i[1])))
a1 = [] 
a2 = []
for i in a:
	a1.append(i[:6])
	a2.append(i[7:])
for i in a:
	print i

for i in reversed(range(len(a2)-1)):
	a2[i+1] = '('+a2[i+1]+')'


for j in reversed(range(len(a2))):
	for i in reversed(range(len(a2))):
		a2[j] = a2[j].replace(a1[i],a2[i])

for i in a2:
	print i

e = ""
for i in a2:
	e += i
	e += '+'
e = e[:len(e)-1]
#print e
'''
f = open('aaaaaaaa','w')
for i in a:
	f.write(i)
	f.write('\n')
f.close()

search in dictionary
'''

'''
b = []
for i in range(len(a)):
	if a[i][0]==a[i][1]:
		b.append([a[i],1])
	else:
		b.append([a[i],1])
'''



