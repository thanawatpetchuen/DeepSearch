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
from multiprocessing import Pool
from threading import Thread, Event


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
        self.log = QTextEdit(self.tab_3)
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
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 0, 4, 1, 1)
        self.progessBar = QtWidgets.QProgressBar(self.tab_3)
        self.progessBar.setProperty('value', 0)
        self.progessBar.setObjectName("progessBar")
        self.gridLayout.addWidget(self.progessBar, 3, 0, 1, 1)
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


    def updateText(self, arg):
        return self.log.append(arg)

    def retranslateUi(self, MainWindow):
        self._translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(self._translate("MainWindow", "MainWindow"))
        self.pushButton_3.setText(self._translate("MainWindow", "Search"))
        self.pushButton_3.clicked.connect(self.Search1)
        # form_layout.addWidget(self.pushButton_3)
        self.pushButton.setText(self._translate("MainWindow", "Pause"))
        self.pushButton.clicked.connect(self.stopThread)
        # self.button_stop_threads.setDisabled(True)
        self.pushButton_4.setText(self._translate("MainWindow", "Search"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), self._translate("MainWindow", "Tab 1"))
        self.menuFiles.setTitle(self._translate("MainWindow", "Files"))
        self.actionOpen.setText(self._translate("MainWindow", "Open"))
        self.actionSave.setText(self._translate("MainWindow", "Save"))
        # self.pushButton_3.clicked.connect(self.Search1)


    def continueThread(self):
        self.stop = True
        if self.stop:
            try:
                self.p = Thread(target=self.myFunction, args=(self.veryLastlink, ))
                self.p.start()
                # self._event.set()
                self.pushButton.setText(self._translate("MainWindow", "Pause"))
                self.pushButton.clicked.disconnect(self.continueThread)
                self.pushButton.clicked.connect(self.stopThread)
                print('Started')
            except:
                pass

    def Search1(self):
        self.rawURL = str(self.lineEdit.text())
        print(self.rawURL)
        if self.rawURL != '':
            if self.checkURL(self.rawURL):
                print("Seach1 ------ Activated !")
                self.search1Activaing(self.rawURL)
                print('https://en.wikipedia.org/wiki/Computer')
            else:
                print("Wrong URL !!!! ")

    def search1Activaing(self, url):
        # QApplication.processEvents()
        self.stop = False
        self.pool = Pool(5)
        try:
            if not self.stop:
                self.continueThread()
                self.p = Thread(target=self.getHTML, args=(url,))
                self.p.start()

        except:
            pass


    def checkURL(self,url):
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return re.match(regex, url) is not None  # True

    def stopThread(self):
        self.history = []
        self.stop = True
        self.pool.terminate()
        self.pool.join()
        self.p.join(timeout=5)
        self.pushButton.setText(self._translate("MainWindow", "Start"))
        self.pushButton.clicked.disconnect()
        self.pushButton.clicked.connect(self.continueThread)
        # self.pushButton_4.clicked.connect(self.continueThread)
        print("Stopped")


    def update_percent(self, temp, p):
        return (p / int(len(temp))) * 100

    def getHTML(self, arg):
        self.url = arg
        # # url = 'https://en.wikipedia.org/wiki/Computer'
        self.html = htmlparser(self.url, '{}.txt'.format(
            self.url.split('//')[-1].replace('/', '').replace('.', '').replace('=', '').replace('?', '')))
        self.html.setup()
        # print(html)
        # print(html.setup)
        # print('1234568')
        self.html_dict = dict()
        self.temp = self.html.beauiful_soup()
        # print('1234568')
        # print(temp)
        # print(len(temp))
        self.temp = self.temp[0:100]
        self.myFunction(self.temp)

    def myFunction(self, linkList):

        self.tree = Tree()
        self.links = linkList
        self.stop = False
        self.temp3 = self.temp
        self.currentlyLink = []
        # temp = temp[0ซ100]
        print('1234568')
        self.percent = 0
        print("Percent: {}%".format(self.update_percent(self.links, self.percent)))
        print('1234568')
        self.tree.create_node("Root", "root", data={'related_link': self.links, 'count': self.html.Count2()})
        # print(tree, 'newdea')
        # print(html.Count2())
        for link in self.links:
            try:
                if not self.stop:
                    self.currentlyLink.append(link)
                    # QApplication.processEvents()
                    # time.sleep(1)
                    # print(link)
                    self.updateText(link)
                    print(link)
                    html_temp = htmlparser(link, '{}.txt'.format(
                        link.split('//')[-1].replace('/', '').replace('.', '').replace('=', '').replace('?', '')))
                    print(link)
                    html_temp.setup()
                    bs_html = html_temp.beauiful_soup()
                    self.html_dict[link] = [bs_html, html_temp.Count2()]
                    self.tree.create_node(link, link, parent='root', data={'related_link': bs_html, 'count': html_temp.Count2()})
                    if len(bs_html) > 0:
                        for link2 in bs_html:
                            html_temp2 = htmlparser(link2, '{}.txt'.format(
                                link.split('//')[-1].replace('/', '').replace('.', '').replace('=', '').replace('?', '')))
                            html_temp2.setup()
                            bs_html2 = html_temp2.beauiful_soup()
                            self.tree.create_node(link2, link2, parent=link,
                                             data={'related_link': bs_html2, 'count': html_temp2.Count2()})
                    print(bs_html)

                    self.percent += 1
                    self.pB = self.update_percent(self.links, self.percent)
                    print("Percent: {}%".format(self.pB))
                    self.progessBar.setValue(self.pB)
                    self.tree.show()

            except:
                self.percent += 1
                self.pB = self.update_percent(self.links, self.percent)
                print("Percent: {}%".format(self.pB))
                self.progessBar.setValue(self.pB)
                print(sys.exc_info())

        print(self.currentlyLink)
        self.veryLastlink = [elem for elem in self.temp3 if elem not in self.currentlyLink]
        print(self.veryLastlink)
        self.history.append(self.tree)

        # self.lastLink()

    def writeFile(self):
        f = open('final.txt', 'w+', encoding='utf-8')
        f.write(str(self.html_dict))
        f.close()
        # print(html_dict)
        print(self.tree.to_json(with_data=True))
        self.tree.show()

        start = time.time()
        temp_tree = [{'link': self.tree[node].tag, 'count': self.tree[node].data['count']['computer']} for node in
                     self.tree.expand_tree(mode=self.tree.ZIGZAG)
                     if (tree[node].data is not None)]
        stop = time.time()
        print(self.tree['root'].data)
        print(temp_tree)
        newlist = sorted(temp_tree, key=itemgetter('count'), reverse=True)
        print("Total time: {}s".format(stop - start))
        print(newlist)
        with open('result/tree.json', 'w+') as fs:
            fs.write(self.tree.to_json(with_data=True))
        self.tree.save2file('result/tree.txt')
        print("SUCCESS, Percent: {}%".format(self.update_percent(self.temp, self.percent)))


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
