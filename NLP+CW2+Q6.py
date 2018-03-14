import nltk
from nltk import tree
from nltk import Nonterminal
from nltk.draw.tree import TreeView

def loadData(path):
    with open(path,'r') as f:
        data = f.read().split('\n')
    return data

def getTreeData(data):
    return map(lambda s: tree.Tree.fromstring(s), data)

# Main script
gram_rules = []
print("loading data..")
data = loadData('parseTrees.txt')
print("generating trees..")
treeData = getTreeData(data)

for t in treeData:
    gram_rules.extend(t.productions())

print("Total rules: " + str(len(gram_rules)) + ' loaded for our system' )


#We now will calculate the probabilities for each rule as the number of times it appears as a perc of all rules
from collections import Counter
import pandas as pd

#We enrich our dataframe with additional fields for probabilities and counters
rules_count = dict(Counter(gram_rules))
rules_df = pd.DataFrame(list(rules_count.items()), columns=['rule','count'])
rules_df['rule_str'] = rules_df.apply(lambda row: str(row['rule']), axis=1)
rules_df['lhs'] = rules_df.apply(lambda row: row['rule'].lhs(), axis=1)
rules_df['rhs'] = rules_df.apply(lambda row: row['rule'].rhs(), axis=1)
rules_df['total_count'] = rules_df.groupby('lhs')['count'].transform(sum)
rules_df['prob'] = rules_df.apply(lambda row: row['count']/row['total_count'], axis=1)
rules_df['production_prob'] = rules_df.apply(lambda row: str(row['rule']) + ' ' + str(row['prob']), axis=1)

#Convert the rules into a grammar in order to create parse trees
rules_list = rules_df['rule'].tolist()
grammar = "\n".join([str(r) for r in rules_list])
grammar = nltk.CFG.fromstring(grammar)

#Generate the dictionary to be used to calculate each tree's probability.
rules_prob = dict(zip(rules_df['rule'], rules_df['prob']))

#Convert the rules into a grammar in order to create parse trees
S = Nonterminal('S')
rules_list = rules_df['rule'].tolist()
grammar = "\n".join([str(r) for r in rules_list])
grammar = nltk.CFG.fromstring(grammar)


#Let's now parse our sentence
sent = 'Show me the meals on the flight from Phoenix'
#We need to lowercase the verb as in our grammar verbs are in lowercase since they can be in
#the middle of the sentence as well. Phoenix should remain in capital case as is a proper noun and not the bird.
sent = sent[0].lower() + sent[1:]
sent = sent.split()
parser = nltk.ChartParser(grammar)

#We will generate the tree parsing using our grammar and calculate the probabilities
i = 0
for tree in parser.parse(sent):
    i += 1
    print("Tree number " + str(i) + ':')
    #Calculate the probability
    prob = 1
    for p in tree.productions():
        prob *= rules_prob[p]
    print("Tree probability " + str(prob))
    print(tree)
    print('\n')

#Most likely parse (highest probability)
tree_prob = 0
for tree in parser.parse(sent):
    #Calculate the probability
    prob = 1
    for p in tree.productions():
        prob *= rules_prob[p]
    if prob > tree_prob:
        tree_prob = prob
        likely_tree = tree
print("Most likely tree probability " + str(tree_prob))
print(likely_tree)

#Save PCFG into a text file
manual_pcfg = []
for key in rules_prob.keys():
    manual_pcfg.append(str(key) + ' [' + str(rules_prob[key]) + ']')
manual_pcfg = "\n".join([r for r in manual_pcfg])

pcfg_file = open("pcfg_manual.txt", "w")
pcfg_file.write(manual_pcfg)
pcfg_file.close()


#In order to validate our results we'll use the NLTK package to
from nltk import induce_pcfg

S = Nonterminal('S')
grammar = induce_pcfg(S, gram_rules)

sent = "show me the meals on the flight from Phoenix".split()
inside_parser = nltk.InsideChartParser(grammar)

i = 1
for tree in inside_parser.parse(sent):
    print('Tree number ' + str(i) + ":")
    print(tree)
    i += 1

print("Using the Viterbi parser from NLTK to determine which tree is most likely")
viterbi_parser = nltk.ViterbiParser(grammar)
for tree in viterbi_parser.parse(sent):
    print(tree)