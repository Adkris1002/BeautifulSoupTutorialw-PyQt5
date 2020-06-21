#Movie scraper based on emotions
#Author: Aditya Krishna

#Import 'BeautifulSoup' and required HTTP modifiers/extractors
from bs4 import BeautifulSoup as SOUP
import re
import requests as HTTP
import sys
import os

#Import `QApplication` and all the required widgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtCore, QtWidgets


#Instantiated a "map"-type object to map emotions to the urls for the matched movies
app_dict = {"Life is too much suffering" : "https://www.imdb.com/list/ls058430399/?sort=num_votes,desc&st_dt=&mode=detail&page=1, asc",
                                            #Feel-good movies
            "Aimless and played" : "https://www.imdb.com/list/ls075091642/?sort=moviemeter,asc&st_dt=&mode=detail&page=1,asc",
                                    #Inspirational drama movies
            "Hopeless" : "https://www.imdb.com/list/ls004803270/?sort=moviemeter,asc&st_dt=&mode=detail&page=1,asc",
                          #Whimsical animated movies
            "Weak" : "https://www.imdb.com/list/ls000053753/?sort=num_votes,desc&st_dt=&mode=detail&page=1, asc",
                      #Underdog movies
            "Life is too dull" : "https://www.imdb.com/list/ls009668187/?sort=moviemeter,asc&st_dt=&mode=detail&page=1,asc",
                                  #Music movies
            "Like laughing and having fun with friends" : "https://www.imdb.com/list/ls052725387/?st_dt=&mode=detail&page=1&sort=list_order,asc",
                                                           #Action-comedies
            "Ready to take on the world with my ride-or-die squad" : "https://www.imdb.com/list/ls097873256/?ref_=rltls_2&sort=user_rating,desc&st_dt=&mode=detail&page=1, asc",
                                                                               #Historical epics 
            "Like expanding and blowing my mind" : "https://www.imdb.com/list/ls026335266/?sort=moviemeter,asc&st_dt=&mode=detail&page=1,asc",
                                                    #Plot-twists and new concepts
            "In love" : "https://www.imdb.com/list/ls042233563/?ref_=rltls_13&sort=user_rating,desc&st_dt=&mode=detail&page=1,asc", 
            
            "I just wanna see the new releases" : "https://www.imdb.com/search/title/?title_type=feature&year=2020-01-01,2020-12-31,asc",
                                                   #The newest releases in theatres and streaming sites 
            "I just wanna see what movies are the greatest of all time" : "https://www.imdb.com/search/title/?title_type=feature&sort=num_votes,desc"}
                                                                           #IMDB's greatest of all time 



#The class that extracts the movie titles from the IMDB genre pages
class PyMovieScraper:
    
    
    #Scrapes the "raw" data from the IMBD site (data is in HTML format so it must be cleaned)
    #Takes argument of the emotion that the user said they felt
    #Returns an array of data where the items have the movie titles inside
    #there's also a lot of "noise" inside
    def scrape(buttonTitle):
        #Gets the value from the emotion key in the application dictionary
        urlhere = app_dict[buttonTitle]
        
        #Extracts raw HTTP data from site
        response = HTTP.get(urlhere)
        data = response.text
        
        #Filters out all most unnecessary information but still far from 
        #extraction of individual movie titles
        soup = SOUP(data, "lxml")
        raw_data = soup.find_all("a", attrs = {"href" : re.compile(r'\/title\/tt+\d*\/')})
        return raw_data
    
    
    #Cleans out the extracted raw data and isolates all the movie titles using a regex
    #Only retrieves about 9 or 10 movies but can be modified for more
    #Returns an array of clean spaced movie titles
    def extract_titles(raw_data): 
        movies = []
    
        count = 0
        
        #Add the movie titles once they are cleaned with the split function to movies
        for item in raw_data:
            tmp = str(item).split('>')
            if (len(tmp) == 3):
                movies.append(tmp[1][:-3])
            
            #count variable manipulates how many movies client wants to see
            if(count > 25):
                break
            count+=1

        return movies
    
    

#Class controls the option window that prompts and take user input
class PyOptionWindow(QMainWindow):
    
    
    #Instantiated a signal variable to be emitted into the next window
    switch_window = QtCore.pyqtSignal(str)
    
    
    #Constructor method that will build a certain sized window
    def __init__(self):
        #View initializer
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle('PyMovieRecommender')
        self.resize(500, 300)
        
        # Set the central widget and layout
        self.layout = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.layout)
        
        #create the display and buttons of the window
        self.create_display()
        self.create_buttons()
    
    
    #Create the display
    def create_display(self):
        # Create the prompt label
        self.prompt = QLabel('<h1>How do you feel right now?</h1>')
        self.layout.addWidget(self.prompt)
        
        
    #Add the clickable buttons through which the user will choose their movies
    def create_buttons(self):
        self.buttons = []
        buttonNum = 0
        
        for buttonTitle in app_dict:
            #Populate the buttons array with QPushButton buttons linked to emotions from the dictionary
            self.buttons.append(QtWidgets.QPushButton(buttonTitle))
             #Add those buttons onto the window
            self.layout.addWidget(self.buttons[buttonNum], buttonNum + 1, 0)
            #Connect each button to a specific method
            #Each button will take you to a different window
            self.buttons[buttonNum].clicked.connect(self.switch)
            buttonNum = buttonNum + 1
            
    
    #Switches the option window to the next window depending on whatever 
    #button the user clicked in the option window
    def switch(self):
        button = self.sender()
        self.switch_window.emit(button.text())
  
    
        
#Class that controls the movie window that just displays all the movies that are scraped
class PyMovieWindow(QtWidgets.QWidget):
    
    
    #Constructor method sets up window and its contents using PyMovieScraper
    def __init__(self, buttonTitle):\
        #Create display
        QtWidgets.QWidget.__init__(self)
        self.resize(400, 300)
        if (buttonTitle == 'I just want to see the new releases'):
            self.setWindowTitle('The new releases are...')
        if (buttonTitle == 'I just wanna see what movies are the greatest of all time'):
            self.setWindowTitle('The greatest of all time are...')
        else:
            self.setWindowTitle('The movies for when you feel like that are...')

        layout = QtWidgets.QGridLayout()

        #Call PyMovieScraper to add the movie titles as labels onto the window
        raw_data = PyMovieScraper.scrape(buttonTitle)
        movies = PyMovieScraper.extract_titles(raw_data)
        for movie in movies:
            layout.addWidget(QtWidgets.QLabel(movie))
            
        
        #Create a return button that takes you to the option window
        self.button = QtWidgets.QPushButton('Go back')
        self.button.clicked.connect(self.goBack)

        layout.addWidget(self.button)
        
        #Create a close button that closes the application
        self.button = QtWidgets.QPushButton('Close')
        self.button.clicked.connect(self.close)
        
        layout.addWidget(self.button)

        self.setLayout(layout)
        
        
    #Method is triggered when return button is clicked
    #The method just restarts the application and takes user back to option Window
    def goBack(self):
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 



#This class controls the switching between windows and the signals that are sent
class PyMovieCtrl:
    
    
    #No need for any constructor method
    def __init__(self):
        pass
    
    
    #Starts the option window class and connects any action inside that window
    #to start the next window's class
    def showOptions(self):
        self.optionWindow = PyOptionWindow()
        self.optionWindow.switch_window.connect(self.showMovies)
        self.optionWindow.show()
                
        
    #Takes in the signal from the action in the previous window and closes the 
    #previous window and opens the display window for the movies
    def showMovies(self, buttonTitle):
        self.movieWindow = PyMovieWindow(buttonTitle)
        self.optionWindow.close()
        self.movieWindow.show()
        


# Client Code
def main():
    # Create an instance of `QApplication`
    pymovie = QApplication(sys.argv)
    # Create instances of the controller
    controller = PyMovieCtrl()
    controller.showOptions()
    # Execute calculator's main loop
    sys.exit(pymovie.exec_())
    
    
if __name__ == "__main__":
    main()
