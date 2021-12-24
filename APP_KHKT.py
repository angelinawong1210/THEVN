def Load_Data(question):
    
    with open('Document\\Questions.txt','r') as file: #open questions stored in text file
        for i in range(50):
            question.append(file.readline()) #store the questions into the list
        file.close() #close the file

def RandomQuestion(question,Tlist):

    text = "Press 'RECORD' button and WAIT 3 SCONDS to record the answer!"
    text = textwrap.fill(text, width=30)
    upper_label['text'] = text #print the message
    
    import random #import random library 
    from playsound import playsound #import play sound library

    x = random.randint(0,49) #random from 0 to 49
    playsound("Audio\\" + str(x+1) + ".mp3") #run the audio file of the question

    text = question[x]
    text = textwrap.fill(text, width=30)
    label["text"] =  text #print the question on the screen

    StartCount(Tlist) #run the start count function to get the start time


def SpeechToText(TList):

    end_time = time.time() #get the end time

    import speech_recognition as sr  #import speech recognition library
    r = sr.Recognizer()

    mic = sr.Microphone(device_index=1) #set up the microphone

    with mic as source: 

        #print the message on the screen
        upper_label['text'] = "Please wait 3 seconds..."
        time.sleep(1)
        root.update()
        upper_label['text'] = "Please wait 2 seconds..."
        time.sleep(1)
        root.update()
        upper_label['text'] = "Please wait 1 seconds..."
        time.sleep(1)
        root.update()
        

        #adjust the speech recognition algorithm to fit the environment's noise level
        r.adjust_for_ambient_noise(mic,duration=1)

        #print the message on the screen
        upper_label['text'] = "Recording...."
        root.update()

        audio = r.listen(source)   #listen to the voice
    
    result = r.recognize_google(audio, language='en-US') #get the result

    with open('Document\\SpeechToText.txt',mode ='w') as file: 
        file.write(result.capitalize()) #wrtie the result into text file
    
        result = textwrap.fill(result, width=30)
        label['text'] = (result.capitalize())  #print the result on the screen

        upper_label['text'] = "Recording completed !" #print the message

        file.close() #close the file

    EndCount(TList,end_time) #run the end time fucntion to store the end_time variable into the list


def GrammarChecking(Tlist):

    level  = "null" #set up the default level variable

    #import proofread library
    import language_tool_python
    tool = language_tool_python.LanguageTool('en-US') 
    
    i = 0 #the number of error. default = 0
    
    with open(r'Document\\SpeechToText.txt', 'r') as fin:    #read the content of the speech
                
        for line in fin: 
            matches = tool.check(line) #check the error
            i = i + len(matches)    #count the error  
            pass
        fin.close() #close the file
    
    text = "The number of mistakes found in the speech is " + str(i)
    text = textwrap.fill(text, width=30)
    upper_label['text'] = text #print the number of mistakes on the program's interface
    
    time_lapsed = (TList[1] - TList[0])%60 #caculate the delay time

    #set the level of the user depending on the delay time
    if (time_lapsed < 0.91486): 
        level = "good"
    elif (0.91486 < time_lapsed < 1.230425):
        level = "normal"
    elif (time_lapsed > 1.230425):
        level = "bad"

    text = "The delay time is " + str(time_lapsed) +  " second. Your level is " + level + "."
    text = textwrap.fill(text, width=30)
    label['text'] = text #print the result on the screen


def StartCount(Tlist):
    global start_time #set up the variable to store the start time
    start_time = time.time() #get the value for the start time
    Tlist.append(start_time) #store start time into a list
    root.update() #update the program

#Finish counting
def EndCount(Tlist,end_time): 
    Tlist.append(end_time) #store the end time into a list
    root.update() #update the program

#Exit 
def Exit():
    exit()

#Restart the program
def Restart():
    label["text"] = "" #clear the screen
    upper_label['text'] = "" 
    TList.clear() #clear the list that stores time
    root.update() #update the program


#MAIN FUNCTION

question = []
Load_Data(question)

#import Graphic library
import tkinter as tk
from tkinter import messagebox

import textwrap #wrap text library 

#import Time library
import time

root = tk.Tk()

#Store time to caculate the delay time
TList = []

root.title('The VN')

HEIGHT = 744
WIDTH = 1052
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

#background
background_image = tk.PhotoImage(file='Image\\background_chinh_thuc.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

#Main frame
frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.05, relwidth=0.5, relheight=0.1, anchor='n')

#Message box
messagebox.showinfo("Instruction", "Click 'Begin' to start the app and listen carefully to the question. As soon as you have the answer, click 'Record' to record your answer and have it converted to text. Finally, click 'Result' to see the result and your level.")

#Begin Button
BeginButton = tk.Button(frame, text="Begin", font=40, command=lambda: RandomQuestion(question,TList))
BeginButton.place(relx=0, relheight=1, relwidth=0.3)

#Record Button
RecordButton = tk.Button(frame, text="Record", font=40,  command=lambda: SpeechToText(TList))
RecordButton.place(relx=0.35, relheight=1, relwidth=0.3)

#Result Button
ResultButton = tk.Button(frame, text="Result", font=40,  command= lambda:  GrammarChecking(TList))
ResultButton.place(relx=0.7, relheight=1, relwidth=0.3)

#Exit Button
ExitButton = tk.Button(root, text="Exit", font=40,  command=lambda: Exit())
ExitButton.place(relx=0.70, rely = 0.9,relheight=0.05, relwidth=0.1)

#Restart Button
RestartButton = tk.Button(root, text="Restart", font=40,  command=lambda: Restart())
RestartButton.place(relx=0.20, rely = 0.9,relheight=0.05, relwidth=0.1)

#lower_frame
lower_frame = tk.Frame(root, bg='white', bd=10)
lower_frame.place(relx=0.5, rely=0.2, relwidth=0.6, relheight=0.6, anchor='n')

#upper label
upper_label = tk.Label(lower_frame)
upper_label.place(relwidth=1, relheight=0.45,rely = 0.01)
upper_label.config(font=("Arial", 18))

#label
label = tk.Label(lower_frame)
label.place(relwidth=1, relheight=0.45,rely = 0.55)
label.config(font=("Arial", 18))

root.mainloop()
