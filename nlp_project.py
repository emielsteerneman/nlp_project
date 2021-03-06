print("Starting up...")

from gensim.test.utils import datapath
from gensim.models import KeyedVectors
import nltk
from nltk.parse.stanford import StanfordDependencyParser

from importlib import reload
import os.path
import pickle

import dynamicCode

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

wnl = nltk.WordNetLemmatizer()

# dependency_parser = StanfordDependencyParser(path_to_jar="./stanford-parser-full-2018-02-27/stanford-parser.jar", path_to_models_jar="./stanford-parser-full-2018-02-27/english.jar")
dependency_parser = StanfordDependencyParser(path_to_jar="./stanford-parser-full-2018-02-27/stanford-parser.jar", path_to_models_jar="./stanford-parser-full-2018-02-27/english.jar")

while True:
	try:
		dynamicCode = reload(dynamicCode)
		dynamicCode.f(word_vectors, dependency_parser, wnl)
	except Exception as e:
		print("Error:", e)

	input("$")
