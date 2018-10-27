import language_check
from nltk import sent_tokenize
import re
import datetime
import numpy as np
import pickle

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
		"Florida Man who is a convicted felon honks horn at cops working an accident. Has numerous drugs and weapons in his car in plain sight.",
		"Florida Man bites off neighbor's ear because he wouldn't give him a cigarette.",
		"Florida Man pokes girlfriend in the eye after she served him waffles instead of pancakes.",
		"Florida Man, once arrested for fighting drag queen with a tiki torch while dressed like KKK member, now running for mayor.",
		"Florida Man claiming to be Teddy Roosevelt's relative banned from Holiday Inn after threatening to hit manager."
	]
	allStats = []

	userInputContextIn = "Florida"

	### Create filenames for output text and stats
	dateStr = datetime.datetime.now().strftime("%Y_%b_%d-%H_%M")
	filePrefix = "outputs/output_test_"
	filenameText = filePrefix + dateStr + ".txt"
	filenameStats =  filePrefix + dateStr + ".pickle"

	# Open file for output text
	with open(filenameText, 'w') as file:
		# For each input string
		for inputStr in userInputStrings:
			file.write(inputStr)
			print(inputStr)
			print()
			# For each of these contexts out
			for cOut in "India Africa Mexico Canada Netherlands Holland France Germany Texas Nevada Alabama Alaska Arizona Arkansas California Colorado".split():
				output, stats = changeContext(word_vectors, dependency_parser, wnl, inputStr, userInputContextIn, cOut)
				allStats += stats

				print(cOut)
				print(output)

				# Write context and text to output file
				file.write("\n\n")
				file.write(cOut)
				file.write("\n")
				file.write(output)
			file.write("\n\n\n")
	file.close()

	# Write statics to pickle for statsAnalyzer.py
	with open(filenameStats, 'wb') as file:
		pickle.dump(allStats, file)
	file.close()


def changeContext(word_vectors, dependency_parser, wnl, input, cIn, cOut):
	# To store:
	# context in, context out, word in, lemma, label in, word out, score

	# Hold the statistics for each conversion
	stats = []
	# Lookup tables to store context mappings
	lookup = {}
	lookup_rejection = []

	# Tokenize input
	text_dep = [my_tokenize(sentence.lower()) for sentence in sent_tokenize(input)]
	# Tokens => Parse tree
	parse = dependency_parser.parse_sents(text_dep)

	for tree in parse: # For each [sentence-tree]
		for dependency_sentence in tree: # For sentence-tree (no idea why sentence is wrapped)
			for dependency in dependency_sentence.triples(): # For each dependency in sentence-tree
				for word, label in [dependency[0], dependency[2]]: # For each (word, label) in dependency
					### Convert word to lemma if possible
					lemma = word
					try:
						lemma = wnl.lemmatize(word, label[0].lower())
					except Exception as e:
						pass

					# Only convert words if it has one of the following labels
					if label in ["NN", "VB"]:
						# Check if word has been converted before
						wordT = lookup.get(lemma)
						# If not, convert it
						if wordT is None:
							try:
								# Find best match
								results = word_vectors.most_similar(positive=[lemma, cOut.strip()], negative=[cIn.strip()])
								# Replace underscores with whitespaces
								wordT = results[0][0].replace("_", " ")
								score = results[0][1]
								# Store stats
								stats.append([cIn, cOut, word, lemma, label, wordT, score])
								# Threshold score
								if(0.4 <= score):
									lookup[lemma] = wordT
									print("      ", lemma.ljust(15), "=>", wordT.ljust(15), score)
								elif lemma not in lookup_rejection:
									lookup_rejection.append(lemma)
									print("REJECT", lemma.ljust(15), "=>", wordT.ljust(15), score)

							# Catch word-not-in-vocabulary error
							except Exception as e:
								print("Error:", e)
	
	### Rebuild sentence by replacing words with their mappings
	output = []
	# For each sentence in text
	for sentence in text_dep:
		# Replace words if possible
		newSentence = [lookup.get(word) or word for word in sentence]
		# Join words with space, add punctuation mark
		sentence = " ".join(newSentence) + "."
		# Add sentence to text
		output.append(sentence)
	# Join sentences with space
	return " ".join(output), stats
