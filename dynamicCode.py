from gensim.test.utils import datapath
from gensim.models import KeyedVectors
import language_check
import nltk, re, pprint
from nltk import word_tokenize, sent_tokenize
from nltk.parse.stanford import StanfordDependencyParser
from nltk.corpus import treebank
import re
import datetime

def my_tokenize(sentence):
	return re.findall(r'([a-zA-Z0-9’]+|[,;])', sentence)

def f(word_vectors, dependency_parser, wnl):
	print("Running dynamic code..")

	userInputStrings = [
		"The drunken Floridian man can not remember carrying an alligator into a liquor store. The Florida man was caught on camera running through a Jacksonville liquor store, and taking the gator into the beer fridge last week. He can’t remember any of it.",
		"Florida Woman tries to scam $600 lottery winner by telling him he won only $5, but the winner was an agent working undercover for the state Lottery Commission’s security division.",
		"Naked Florida Man Drinks 2 Liters of Vodka, Burns down House Baking Cookies on George Foreman Grill",
		"Naked Florida man chases people and cops around Chic-Fil A parking lot telling them they’re gay for looking at his penis",
		"Florida Man causes $100k in damage to Walmart liquor store under construction with hotwired forklift. gives police his name as Alice Wonderland and says a hookah-smoking caterpillar told him to do it.",
		"Florida Man goes fishing and catches a kilo of marijuana. Calls it an early birthday gift from Pablo Escobar",
		"Florida man robs bank, strips naked, then runs down the street throwing stolen money everywhere.",
		"Florida Man who is a convicted felon honks horn at cops working an accident. Has numerous drugs and weapons in his car in plain sight."
	]

	userInputContextIn = "Florida"
	userInputContextOut = "Canada"

	dateStr = datetime.datetime.now().strftime("%Y_%b_%d-%H_%M")
	with open('output_' + dateStr + '.txt', 'w') as file:
		for inputStr in userInputStrings:
			file.write(inputStr)
			print(inputStr)
			print()
			for cOut in "India Mexico Canada Netherlands Holland France Germany Texas Nevada".split():
				output = changeContext(word_vectors, dependency_parser, wnl, inputStr, userInputContextIn, cOut)
				print(cOut)
				print(output)
				print("\n")
				file.write("\n")
				file.write(cOut)
				file.write("\n")
				file.write(output)
			file.write("\n\n\n")
	file.close()


def changeContext(word_vectors, dependency_parser, wnl, input, cIn, cOut):
	# Tokenize input
	text_dep = [my_tokenize(sentence.lower()) for sentence in sent_tokenize(input)]
	# Tokens => Parse tree
	parse = dependency_parser.parse_sents(text_dep)

	# Lookup table to store context mappings
	lookup = {}
	lookup_rejection = []

	for tree in parse:
		for dependency_sentence in tree:
			for dependency in dependency_sentence.triples():
				for word, label in [dependency[0], dependency[2]]:

					lemma = word
					try:
						lemma = wnl.lemmatize(word, label[0].lower())
						print(word, "=>", lemma)
					except Exception as e:
						# print("Error:", e)
						pass

					if label in ["NN", "NNP"]:
						wordT = lookup.get(lemma)
						if wordT is None:
							try:
								results = word_vectors.most_similar(positive=[lemma, cOut.strip()], negative=[cIn.strip()])
								wordT = results[0][0].replace("_", " ")
								if(0.4 <= results[0][1]):
									lookup[lemma] = wordT
									print("      ", lemma.ljust(15), "=>", wordT.ljust(15), results[0][1])
								elif lemma not in lookup_rejection:
									lookup_rejection.append(lemma)
									print("REJECT", lemma.ljust(15), "=>", wordT.ljust(15), results[0][1])
							except Exception as e:
								print("Error:", e)
	output = []
	for sentence in text_dep:
		newSentence = [lookup.get(word) or word for word in sentence]
		sentence = " ".join(newSentence) + "."
		output.append(sentence)
	
	return " ".join(output)
