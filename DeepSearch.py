from collections import Counter

import urllib.request
from bs4 import BeautifulSoup
# from martinluther import martinLuther
from treelib import Node, Tree
import sys
import re
import time
from operator import itemgetter
import dill

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

<<<<<<< HEAD
    def saveFile(self,url_root):
        dill_file = '{}_tree'.format(url_root)
=======

def update_percent(temp, p):
    return (p/int(len(temp)))*100

>>>>>>> bd781664e5c08bcab595917265a944274d79e106
if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/Computer'
    html = htmlparser(url, '{}.txt'.format(url.split('//')[-1].replace('/', '').replace('.', '').replace('=', '').replace('?', '')))
    html.setup()
    html_dict = dict()
    temp = html.beauiful_soup()
    tree = Tree()

    # print(len(temp))
<<<<<<< HEAD
    temp = temp[0:5]
=======
    temp = temp[0:50]
    percent = 0
    print("Percent: {}%".format(update_percent(temp, percent)))
>>>>>>> bd781664e5c08bcab595917265a944274d79e106
    tree.create_node("Root", "root", data={'related_link': temp, 'count': html.Count2()})
    print(tree, 'newdea')
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
            percent += 1
            print("Percent: {}%".format(update_percent(temp, percent)))
            tree.show()
        except:
            percent += 1
            print("Percent: {}%".format(update_percent(temp, percent)))
            print(sys.exc_info())

    f = open('final.txt', 'w+', encoding='utf-8')
    f.write(str(html_dict))
    f.close()
    # print(html_dict)
    print(tree.to_json(with_data=True))
    tree.show()

    start = time.time()
    temp_tree = [{'link': tree[node].tag, 'count': tree[node].data['count']['computer']} for node in tree.expand_tree(mode=tree.ZIGZAG)
                 if (tree[node].data is not None)]
    stop = time.time()
    print(tree['root'].data)
    print(temp_tree)
    newlist = sorted(temp_tree, key=itemgetter('count'), reverse=True)
    print("Total time: {}s".format(stop-start))
    print(newlist)
    with open('result/tree.json', 'w+') as fs:
        fs.write(tree.to_json(with_data=True))
    tree.save2file('result/tree.txt')
    print("SUCCESS, Percent: {}%".format(update_percent(temp, percent)))

