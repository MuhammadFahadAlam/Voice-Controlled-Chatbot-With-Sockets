from tkinter import *
import time
import datetime
import pyttsx3
import speech_recognition as sr
from threading import Thread
import requests
from bs4 import BeautifulSoup
import socket
#import pickle


def wishme():
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        text = "Good Morning sir. I am Jarvis. How can I Serve you?"
    elif 12 <= hour < 18:
        text = "Good Afternoon sir. I am Jarvis. How can I Serve you?"
    else:
        text = "Good Evening sir. I am Jarvis. How can I Serve you?"

    canvas2.create_text(10,10,anchor =NW , text=text,font=('Candara Light', -25,'bold italic'), fill="white",width=350)
    p1=Thread(target=speak,args=(text,))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()

def shut_down():
    p1=Thread(target=speak,args=("Shutting down. Thankyou For Using Our Sevice. Take Care, Good Bye.",))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()
    time.sleep(7)
    root.destroy()




def speak(text):
    global flag
    engine.say(text)
    engine.runAndWait()
    flag=False


def get_answer_from_server(qs):
    global flag2
    global loading
    
    s.send(qs.encode())
    s_messg=s.recv(1024)
    print("message from server: ",s_messg.decode())
    answer = s_messg.decode()
    canvas2.create_text(10, 225, anchor=NW, text=answer, font=('Candara Light', -25,'bold italic'),fill="white", width=350)
    flag2 = False
    loading.destroy()

    p1=Thread(target=speak,args=(answer,))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()
    

def transition2():
    global img1
    global flag
    global flag2
    global frames
    global canvas
    local_flag = False
    for k in range(0,5000):
        for frame in frames:
            if flag == False:
                canvas.create_image(0, 0, image=img1, anchor=NW)
                canvas.update()
                flag = True
                return
            else:
                canvas.create_image(0, 0, image=frame, anchor=NW)
                canvas.update()
                time.sleep(0.1)
        

def takecommand():
    global loading
    global flag
    global flag2
    global canvas2
    global query
    global img4
    if flag2 == False:
        canvas2.delete("all")
        canvas2.create_image(0,0, image=img4, anchor="nw")

    speak("I am listening.")
    flag= True
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 4000
    with sr.Microphone() as source:
        print("Listening...")
        #r.pause_threshold = 3
        audio = r.listen(source,timeout=4,phrase_time_limit=4)

    try:
        print("Recognizing..")
        query = r.recognize_google(audio, language='en-in')
        print(f"user Said :{query}\n")
        query = query.lower()
        canvas2.create_text(490, 120, anchor=NE, justify = RIGHT ,text=query, font=('fixedsys', -30),fill="white", width=350)
        global img3
        loading = Label(root, image=img3, bd=0)
        loading.place(x=900, y=622)

    except Exception as e:
        print(e)
        speak("Say that again please")
        return "None"




def main_window():
    global query
    wishme()
    while True:
        if query != None:
            if 'shutdown' in query or 'quit' in query or 'stop' in query or 'goodbye' in query:
                shut_down()
                break
            else:
                get_answer_from_server(query)
                query = None

    


if __name__ == "__main__":

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #host=socket.gethostname()
    s.connect(('192.168.19.138',7634))   

    loading = None
    query = None
    flag = True
    flag2 = True

    engine = pyttsx3.init() # Windows
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-10)

    root=Tk()
    root.title("Intelligent Chatbot")
    root.geometry('1360x690+-5+0')
    root.configure(background='white')

    img1= PhotoImage(file='static/chatbot-image.png')
    img2= PhotoImage(file='static/button-green.png')
    img3= PhotoImage(file='static/icon.png')
    img4= PhotoImage(file='static/terminal.png')
    background_image=PhotoImage(file="static/last.png")

    f = Frame(root,width = 1360, height = 690)
    f.place(x=0,y=0)
    
    background_label = Label(root, image=background_image)
    background_label.place(x=0, y=0)

    frames = [PhotoImage(file='static/chatgif.gif',format = 'gif -index %i' %(i)) for i in range(20)]
    canvas = Canvas(root, width = 800, height = 596)
    canvas.place(x=10,y=10)
    canvas.create_image(0, 0, image=img1, anchor=NW)
    question_button = Button(root,image=img2, bd=0, command=takecommand)
    question_button.place(x=200,y=625)

    frame=Frame(root,width=500,height=596)
    frame.place(x=825,y=10)
    canvas2=Canvas(frame,bg='#FFFFFF',width=500,height=596,scrollregion=(0,0,500,900))
    vbar=Scrollbar(frame,orient=VERTICAL)
    vbar.pack(side=RIGHT,fill=Y)
    vbar.config(command=canvas2.yview)
    canvas2.config(width=500,height=596, background="black")
    canvas2.config(yscrollcommand=vbar.set)
    canvas2.pack(side=LEFT,expand=True,fill=BOTH)
    canvas2.create_image(0,0, image=img4, anchor="nw")

    task = Thread(target=main_window)
    task.start()
    root.mainloop()
