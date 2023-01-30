pdf_scrapy.py and get_transaction.py are a set of python methods picks a pdf from a location on the file system and loads it into memory.
it scans through the pdf and match a pattern using regular expressions.
it then creates a list and convert it to a pandas dataframe and saves the data in a mongo db.
it uses uses the following librabries: py_pdf_parser, pandas and re (regular expressions).


web_scrape_todisk.py is a sample pseudo code for a client who wanted a webpage(html) scraped and stored in a pdf.
