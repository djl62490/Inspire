import goodreadsScraper

URL = "https://www.goodreads.com/work/quotes/2938937"

quotes = goodreadsScraper.getCleanSoup(URL).find_all("div", class_="quoteText")

goodreadsScraper.insertAll(quotes)
