import nltk

# here we define a grammar
grammar = nltk.CFG.fromstring("""
S -> NP VP
S -> Aux NP VP
S -> VP
NP -> Pronoun
NP -> Proper-Noun
NP -> Det Nominal
Nominal -> N
Nominal -> Nominal N
Nominal -> Nominal PP
VP -> V
VP -> V NP
VP -> V NP PP
VP -> V PP
VP -> VP PP
PP -> Preposition NP
S -> IVP
IVP -> IVerb NP NP
IVP -> IVerb NP NP PP
IVerb -> 'list'
Det -> 'that' | 'this' | 'the' | 'a'
N -> 'book' | 'flight' | 'meal' | 'money' | 'seats'
V -> 'book' | 'include' | 'prefer' | 'show' | 'list'
Pronoun -> 'I' | 'she' | 'me'
Proper-Noun -> 'Houston' | 'NWA' | 'denver'
Aux -> 'does'
Preposition -> 'from' | 'to' | 'on' | 'near' | 'through'
""")

sent = 'List me the seats on the flight to Denver'
sent = sent.lower().split()
parser = nltk.ChartParser(grammar)

for tree in parser.parse(sent):
    print(tree)


# Modified grammar with new rule at the bottom
grammar = nltk.CFG.fromstring("""
S -> NP VP
S -> Aux NP VP
S -> VP
NP -> Pronoun
NP -> Proper-Noun
NP -> Det Nominal
Nominal -> N
Nominal -> Nominal N
Nominal -> Nominal PP
VP -> V
VP -> V NP
VP -> V NP PP
VP -> V PP
VP -> VP PP
PP -> Preposition NP
S -> IVP
IVP -> IVerb NP NP
IVP -> IVerb NP NP PP
IVerb -> 'list'
Det -> 'that' | 'this' | 'the' | 'a'
N -> 'book' | 'flight' | 'meal' | 'money' | 'seats'
V -> 'book' | 'include' | 'prefer' | 'show' | 'list'
Pronoun -> 'I' | 'she' | 'me'
Proper-Noun -> 'Houston' | 'NWA' | 'denver'
Aux -> 'does'
Preposition -> 'from' | 'to' | 'on' | 'near' | 'through'
NP -> NP PP
""")

sent = 'List me the seats on the flight to Denver'
sent = sent.lower().split()
parser = nltk.ChartParser(grammar)

for tree in parser.parse(sent):
    print(tree)

print(grammar)

