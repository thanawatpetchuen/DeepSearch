from collections import Counter

import urllib.request
from bs4 import BeautifulSoup
# from martinluther import martinLuther
import sys


class wordCount:
    def __init__(self, file):
        self.file = file
        self.word = []

    def Count(self, k):
        self.readword = open("clean_{}".format(self.file), 'r+', encoding='utf-8')
        self.readword2 = self.readword.readlines()

        self.wordlist = [x.split() for x in self.readword2]
        # print(self.wordlist)
        # print(len(self.wordlist))
        flat_list = [item for self.wordlist in self.wordlist for item in self.wordlist]
        # print(flat_list)
        # print(len(flat_list))
        c = Counter(flat_list)
        result = c.most_common(k)
        try:
            print(c.get(['computer']))
        except:
            print("Not have computer!")
        return result

    def Count2(self):
        self.readword = open("clean_{}".format(self.file), 'r+', encoding='utf-8')
        self.readword2 = self.readword.readlines()
        self.wordlist = [x.split() for x in self.readword2]

        flat_list = [item for self.wordlist in self.wordlist for item in self.wordlist]

        c = Counter(flat_list)
        try:
            print(c['computer'])
            return c['computer'] + c['Computer']
        except:
            print("Not have computer!")
        # return result


class htmlparser(wordCount):
    def __init__(self, url, dest):
        super(htmlparser, self).__init__(dest)
        self.url = url
        self.dest = dest
        temp_html = ''

    def begin(self):
        urllib.request.urlretrieve(self.url, self.dest)

    def read_to_temp_html(self):
        temp = ''
        f = open(self.dest, 'r', encoding='utf-8')
        for line in f:
            temp += line
        f.close()
        self.temp = temp

    def beauiful_soup(self):
        bs = BeautifulSoup(self.temp, 'html.parser')
        cleantext = BeautifulSoup(self.temp, 'html.parser').text

        f = open("clean_{}".format(self.dest), 'w', encoding='utf-8')
        f.write(cleantext)
        f.close()
        bs_list = []
        for link in bs.select('a'):
            if link.has_attr('href') and ('http' in link['href']):
                bs_list.append(link['href'])
        return bs_list

    def setup(self):
        self.begin()
        self.read_to_temp_html()


if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/Computer'
    html = htmlparser(url, '{}.txt'.format(url.split('//')[-1].replace('/', '').replace('.', '').replace('=', '').replace('?', '')))
    html.setup()
    html_dict = dict()
    temp = html.beauiful_soup()
    print(temp)
    print(html.Count2())

    for link in temp:
        try:
            html_temp = htmlparser(link, '{}.txt'.format(link.split('//')[-1].replace('/', '').replace('.', '').replace('=', '').replace('?', '')))
            html_temp.setup()
            bs_html = html_temp.beauiful_soup()
            html_dict[link] = [bs_html, html_temp.Count2()]
            print(bs_html)
        except:
            print(sys.exc_info())

    print(html_dict)
