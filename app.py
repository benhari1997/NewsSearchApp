#====================libraries======================

from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import re

#====================App class======================

class NewsApp(QDialog):

    def __init__(self, parent=None):
        super(NewsApp, self).__init__(parent)

        self.news=None

        #creating the app boxes by calling the functions defined below 
        self.createResultTabWidget()
        self.createConnectionBox()
        self.createSearchBox()
        
        #dispays the connection status message
        self.ConnStatus = QPushButton("Not connected")
        self.ConnStatus.setFlat(True)

        #dispays the update status message
        self.UpdateStatus = QPushButton(":::")
        self.UpdateStatus.setFlat(True)

        #Creating the main layout
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.ConnectionBox, 0, 0)
        mainLayout.addWidget(self.ConnStatus, 1, 0)
        mainLayout.addWidget(self.UpdateStatus, 1, 1)
        mainLayout.addWidget(self.SearchBox, 0, 1)
        mainLayout.addWidget(self.ResultTabWidget,2,0,1,2)
        
        #Stretches
       	mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)

        self.setLayout(mainLayout)

        #App style, size, title and icon 
        self.setWindowTitle("News App")
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.setFixedSize(640, 480)
        self.setWindowIcon(QtGui.QIcon('data/images/icon.png'))


    #Box creation functions:
    def createConnectionBox(self):
        """ This function creates the connection box
            buttons, triggers and layouts.
        """

        self.ConnectionBox = QGroupBox("Connection Info : ")

        #identification infos (by default set on the right values to test the app easily)
        self.lineEdit_user = QLineEdit('benhari')
        self.lineEdit_pw = QLineEdit('benhari')
        self.lineEdit_pw.setEchoMode(QLineEdit.Password)

        #connect and disconnect buttons
            #buttons
        self.ConnPushButton = QPushButton("Connect")
        self.DiscPushButton = QPushButton("Disconnect")
            #triggered actions
        self.ConnPushButton.clicked.connect(self.connect)
        self.DiscPushButton.clicked.connect(self.disconnect)

        #Layouts
        Connbox = QHBoxLayout()
        Connbox.addWidget(self.ConnPushButton)
        Connbox.addWidget(self.DiscPushButton)

        layout = QGridLayout()
        layout.addWidget(self.lineEdit_user, 0, 0, 1, 2)
        layout.addWidget(self.lineEdit_pw, 1, 0, 1, 2)
        layout.addLayout(Connbox, 2, 0, 1, 2)

        layout.setRowStretch(5, 1)
        self.ConnectionBox.setLayout(layout)

    def createSearchBox(self):
        """ This function creates the search box
            buttons, triggers and layouts.
        """

        self.SearchBox = QGroupBox('Search :')
        self.SearchBox.setEnabled(False)

        #search bar
        self.lineEdit_search = QLineEdit("?")

        #creating buttons
        self.searchPushButton = QPushButton("Search")
        self.updatePushButton = QPushButton("Update News Database")

        #triggers
        self.searchPushButton.clicked.connect(self.search)
        self.updatePushButton.clicked.connect(self.updateNews)

        #layouts
        layout = QVBoxLayout()
        layout.addWidget(self.lineEdit_search)
        layout.addWidget(self.searchPushButton)
        layout.addWidget(self.updatePushButton)
        
        layout.addStretch(1)
        self.SearchBox.setLayout(layout)

    def createResultTabWidget(self):
        """This function creates the display tables"""

        #main tab
        self.ResultTabWidget = QTabWidget()
        self.ResultTabWidget.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)
        self.ResultTabWidget.setEnabled(False)

        #creating sub-tables
        self.SearchTableWidget = QTableWidget(6, 6)
        self.NewsTableWidget = QTableWidget(6, 6)

        #adding the sub-tables to the main tab 
        self.ResultTabWidget.addTab(self.SearchTableWidget, "Search results")
        self.ResultTabWidget.addTab(self.NewsTableWidget, "Latest News")


    #triggered functions
    def connect(self) :
        """if the id and the password is correct it connects
            to the database and allows the user to use the
            other features; if it isn't, it displays a message error.
        """

        try :
            #database connection
            self.news = database_conn(self.lineEdit_user.text(),
                                        self.lineEdit_pw.text())

            #enabling other features
            self.lineEdit_pw.setEnabled(False)
            self.lineEdit_user.setEnabled(False)
            self.SearchBox.setEnabled(True)
            self.ResultTabWidget.setEnabled(True)
            self.ConnPushButton.setEnabled(False)

            #the displayed message
            self.ConnStatus.setText("Connected !")
            self.ConnStatus.setStyleSheet("color: green")

        except :
            #the displayed message
            self.ConnStatus.setText("Wrong Password or Id")
            self.ConnStatus.setStyleSheet("color: red")

    def disconnect(self):
        """This function disconnects the app and disables 
        all the fields except the connection fields""" 

        #enabling/disabling
        self.lineEdit_pw.setEnabled(True)
        self.lineEdit_user.setEnabled(True)
        self.SearchBox.setEnabled(False)
        self.ResultTabWidget.setEnabled(False)

        #the displayed message
        self.ConnStatus.setText("Disconnected !")
        self.ConnStatus.setStyleSheet("color: black")
        self.lineEdit_pw.setText("")

    def search(self):
        """This function when triggered searches for the wanted 
        text in the database and then displays the results"""

        #extracting the results
        search_text = self.lineEdit_search.text()
        search_results = list(
            self.news.find(
                { 'Article Title' : { "$regex": '.*'+
                search_text+'.*' , "$options" :'i' } }))

        #displaying the results 
        row_count = (len(search_results))
        column_count = (len(search_results[0]))
            #number of columns and rows
        self.SearchTableWidget.setColumnCount(column_count) 
        self.SearchTableWidget.setRowCount(row_count)
            #headers
        self.SearchTableWidget.setHorizontalHeaderLabels(
                (list(search_results[0].keys())[1:]))
            #filling the cells
        for row in range(row_count):  
            for column in range(column_count-1):
                item = (list(search_results[row].values())[column+1])
                self.SearchTableWidget.setItem(row, column, QTableWidgetItem(item))

    def updateNews(self):
        """ This function extracts the news from the
            main Daily mail page and stores and displays
            them on the app.
            """

        #the website url
        url = "https://www.dailymail.co.uk" # I choose dailymail as an example.
        
        #creating the request
        req = requests.get(url)
        req.status_code

        #getting the coverpage content (its where we can find the most recent news)
        coverpage_content = req.content

        #Extracting the 'raw' news
        soup = BeautifulSoup(coverpage_content, 'html5lib')
        coverpage_news = soup.find_all('h2', class_='linkro-darkred')
        
        articles_nbr = 5 #I choose 5 so it doesn't take much time 
        #to load but we can do more as far as we dont exceed 'len(coverpage_news)'

        #empty lists to fill with infos
        contents = []
        links = []
        titles = []

        #Info extraction 
        for n in np.arange(0, articles_nbr):

            #extracting the link
            link = url + coverpage_news[n].find('a')['href']
            links.append(link)

            #extracting the title
            title = coverpage_news[n].find('a').get_text()
            titles.append(title)

            #extracting the content
                #finding paragraphs
            article = requests.get(link)
            article_content = article.content
            soup_article = BeautifulSoup(article_content, 'html5lib')
            body = soup_article.find_all('p', class_='mol-para-with-font')

                #merging paragraphs
            list_paragraphs = []
            for p in np.arange(0, len(body)):
                paragraph = body[p].get_text()
                list_paragraphs.append(paragraph)
                final_article = " ".join(list_paragraphs)

                #Removing special characters
            final_article = re.sub("\\xa0", "", final_article)
            
            contents.append(final_article)

        #transforming the extracted news infos into a 'records' dictionnary
        today_news = pd.DataFrame({'Article Title': titles,
             'Article Link': links,
             'Content': contents,
             'Source': 'Daily Mail'}).to_dict('records')

        #updating the dataframe with the new values
        self.news.insert_many(today_news)

        #displaying the new elements in our news table
            #number of columns and rows 
        row_count = (len(today_news))
        column_count = (len(today_news[0]))
        self.NewsTableWidget.setColumnCount(column_count) 
        self.NewsTableWidget.setRowCount(row_count)
            #headers
        self.NewsTableWidget.setHorizontalHeaderLabels(
                (list(today_news[0].keys())))
            #filling the cells
        for row in range(row_count):  
            for column in range(column_count-1):
                item = (list(today_news[row].values())[column])
                self.NewsTableWidget.setItem(row,
                                             column,
                                             QTableWidgetItem(str(item)))

        #changing the update status
        self.UpdateStatus.setText("Updated !")
        self.UpdateStatus.setStyleSheet("color: green")

#==================other functions=====================

#Database connnection function
def database_conn(id, password):
    """It connects us to the MongoDb database using the given id and password 
    and returns the collection that'll be used to trigger the database commands"""

    client = MongoClient('mongodb+srv://'+str(id)+':'+str(password)+
        '@gemoproject-jswza.mongodb.net/test?retryWrites=true&w=majority')
    db = client.get_database('News_db')
    news = db.News
    return news

#=====================execution========================

#App execution
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    newsApp = NewsApp()
    newsApp.show()
    sys.exit(app.exec_()) 
