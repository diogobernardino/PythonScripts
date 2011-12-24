import argparse

INPUT_FILENAME = 'data.txt'
OUTPUT_FILENAME = 'sorted.txt'

class Customer(object):
	def __init__(self, id, name):
		self.id = id
		self.name = name
	def __cmp__(self, customer):
		if self.id < customer.id:
			return -1
		elif self.id >= customer.id:
			return 1
	def __str__(self):
		return '%d %s'%(self.id,self.name)

def quicksort(l):
	if l == []: 
		return []
	else:
		pivot = l[0]
		lesser = quicksort([x for x in l[1:] if cmp(x, pivot) == -1])
		greater = quicksort([x for x in l[1:] if cmp(x, pivot) == 1])
		return lesser + [pivot] + greater

if __name__ == '__main__':
	arguments = argparse.ArgumentParser(description='Sort list')
	arguments.add_argument( '-f','--file', metavar='<Filename>', required=True, help='File containing data' )
	arguments.add_argument('-o','--output', default='sorted.txt', help='File containing de output data')
	options = arguments.parse_args()

	#read data
	#f = open('data.txt', 'r')
	f = open(options.file, 'r')
	customers = []
	for p in f.readlines()[1:]:
		aux = p.split(';')
		customers.append(Customer(int(aux[0]), aux[1]))
	f.close()

	#write sorted data
	#f = open(OUTPUT_FILENAME, 'w')
	f = open(options.output, 'w')
	for c in quicksort(customers):
		f.write(str(c))
	f.close()


	
	
	
	
	