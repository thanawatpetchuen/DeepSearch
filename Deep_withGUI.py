from time import sleep
import multiprocessing
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

class Worker(QObject):
    """
    Must derive from QObject in order to emit signals, connect slots to other signals, and operate in a QThread.
    """

    sig_step = pyqtSignal(int, str)  # worker id, step description: emitted every step through work() loop
    sig_done = pyqtSignal(int)  # worker id: emitted at end of work()
    sig_msg = pyqtSignal(str)  # message to be shown to user

    def __init__(self, id: int):
        super().__init__()
        self.__id = id
        self.__abort = False

    @pyqtSlot()
    def work(self):
        """
        Pretend this worker method does work that takes a long time. During this time, the thread's
        event loop is blocked, except if the application's processEvents() is called: this gives every
        thread (incl. main) a chance to process events, which in this sample means processing signals
        received from GUI (such as abort).
        """
        thread_name = QThread.currentThread().objectName()
        thread_id = int(QThread.currentThreadId())  # cast to int() is necessary
        self.sig_msg.emit('Running worker #{} from thread "{}" (#{})'.format(self.__id, thread_name, thread_id))

        for step in range(100):
            time.sleep(0.1)
            self.sig_step.emit(self.__id, 'step ' + str(step))

            # check if we need to abort the loop; need to process events to receive signals;
            app.processEvents()  # this could cause change to self.__abort
            if self.__abort:
                # note that "step" value will not necessarily be same for every thread
                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                break

        self.sig_done.emit(self.__id)

    def abort(self):
        self.sig_msg.emit('Worker #{} notified to abort'.format(self.__id))
        self.__abort = True

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

    def saveFile(self,url_root, dataTree):
        self.url_root = url_root
        self.dataTree = dataTree
        self.dill_format = 'result_output'
        with open(self.dill_format, 'wb') as file:
            dill.dump(self.dataTree, file)

    def openFile(self):
        self.dillFile2 = open(self.dill_format, 'rb')
        openTree = dill.load(self.dillFile2)
        # print(type(openTree))
        # openTree.show()
        a = (openTree.to_json(with_data = True), "55555555555555555555555555555555555555555555555555555555555555+")
        temp_tree = [{'link': openTree[node].tag, 'count': openTree[node].data['count']['computer']} for node in
                     openTree.expand_tree(mode=openTree.ZIGZAG)
                     if (openTree[node].data is not None)]
        print(temp_tree)
        print(openTree, '+555555555')

def setup(event):
    global unpaused
    unpaused = event

def myFunction(arg):
    unpaused.wait()
    url = arg
    print(arg)
    html = htmlparser(url, '{}.txt'.format(
        url.split('//')[-1].replace('/', '').replace('.', '').replace('=', '').replace('?', '')))
    html.setup()
    html_dict = dict()
    temp = html.beauiful_soup()
    tree = Tree()
    print('asdfaisjdfiaojwefoiawjefio')
    # print(len(temp))
    temp = temp[0:100]
    tree.create_node("Root", "root", data={'related_link': temp, 'count': html.Count2()})
    print(tree, 'newdea')
    # print(html.Count2())

    for link in temp:
        try:
            html_temp = htmlparser(link, '{}.txt'.format(
                link.split('//')[-1].replace('/', '').replace('.', '').replace('=', '').replace('?', '')))
            html_temp.setup()
            bs_html = html_temp.beauiful_soup()
            html_dict[link] = [bs_html, html_temp.Count2()]
            tree.create_node(link, link, parent='root', data={'related_link': bs_html, 'count': html_temp.Count2()})
            if len(bs_html) > 0:
                for link2 in bs_html:
                    html_temp2 = htmlparser(link2, '{}.txt'.format(
                        link.split('//')[-1].replace('/', '').replace('.', '').replace('=', '').replace('?', '')))
                    html_temp2.setup()
                    bs_html2 = html_temp2.beauiful_soup()
                    tree.create_node(link2, link2, parent=link,
                                     data={'related_link': bs_html2, 'count': html_temp2.Count2()})
            print(bs_html)
            tree.show()
        except:
            print(sys.exc_info())

        temp_tree = [{'link': tree[node].tag, 'count': tree[node].data['count']['computer']} for node in
                     tree.expand_tree(mode=tree.ZIGZAG)
                     if (tree[node].data is not None)]
        stop = time.time()
        # print(tree['root'].data)
        print(temp_tree)

if __name__ == "__main__":
    event = multiprocessing.Event() # initially unset, so workers will be paused at first
    pool = multiprocessing.Pool(6, setup, (event,))
    result = pool.map_async(myFunction, ['https://en.wikipedia.org/wiki/Computer'])
    event.set()   # unpause workers
    sleep(5)
    event.clear() # pause after five seconds
    sleep(5)
    event.set()   # unpause again after five more seconds
    result.wait() # wait for the rest of the work to be completed
