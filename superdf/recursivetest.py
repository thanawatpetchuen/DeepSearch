from collections import Counter

import urllib.request
from bs4 import BeautifulSoup
# from martinluther import martinLuther
from treelib import Node, Tree
import sys
import re
import time
from operator import itemgetter
import shutil
import os
import json


class wordCount:
    def __init__(self, file):
        self.file = file
        self.word = []

    def Count(self, k):
        self.readword = open("temp/clean_{}".format(self.file), 'r+', encoding='utf-8')
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
        words = re.findall(r'\w+', open("temp/clean_{}".format(self.file), encoding='utf-8').read())
        c = Counter(words)
        # print(c)
        try:
            # print(c['computer'])
            return c
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
        urllib.request.urlretrieve(self.url, 'temp/'+self.dest)

    def read_to_temp_html(self):
        temp = ''
        f = open('temp/'+self.dest, 'r', encoding='utf-8')
        for line in f:
            temp += line
        f.close()
        self.temp = temp

    def beauiful_soup(self):
        bs = BeautifulSoup(self.temp, 'html.parser')
        cleantext = BeautifulSoup(self.temp, 'html.parser').text

        f = open("temp/clean_{}".format(self.dest), 'w', encoding='utf-8')
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



def update_percent(temp, p):
    return (p/int(len(temp)))*100

class deep_search:
    def __init__(self):
        url = 'https://en.wikipedia.org/wiki/Computer'
        html = htmlparser(url, '{}.txt'.format(url.split('//')[-1].replace('/', '').replace('.', '').replace('=', '').replace('?', '')))
        html.setup()
        self.html_dict = dict()
        temp = html.beauiful_soup()
        self.tree = Tree()
        self.level = 0
        # print(len(temp))
        # self.temp = temp[0:100]
        self.temp = temp
        self.percent = 0
        print("Percent: {}%".format(update_percent(temp, self.percent)))
        self.tree.create_node("Root", "root", data={'related_link': temp, 'count': html.Count2()})
        self.unsearch = []

    def deepsearch(self, link, temp):
        if len(temp) == 0:
            return
        if self.level > 1:
            print("Over!")
            print("Level: ", self.level)
            self.level = 0
            self.unsearch.append(self.tree.get_node(link))
            return
        else:
            print("Level: ", self.level)
            for link2 in temp:
                print(link2)
                try:
                    html_temp2 = htmlparser(link2, '{}.txt'.format(
                        link.split('//')[-1].replace('/', '').replace('.', '').replace('=', '').replace('?', '')))
                    html_temp2.setup()
                    bs_html2 = html_temp2.beauiful_soup()
                    self.tree.create_node(link2, link2, parent=link, data={'related_link': bs_html2, 'count': html_temp2.Count2()})
                    if len(bs_html2) > 0:
                        self.level += 1
                        return self.deepsearch(link2, bs_html2)
                except:
                    print(sys.exc_info())
        # pass

    def search(self):
        for link in self.temp:
            try:
                html_temp = htmlparser(link, '{}.txt'.format(link.split('//')[-1].replace('/', '').replace('.', '').replace('=', '').replace('?', '')))
                html_temp.setup()
                bs_html = html_temp.beauiful_soup()
                self.html_dict[link] = [bs_html, html_temp.Count2()]
                self.tree.create_node(link, link, parent='root', data={'related_link': bs_html, 'count': html_temp.Count2()})
                # Start
                # if len(bs_html) > 0:
                #     self.level += 1
                #     print("Level: ", self.level)
                #     self.deepsearch(link, bs_html)
                # print(bs_html)
                # End
                self.percent += 1
                print("Percent: {}%".format(update_percent(self.temp, self.percent)))
                self.tree.show()
            except:
                self.percent += 1
                print("Percent: {}%".format(update_percent(self.temp, self.percent)))
                print(sys.exc_info())

        self.finalize()

    def finalize(self):

        f = open('final.txt', 'w+', encoding='utf-8')
        f.write(str(self.html_dict))
        f.close()
        # print(html_dict)
        print(self.tree.to_json(with_data=True))
        self.tree.show()

        start = time.time()
        temp_tree = [{'link': self.tree[node].tag, 'count': dict(self.tree[node].data['count'])} for node in self.tree.expand_tree(mode=self.tree.ZIGZAG)
                     if (self.tree[node].data is not None)]
        stop = time.time()
        print(self.tree['root'].data)
        print(temp_tree)
        # newlist = sorted(temp_tree, key=itemgetter('count'), reverse=True)
        print("Total time: {}s".format(stop-start))
        # print(newlist)
        with open('result/tree.json', 'w+') as fs:
            fs.write(self.tree.to_json(with_data=True))
        self.tree.save2file('result/tree.txt')
        # print(type(temp_tree))
        temp_dict = {}
        for i, item in enumerate(temp_tree):
            temp_dict['item_{}'.format(i)] = item
        # print(temp_dict)
        with open('result/jt.json', 'w', encoding="utf-8") as f:
            json.dump(temp_dict, f)
        print("SUCCESS, Percent: {}%".format(update_percent(self.temp, self.percent)))
        print("=======Unsearch=======")
        print(self.unsearch)
        print("======================")
        shutil.rmtree('temp')
        os.mkdir('temp')


if __name__ == '__main__':
    dp = deep_search()
    dp.search()
