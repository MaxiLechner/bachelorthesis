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

	#for i in range(len(T)):
	#	print T[i], Tsorted[i]

	Tindex = sorted(range(len(T)), key=lambda k: T[k])
	#print Tindex
	#print Tindex[4]
	#print sorted(range(len(Tsorted)), key=lambda k: Tsorted[k])

	
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
				abc[j] = Tindex[binary_search(Tsorted,calculateTag(b[i]))]
				#abc[j] = binary_search(Tsorted,calculateTag(b[i]))
			else:
				abc[j] = -Tindex[binary_search(Tsorted,calculateTag(b[i]))]
				#abc[j] = -binary_search(Tsorted,calculateTag(b[i]))
		if np.sum(abc)!=0:
			rowcol.append(i)
			data.append(-J * (np.sum(abc))/(abs(abc[0])))
		'''Off Diagonal'''		
		for j in range(n):
			off_col.append(Tindex[binary_search(Tsorted,calculateTag(np.bitwise_xor(d[i],onlyone1[j])))])
		#	print d[i], onlyone1[j], np.bitwise_xor(d[i],onlyone1[j]), 'Tag:',calculateTag(np.bitwise_xor(d[i],onlyone1[j])), 'search:', Tindex[binary_search(Tsorted,calculateTag(np.bitwise_xor(d[i],onlyone1[j])))]
			#print binary_search(Tsorted,calculateTag(np.bitwise_xor(d[i],onlyone1[j])))
			off_row.append(i)
			off_data.append(-h)
		#print '#######'

	Diagonal = sparse.csr_matrix((data,(rowcol,rowcol)), dtype=np.double).toarray()
	Off_Diagonal = sparse.csr_matrix((off_data, (off_row,off_col)), dtype=np.double).toarray()
	
	##########################################################
	'''Diagonalize Full Hamiltonian'''

	Ham = Diagonal + Off_Diagonal
	#print Ham
	vals, vecs = arp.eigsh(Ham, k=1, which='SA')
	return vals[0]#,vecs
#sigmaz = np.matrix([[1,0],[0,-1]])
if __name__ == "__main__":
	ED(3,1.5)
'''
myList = [1, 2, 3, 100, 5]
asdasd = [[i[0],i[1]] for i in sorted(enumerate(myList), key=lambda x:x[1])]
asdasd1 = []
asdasd2 = []
for i in range(len(asdasd)):
	print asdasd[i], myList[i]
	asdasd1.append(asdasd[i][0])
	asdasd2.append(asdasd[i][1])

print asdasd
print binary_search(asdasd2,100)

return asdasd1[4]
'''
'''
print ED(2,1.5)[0]
print ED(2,1.5)[1]
ase = np.array(ED(2,1.5)[1])
for i in range(len(ase)):
	ase[i] = -ase[i]
print ED(2,1.5)[1][0], ED(2,1.5)[1][1]
print sigmaz*ED(2,1.5)[1][:2]# + ED(2,1.5)[1][2:]
asd = np.array([-0.57363485,0.41345261,-0.41345261,-0.57363485])+np.array([-0.57363485,-0.41345261,-0.41345261,0.57363485])
print ase
print np.dot(asd,ase)
'''