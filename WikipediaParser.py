import urllib
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


startURL = "https://en.wikipedia.org/wiki/Donald_Trump"

#filename to save results to
filename = "WikipediaMap.csv"
searched = []
searched.append("/wiki/Donald_Trump")

#number of levels to search
levels = 1

f = open(filename,"w")


def parsePage(myURL,count):
	try:
		thisFrontier = []
		#open and read the wikipedia page
		uClient = uReq(myURL)
		page_html = uClient.read()
		uClient.close();

		#find all paragraphs of text
		page_soup = soup(page_html, "html.parser")
		page_content = page_soup.body.find("div", {"id":"content"})
		body_content = page_content.find("div",{"id":"bodyContent"})
		body_text = body_content.find("div", {"id":"mw-content-text"})
		body = body_text.find("div",{"class":"mw-parser-output"})
		paragraphs = body.find_all("p")

		#parse page title and write as first column
		page_title = page_content.h1.text
		print(str(count) + " , " + page_title)
		f.write(page_title.replace(",","|")+ ",")


		#search for every link on the page
		for p in paragraphs:
			links = p.find_all("a")
			for link in links:
				try:
					url = link["href"]
					#ignore sources and on-page links
					if "#" not in url:
						try:
							title = link["title"].replace(",","|")
							#ignore certain types of wikipedia pages
							if "List" not in title and "Help:" not in title:
								#print(title + ": " + url)
								f.write(title + ",")
								#add pages that need to be searched
								if url not in searched and count > 0:
									thisFrontier.append(url)
									searched.append(url)
						except:
							continue#print("ERROR: " + url)
				except:
					continue#print("ERRROR READING URL")
		else:
			#next line of the csv
			f.write("\n");
			if count == 0:
				return
			#search all the links on this page
			for page in thisFrontier:
				parsePage("https://en.wikipedia.org" + page, count - 1)

	#not sure what these errors are but they're pretty infrequent
	except Exception as e:
		print(e)



parsePage(startURL,levels)


