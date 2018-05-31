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
import nltk
import os
import shutil
import copy


class wordCount:
    """ A Class that count word from file with NLTK"""

    def __init__(self, file):
        # Initialization
        self.file = file
        self.word = []

    def Count(self):
        wnl = nltk.stem.WordNetLemmatizer()  # Create nltk WordNetLemmatizer object

        # Read file and add words to list
        words = re.findall(r'\w+', open("temp/clean_{}".format(self.file), encoding='utf-8').read())
        temp_word = []
        for item in words:
            # To iterate through word in all words to remove stem
            word = wnl.lemmatize(nltk.tokenize.word_tokenize(item)[0].lower())  # Lower the word and lemmatize them
            temp_word.append(word)  # Add word to temp list
        c = Counter(temp_word)  # Counter words in list to dict
        return c

class htmlparser(wordCount):
    """ A class that take url and file destination to get HTML.
        After that, read the file and do Beautiful Soup for find specific attribute. """

    def __init__(self, url, dest):
        # Initialization
        super(htmlparser, self).__init__(dest)  # Use inherited wordCount
        self.url = url
        self.dest = dest

    def begin(self):
        urllib.request.urlretrieve(self.url, 'temp/'+self.dest)  # Get the html of URL

    def read_to_temp_html(self):
        # Read file and set to local variable
        temp = ''
        f = open('temp/'+self.dest, 'r', encoding='utf-8')
        for line in f:
            temp += line
        f.close()
        self.temp = temp

    def beauiful_soup(self):
        bs = BeautifulSoup(self.temp, 'html.parser')  # Create a BeautifulSoup object by html.parser type
        cleantext = BeautifulSoup(self.temp, 'html.parser').text  # Create another BeautifulSoup object with text-only

        # Write clean text to file for further counting words
        f = open("temp/clean_{}".format(self.dest), 'w', encoding='utf-8')
        f.write(cleantext)
        f.close()

        # Iterate through html to get all links (href)
        bs_list = []
        for link in bs.select('a'):
            if link.has_attr('href') and ('http' in link['href']):
                bs_list.append(link['href'])
        return bs_list

    def setup(self):
        # Just main function
        self.begin()
        self.read_to_temp_html()



class Ui_MainWindow(object):
    """ Main UI of program using PyQt5"""
    NUM_THREADS = 5
    sig_start = pyqtSignal()
    sig_abort_workers = pyqtSignal()

    def __init__(self, MainWindow):

        # Initialization
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
        self.gridLayout.addWidget(self.log, 2, 0, 1, 3)
        self.progress = QtWidgets.QListWidget(self.tab_3)
        self.progress.setObjectName("listWidget_2")
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
        self.actionLoad = QtWidgets.QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.menuFiles.addAction(self.actionOpen)
        self.menuFiles.addAction(self.actionSave)
        self.menuFiles.addAction(self.actionLoad)
        self.menubar.addAction(self.menuFiles.menuAction())


        self.all_link = {}
        self.found_link = []

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def updateText(self, arg):
        return self.log.append(arg)

    def retranslateUi(self, MainWindow):
        # Setting display text on UI object
        self._translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(self._translate("MainWindow", "MainWindow"))
        self.pushButton_3.setText(self._translate("MainWindow", "Search"))
        self.pushButton_3.clicked.connect(self.Search1)
        self.pushButton.setText(self._translate("MainWindow", "Pause"))
        self.pushButton.clicked.connect(self.stopThread)
        self.pushButton_4.setText(self._translate("MainWindow", "Search"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), self._translate("MainWindow", "Tab 1"))
        self.menuFiles.setTitle(self._translate("MainWindow", "Files"))
        self.actionOpen.setText(self._translate("MainWindow", "Open"))
        self.actionSave.setText(self._translate("MainWindow", "Save"))
        self.actionLoad.setText(self._translate("MainWindow", "Load"))
        self.lineEdit_2.textChanged.connect(self.search_dict)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionLoad.triggered.connect(self.loadFile)
        self.progress.itemDoubleClicked.connect(self.openLink)

    def loadFile(self):
        self.openDict = copy.deepcopy(self.all_link)
        print(self.openDict)
        self.dataLoaded = True
        self.dr = 'loaded'
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Data is successful loaded.")
        msg.setWindowTitle("Success")
        msg.exec_()


    def openLink(self, item):
        #  When double-clicked on list item will open that link in browser
        item_link = item.text().split(', ')[1]
        if item_link != "Root":
            os.startfile(item_link)

    def search_dict(self, text):
        # To Search a word from dict
        try:
            if self.dr != '' or self.dataLoaded:
                self.progress.clear()
                filter_search = [{'count': self.openDict[item]['count'][text], 'link': item} for item in self.openDict]
                for item in sorted(filter_search, key=itemgetter('count'), reverse=True):
                    try:
                        if item['count'] != 0:
                            self.progress.addItem('({}), {}'.format(item['count'], item['link']))
                    except:
                        pass

        except:
            pass

    def openFile(self):
        # Open dill file and load
        self.dr = str(QtWidgets.QFileDialog.getOpenFileName()[0])
        if self.dr != '':
            with open(self.dr, 'rb') as f:
                self.openDict = dill.load(f)

            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Data[{}] is successful loaded.".format(self.dr.split('/')[-1]))
            msg.setWindowTitle("Success")
            msg.exec_()

    def continueThread(self):
        self.stop = True
        if self.stop:
            try:
                self.stop = False
                self.p = Thread(target=self.search, args=(self.unsearch2, ))
                self.p.start()
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

    def saveFile(self):
        # Dill all link which already searched to file
        fileName = str(QtWidgets.QFileDialog.getSaveFileName()[0])
        try:
            if fileName:
                print(fileName)
                with open(fileName, 'wb') as file:
                    dill.dump(self.all_link, file)
        except:
            print(sys.exc_info())

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
        print("Stopped")
        self.finalize()


    def update_percent(self, temp, p):
        return (p / int(len(temp))) * 100

    def getHTML(self, arg):
        # Take url to htmlparser class and produce relate link of the url
        # This is first time of running the searching program
        self.url = arg
        # html parser and beautiful soup section
        self.html = htmlparser(self.url, '{}.txt'.format(
            self.url.split('//')[-1].replace('/', '').replace('.', '').replace('=', '').replace('?', '')))  # Remove non-ASCII
        self.html.setup()
        self.html_dict = dict()
        self.temp = self.html.beauiful_soup()

        # Init link
        self.temp = self.temp
        self.unsearch2 = set()
        self.found_link.append(self.url)
        self.all_link.update({self.url: {'related_link': self.temp, 'count': self.html.Count()}})
        self.stop = False
        self.dataLoaded = False
        self.search(self.temp)

    def search(self, list_link=None, second=False):
        if second:
            # Second time of running for n+1 level
            if self.unsearch2 == []:
                # Unsearch is empty means that, it's done!
                print("=======COMPLETE=======")
                self.finalize()  # Do final stuff
            else:
                    temp_search = set()  # Make a temp list(set) to store result of beautifulSoup
                    for real_link in self.unsearch2:
                        # Loop Through unsearch list and if that link is not in all_link list then it will start working normally
                        if not self.stop and (real_link not in self.all_link):
                            try:
                                # html parser and beautiful soup section
                                html_temp = htmlparser(real_link, '{}.txt'.format(real_link.split('//')[-1].replace('/', '').replace('.', '').replace('=', '').replace('?', '')))
                                html_temp.setup()
                                bs_html = html_temp.beauiful_soup()
                                # Update all_link list with new result of beautiful soup
                                self.found_link.append(real_link)
                                self.all_link.update({real_link: {'related_link': bs_html, 'count': html_temp.Count()}})
                                temp_search.update(bs_html)  # Add result to temp list
                                self.log.append(real_link)  # Add link to search progress of GUI
                            except:
                                print(sys.exc_info())
                        else:
                            self.found_link.append(real_link)

                    self.unsearch2.update(temp_search)  # Update unsearch list with temp list
            self.search(second=True)
        else:
            unsearch = copy.deepcopy(list_link)  # Make a copy of input argument for avoiding a list(set) size error
            if not self.stop:
                for real_link in unsearch:
                    # Loop through link in unsearch whose are came from argument of this function
                    if not self.stop and (real_link not in self.all_link):
                        try:
                            # html parser and beautiful soup section
                            html_temp = htmlparser(real_link, '{}.txt'.format(real_link.split('//')[-1].replace('/', '').replace('.', '').replace('=', '').replace('?', '')))
                            html_temp.setup()
                            bs_html = html_temp.beauiful_soup()
                            # Update all_link list with new result of beautiful soup
                            self.found_link.append(real_link)
                            self.all_link.update({real_link: {'related_link': bs_html, 'count': html_temp.Count()}})
                            self.unsearch2.update(bs_html)  # Need to update the unsearch list
                            self.log.append(real_link)  # Add link to search progress of GUI
                        except:
                            print(sys.exc_info())
                    else:
                        self.found_link.append(real_link)

                self.search(second=True)  # Going to next level of searching

    def finalize(self):
        # This function is about saving the output of searching with dill and clear temp folder
        print("=======ALL LINK=======")
        print(self.all_link)
        print("=======UNSEARCH=======")
        print(self.unsearch2)
        print("======FoundLink=======")
        print(Counter(self.found_link))
        self.openDict = self.all_link
        self.dataLoaded = True
        self.dr = 'loaded'
        with open('final_output', 'wb') as file:
            dill.dump(self.all_link, file)
        shutil.rmtree('temp')
        os.mkdir('temp')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    ui.__init__(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
