import nltk
from nltk import tree

def loadData(path):
	with open(path,'r') as f:
		data = f.read().split('\n')
	return data

def getTreeData(data):
	return map(lambda s: tree.Tree.fromstring(s), data)

# Main script
print("loading data..")
data = loadData('parseTrees.txt')
print("generating trees..")
treeData = getTreeData(data)
print("done!")
