# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DeepSeah_Final1.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QPushButton, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
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



class Ui_MainWindow(object):
    NUM_THREADS = 5
    sig_start = pyqtSignal()
    sig_abort_workers = pyqtSignal()

    def __init__(self, MainWindow):
        super().__init__()

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(797, 530)
        form_layout = QVBoxLayout()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout.setObjectName("gridLayout")
        self.log = QtWidgets.QListWidget(self.tab_3)
        self.log.setObjectName("listWidget")
        # form_layout.addWidget(self.log)
        self.gridLayout.addWidget(self.log, 2, 0, 1, 3)
        self.progress = QtWidgets.QListWidget(self.tab_3)
        self.progress.setObjectName("listWidget_2")
        # form_layout.addWidget(self.progress)
        self.gridLayout.addWidget(self.progress, 2, 4, 1, 4)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 0, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.tab_3)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 7, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 0, 7, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 0, 4, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 797, 21))
        self.menubar.setObjectName("menubar")
        self.menuFiles = QtWidgets.QMenu(self.menubar)
        self.menuFiles.setObjectName("menuFiles")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuFiles.addAction(self.actionOpen)
        self.menuFiles.addAction(self.actionSave)
        self.menubar.addAction(self.menuFiles.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        QThread.currentThread().setObjectName('main')  # threads can be named, useful for log output
        self.__workers_done = None
        self.__threads = None

    def updateText(self, arg):
        return self.log.addItems(arg)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_3.setText(_translate("MainWindow", "Search"))
        self.pushButton_3.clicked.connect(self.Search1)
        # form_layout.addWidget(self.pushButton_3)
        self.pushButton.setText(_translate("MainWindow", "Pause"))
        # self.pushButton.clicked.connect(self.abort_workers)
        # self.button_stop_threads.setDisabled(True)
        self.pushButton_4.setText(_translate("MainWindow", "Search"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Tab 1"))
        self.menuFiles.setTitle(_translate("MainWindow", "Files"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        # self.pushButton_3.clicked.connect(self.Search1)



    def Search1(self):
        rawURL = self.lineEdit.text()
        if rawURL != '':
            if self.checkURL(rawURL):
                print("Seach1 ------ Activated !")
                self.search1Activaing(rawURL)
                print('https://en.wikipedia.org/wiki/Computer')
            else:
                print("Wrong URL !!!! ")

    def search1Activaing(self, url):
        # QApplication.processEvents()
        myFunction(url)
        print('1')

    def checkURL(self,url):
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return re.match(regex, url) is not None  # True

    def start_threads(self):
        print('1')
        self.log.append('starting {} threads'.format(self.NUM_THREADS))
        print('1')
        self.pushButton_3.setDisabled(True)
        print('1')
        self.pushButton.setEnabled(True)
        print('1')

        self.__workers_done = 0
        self.__threads = []
        for idx in range(self.NUM_THREADS):
            print('1')
            worker = Worker(idx)
            thread = QThread()
            thread.setObjectName('thread_' + str(idx))
            self.__threads.append((thread, worker))  # need to store worker too otherwise will be gc'd
            worker.moveToThread(thread)
            print('2')
            try:
            # get progress messages from worker:
                worker.sig_step.connect(self.on_worker_step)
                print('1')
                worker.sig_done.connect(self.on_worker_done)
                print('1')
                worker.sig_msg.connect(self.log.append)
            except:
                print("=======FROM Inner Combobox=======")
                print(sys.exc_info()[0], sys.exc_info()[1])
                print("=================================")

            # control worker:
            self.sig_abort_workers.connect(worker.abort)
            # get read to start worker:
            # self.sig_start.connect(worker.work)  # needed due to PyCharm debugger bug (!); comment out next line
            thread.started.connect(worker.work)
            thread.start()  # this will emit 'started' and start thread's event loop

            # self.sig_start.emit()  # needed due to PyCharm debugger bug (!)

    @pyqtSlot(int, str)
    def on_worker_step(self, worker_id: int, data: str):
        self.log.append('Worker #{}: {}'.format(worker_id, data))
        self.progress.append('{}: {}'.format(worker_id, data))

    @pyqtSlot(int)
    def on_worker_done(self, worker_id):
        self.log.append('worker #{} done'.format(worker_id))
        self.progress.append('-- Worker {} DONE'.format(worker_id))
        self.__workers_done += 1
        if self.__workers_done == self.NUM_THREADS:
            self.log.append('No more workers active')
            self.button_start_threads.setEnabled(True)
            self.button_stop_threads.setDisabled(True)
            # self.__threads = None

    @pyqtSlot()
    def abort_workers(self):
        self.sig_abort_workers.emit()
        self.log.append('Asking each worker to abort')
        for thread, worker in self.__threads:  # note nice unpacking by Python, avoids indexing
            thread.quit()  # this will quit **as soon as thread event loop unblocks**
            thread.wait()  # <- so you need to wait for it to *actually* quit

        # even though threads have exited, there may still be messages on the main thread's
        # queue (messages that threads emitted before the abort):
        self.log.append('All threads exited')

def update_percent(temp, p):
    return (p/int(len(temp)))*100

def myFunction(arg):
    url = arg
    # url = 'https://en.wikipedia.org/wiki/Computer'
    html = htmlparser(url, '{}.txt'.format(
        url.split('//')[-1].replace('/', '').replace('.', '').replace('=', '').replace('?', '')))
    html.setup()
    html_dict = dict()
    temp = html.beauiful_soup()
    tree = Tree()

    # print(len(temp))
    temp = temp[0:5]
    temp = temp[0:50]
    percent = 0
    print("Percent: {}%".format(update_percent(temp, percent)))

    tree.create_node("Root", "root", data={'related_link': temp, 'count': html.Count2()})
    print(tree, 'newdea')
    # print(html.Count2())
    MW = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    for link in temp:
        try:
            QApplication.processEvents()
            time.sleep(1)
            print(link)
            ui.updateText(str(link))
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
    temp_tree = [{'link': tree[node].tag, 'count': tree[node].data['count']['computer']} for node in
                 tree.expand_tree(mode=tree.ZIGZAG)
                 if (tree[node].data is not None)]
    stop = time.time()
    print(tree['root'].data)
    print(temp_tree)
    newlist = sorted(temp_tree, key=itemgetter('count'), reverse=True)
    print("Total time: {}s".format(stop - start))
    print(newlist)
    with open('result/tree.json', 'w+') as fs:
        fs.write(tree.to_json(with_data=True))
    tree.save2file('result/tree.txt')
    print("SUCCESS, Percent: {}%".format(update_percent(temp, percent)))

if __name__ == "__main__":
    import sys
    import locale
    app = QtWidgets.QApplication(sys.argv)
    # locale.setlocale(locale.LC_ALL, 'en US')
    # print(QtCore.QLocale())

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    ui.__init__(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
