import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
from googlesearch import search
import random
import pyautogui as pa
import pywhatkit
from gnewsclient import gnewsclient
import wolframalpha
import time as timee
import smtplib
from email.message import EmailMessage
from pygame import mixer
mixer.init()

engine = pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

musicdir="D:\\Music"
songs = os.listdir(musicdir)

app_id = 'RR8RAK-3P9VK59UJL'

email_list = {'balaji':'balajik272003@gmail.com',
            'karan':'rkaran0930@gmail.com',
            'kowsalya':'kowsikaruppaiyak@gmail.com',
            'hariharan':'hariharan276@gmail.com'}

def fetch_news():
    global news_list
    client = gnewsclient.NewsClient(language='english',location='India', topic='Sports',  max_results=3) 
    news_list = client.get_news()
    
def speak(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour=int(datetime.datetime.now().hour)
    if(hour>=0 and hour<12):
        speak("\nGOOD MORNING SIR")
    elif(hour>=12 and hour <18):
        speak("GOOD AFTERNOON SIR")
    else:
        speak("GOOD EVENING SIR")
    #speak("HOW CAN I HELP YOU")
    
def takeCommand():
    #It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        #print("\nSay that again please...\n")  
        return "none"
    return query

def wikipedia_seach(query):

    speak("searching in wikipedia")
    query=query.replace("wikipedia","")
    results=wikipedia.summary(query,sentences=2)
    speak("according to wikipedia\n")
    speak(results)
    print("\n")

def open_website_or_software(query):
    
    if('command prompt' in query) or ('command' in query):
            os.system("start cmd")
    elif('notepad' in query):
        os.system("notepad")
    elif('power point' in query) or ('ppt' in query):
        os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE")
    else: 
        query=query.replace("open ","")
        while(' ' in query):
            query=query.replace(" ","")
        webbrowser.open('www.'+query+'.com')
    timee.sleep(3)      

def search_from_any_website(query):
    if 'search ' in query:
        query = query.replace("search ","")
    try:
        ans = search(query, num_results=2)
        webbrowser.open(ans[0])
    except:
        webbrowser.open(ans[1])
    speak("openning in website..")

def youtube(query):
    
    try:
        if "from youtube" in query:
            query = query.replace("from youtube","")
            pywhatkit.playonyt(query)
                
        elif "in youtube" in query:
            query = query.replace("in youtube","")
            pywhatkit.playonyt(query)
            
        aknoledgment = "playing "+ query
        speak(aknoledgment)
    except:
        google_search(query)

def playmusic():
    a= random.randint(0,len(songs))
    speak("playing music...")
    os.startfile(os.path.join(musicdir,songs[a]))
    timee.sleep(4)

def date():
    d = datetime.datetime.today()
    todays_date = "sir,todays date is " + d.strftime("%d %B %Y")
    speak(todays_date)

def current_time():
    strTime = datetime.datetime.now().strftime("%I:%M:%S")    
    speak(f"Sir, the time is {strTime}")

def news():
    
    try:		    
        print('Yes sir loading')
        for item in news_list:
            speak("Headlines: "+ item['title'])
            print("\nLink : ", item['link']) 
            print('____________________________________________________________') 
        fetch_news()

    except:
      	speak('An error occured\n')

def wolframalpha_search(query):
    global temp
    temp = query
    try:
        try:
            speak('searching....')
            client = wolframalpha.Client(app_id) 
            if "what is" in query:
                query = query.replace("what is ","")
            elif "which is" in query:
                query = query.replace("which is ","")
            print(query)
            res = client.query(query)
            answer = next(res.results).text
            speak('Got it sir\n')
            speak(answer)
            
        except:
            #speak("Opening in website")
            wikipedia_seach(query)
    except: 
        google_search(temp)

def google_search(query):
    global b
    try:
        if 'search in google' in query:
            query=query.replace("search in google","")
        elif 'in google' in query:
            query=query.replace("in google","")
        elif 'from google' in query:
            query=query.replace("from google","")
        webbrowser.open('https://www.google.com/search?q='+query)
        b=1
        # ans = search(query, num_results=2)
        # webbrowser.open(ans[0])
        speak("opening in google")
    except:
        speak("sorry sir no more result")

def info_for_mail():
    global receiver
    speak("to whom you want to send email")
    #global name,subject,receiver
    name = decide_t_or_s(a)
    print(name)
    if('none' in name):
        info_for_mail()
        return
    try:
        receiver = email_list[name]
    except:
        speak("sorry coudn't find gmail")
        info_for_mail()
        return
    
    print(receiver)
    speak("what is the subject of your email?")
    subject = decide_t_or_s(a)
    while('none' in subject):
        speak("what is the subject of your email?")
        subject = decide_t_or_s(a)

    speak('What should I say? ')
    content = decide_t_or_s(a)
    while('none' in content):
        speak('What should I say? ')
        content = decide_t_or_s(a)
        
    speak("shall i send the mail? ")
    confirmation = decide_t_or_s(a)
    while('none' in confirmation):
        speak("shall i send the mail? ")
        confirmation = decide_t_or_s(a)

    if(('yes' in confirmation) or ('ok' in confirmation)):
        speak("yes sir , sending the email")
        sending_mail(subject,content,receiver)
    elif (('no' in confirmation) or ('dont send' in confirmation)):
        speak("ok sir , do you want to create new mail?")
        new_mail = decide_t_or_s(a)
        if(('yes' in new_mail) or ('i want to create' in new_mail) or ('i want to send new mail' in new_mail)):
            info_for_mail()
        elif(('no' in new_mail) or ('i dont want to create' in new_mail) or ('i dont want to send' in new_mail)):
            speak("ok sir")
        else:
            speak("ok sir")
    else:
        speak("sending the email...")
        sending_mail(subject,content,receiver)
    # automation in sending the email
def sending_mail(subject,content,receiver):
    try: 
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("rkaran3009@gmail.com", 'karan22334455')
        email=EmailMessage()
        email['From'] = 'rkaran3009@gmail.com'
        email['To'] = receiver
        email['Subject'] = subject
        email.set_content(content)
        server.send_message(email)
        server.close()
        speak('Email sent!!!')
    except:
        speak('Sorry Sir! I am unable to send your message at this moment!')
# Automation code for remainder
def reminder():
    global remind,time,am,reminder_set
    reminder_set=0
    am=0
    speak("What should i remind you? ")
    remind = decide_t_or_s(a)
    while('none' in remind):
        speak("What should i remind you? ")
        remind = decide_t_or_s(a)

    speak("\ntell me the time(with am or pm): ")
    time = decide_t_or_s(a)
    while(('none' in time) or (('a.m.' not in query) and ('p.m' not in query))):
        speak("\ntell me the time(with am or pm): ")
        time = decide_t_or_s(a)
    try:
        if(':00' in time):
            time = time.replace(":00 ","")

        if('a.m.' in time):
            time = time.replace("a.m.","")
            while(' ' in time):
                time = time.replace(" ","")
            time = int(time)
            speak("your reminder is set")
            am=1
            reminder_set = 1

        if('p.m.' in time):
            time =time.replace("p.m.","")
            while(' ' in time):
                time = time.replace(" ","")
            time = int(time)
            time = time + 12
            speak("your reminder is set")
            am=0
            reminder_set = 1
    except: 
        speak("Invalid time input set the reminder again")

    set_reminder(remind,time)

def set_reminder(remind,time):
    global reminder_set
    hour=int(datetime.datetime.now().hour)
    if(am==1):
        if(hour>12):
            hour = hour - 12
    if(time == hour):
        reminder_set = 0
        speak(remind)

def working(query):
    
    if 'open' in query:
        global c,b
        open_website_or_software(query)
        c=0
        b=1

    elif ('play music' in query) or ('play any music' in query):
        playmusic()
        timee.sleep(3)
        c=0
        b=1
    
    elif 'time' in query:
        current_time()
        c=0

    elif 'date' in query:
        date()
        c=0
         
    elif ('from youtube' in query) or ('in youtube' in query):
        youtube(query)
        timee.sleep(3)
        c=0
        b=1

    elif 'news' in query:
        news()
        c=0

    elif ('bye' in query) or ('quit' in query) or ('close' in query):
        speak('okay sir, bye..')
        exit()

    elif 'wikipedia' in query:
        c=0
        try: 
            wikipedia_seach(query)
        except:
            ans = search(query, num_results=2)
            webbrowser.open(ans[0])
            b=1
    elif ('search' in query) and ('google' not in query) and (('from' in query) or ('in' in query)):
        search_from_any_website(query)
        c=0
        b=1

    elif ('search in google' in query) or ('in google' in query) or ('from google' in query):
        google_search(query)
        c=0
    
    elif ('what is' in query) or ('which is' in query) or ('weather' in query) :
        wolframalpha_search(query)
        c=0

    elif ('email'in  query) or ('mail' in query) and ('open' not in query):
        info_for_mail()
        c=0
    
    elif ('jarvis sleep' in query) or ('sleep mode' in query):
        b=1

    elif ('reminder' in query) or ('set reminder' in query):
        reminder()

    elif ('none' not in query):
        speak("Say that again please...\n")

    elif ('i want to speak' in query) or ('speak' in query):
        global a
        a=2
        speak("yes sir you can speak whats your query...")

    elif('i want to type' in query) or ('type' in query):
        a=1
        speak("yes sir you can type...")

    else:
        c=c+1
        if(c==3):
            b=1    

def typing():
    text = input("\nyou--> ")
    return text

def speaking():
    
    query = takeCommand().lower()
    return query

def decide_t_or_s(a):
    global query
    if(a==1):
        query = typing()
    elif(a==2):
        query = speaking()
    return query

def typeorspeak():
    speak("Do you want to Type or Speak?")
    mode = takeCommand().lower()

    if 'type' in mode:
        global a
        a =1
        speak("yes sir you can type...")
        
    elif 'speak' in mode:
        a=2
        speak("yes sir you can speak whats your query...")
        
    else:
        speak("Invalid CHOICE\n")
        typeorspeak()


if __name__ == "__main__":
    fetch_news()
    wishme()
    t_or_s = typeorspeak()
    global initial,reminder_set
    reminder_set = 0
    c=0
    b=0
    initial=0
    query= ' '
    while True:
        if(initial!=0):
            query = decide_t_or_s(a)
        else:
            pass
        if(reminder_set == 1):
            print("checking reminder")
            set_reminder(remind,time)
        if ('wake up jarvis' in query) or (initial==0) or ('wake up' in query): #INITIAL = 0 SO NO NEED TO SAY WAKE UP AT BEGINNING
            initial = 1
            if('wake up jarvis' in query) or ('wake up' in query):
                speak("yes sir, I'm wake up")
            while True:
                query = decide_t_or_s(a)
                working(query)
                if(b==1):
                    soundobj = mixer.Sound("Free_Rewind-Swipe-1_REWSE01042.wav")
                    soundobj.play()
                    timee.sleep(1)
                    soundobj.stop()
                    speak("sleep mode\n")
                    b=0
                    c=0
                    break
