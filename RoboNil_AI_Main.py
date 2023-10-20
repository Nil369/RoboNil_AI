# Hello sir/mam,
# This python code is written by AKASH HALDER

import sys
import time
from gtts import gTTS
from playsound import playsound
from time import sleep
from googletrans import Translator
import googletrans
import pyautogui
from PyQt5.QtWidgets import QWidget,QGraphicsDropShadowEffect,QVBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtWidgets import QApplication
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QTimer, QTime, QDate, Qt, QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from PyQt5 import QtGui
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QThread
from Robonil_gui import Ui_RoboNil_AI
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import openai
from config import apikey
import requests
import json


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# ui.terminalPrint (voices[1].id)
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)

def speak(audio):
    ui.updateMovieDynamically("speaking")
    engine.say(audio)
    engine.runAndWait()

def ai(prompt):
        openai.api_key = apikey
        text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

        response = openai.Completion.create(
            # model="text-davinci-003",
            model="gpt-3.5-turbo",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # todo: Wrap this inside of a  try catch block
        # ui.terminalPrint(response["choices"][0]["text"])
        text += response["choices"][0]["text"]
        if not os.path.exists("Openai"):
            os.mkdir("Openai")

            # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
        with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
            f.write(text)


chatStr = ""
    # https://youtu.be/Z3ZAJoi4x6Q
def chat(query):
        global chatStr
        ui.terminalPrint(chatStr)
        openai.api_key = apikey
        chatStr += f"Akash: {query}\n RoboNil: "
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt= chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # todo: Wrap this inside of a  try catch block
        print("Robonil: ",response["choices"][0]["text"])
        speak(response["choices"][0]["text"])
        chatStr += f"{response['choices'][0]['text']}\n"
        return response["choices"][0]["text"]


def wishMe():
     hour = int(datetime.datetime.now().hour)
     if hour>=0 and hour<12:
        ui.terminalPrint("Good Morning!")
        speak("Good Morning!")
     elif hour>=12 and hour<18:
        ui.terminalPrint("Good Afternoon!")
        speak("Good Afternoon!")
     elif hour>=18 and hour<20:
        ui.terminalPrint("Good Evening!")
        speak("Good Evening!")
     
def translategl(query):
    speak("SURE SIR")
    ui.terminalPrint(googletrans.LANGUAGES)
    translator = Translator()
    speak("Choose the language in which you want to translate")
    b = input("To_Lang :- ")   
    text_to_translate = translator.translate(query,src = "auto",dest= b,)
    text = text_to_translate.text
    try : 
        speakgl = gTTS(text=text, lang=b, slow= False)
        speakgl.save("voice.mp3")
        playsound("voice.mp3")
        
        time.sleep(5)
        os.remove("voice.mp3")
    except:
        ui.terminalPrintprint("Unable to translate")


NEWS_API_KEY = '95ffa5f296884a8c8b9a346ec86de814'
NEWS_API_BASE_URL = 'https://newsapi.org/v2/top-headlines'
COUNTRY_CODE = 'in' 
def get_news(api_key, country_code='us', num_articles=5):
    parameters = {
            'country': country_code,
            'apiKey': api_key,
            'pageSize': num_articles
        }

    try:
            response = requests.get(NEWS_API_BASE_URL, params=parameters)
            response.raise_for_status()
            data = response.json()
            articles = data['articles']
            return articles
    except requests.exceptions.HTTPError as http_err:
            ui.terminalPrint(f"HTTP error occurred: {http_err}")
    except Exception as err:
            ui.terminalPrint(f"Error occurred: {err}")
    return None



class RoboNil(QThread):
    def __init__(self):
        super(RoboNil,self).__init__()
        

    def run(self):
        self.TaskExecution()

    
       
    def takeCommand(self):

        ui.updateMovieDynamically("listening")
        #It takes microphone input from the user and returns string output

        r = sr.Recognizer()
        with sr.Microphone() as source:
            ui.terminalPrint("RoboNil Listening...")
            r.pause_threshold = 1
            r.phrase_threshold = 0.3 
            r.non_speaking_duration = 0.9
            audio = r.listen(source)
        try:
            ui.updateMovieDynamically("loading") 
            ui.terminalPrint("Recognizing...")    
            query = r.recognize_google(audio, language='en-in') #Using google for voice recognition.
            ui.terminalPrint(f"User said: {query}\n")  #User query will be ui.terminalPrinted.

        except Exception as e:
            

            # ui.terminalPrint(e)    
            ui.terminalPrint("Robonil: Some Error Occured...Sorry from RoboNil") #Say that again will be ui.terminalPrinted in case of improper voice 
            speak("Sorry! Speak again please")
            return "None" #None string will be returned
        return query
    
    def TaskExecution(self):
     
     wishMe()
    #  strTime = datetime.datetime.now().strftime("%H:%M:%S")  
    #  ui.terminalPrint(f" Current time : {strTime}")
     ui.terminalPrint('''\nHi...I am Robo Nil A.I created by Akash...How can I help you?\n
          To exit the program say "Shutdown Robonil" \n''')
     ui.terminalPrint("                         **********                                      ")   
     speak("Hi...I am Robo Nil AI created by Akash ")
     while True:
      
      
      self.query = self.takeCommand().lower()
      ui.updateMovieDynamically("loading")
      # Can add more sites in list
      sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],["amazon","https://www.amazon.in/"],
               
               ["hotstar","https://www.hotstar.com/"], ["spotify", "https://open.spotify.com/"], ["gmail","https://mail.google.com/mail/u/0/"], 
               
               ["flipkart","https://www.flipkart.com/"], ["stackoverflow","https://stackoverflow.com/"], ["music", "https://open.spotify.com/album/2JGNXENXZNfriWZkpW8qKc"],
               ["chatgpt", "https://chat.openai.com/"], ["instagram","https://www.instagram.com/"],["facebook", "https://www.facebook.com/"]]
      for site in sites:
            if f"Open {site[0]}".lower() in self.query.lower():
                ui.updateMovieDynamically("loading")
                speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

      if 'wikipedia'in self.query:
         try:
          
          speak("Searching...")
        
          self.query = self.query.replace("wikipedia", "")
          results = wikipedia.summary(self.query, sentences=2) 
          speak("According to Wikipedia")
         
          ui.terminalPrint(results)
          speak(results)

         except Exception as e:
              ui.terminalPrint("Sorry... I was unable to find anything...Try again🔃")
              speak("Sorry ... I was unable to find anything...Try again")


      elif 'what is your name' in self.query:
            
            ui.terminalPrint("My name is RoboNil")
            speak("My name is RoboNil")
    
            ui.terminalPrint("What do you want me to do?")
            speak("What do you want me to do?")


      elif 'play music' in self.query:
          webbrowser("https://open.spotify.com/")
            # music_dir = 'C:\\Users\\akash\\Music\\AUDIO LIBRARY'
            # songs = os.listdir(music_dir)
            # ui.terminalPrint(songs)    
            # os.startfile(os.path.join(music_dir, songs[0]))

      elif 'the time' in self.query:
           
            strTime = datetime.datetime.now().strftime("%H:%M:%S")  
            ui.terminalPrint(f"Sir, the time is {strTime}")  
            speak(f"Sir, the time is {strTime}")

      elif "Using artificial intelligence".lower() in self.query.lower():
          
          ai(prompt=self.query)

      elif 'open code' in self.query:
            codePath = "C:\\Users\\akash\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

      elif 'Open Chrome' in self.query:
        ui.terminalPrint("Opnening Chrome")
        speak("Opnening Chrome Sir")
        codePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        os.startfile(codePath)

      elif "tell me about yourself" in self.query:
          
          ui.terminalPrint('''
            My name is RoboNil and I am an artificially intelligent robot programmed by Akash Halder to help people with various tasks. 
            I have been designed to understand natural language and interact with people. I am also able to process 
            requests and provide helpful information quickly and accurately. Additionally, I have been programmed to
            recognize patterns and to learn from experience.''')
          
          speak('''My name is RoboNil and I am an artificially intelligent robot programmed by Akash Halder to help people with various tasks. 
                I have been designed to understand natural language and interact with people. 
                I am also able to process requests and provide helpful information quickly and accurately. 
                Additionally, I have been programmed to recognize patterns and to learn from experience.''')
          
      elif 'Who created you'in self.query:
          ui.terminalPrint("I am created by Akash Halder")
          speak("I am created by Akash Halder")

      elif 'Who programmed you'in self.query:
          ui.terminalPrint("I am created by Akash Halder")
          speak("I am created by Akash Halder")
        

      elif "open" in self.query:
          from Dictapp import openappweb
          openappweb(self.query)

      elif "close" in self.query:
            from Dictapp import closeappweb
            closeappweb(self.query)

      elif "google" in self.query:
           from SearchNow import searchGoogle
           searchGoogle(self.query)

      elif "youtube" in self.query:
           from SearchNow import searchYoutube
           searchYoutube(self.query)  


      elif 'maximize this window' in self.query: 
            pyautogui.hotkey('alt', 'space') 
            time.sleep(1) 
            pyautogui.press('x') 
 
 
      elif 'google search' in self.query: 
            self.query = self.query.replace("google search", "") 
            pyautogui.hotkey('alt', 'd') 
            pyautogui.write(f"{self.query}", 0.1) 
            pyautogui.press('enter') 
 
 
      elif 'youtube search' in self.query: 
            self.query = self.query.replace("youtube search", "") 
            pyautogui.hotkey('alt', 'd') 
            time.sleep(1) 
            pyautogui.press('tab') 
            pyautogui.press('tab') 
            pyautogui.press('tab') 
            pyautogui.press('tab') 
            time.sleep(1) 
            pyautogui.write(f"{self.query}", 0.1) 
            pyautogui.press('enter') 
 
 
      elif 'open new window' in self.query: 
            pyautogui.hotkey('ctrl', 'n') 
 
 
      elif 'open incognito window' in self.query: 
            pyautogui.hotkey('ctrl', 'shift', 'n') 
 
  
      elif 'minimise this window' in self.query: 
           pyautogui.hotkey('alt', 'space') 
           time.sleep(1) 
           pyautogui.press('n') 
 
 
      elif 'open history' in self.query: 
            pyautogui.hotkey('ctrl', 'h') 
 
 
      elif 'open downloads' in self.query: 
            pyautogui.hotkey('ctrl', 'j') 
 
 
      elif 'previous tab' in self.query: 
            pyautogui.hotkey('ctrl', 'shift', 'tab') 
 
 
      elif 'next tab' in self.query: 
            pyautogui.hotkey('ctrl', 'tab') 
 
 
      elif 'close tab' in self.query: 
            pyautogui.hotkey('ctrl', 'w') 
 
 
      elif 'close window' in self.query: 
            pyautogui.hotkey('ctrl', 'shift', 'w') 

      elif "volume up" in self.query: 
            pyautogui.press("volumeup") 
            pyautogui.press("volumeup") 
            pyautogui.press("volumeup") 
            pyautogui.press("volumeup") 
            pyautogui.press("volumeup") 
            pyautogui.press("volumeup") 
            pyautogui.press("volumeup") 
            pyautogui.press("volumeup") 
            pyautogui.press("volumeup") 
            pyautogui.press("volumeup") 
            pyautogui.press("volumeup") 
            pyautogui.press("volumeup") 
            pyautogui.press("volumeup") 
            
         
      elif "volume down" in self.query: 
            pyautogui.press("volumedown") 
            pyautogui.press("volumedown") 
            pyautogui.press("volumedown") 
            pyautogui.press("volumedown") 
            pyautogui.press("volumedown") 
            pyautogui.press("volumedown") 
            pyautogui.press("volumedown") 
            pyautogui.press("volumedown") 
            pyautogui.press("volumedown") 
            
 
 
      elif "mute" in self.query: 
            pyautogui.press("volumemute") 
 
 
      elif "refresh" in self.query: 
            pyautogui.moveTo(1551,551, 2) 
            pyautogui.click(x=1551, y=551, clicks=1, interval=0, button='right') 
            pyautogui.moveTo(1620,667, 1) 
            pyautogui.click(x=1620, y=667, clicks=1, interval=0, button='left') 
 
 
      elif "scroll down" in self.query: 
            pyautogui.scroll(1000)






      elif 'shutdown' in self.query:
           ui.terminalPrint("Robonil: Shutting down sir...Thanks for investing your time")
           speak(" Shutting down sir...Thanks for investing your time")
           exit()


# This python code is written by AKASH HALDER
# Weather App
      elif 'open weather app' in self.query:
          ui.updateMovieDynamically("loading")
          speak("Opening Akash's Weather app sir...")
          import requests
          import json

       
          while True:
             
             
             try:
               
               ui.terminalPrint("=================== Akash's Weather App (version=1.1.1) ==================")
               ui.terminalPrint("To know the temperature of your  city tell me the name of your  city: \n")
               ui.terminalPrint( "To Exit the weather app say'exit weather app' :" )
               speak("To know the temperature Tell me the name of your  city:")
               city = self.takeCommand()

               if 'exit weather app' in city :
                    
                    ui.terminalPrint("Bye Bye my friend . \nThanks for using  Akash's Weather App.")
                    speak("Closing Weather App. \nThanks for using  Akash's Weather App.")
                    break

               url = f"https://api.weatherapi.com/v1/current.json?key=dc5799ac63574ee9a66182700230807&q={city}"

              
               r = requests.get(url)
        
               wdic = json.loads(r.text)
               w = (wdic["current"]["temp_c"])
               ui.terminalPrint(f"The current temperature in {city} is {w} degrees Celsius")
               speak(f"The current temperature in{city} is {w} degrees Celsius")
             except:
              
              ui.terminalPrint("Sorry!Something went wrong... try again 🔃",)
              speak("Sorry!Something went wrong... try again")

             

      elif "reset chat".lower() in self.query.lower():
            chatStr = ""

      elif 'open news' in self.query:
          ui.updateMovieDynamically("loading")
          ui.terminalPrint("Fetching News sir...")
          speak("Fetching News sir...")
          news_articles = get_news(NEWS_API_KEY, COUNTRY_CODE, num_articles=3)

          if news_articles:
           for idx, article in enumerate(news_articles, 1):
            ui.terminalPrint(f"Article {idx}:")
            speak(f"Article {idx}:")
            ui.terminalPrint("Title:", article['title'])
            speak( article['title'])
            ui.terminalPrint("Description:", article['description'])
            speak( article['description'])
            ui.terminalPrint("Source:", article['source']['name'])
            ui.terminalPrint("URL:", article['url'])
            ui.terminalPrint()
          else:
           ui.updateMovieDynamically("speaking")
           ui.terminalPrint("Failed to fetch news articles.")
           speak("Failed to fetch news articles.")

      else:
            ui.terminalPrint("Chatting...")
            chat(self.query)
    
    # This python code is written by AKASH HALDER


    
    def sendEmail(to, content):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('youremail@gmail.com', 'your-password')
        server.sendmail('youremail@gmail.com', to, content)
        server.close()


        
class Robonil_GUI(QWidget):
    def __init__(self):
        super(Robonil_GUI, self).__init__()
        

        
        self.RobonilUi = Ui_RoboNil_AI()
        self.RobonilUi.setupUi(self)
        self.RobonilUi.pushButton.clicked.connect(self.runAllMovies)
        self.RobonilUi.pushButton_2.clicked.connect(self.close)
        self.RobonilUi.pushButton_6.clicked.connect(self.manualCodeFromTerminal)
        self.RobonilUi.pushButton_3.clicked.connect(self.open_google)
        self.RobonilUi.pushButton_5.clicked.connect(self.open_Youtube)
        
    def open_google(self):
        url = QUrl("https://www.google.com")
        QDesktopServices.openUrl(url)

    def open_Youtube(self):
        url = QUrl("https://www.youtube.com")
        QDesktopServices.openUrl(url)   
        

    
    def runAllMovies(self):
    
      

        self.RobonilUi.arcmovie = QtGui.QMovie("C:\\Users\\akash\\OneDrive\\Desktop\\ROBONIL AI\\GUI\\Images\\Arc.gif")
        self.RobonilUi.label_5.setMovie(self.RobonilUi.arcmovie)
        self.RobonilUi.arcmovie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        self.RobonilUi.movie = QtGui.QMovie(":/resource/GUI/Images/Sound wave.gif")
        self.RobonilUi.label_3.setMovie(self.RobonilUi.movie)
        self.RobonilUi.movie.start()

        self.RobonilUi.listeningmovie = QtGui.QMovie(":/resource/GUI/Images/Listening.gif")
        self.RobonilUi.label_6.setMovie(self.RobonilUi.listeningmovie)
        self.RobonilUi.listeningmovie.start()

        self.RobonilUi.arc_1movie = QtGui.QMovie("GUI/Images/AI.gif")
        self.RobonilUi.label_9.setMovie(self.RobonilUi.arc_1movie)
        self.RobonilUi.arc_1movie.start()

        self.RobonilUi.loadingmovie = QtGui.QMovie("C:\\Users\\akash\\OneDrive\\Desktop\\ROBONIL AI\\GUI\\Images\\Listening.gif")
        self.RobonilUi.label_7.setMovie(self.RobonilUi.loadingmovie)
        self.RobonilUi.loadingmovie.start()

        self.RobonilUi.intmovie = QtGui.QMovie(":/resource/GUI/Images/Initializing system.gif")
        self.RobonilUi.label_2.setMovie(self.RobonilUi.intmovie)
        self.RobonilUi.intmovie.start()
        
        self.RobonilUi.hackingmovie = QtGui.QMovie(":/resource/GUI/Images/hacking_1.gif")
        self.RobonilUi.label_10.setMovie(self.RobonilUi.hackingmovie)
        self.RobonilUi.hackingmovie.start()

    
        self.media_player = QMediaPlayer(self)
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile("C:\\Users\\akash\\OneDrive\\Desktop\\ROBONIL AI\\GUI\\vozrobotr2c3po-105470.mp3")))
        self.media_player.play()

        self.media_player = QMediaPlayer(self)
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile("C:\\Users\\akash\\OneDrive\\Desktop\\ROBONIL AI\\GUI\\system_activated.mp3")))
        self.media_player.play()
        # self.media_player = QMediaPlayer(self)
        # self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile("C:\\Users\\akash\\OneDrive\\Desktop\\ROBONIL AI\\GUI\\activation-finished-82915.mp3")))
        # self.media_player.play()
        
        
        self.media_player = QMediaPlayer(self)
        # Play the music after a short delay (to ensure the GIF starts first)
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile("C:\\Users\\akash\\OneDrive\\Desktop\\ROBONIL AI\\GUI\\yt1s.com - Binary Code  Interface Sound Effects  SciFi Computer Beeps  Data Processing Sounds.mp3")))
        self.media_player.stateChanged.connect(self.on_media_state_changed)
       # Play the music after a short delay (to ensure the GIF starts first)
        QTimer.singleShot(100, self.play_music)
        # Play the music
        startExecution.start()

    
    def updateMovieDynamically(self, state):
        if state == "listening":
            self.RobonilUi.label_6.raise_()
            self.RobonilUi.label_9.hide()
            self.RobonilUi.label_7.hide()
            self.RobonilUi.label_6.show()

        elif state == "loading":
            self.RobonilUi.label_7.raise_()
            self.RobonilUi.label_9.hide()
            self.RobonilUi.label_6.hide()
            self.RobonilUi.label_7.show()

        elif state == "speaking":
            self.RobonilUi.label_9.raise_()
            self.RobonilUi.label_7.hide()
            self.RobonilUi.label_6.hide()
            self.RobonilUi.label_9.show()

    

    def play_music(self):
         self.media_player.setVolume(25)
         self.media_player.play()
        
    
    def on_media_state_changed(self, state):
        if state == QMediaPlayer.StoppedState:
            # Restart the music and GIF when the music finishes playing
            self.media_player.setPosition(0)
            self.media_player.play()
    

            
    
    def showTime(self):
        current_time = QTime.currentTime()
        current_Date = QDate.currentDate()
        label_time = current_time.toString('   hh:mm:ss ')
        label_date = current_Date.toString('  dd / MM / yy')
        self.RobonilUi.textBrowser.setText(label_date)
        self.RobonilUi.textBrowser_2.setText(label_time)
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setColor(Qt.blue)  # Set the color of the glow effect
        glow_effect.setOffset(9)       # Set the offset of the glow
        glow_effect.setBlurRadius(10)  # Set the blur radius to control the glow intensity
        self.RobonilUi.textBrowser_2.setGraphicsEffect(glow_effect)
        #Qt.ISODate

        # Apply the QGraphicsDropShadowEffect to the QTextBrowser
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setColor(Qt.blue)  # Set the color of the glow effect
        glow_effect.setOffset(9)       # Set the offset of the glow       
        glow_effect.setBlurRadius(10) 
        self.RobonilUi.textBrowser.setGraphicsEffect(glow_effect)


    def terminalPrint(self, text):
        self.RobonilUi.textBrowser_3.append(text)

    def manualCodeFromTerminal(self):
        cmd = self.RobonilUi.lineEdit.text()
        if cmd:
            self.RobonilUi.lineEdit.clear()
            self.RobonilUi.textBrowser_3.append(f"You typed >> {cmd}")

            if cmd == "exit":
                ui.close()
            elif cmd == "help":
                self.terminalPrint('''
            My name is RoboNil and I am an artificially intelligent robot programmed by Akash Halder to help people with various tasks. 
            I have been designed to understand natural language and interact with people. I am also able to process 
            requests and provide helpful information quickly and accurately. Additionally, I have been programmed to
            recognize patterns and to learn from experience.''')

        
                    

            else:
                pass

        else:
            pass



    
startExecution = RoboNil()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Robonil_GUI()
    ui.show()
    sys.exit(app.exec_())
