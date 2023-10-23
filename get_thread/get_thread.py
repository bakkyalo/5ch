import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib import ticker  # 16進数にする為のもの
import re  # 正規表現

title_array = []
dataset = []

URL = 'https://eagle.5ch.net/livejupiter/subback.html'

# なんJ の現行スレタイを取ってくる
def fetchThreadTitle():
    global title_array
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    titleList = soup.find('small', id='trad').find_all('a')
    title_array = [t.text.split(' ')[1] for t in titleList]
    # print(title_array)


# 読み方が あ～し で始まる常用漢字がすべて入っている a_shi.txt を読み込む
def loadAtoSHI():
    f = open('./a_shi.txt', mode='r')
    a_to_shi = f.read().replace('\n', '')

    f = open('./han.txt', mode='r')
    global han
    han = f.read().replace('\n', '')

    # a-shi に無いやつを探す
    cnt = 0
    for c in han:
        if(not c in a_to_shi):
            # print(c, c in a_to_shi)
            cnt += 1
    print(cnt)


    # title も表示する
    cnt = 0
    re_hanji = re.compile(r'[\u4e00-\u9fff]')
    for title in title_array:
        for c in title:
            # まず漢字かどうか
            if(re_hanji.fullmatch(c)):
                if(not c in a_to_shi):
                    print(c , title, " not found.")
                    cnt += 1
    print(cnt)


# 正規表現による NG のテスト
def ngByRegex():
    pattern = "^[あ-ん]*([" + han + "][あ-ん]*){4,}$"
    # ng_reg = re.compile(pattern)
    ng_reg = re.compile('{}'.format(re.escape(pattern)))

    cnt = 0
    for title in title_array:
        if(ng_reg.fullmatch(title)):
            print("NG: ", title)
            cnt += 1
    print("NG: " , cnt, "/", len(title_array))

    cnt = 0
    for title in title_array:
        if(not ng_reg.fullmatch(title)):
            print("OK: ", title)
            cnt += 1
    print("OK: " , cnt, "/", len(title_array))


# 文字コードの解析
def analyzeCharacter():
    global title_array
    for title in title_array:
        for chara in title:
            unicode = chara.encode('unicode-escape')
            order = ord(chara)
            dataset.append(order)

            # 関係ないと思われる物は削除したい

            with open('dataset.csv', mode='a') as f:
                f.write(chara + "," + str(order) + "," + str(unicode) + "\n") 
            
            with open('han.txt', mode='a') as f:
                if int('0x4e00', 16) <= ord(chara) and ord(chara) <= int('0x9fff', 16):
                    f.write(chara)

        # print(t.encode('unicode-escape'))
    
def createHistogram():
    # make histogram
    fig, ax = plt.subplots()
    ax.hist(dataset, bins=128)

    def hex_formatter(x, pos) :
        return hex(int(x))

    hex_format = ticker.FuncFormatter(hex_formatter)

    ax.xaxis.set_major_formatter(hex_format)

    # hiragana band
    # ax.fill_between(dataset, 0, 1, where= dataset < 10000)
    ax.set_xlabel('Unicode')
    ax.set_title('Unicode distribution of Nan-J thread title')


    ax.vlines(x=ord("ぁ"), ymin=0, ymax=500, label='\\u3041', colors='r', linestyles='dashed', linewidth=1)
    ax.vlines(x=ord("ゔ"), ymin=0, ymax=500, label='\\u3094', colors='r', linestyles='dashed', linewidth=1)

    # ax.vlines(x=int('0x3400', 16), ymin=0, ymax=500, label='\\u3400', colors='b', linestyles='dashed', linewidth=1)
    ax.vlines(x=int('0x4e00', 16), ymin=0, ymax=500, label='\\u4e00', colors='b', linestyles='dashed', linewidth=1)
    ax.vlines(x=int('0x9fff', 16), ymin=0, ymax=500, label='\\u9fff', colors='b', linestyles='dashed', linewidth=1)
    ax.legend()


    fig.savefig('unicode_distribution.png')
    


        


if __name__ == '__main__':
    fetchThreadTitle()
    analyzeCharacter()
    createHistogram()
    loadAtoSHI()
    ngByRegex()
