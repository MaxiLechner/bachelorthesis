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
def ED_2D(n,m,h):
	J = 1 
	
	row = np.array(range(2**(n*m)))

	l = [bin(x)[2:].rjust(n*m, '0') for x in range(2**(n*m))]
	b = np.array([np.array(map(int, i)) for i in l])
	d = np.array([np.array(map(int, i)) for i in l])
	onlyone1 = []
	for i in range((n*m)):
		onlyone1.append(b[2**i])
	onlyone1 = np.asarray(onlyone1)

	###########################################################
	'''Sort Tags'''
	T = []
	for i in range(2**(n*m)):
		 T.append(calculateTag(b[i]))

	Tsorted = np.asarray(qsort(T))

	#for i in range(len(T)):
	#	print T[i], Tsorted[i]

	Tindex = sorted(range(len(T)), key=lambda k: T[k])
	#print Tindex
	#print Tindex[4]
	#print sorted(range(len(Tsorted)), key=lambda k: Tsorted[k])

	###########################################################
	data = []
	data1 = []
	data2 = []
	data3 = []
	rowcol = []
	abc1 = np.zeros(((n*m)-1), dtype=np.double)
	abc2 = np.zeros(((n*m)-1), dtype=np.double)
	v = []
	f = []
	off_row = []
	off_col = []
	off_data = []
	
	for i in range(2**(n*m)):
		'''Diagonal'''

		'''horizontal bonds'''
		v1 = 0
		v2 = 0
		for j in range(n):
			for k in range(m-1):
				if b[i,k+j*m] == b[i,k+1+j*m]:
					v1 +=1
				else:
					v1 -=1
		data1.append(-J*v1)

		'''vertical bonds'''
		for j in range((n-1)*m):
			if b[i,j] == b[i,j+m]:
				v2 += 1
			else:
				v2 -= 1
		data2.append(-J*v2)
		
		'''Off Diagonal'''		
		for j in range(n*m):
				off_col.append(Tindex[binary_search(Tsorted,calculateTag(np.bitwise_xor(d[i],onlyone1[j])))])
				
				#print d[i], onlyone1[j], np.bitwise_xor(d[i],onlyone1[j]), 'index:', Tindex[binary_search(Tsorted,calculateTag(np.bitwise_xor(d[i],onlyone1[j])))]
				
				off_row.append(i)
				off_data.append(-h)
	
	for i in range(len(data1)):
		data3.append(data1[i] + data2[i])
	for i in range(len(data3)):
		if data3[i] != 0:
			data.append(data3[i])
			rowcol.append(i)
	
	Diagonal = sparse.csr_matrix((data,(rowcol,rowcol)), dtype=np.double).toarray()
	Off_Diagonal = sparse.csr_matrix((off_data, (off_row,off_col)), dtype=np.double).toarray()
	
	##########################################################
	'''Diagonalize Full Hamiltonian'''
	#print Off_Diagonal
	Ham = Diagonal + Off_Diagonal
	
	#print Ham
	
	vals, vecs = arp.eigsh(Ham, k=1, which='SA')
	return vals[0],vecs

if __name__ == "__main__":
	ED_2D(2,2,1)
#print ED_2D(2,2,1)