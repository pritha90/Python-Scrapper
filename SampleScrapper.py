from requests import session
import re
import sys
from bs4 import BeautifulSoup, Comment
import HTMLParser
import urllib2
with session() as c:
	i = 1
	while(i>0):
		toefl_url = "http://www.toeflgoanywhere.org/asu-search/index.php?c=search&m=result&keywords=&country=US&perpage=2000&pagenum="+str(i)+"&search_by=location"
		response = c.get(toefl_url)
		soup =  BeautifulSoup(response.content, "html.parser")
		rows = soup.findAll('tr',{"class","main-row"})
		range = soup.find("div", {"class","select-box"})
		range_split = range.text.split("of")
		total = int(range_split[1].split("|")[0])
		items_crawled = int(range_split[0].split("-")[1])
		if(items_crawled == total):
			i = 0
		else:
			i+=1
		for row in rows:
			code = row.findAll("div" ,{"class","id-code"})
			name = row.text.strip().split("\n")[0]
			dicode = row.text.strip().split("\n")[1].strip()
			matchObj = re.match( r'DI Code: ([A-Za-z0-9]+) .*', dicode, re.M|re.I)
			with open("toefl_codes.csv","a+") as g:
				g.write(name.encode('utf-8').strip()+","+dicode.encode('utf-8').strip()+"\n")
