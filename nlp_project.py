print("Starting up...")

from gensim.test.utils import datapath
from gensim.models import KeyedVectors
import language_check
import nltk, re, pprint
from nltk import word_tokenize, sent_tokenize
from nltk.parse.stanford import StanfordDependencyParser
from nltk.corpus import treebank

import os.path
import pickle
import time

### ### ### ### LOADING PICKLE ### ### ### ###
picklePath = "/nlp/pickle.obj"					# Pickle path

if os.path.isfile(picklePath):
	print("Loading pickle..")
	with open(picklePath, 'rb') as pickleFile:
		word_vectors = pickle.load(pickleFile)
		print("Pickle loaded")
else:
	path = "/nlp/GoogleNews-vectors-negative300.bin"
	print("Loading file..")
	word_vectors = KeyedVectors.load_word2vec_format(datapath(path), binary=True)
	print("Writing pickle..")
	filehandler = open(picklePath, 'wb')			# Open file handler
	pickle.dump(word_vectors, filehandler, pickle.HIGHEST_PROTOCOL)		# Dump vector into file
### ### ### ### ### ### ### ### ### ### ### ### 

spellCheck = language_check.LanguageTool('en-GB')
wnl = nltk.WordNetLemmatizer()



dependency_parser = StanfordDependencyParser(path_to_jar="/nlp/stanford-parser-full-2018-02-27/stanford-parser.jar", path_to_models_jar="/nlp/stanford-parser-full-2018-02-27/english.jar")

iterator = 0
while True:
	if iterator > 0:
		userInputString 	= input("type your string     : ")
		userInputContextIn  = input("type your in context : ")
		userInputContextOut = input("type your out context: ")
	else:
		userInputString = "The drunken Floridian man cannot remember carrying an alligator into a liquor store."#" The Florida man was caught on camera running through a Jacksonville liquor store, and taking the gator into the beer fridge last week. He can’t remember any of it."
		userInputContextIn = "America"
		userInputContextOut = "Mexico"

	text = [[wnl.lemmatize(word.lower()) for word in word_tokenize(sentence)] for sentence in sent_tokenize(userInputString)]
	text_dep = [word_tokenize(sentence) for sentence in sent_tokenize(userInputString)]
	
	print(wnl.lemmatize("Floridian"))
	# normalizedWordlist = word_tokenize(userInputString)
	# normalizedWordlist = [wnl.lemmatize(word.lower()) for word in text]
	# nltk.download('averaged_perceptron_tagger')
	# nltk.download('maxent_ne_chunker')
	# nltk.download('words')
	# nltk.download('treebank')

	# tokens = word_tokenize(userInputString)
	# print(tokens)

	# tagged = nltk.pos_tag(tokens)
	# print(tagged)

	# entities = nltk.chunk.ne_chunk(tagged)
	# print(entities)

	# entities.draw()

	# t = treebank.parsed_sents('wsj_0001.mrg')[0]
	# t.draw()

	# time.sleep(60)
	# text = wnl.lemmatize(word.lower() for word in word_tokenize(userInputString))
	parse = dependency_parser.parse_sents(text_dep)
	print(parse, "\n\n", text, "\n\n", text_dep, "\n\n")

	tree = parse.__next__()
	parse2 = tree.__next__()
	# list(tree.triples())
	for i in parse2.triples():
		print((i[0][0]).ljust(15),"has", (i[1]).ljust(10), (i[2][0]).ljust(15), "and POS tag", i[0][1])
	print(list(parse2.triples()))
	exit(1)

	outputSentence = []
	for sentence in text:
		for word in sentence:
			try:
				result = word_vectors.most_similar(positive=[word, userInputContextOut.strip()], negative=[userInputContextIn.strip()])
				print("{} => {}: {:.4f}".format(word, *result[0]))
				outputSentence.append(str(result[0][0]).replace("_", " "))
			except:
				print(word)
				outputSentence.append(word)

	print("\n")
	print(userInputString.strip())
	outputSentence = " ".join(outputSentence)
	print(outputSentence)		
	# result = word_vectors.most_similar(positive=['germany', 'amsterdam'], negative=['netherlands'])

	matches = spellCheck.check(outputSentence)
	# print(matches)
	outputSentence = language_check.correct(outputSentence, matches)
	print(outputSentence)
	print("\n")	
	# result = word_vectors.most_similar(positive=['woman', 'king'], negative=['man'])
	# result = word_vectors.most_similar(positive=['germany', 'amsterdam'], negative=['netherlands'])
	# Florida man brings alligator to convenience store, chases customers.
	iterator += 1





