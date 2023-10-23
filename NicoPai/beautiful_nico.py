# beautiful_nico.py
# Author: Kasumin
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

commaArray = []
nicopaiArray = [710]

# Fetch all comma values from 5ch's html using requests and BS4
def fetchComma():
    response = requests.get('https://fate.5ch.net/test/read.cgi/lovelive/1693637460/')
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find <span class="date">~</span> and push the comma value into commaArray.
    dates = soup.find_all('span', {'class': 'date'})
    for d in dates:
        commaArray.append( int(d.get_text()[-2:]) )

# Calculate Nico-Senpai's oppai using commaArray
def calcNicopai():
    # First, calculate oppai in [mm] to avoid float error propagation
    global nicopaiArray
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
        
        nicopaiArray.append(oppai)
    
    # Finally, convert [mm] units to [cm]
    nicopaiArray = [ x / 10 for x in nicopaiArray ]

# Create a graph of Nico-Senpai's oppai fluctuations
def createGraph():
    # record maximun, minimum, and latest oppai
    maxY = max(nicopaiArray)
    maxX = nicopaiArray.index(maxY)

    minY = min(nicopaiArray)
    minX = nicopaiArray.index(minY)

    nowX = len(nicopaiArray) - 1
    nowY = nicopaiArray[nowX]

    fig, ax = plt.subplots(figsize=(9, 6))
    
    # Title and label
    ax.set_title('https://fate.5ch.net/test/read.cgi/lovelive/1693637460/', fontsize=14)
    ax.set_xlabel('# of res', fontsize=18)
    ax.set_ylabel('Nico-Senpai\'s Oppai [cm]', fontsize=18)
    ax.tick_params(labelsize=14)

    # Setup help line
    ax.xaxis.set_minor_locator(MultipleLocator(10))
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    ax.grid(which='major')
    ax.grid(which='minor', color='#CCCCCC', linestyle='--')
    ax.axhline(71, color='#777777')

    # plot graph
    ax.plot(nicopaiArray, color="#ff66d9")

    # insert minimum oppai
    if nowX != minX:
        ax.text(minX, minY, '{:.1f} cm'.format(minY), fontsize='large', \
                verticalalignment='top', horizontalalignment='right')
    # insert maximum oppai
    if nowX != maxX:
        ax.text(maxX, maxY, '{:.1f} cm'.format(maxY), fontsize='large', \
                verticalalignment='bottom', horizontalalignment='right')
    # insert current oppai
    ax.text(nowX, nowY, '{:.1f} cm'.format(nowY), fontsize='large', \
                verticalalignment='center', horizontalalignment='left')

    fig.savefig('beautiful_nicopai.png')
    # plt.show()

if __name__ == '__main__':
    fetchComma()
    calcNicopai()
    createGraph()
