import numpy as np
from scipy import sparse
import scipy.sparse.linalg.eigen.arpack as arp

def calculateTag(x):
	a = 0
	for i in range(len(x)):
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
def ED(n,h):
	#n: number of sites
	J = 1 #coupling for sum_{<ij>}s^z_i s^z_j
	#h: #coupling for sum_{i}s^x_i
	row = np.array(range(2**n))

	l = [bin(x)[2:].rjust(n, '0') for x in range(2**n)]
	b = np.array([np.array(map(int, i)) for i in l])
	d = np.array([np.array(map(int, i)) for i in l])
	onlyone1 = []
	for i in range(n):
		onlyone1.append(b[2**i])
	onlyone1 = np.asarray(onlyone1)
	###########################################################
	'''Sort Tags'''
	T = []
	for i in range(2**n):
		 T.append(calculateTag(b[i]))

	Tsorted = np.asarray(qsort(T))

	###########################################################
	data = [-J*(n-1.)]
	rowcol = [0]
	abc = np.zeros((n-1), dtype=np.double)

	off_row = []
	off_col = []
	off_data = []


	for i in range(2**n):
		'''Diagonal'''
		for j in reversed(range(n-1)):
			if b[i,j]==b[i,j+1]:
				abc[j] = binary_search(Tsorted,calculateTag(b[i]))
			else:
				abc[j] = -binary_search(Tsorted,calculateTag(b[i]))
		if np.sum(abc)!=0:
			rowcol.append(i)
			data.append(-J * (np.sum(abc))/(abs(abc[0])))
		'''Off Diagonal'''		
		for j in range(n):
			off_col.append(binary_search(Tsorted,calculateTag(np.bitwise_xor(d[i],onlyone1[j]))))
			off_row.append(i)
			off_data.append(-h)

	Diagonal = sparse.csr_matrix((data,(rowcol,rowcol)), dtype=np.double).toarray()
	Off_Diagonal = sparse.csr_matrix((off_data, (off_row,off_col)), dtype=np.double).toarray()
	##########################################################
	'''Diagonalize Full Hamiltonian'''

	Ham = Diagonal + Off_Diagonal
	#print Ham
	vals, vecs = arp.eigsh(Ham, k=1, which='SA')
	return vals[0]
if __name__ == "__main__":
	ED(12,1)
