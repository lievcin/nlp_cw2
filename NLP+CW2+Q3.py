import nltk
from nltk.corpus import treebank
# nltk.download('treebank')
sentence22 = treebank.parsed_sents('wsj_0003.mrg')[21]
sentence7 = treebank.parsed_sents('wsj_0003.mrg')[6]
sentence13 = treebank.parsed_sents('wsj_0004.mrg')[12]

print(sentence22)
sentence22.productions()

print(sentence7)
sentence7.productions()

print(sentence13)
sentence13.productions()

