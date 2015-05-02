import numpy as np
from scipy import sparse
import scipy.sparse.linalg.eigen.arpack as arp

def calculateTag(x):
	a = 0
	for i in range(n):
		a += np.sqrt(100*i + 3) * x[i]
	return a

def binary_search(l, value):
    low = 0
    high = len(l)-1
    while low <= high: 
        mid = (low+high)//2
        if l[mid] > value: high = mid-1
        elif l[mid] < value: low = mid+1
        else: return mid
    return -1

def qsort(list):
    if list == []: 
        return []
    else:
        pivot = list[0]
        lesser = qsort([x for x in list[1:] if x < pivot])
        greater = qsort([x for x in list[1:] if x >= pivot])
        return lesser + [pivot] + greater

#############################################################

n = 3 #number of electrons
J = 1 # coupling constant in z direction
h = -1 # coupling contant in x direction
row = np.array(range(2**n))

l = [bin(x)[2:].rjust(n, '0') for x in range(2**n)]
b = np.array([np.array(map(int, i)) for i in l])
d = np.array([np.array(map(int, i)) for i in l])


j = [bin(x)[2:].rjust(n, '0') for x in range(2**n)]
for i in range(2**n):
	j[i] = j[0][:n-1]
q = np.array([np.array(map(int, i)) for i in j])

###########################################################
'''Sort Tags'''
T = []
for i in range(2**n):
	 T.append(calculateTag(b[i]))

Tsorted = np.asarray(qsort(T))

###########################################################
'''H_diag'''


for i in range(2**n):
	for j in reversed(range(n-1)):
		if b[i,j]==b[i,j+1]:
			q[i,j] = binary_search(Tsorted,calculateTag(b[i]))
		else:
			q[i,j] = -binary_search(Tsorted,calculateTag(b[i]))		


data = [0]*2**n
ppp = [0]*2**n

for i in range(2**n):
	data[i] = np.sum(q[i])
	if data[i]!=0:
		data[i] = J * (data[i])/(abs(q[i,0]))
	if q[i,0] == 0:
		data[i] = J * len(q[i])
	ppp[i] = abs(q[i,0])

Diagonal = sparse.csr_matrix((data, (row,row)), shape=(2**n,2**n), dtype=float).toarray()

##########################################################
'''Off Diagonal'''

qwerty = [bin(2**x)[2:].rjust(n, '0') for x in range(n)]
qwertz = np.array([np.array(map(int, i)) for i in qwerty])

asd = np.zeros((2**n,n), dtype=np.double)
zeros = [0]*2**n
Off_Diagonal = sparse.csr_matrix((zeros, (row,row)), shape=(2**n,2**n), dtype=float).toarray()

for i in range(2**n):
	for j in range(n):
		asd[i,j] = binary_search(Tsorted,calculateTag(np.bitwise_xor(d[i],qwertz[j])))
		Off_Diagonal[i,asd[i,j]] = h


##########################################################
''' Diagonalize Full Hamiltonian'''

Ham = Diagonal + Off_Diagonal
print Ham
#vals, vecs = arp.eigsh(Ham, k=3)
#print vals

#g = [i[0] for i in sorted(enumerate(T), key=lambda x:x[1])]