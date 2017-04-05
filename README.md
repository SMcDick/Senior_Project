# Amazon Textbook Arbitrage - Senior Project

My product is a computer program capable of scraping Amazon's textbook catalog and pulling various points of data from the pages collected.

My project is split into 4 folders, each consisting of different types of programs:

  - AmazonTextbookArbitrage
  - TextBookAPI
  - RedditBot
  - TradeInPrediction

# Amazon Textbook Arbitrage

Please view the "HeavilyCommented.py" file for all the information about this program.  This is the main file I have been working on.

The Arbitrage Program: 

  - Generates Amazon URLs
  - Grabs the website and saves it to the /HTML/ Folder
  - Open up the HTML documents and grabs various points of data
  - Saves all results into a CSV
  - Saves profitable books into a JSON that can be used by a web app



```
Python Arbitrage.py
```



### Textbook API

This is basically a single use version version of the Arbitrage Finder program.  This program is able to scrape info from Biblio, Half, and Amazon.

```
#Example 1 - saving Biblio results to a CSV
>>> import TextbookAPI
>>> ASIN = '0131988425'
>>> ListOfASIN = []
>>> for i in range(100):
>>> 	ListOfASIN.append(ASIN)
>>> Results = TextbookAPI.Biblio(ListOfASIN, CSV='Biblio.csv', Debug=0)
```

## Reddit Bot

This is a program I created to market the site, but the use cases for this program are virtually endless.  This uses the Selenium module to automate browsing activities, but it's able to imitate regular browsers (Chrome, Safari, Firefox, etc) using the same method I use in the Arbitrage Finder program.  This program has the following features:

- Create Reddit Accounts
- Generate new Username/Passwords
- Refresh IP address using a 4G Android Phone & Hotspot
- Detect Reposting Posts on Reddit
- Generate Reddit Comments
- Post Reddit Comments
- Create Hotmail Accounts
- Verify Reddit Accounts
- "Break" Captcha
- Upvote/Downvote randomly
- Targeted Upvotes/Downvotes

# Trade-In Prediction

This is a program I made to predict trade in price based on data I've pull from the Amazon Scraping I've done.  I'm able to predict Trade in Price with 71% accuracy (adjusting for a 10% margin of error).

The Database CSV included in this repo is roughly 200,000 lines long, but the accuracy should increase as the dataset gets larger.

```
Python Predict.py
```