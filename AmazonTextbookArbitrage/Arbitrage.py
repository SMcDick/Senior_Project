from __future__ import division
import csv
import time
from datetime import datetime
import requests
import random
import re
import json
from datetime import datetime
import bs4
import math
import shutil
import RandomHeaders
import os
import threading




proxies = {
		  "http": '108.59.14.203:13010',
		  "https": '108.59.14.203:13010',
		}
###This is the line where I configure the Proxies I want to use


BookList = []
#This "List" will be filled up as the program runs

lenurl=15
# This is the amount of pages I want to generate per URL.  So clicking on page 2 in an Amazon search would be equivalent to setting this to "2"
URLs = []
#This list of URLs will be updated as the program runs
threads = 10
#Amount of times I want this to run simultaniously
Done = []
#This is the "Completed" pages list - currently set to 0 but it will be updated as the program runs

lock = threading.Lock()
#This will allow you to modify documents wihout disrupting threads that are currently updating the same documents.  It will wait until the other thread is finished before starting
global name
name = 0
#This is a global variable, which means that all threads will see it without importing a variable.  This "name" variable will be used to generate file names for saving scraped pages


def Name():
	global name
	name = name + 1
	location = 'HTML/' + str(name) + '.html'
	return location
#Calling this function will return a numerical value + '.html' to generate file names for the websites being saved

with open('Database.csv', 'w') as csv_file:
	writer = csv.writer(csv_file)
#This opens up "Database.csv", but it opens it as a new file.  If it already exists it will overwrite it with a blank document.  The 'w' stands for write, while an 'a' stands for append.

def Profitable(Book):
	return float(Book["Trade"]) - float(Book["Price"]) > 0 
#This will either return "True" or "False" depending on the profitability of the book

def get_dec(x):
	a = (float(''.join(ele for ele in x if ele.isdigit() or ele == '.')))
	a = float("{0:.2f}".format(a))
	return a
#This looks overly complicated, but it's basically converting a text or string - like: "$8.42" into a numerical value - like: 8.42


def ReturnElementsPage(page):
	Information = []
	#This is a local list - which means other python functions won't see it
	ProductSelector = '.a-fixed-left-grid-inner'
	#This is the CSS selector for the product on Amazon
	TradeSelector = '.a-text-normal .a-size-small .a-color-base'
	#This is the CSS selector for the trade in price on Amazon
	PriceSelector = '.a-spacing-none .a-size-base.a-color-base' #[-1] to select last element
	#This is the CSS selector for the purchase price on Amazon
	TitleSelector = '.s-access-title'
	#This is the CSS selector for the title on Amazon
	# Note that nothing is actually being done here - it's just defining the variables.
	for Product in page.select(ProductSelector):
		#This is selecting the individual products on the page and converting it into a list - then it's iterating over that list and calling each item "Product"
		try:
			#I'm using a try/except loop here, so it "Catches" any errors and ignores them
			NewData = {
			"ASIN": (str(Product.select('a')[0]).partition('/dp/')[2]).partition('/ref=')[0],
			#This is searching for the first "a" element, or the first link in the product section of the page scraped.  Then it's taking that link and splitting at apart at '/dp', and taking the second half
			#and splitting that half at '/ref=' and selecting the first half.  This returns the ASIN or product number of the Amazon Product.
			"Price": (get_dec(str(Product.select(PriceSelector)[-1])) + 3.99),
			"Title": Product.select(TitleSelector)[0].getText(),
			"Image": re.search("(?P<url>https?://[^\s]+)", str(Product.select('.s-access-image')[0]).split(',')[-1]).group("url")
			}
			try:
				NewData["Trade"] = get_dec(str(Product.select(TradeSelector)[0]))
			except:
				NewData["Trade"] = 0.00
			if len(str(NewData["Trade"])) < 2:
				NewData["Trade"] = 0
			Information.append(NewData) 
		except BaseException as exp:
			pass
	return Information


def DownloadURLs(URL):
	for URL in URL:
		try:
			res = requests.get(URL, headers=RandomHeaders.LoadHeader(), proxies=proxies)
			a = True
		except:
			try:
				res = requests.get(URL, headers=RandomHeaders.LoadHeader(), proxies=proxies)
				a = True
			except:
				a = False
				pass
		if a == True:
			FileName = Name()
			with open(FileName, "w") as f:
				f.write(res.content)
			print(str(FileName))


def ScrapeLocalFiles():
	time.sleep(random.randint(0, 20))
	for html in os.listdir("HTML/"):
		if html not in Done:
			Done.append(html)
			try:
				page = bs4.BeautifulSoup(open('HTML/' + str(html), 'r'), "lxml")
				Books = ReturnElementsPage(page)
				for Book in Books:
					for CurrentBook in BookList:
						try:
							if Book["ASIN"] == CurrentBook["ASIN"]:
								BookList.remove(CurrentBook)
								print('removed')

						except BaseException as exp:
							print(exp)
							pass
					try:
						with open('Database.csv', 'a') as csv_file:
							f = []
							writer = csv.writer(csv_file)
							f.append(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
							for key, value in Book.items():
								f.append(value)
							if len(f) == 6:
								writer.writerow(f)	
						if Book["Trade"] - Book["Price"] < 0:
							URL = 'https://www.amazon.com/dp/{}'.format(Book["ASIN"])
							res = requests.get(URL, headers=RandomHeaders.LoadHeader(), proxies=proxies)
							page = bs4.BeautifulSoup(res.text, "lxml")
							Book["Trade"] = get_dec(page.select('#tradeInButton_tradeInValueLine')[0].getText().replace('Gift Card.', ''))
							Book["Price"] = get_dec(page.select('#singleLineOlp .a-color-price')[0].getText()) + 3.99
							if Book["Trade"] - Book["Price"] < 0:
								BookList.append(Book)
					except:
						pass
			
			except UnicodeEncodeError:
				print('Unicode Error on {}'.format(str(html)))
				pass

def ReturnRecent(ASIN):
	for info in reversed(list(csv.reader(open(Database, 'r')))):
		if str(ASIN) in str(info):
			return info





def chunks(list, chunk_size):
    return [list[offs:offs+chunk_size] for offs in range(0, len(list), chunk_size)]



def Expired(dict, minutes=15):
	return float(time.strftime("%Y%m%d%H%M%S")) - float(dict["Time"]) > (60*int(minutes))



def UpdateJSON(JSONFile='data.txt'):
	while True:
		with open(JSONFile, 'w') as outfile:
			json.dump(BookList, outfile)


ListOfKeywords='Keywords.txt'

Keywords = [line.rstrip('\n') for line in open(ListOfKeywords)]
for keyword in Keywords:
	keyword = keyword.replace(" ", "+")
	for pagenumber in range(1, lenurl):
		URLs.append('https://www.amazon.com/s/%3Atextbooks&page={}&keywords={}&ie=UTF8&rh=n%3A283155%2Ck'.format(pagenumber, keyword))

URLs = chunks(URLs, int(len(URLs) / threads) + 1)


threads = threading.Thread(target=UpdateJSON)
threads.start()
threads = [threading.Thread(target=DownloadURLs, args=(url,)) for url in URLs]
for thread in threads:
	thread.start()
threads = [threading.Thread(target=ScrapeLocalFiles) for i in range(30)]
for thread in threads:
	thread.start()
