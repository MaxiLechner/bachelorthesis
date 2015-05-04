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

n = 4 #number of electrons
J = 1 # coupling constant in z direction
h = 1 # coupling contant in x direction
row = np.array(range(2**n))

l = [bin(x)[2:].rjust(n, '0') for x in range(2**n)]
b = np.array([np.array(map(int, i)) for i in l])
d = np.array([np.array(map(int, i)) for i in l])


###########################################################
'''Sort Tags'''
T = []
for i in range(2**n):
	 T.append(calculateTag(b[i]))

Tsorted = np.asarray(qsort(T))

###########################################################
'''H_diag'''
data = [-J*(n-1.)]
rowcol = [0]
abc = np.zeros((n-1), dtype=np.double)

for i in range(2**n):
	for j in reversed(range(n-1)):
		if b[i,j]==b[i,j+1]:
			abc[j] = binary_search(Tsorted,calculateTag(b[i]))
		else:
			abc[j] = -binary_search(Tsorted,calculateTag(b[i]))
	if np.sum(abc)!=0:
		rowcol.append(i)
		data.append(-J * (np.sum(abc))/(abs(abc[0])))

Diagonal = sparse.csr_matrix((data,(rowcol,rowcol)), dtype=float).toarray()

##########################################################
'''Off Diagonal'''

qwerty = [bin(2**x)[2:].rjust(n, '0') for x in range(n)]
qwertz = np.array([np.array(map(int, i)) for i in qwerty])

asd = np.zeros((2**n,n), dtype=np.double)
zeros = [0]*2**n
Off_Diagonal = sparse.csr_matrix((zeros, (row,row)), shape=(2**n,2**n), dtype=float).toarray()
#print Off_Diagonal
col = []
off_diag_data = []

for i in range(2**n):
	for j in range(n):
		asd[i,j] = binary_search(Tsorted,calculateTag(np.bitwise_xor(d[i],qwertz[j])))
		Off_Diagonal[i,asd[i,j]] = -h
		#print asd[i,j]
#print row

##########################################################
'''Diagonalize Full Hamiltonian'''

Ham = Diagonal + Off_Diagonal
print Ham
#vals, vecs = arp.eigsh(Ham, k=3)
#print vals

#g = [i[0] for i in sorted(enumerate(T), key=lambda x:x[1])]