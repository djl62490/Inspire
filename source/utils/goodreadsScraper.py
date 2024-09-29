import requests
from bs4 import BeautifulSoup
import pglib
from langdetect import detect

def getCleanSoup(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    prettySoup = BeautifulSoup(soup.prettify(), "html.parser")

    for script in prettySoup.findAll("script"):
        script.replace_with("")
    return prettySoup
    
def insertAll(quotes):
    for element in quotes:
        quote = getQuote(element)
        author = getAuthor(element)
        title = getTitle(element)

        #skip quote if not english
        if not isEnglish(quote): continue

        # if no source available, use "unknown"
        sourceType = 5 if title==None else 1

        # insert info into db
        pglib.insert(quote, author, sourceType, title)

def insert(quotes, idx):
    quote = getQuote(quotes[idx])
    author = getAuthor(quotes[idx])
    title = getTitle(quotes[idx])

    if title == None: sourceType = 5 
    else: sourceType = 1

    pglib.insert(quote, author, sourceType, title)

# Prints the scraped quote texts, authors, and sources for debugging purposes
def debugPrint(quotes):
    for element in quotes:
        # buffer elements
        quote = element.contents[0].strip()
        author = getAuthor(element)
        title = getTitle(element)
 
        # print all
        print(quote + "\n")
        if author == None:
            print("N/A" + "\n")
        print(author + "\n")
        if title == None:
            print("N/A" + "\n" + "\n")
        else:
            print(title + "\n" + "\n")

# Returns cleaned up quote text from the html element
def getQuote(element):
    return element.contents[0].strip()

# Returns the author of a single html element
def getAuthor(element):
    try:
        author = element.find("span",class_="authorOrTitle").contents[0].strip().replace(",","")
    except:
        author = None
    return author

# Returns the source title of a single html element
def getTitle(element):
    try:
        title = element.find("a",class_="authorOrTitle").contents[0].strip() 
    except:
        title = None
    return title

# Returns true is text is english, false if not english
def isEnglish(text):
    return True if detect(text)=="en" else False