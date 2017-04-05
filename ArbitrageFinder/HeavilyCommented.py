from __future__ import division
#python 2.7 deals with non-int division very weird.  For instance - 1/2 == 1 and 3/2 == 2.
import csv
#This module allows me to edit CSV or excel files from Python
import time
#This allows the program to keep time.  I use this to pause or sleep the program to set intervals.
from datetime import datetime
#This allows the program to grab the current date and time
import requests
#This module allows you to grab web pages without accessing them from a browser
import random
#this allows random choice and random integer generation
import re
#This helps with pattern matching, specifically used in this program for finding URLs
import json
#I'm using json to store profitable books to pull them and add to the website
import bs4
#this helps with CSS selection if used with the requests module
import shutil
#this is a better way of doing OS commands and moving documents
import RandomHeaders
#program I wrote to randomize browser headers and decrease the rate limitations on the Amaozn site
import os
#allows you to run os commands from python
import threading
#lets you run functions simultaniously




proxies = {
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
			#This is selecting the price on the page by searching for the previously defined Price CSS selector and grabbing the last element it finds on this portion of the page
			#Then it's using the "get_dec" function higher up in the program to convert it into something we can Add/Subtract from.  Then I add the assumed 3.99 shipping cost for textbooks
			"Title": Product.select(TitleSelector)[0].getText(),
			#This selects the title css elements and removes the HTML tags around it
			"Image": re.search("(?P<url>https?://[^\s]+)", str(Product.select('.s-access-image')[0]).split(',')[-1]).group("url")
			#This searches for the '.s-access-image' css element and selects the first one.  Then it splits it at the ',' character and returns the last result
			#tuses regex to search for a url in that string.  This is the address of the books cover
			}
			try:
				#it's going to try/except, as books with no trade in value will not have the TradeSelector css element, and will return an error
				NewData["Trade"] = get_dec(str(Product.select(TradeSelector)[0]))
				#This is selecting the Trade in value using the previously defined CSS selector, and converting it into a number we can add/subtract from
			except:
				NewData["Trade"] = 0.00
				#if the tradeinselector css element is not found, that means the book is not eligible for trade in
			if len(str(NewData["Trade"])) < 2:
				NewData["Trade"] = 0
				#This was getting some errors where the program would return single number trade values - like $4 or $7.  This shouldn't happen, and it was an error from grabbing a rental price on the site
			Information.append(NewData) 
			#This appends the NewData dictionary we just created to the information list that was created in this function.
		except BaseException as exp:
			#This is a method of ignoring errors in python.  If it finds an error it just passes.  If i put print(exp) it will print the error.  I very rarely get errors in this function, so I pass
			# on the ones that cause errors and don't save that book
			pass
	return Information
	#This returns that local list created at the beginning of this program.


def DownloadURLs(URL):
	#This function is "downloading" the pages from amazon
	#URL is actually a list, and it will iterate over the entire list of URLs
	for URL in URL:
		try:
			res = requests.get(URL, headers=RandomHeaders.LoadHeader(), proxies=proxies)
			#This grabs the URL it's current on - the header is randomized and the proxies are the same proxies defined earlier.
			a = True
			#This is a placeholder to res != None or res == None
		except:
			try:
				res = requests.get(URL, headers=RandomHeaders.LoadHeader(), proxies=proxies)
				#This grabs the URL it's current on - the header is randomized and the proxies are the same proxies defined earlier.
				a = True
				#This is a placeholder to res != None or res == None
			except:
				a = False
				#This is a placeholder to res != None or res == None
				pass
		if a == True:
			#This is a placeholder to res != None or res == None
			FileName = Name()
			#This calls that filename function from earlier
			with open(FileName, "w") as f:
				#it names the file the result of the Name() function
				f.write(res.content)
				#it writes the webpage to the file
			print(str(FileName))
			#it prints x.HTML, with x representing the current page number it's on


def ScrapeLocalFiles():
	time.sleep(random.randint(0, 20))
	#This makes it so all 30 threads don't start at the exact same time
	for html in os.listdir("HTML/"):
		#This iterates over all the HTML files in the HTML/ directory
		if html not in Done:
			#This means another function or thread hasn't already scanned it
			Done.append(html)
			#This will mark that file as already been scanned
			try:
				page = bs4.BeautifulSoup(open('HTML/' + str(html), 'r'), "lxml")
				#This selects the file and converts it into a BS4 page
				Books = ReturnElementsPage(page)
				#This will run the ReturnElementsPage function on that BS4 page
				for Book in Books:
					for CurrentBook in BookList:
						#BookList is the current books that are profitable
						try:
							if Book["ASIN"] == CurrentBook["ASIN"]:
								BookList.remove(CurrentBook)
								print('removed')
								#This updates the current book in BookList

						except BaseException as exp:
							print(exp)
							#print the error, but still ignore it
							pass
					try:
						with open('Database.csv', 'a') as csv_file:
							#opens up the main database csv to store ALL book info
							f = []
							#f is  blank list that will be filled
							writer = csv.writer(csv_file)
							#writing to the CSV file
							f.append(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
							#adds the current time to the "f" list
							for key, value in Book.items():
								#This iterates over all the dictionary results in the Book dictionary that was created by ReturnElementsPage()
								f.append(value)
								#This add the value to the "f" list
							if len(f) == 6:
								#This confirms that all values were grabbed by the program.  Occasionally the IMG file will be blank so this program will ignore those
								writer.writerow(f)
								#It writes the f list to the csv defined as writer	
						if Book["Trade"] - Book["Price"] > 0:
							#Determines if the book is profitable
							URL = 'https://www.amazon.com/dp/{}'.format(Book["ASIN"])
							#Defines the Amazon page for that book
							res = requests.get(URL, headers=RandomHeaders.LoadHeader(), proxies=proxies)
							#Pulls the website and saves the result as res
							page = bs4.BeautifulSoup(res.text, "lxml")
							#Converts res to res.text and loads it into BS4
							Book["Trade"] = get_dec(page.select('#tradeInButton_tradeInValueLine')[0].getText().replace('Gift Card.', ''))
							#Selects the Trade in css selector on the main book page instead of search results to confirm that the saved value is correct
							Book["Price"] = get_dec(page.select('#singleLineOlp .a-color-price')[0].getText()) + 3.99
							#Selects the Price css selector on the main book page instead of search results to confirm that the saved value is correct
							if Book["Trade"] - Book["Price"] < 0:
								BookList.append(Book)
								#If the book is confirmed to be profitable, it adds the ASIN to the BookList list
					except:
						pass
			
			except UnicodeEncodeError:
				#Unicode errors are really annoying but pretty rare.  Changing the entire program to default to utf8 caused a lot of problems, so I just ignore the errors and skip on any books that have these.
				print('Unicode Error on {}'.format(str(html)))
				pass

def ReturnRecent(ASIN):
	for info in reversed(list(csv.reader(open(Database, 'r')))):
		#Database contains the Database of Books - the list is iterated over and each line is referred to as "info"
		if str(ASIN) in str(info):
			#If the ASIN matches, it returns the first result from the reversed list - which is the newest pulled data for that book
			return info





def chunks(list, chunk_size):
	#This breaks a list of URLs into a list of lists of URLs
    return [list[offs:offs+chunk_size] for offs in range(0, len(list), chunk_size)]



def Expired(dict, minutes=15):
	#Determines if the book price has "Expired" and if it needs to be rescanned to determine if it's still profitable
	return float(time.strftime("%Y%m%d%H%M%S")) - float(dict["Time"]) > (60*int(minutes))



def UpdateJSON(JSONFile='data.txt'):
	#This is the main file that the website uses to pull information from the program
	while True:
		with open(JSONFile, 'w') as outfile:
			json.dump(BookList, outfile)
			#This continously writes the BookList list to the data.txt json file.


ListOfKeywords='Keywords.txt'
#This is a list of commonly searched academic keywords.  I add to this list frequently, and I've scanned a bunch of different college course sites to find relevant keywords to search.

Keywords = [line.rstrip('\n') for line in open(ListOfKeywords)]
#This converts that "Keywords.txt" file into a list by removing the new line ("\n") characters.
for keyword in Keywords:
	keyword = keyword.replace(" ", "+")
	#Amazon doesn't allow spaces in their URLs, so it is replaced with a "+"
	for pagenumber in range(1, lenurl):
		#This goes in a range of 1 (Page 1) to the number inputted at the top of the program
		URLs.append('https://www.amazon.com/s/%3Atextbooks&page={}&keywords={}&ie=UTF8&rh=n%3A283155%2Ck'.format(pagenumber, keyword))
		#This adds to the URL to the URLs list

URLs = chunks(URLs, int(len(URLs) / threads) + 1)
#This breaks that URLs list into a list of lists of URLs


threads = threading.Thread(target=UpdateJSON)
threads.start()
#Simply starting the UpdateJSON thread


threads = [threading.Thread(target=DownloadURLs, args=(url,)) for url in URLs]
for thread in threads:
	thread.start()
#Starting the DownloadURLs function for every chunk of URLs set - len(URLs) should be equal to int(ThreadCount)

threads = [threading.Thread(target=ScrapeLocalFiles) for i in range(30)]
for thread in threads:
	thread.start()
#This starts 30 instances of the ScrapeLocalFiles thread