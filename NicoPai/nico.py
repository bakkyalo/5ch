# nico.py
# Author: Kasumin
import urllib.request
from html.parser import HTMLParser
import matplotlib.pyplot as plt
# from bs4 import BeautifulSoup

# with urllib.request.urlopen('https://fate.5ch.net/test/read.cgi/lovelive/1693637460/') as response:
#     html = response.read()
#     print(html)

commaArray = []
nicoPaiArray = [710]

# HTML parser
# Find <span class="date">~</span> and push the comma value into commaArray.
class findDateParser(HTMLParser):
    isInDate = False

    def handle_starttag(self, tag, attrs):
        # Note: attrs is a list and attrs[0] is a tuple such as {'class', 'date'}.
        if tag == "span" and attrs[0][1] == "date":
            self.isInDate = True
            # print(attrs[0][1])

            # for x in attrs:
            #     print(type(x))
            #     print(x[1])

            # print("Encountered a start <span> tag.")
    
    def handle_endtag(self, tag):
        if tag == "span":
            self.isInDate = False
            # print("Encountered an end </span> tag.")
    
    def handle_data(self, data):
        if self.isInDate == True:
            commaArray.append(int(data[-2:]))

# Request html from 5ch
req = urllib.request.Request('https://fate.5ch.net/test/read.cgi/lovelive/1693637460/')
req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36')

with urllib.request.urlopen( req ) as res:
    text = res.read().decode('cp932')
    # print(text)

    parser = findDateParser()
    parser.feed(text)
    # print(commaArray)


# Calculate Nico-Senpai's oppai using commaArray
def calcNicoPai():
    oppai = 710
    for comma in commaArray:
        if comma == 25:
            oppai += 10
        elif comma == 71:
            oppai = 710
        elif comma % 11 == 0:
            oppai -= 10
        else:
            oppai += 1
        
        nicoPaiArray.append(oppai)

if __name__ == '__main__':
    calcNicoPai()

    plt.figure(figsize=(9, 6))
    plt.plot([x / 10 for x in nicoPaiArray], color="#ff66d9")
    plt.title('https://fate.5ch.net/test/read.cgi/lovelive/1693637460/')
    plt.xlabel('# of res')
    plt.ylabel('Nico-Senpai\'s Oppai [cm]')
    plt.savefig('nicopai.png')
    # plt.show()