import pickle
import numpy as np
import matplotlib.pyplot as plt

#inputFile = "outputs/output_test_2018_Oct_24-15_47.pickle"
inputFile = "outputs/output_test_2018_Oct_24-16_45.pickle"
#inputFile = "outputs/output_test_2018_Oct_25-23_10.pickle"

# Structure of each stat in stats:
# context in, context out, word in, lemma, label in, word out, score
with open (inputFile, 'rb') as fp:
    stats = pickle.load(fp)

unique_stats = [list(x) for x in set(tuple(x) for x in stats)]

def maxScore(lst):
	maxScore = 0
	maxStat = None
	for stat in lst:
		if maxScore < stat[6]:
			maxScore = stat[6]
			maxStat = stat
	return maxStat

def minScore(lst):
	minScore = 1
	minStat = None
	for stat in lst:
		if stat[6] < minScore:
			minScore = stat[6]
			minStat = stat
	return minStat

def getTransformations(lst, word):
	cOutStats = list(filter(lambda stat : stat[2].lower() == word, lst))
	transformations = list(set([(stat[2], stat[5]) for stat in cOutStats]))
	return transformations

# transitions where the output word equals the context-out, meaning that the input word is close to the context-in (Florida)
def getSmallVectors(lst):
	cOutStats = list(filter(lambda stat : stat[1].lower() == stat[5].lower(), lst))
	transformations = list(set([stat[2] for stat in cOutStats]))
	return transformations

# Transitions with min and max score
print("Max ", maxScore(unique_stats))
print("Min ", minScore(unique_stats))
print("Mean", np.mean([stat[6] for stat in unique_stats]))

### Create bar plot with 100 containers
# barData = np.zeros(50)
# for stat in unique_stats:
# 	barData[int(stat[6] * len(barData))] += 1
# plt.xlabel("Similarity score")
# plt.ylabel("Number of results")

# plt.bar(np.linspace(0, 1, len(barData)), barData, width=1/len(barData), align='edge')
# plt.savefig(inputFile + ".png")
# plt.show()


contexts = list(set( [stat[1] for stat in unique_stats] ))
labels = list(set( [stat[4] for stat in unique_stats] ))

### Calculate mean and covariance of labels
print("\nMean and Covariance of scores per label")
for label in labels:
	labelStats = list(filter(lambda stat : stat[4] == label, unique_stats))
	scores = [stat[6] for stat in labelStats]
	print(len(labelStats) ,label, np.mean(scores), np.cov(scores))
	if label != "NN":
		for stat in labelStats:
			print(stat[2].ljust(20), stat[5])
		print(list(set([stat[2] for stat in labelStats])))	
	
	# meanAndCov.append([cOut, np.mean(scores), np.cov(scores)])

### Calculate mean and covariance of scores
print("\nMean and Covariance of scores per context")
meanAndCov = [] 
for cOut in contexts:
	cOutStats = list(filter(lambda stat : stat[1] == cOut, unique_stats))
	scores = [stat[6] for stat in cOutStats]
	meanAndCov.append([cOut, np.mean(scores), np.cov(scores)])

meanAndCov = sorted(meanAndCov, key=lambda stat: stat[1], reverse=True)
for cOut, mean, cov in meanAndCov:
	print(cOut.ljust(12), "mean=%.03f cov=%.04f" % (mean, cov))

### Find some cool cultural transitions
print("\nSome cool cultural transitions")
for cOut in contexts:
	cOutStats = list(filter(lambda stat : stat[1] == cOut, unique_stats))
	print(cOut.ljust(12), getTransformations(cOutStats, "lottery"))

### Check which words are closely related to Florida
print("\nWords closely related to Florida")
for cOut in contexts:
	cOutStats = list(filter(lambda stat : stat[1] == cOut, unique_stats))
	print(cOut.ljust(12), getSmallVectors(cOutStats))


# for stat in sorted(unique_stats, key=lambda stat: stat[6]):
# 	print(stat[1].ljust(20), stat[2].ljust(20), stat[5].ljust(30), stat[6])

