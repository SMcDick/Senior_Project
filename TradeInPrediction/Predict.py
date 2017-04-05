from __future__ import division
from sklearn import tree
import csv
import time
from sklearn.metrics import accuracy_score

def Convert(x):
	a = (float(''.join(ele for ele in x if ele.isdigit() or ele == '.')))
	a = float("{0:.2f}".format(a))
	return a

Data = []
Price = []
Trade = []
Test = []
true = []
predict = []
Correct = []

fh = open('database.csv', 'r')
for line in fh:
	try:
		ap = line.strip().split(',')
		if len(str(ap[3])) > 10:
			pass
		else:
			Data.append([str(Convert(ap[3])), str(Convert(ap[4]))])
	except BaseException as exp:
		pass

for i in range(len(Data)):
	save = Data[i]
	Data.remove(save)
	Test.append(save)
	if i > 100:
		break
for e in Data:
	Price.append([e[0]])
for a in Data:
	Trade.append(a[1])



clf = tree.DecisionTreeClassifier()
clf = clf.fit(Price, Trade)
for i in range(len(Test)):
	inpt = Test[i]
	a = clf.predict(inpt[0])
	true.append(str(Convert(inpt[1])))
	predict.append(str(Convert(a[0])))
for i in range(len(true)):
	difference = Convert(predict[i]) - Convert(true[i])
	percent = (difference / Convert(true[i])) * 100
	if int(percent) < 10:
		Correct.append(i)

	'''if abs() < 4:
		Correct.append(i)'''
accurate = len(Correct) / len(Test)
accurate = accurate * 100
print('{}% Accuracy'.format(accurate))