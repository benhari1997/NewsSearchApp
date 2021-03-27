**PyQt5 & mongodb - News search application project :**
___
This project is a small implementation of a Pyqt application that <b> mines </b> and displays the articles informations from a specific website (dailymail used as an examlple) by key search. its different functionnalities are the following :

+ The app allows the user to connnect to a mongodb cloud database 
and then allows him to do searches on the articles stored in it.
+ The articles infos stored in the database were extracted from 
Dailymail cover page using beatifulsoup and py clicking on the 
'update news database' button, the user will be able to update 
the database with the recent articles from the same source. When updated,
the new articles are shown in the tab called 'latest news' .
+ The default <b>user id & password</b> are : benhari & benhari (already written by default).

> #### Execution :
___
The app is executed through the <code> app.py </code> python file.

> #### Requirements :
___
- Python v > 3.0 
- PyQt5
- Pymongo
- BeautifulSoup
- _a stable connection_

> #### Snapshots : 
___
- ![Example 1](https://github.com/benhari1997/NewsSearchApp/tree/master/examples/interface-example-1.PNG)

- ![Example 2](https://github.com/benhari1997/NewsSearchApp/tree/master/examples/interface-example-2.PNG)

> #### Bibliography : 
___

- Mongodb in python documentation : https://pymongo.readthedocs.io/en/stable/
- "Extracting data on html with beautifulSoup", _pluralsight_ : https://www.pluralsight.com/guides/extracting-data-html-beautifulsoup
- PyQt documentation : https://doc.qt.io/qtforpython/api.html
___
___
> #### Author : Benhari Abdessalam
> #### Date : 21/02/2020

