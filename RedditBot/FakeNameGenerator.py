import csv
import random
import sys
reload(sys)
sys.setdefaultencoding("utf-8")





with open('info.csv', 'rb') as f:
    reader = csv.reader(f)
    FakeInfo = list(reader)
with open('world-universities.csv', 'rb') as f:
    reader = csv.reader(f)
    CollegeList = list(reader)

def FirstName():
	Info = random.choice(FakeInfo)
	return Info[1]

def Gender():
	Info = random.choice(FakeInfo)
	return Info[0]

def MiddleInitial():
	Info = random.choice(FakeInfo)
	return Info[2]

def LastName():
	Info = random.choice(FakeInfo)
	return Info[3]

def Address():
	Info = random.choice(FakeInfo)
	return Info[4]

def City():
	Info = random.choice(FakeInfo)
	return Info[5]

def Zip():
	Info = random.choice(FakeInfo)
	return Info[7]

def State():
	Info = random.choice(FakeInfo)
	return Info[6]

def Password():
	Info = random.choice(FakeInfo)
	return Info[8]


def Birthday():
	Info = random.choice(FakeInfo)
	return Info[9]

def Occupation():
	Info = random.choice(FakeInfo)
	return Info[10]

def Company():
	Info = random.choice(FakeInfo)
	return Info[11]

def School():
	Found = False
	while Found == False:
		try:
			College = random.choice(CollegeList)
			College = str(College[0]).encode("ascii")
			if '(' not in str(College):
				Found = True
		except:
			Found = False
	return College


def TwoDates(start, end, timebetween):
	StartDate = random.randint(start, end)
	EndDate = StartDate + timebetween
	return [StartDate, EndDate]


def Title():
	Info = random.choice(FakeInfo)
	return Info[12]


