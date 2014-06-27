from types import NoneType
from pprint import PrettyPrinter
from re import sub

class Node(object):
    def __init__(self, value, path, _type):
        self.value = value
        self.path =path
        self._type = _type
        
    def __str__(self):
        return str(self.value)

    def __repr__(self):
    	return str(self.value)


g=Node(1,1,1)

pp = PrettyPrinter()

valTypes =  [str,int,float,unicode,long, bool,NoneType,type(g)]

def TypeCheck(thing):
	'''checks what thing is, in json terms
		so possibilities are object, array, value'''
	if type(thing) == dict:
		return 'object'
	elif type(thing) == list:
		return 'array'
	elif type(thing) in valTypes:
		return 'value'
	else:
		raise TypeError

def consumeCol(obj, path = [], index = 0):
	'''turns the json into a nested list
		each of the actual nodes are Node objects 
		with a defined index and type'''
	how = TypeCheck(obj)
	return {
		'object': lambda x: [[Node(a, path, 'key'),consumeCol(b, path + [a])] for a, b in x.items()],
		'array': lambda x:  [[Node(i, path, 'index'), consumeCol(j, path +[str(i)])] for i, j in enumerate(x)],
		'value': lambda x: Node(x, path, 'value')
	}.get(how, how)(obj)

def spreadCols(arr):
	'''takes an object which has passed through consumeCol
		spreads the values out to give an array'''
	if type(arr) in valTypes:
		yield arr
	elif type(arr) == list:
		for col in arr:
			node, childs = col[0], col[1]
			for x in spreadCols(childs):
				if type(x) == list:
					bit =[node]
					bit.extend(x)
					yield bit
				else:
					yield [node, x]

def gatherRows(arr, col = 0):
	try:
		curr = arr[0][col]
	except:
		return arr, col
	if curr._type == 'value' or (curr._type == 'key' and arr[0][col+1]._type != 'index'):
		return arr, col
	splits = [0]
	for i, row in enumerate(arr):
		if row[col] != curr:
			splits.append(i)
			curr = row[col]
	split = []
	splits.append(i+1)
	for i in range(len(splits)-1):
		nextDown, dummy= gatherRows(arr[splits[i]:splits[i+1]], col + 1)
		if nextDown != []:
			if type(nextDown[0]) == list and type(nextDown[0][0]) == list:
				split.extend(nextDown)
			else:
				split.append(nextDown)
	return (split, dummy)


def Collimate(obj):
	array, splitLevel = obj
	inrows, outrows = [], []
	rows, heads = [], []
	for row in array:
		if splitLevel == 0:
			inrows.append(row)
			outrows.append([])
			continue
		inrows.append(row[0][:splitLevel])
		outrows.append([i[-1] for i in row])

	for i in range(len(inrows)):
		row = inrows[i] + outrows[i]
		rows.append(row)
		for i in row:
			head = '.'.join(i.path[splitLevel:])
			i.head = head
			heads.append(head)
	heads = list(set(heads))
	newrows = []
	print rows
	for oldrow in rows:
		newrow = []
		print oldrow
		for i, head in enumerate(heads):
			print head
			try:
				cell = [j for j in oldrow if j.head == head][0]
			except Exception as e:
				print e
				cell = Node('',head,'value')
			newrow.append(cell)
		newrows.append(newrow)
	print heads
	print newrows
	return [heads]+newrows






def stack(obj):
	collimated = consumeCol(obj)
	arrayed = [i for i in spreadCols(collimated)]
	rows = gatherRows(arrayed)
	#pp.pprint(rows)
	csv = Collimate(rows)
	return csv


def test():
	from csv import writer
	wrrr = writer(open('STOMPTESTS.csv','wb'))
	for name, test in tests.items():
		print name
		result = stack(test)
		wrrr.writerows([[],[],[name],[test],[]])
		wrrr.writerows(result)


if __name__ == '__main__':
	from tests import tests
	test()







