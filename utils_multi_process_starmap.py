import multiprocessing
from multiprocessing import Process, Pool
import time
##VPR
## get the total number of CPU
maxPll = multiprocessing.cpu_count() - 1


def run_stuff(array1, array2, singleValue):

	print(singleValue, array1, array2)
	time.sleep(5)



if __name__ == "__main__":
	
	singleValue=[]
	array1=[]
	array2=[]
	for j in range(0, 30):
		singleValue.append(j)
		array1.append([j,j+1])
		array2.append([j+100,j+100+1])
		
	
	valuesA = zip(array1,array2,singleValue)

	with Pool(maxPll) as pool:
		res = pool.starmap(run_stuff, valuesA)	