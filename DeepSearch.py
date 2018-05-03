from collections import Counter

import urllib.request
from bs4 import BeautifulSoup
# from martinluther import martinLuther
from treelib import Node, Tree
import sys
import re
import time

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
        words = re.findall(r'\w+', open("clean_{}".format(self.file), encoding='utf-8').read())
        # self.readword = open("clean_{}".format(self.file), 'r+', encoding='utf-8')
        # self.readword2 = self.readword.readlines()
        # self.wordlist = [x.split() for x in self.readword2]
        #
        # flat_list = [item for self.wordlist in self.wordlist for item in self.wordlist]

        c = Counter(words)
        # print(c)
        try:
            # print(c['computer'])
            return int(c['computer']) + int(c['Computer'])
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
    tree = Tree()
    # print(len(temp))
    temp = temp[0:100]
    tree.create_node("Root", "root")
    # print(html.Count2())

    for link in temp:
        try:
            html_temp = htmlparser(link, '{}.txt'.format(link.split('//')[-1].replace('/', '').replace('.', '').replace('=', '').replace('?', '')))
            html_temp.setup()
            bs_html = html_temp.beauiful_soup()
            html_dict[link] = [bs_html, html_temp.Count2()]
            tree.create_node(link, link, parent='root', data={'related_link': bs_html, 'count': html_temp.Count2()})
            if len(bs_html) > 0:
                for link2 in bs_html:
                    html_temp2 = htmlparser(link2, '{}.txt'.format(link.split('//')[-1].replace('/', '').replace('.', '').replace('=', '').replace('?', '')))
                    html_temp2.setup()
                    bs_html2 = html_temp2.beauiful_soup()
                    tree.create_node(link2, link2, parent=link, data={'related_link': bs_html2, 'count': html_temp2.Count2()})
            # print(bs_html)
            tree.show()
        except:
            print(sys.exc_info())

    f = open('final.txt', 'w+', encoding='utf-8')
    f.write(str(html_dict))
    f.close()
    # print(html_dict)
    print(tree.to_json(with_data=True))
    tree.show()

    start = time.time()
    temp_tree = [{'link':tree[node].tag, 'count': tree[node].data['count']} for node in tree.expand_tree(mode=tree.ZIGZAG)
                 if (tree[node].data is not None)]
    stop = time.time()
    print(temp_tree)
    print("Total time: {}s".format(stop-start))
