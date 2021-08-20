import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from tkinter import *
from PIL import Image,ImageTk
from tkinter import filedialog

window = Tk()
window.title('Face Recognition App')
window.geometry("305x455")

myImg = ImageTk.PhotoImage(Image.open("background.jpg"))
myLabel = Label(image=myImg)
myLabel.grid(row=0, column=0, columnspan=3)

def addNew():
    global newImage
    window.filename = filedialog.askopenfilename(initialdir="/faceRec/Images", title="Select a file", filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))
    #newLabel1 = Label(window, text=window.filename)
    #newLabel1.grid(row=2, column=0, columnspan=3)
    #newImage = ImageTk.PhotoImage(Image.open(window.filename))
    newLabel2 = Label(window, text="New reference image added.").grid(row=3, column=0, columnspan=3)

    #newImage_label = Label(image=newImage).grid(row=0, column=2, columnspan=3)

def scanNow():
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.5, 0.5)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesInFrame = face_recognition.face_locations(imgS)
        encodeFaces = face_recognition.face_encodings(imgS, facesInFrame)

        for encodings, locations in zip(encodeFaces, facesInFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodings)
            faceDistances = face_recognition.face_distance(encodeListKnown, encodings)
            print(faceDistances)
            matchIndex = np.argmin(faceDistances)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                print(name)
                y1, x2, y2, x1 = locations
                y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                markAttendance(name)

        cv2.imshow('Webcam', img)
        cv2.waitKey(1)

myButton1 = Button(window, text="Add new reference", command=addNew)
myButton2 = Button(window, text="Scan now", command=scanNow)
myButton3 = Button(window, text="Exit", command=window.quit)

myButton1.grid(row=1, column=0)
myButton2.grid(row=1, column=1)
myButton3.grid(row=1, column=2)


path = 'Images'
images = []
classNames = []
myList = os.listdir(path)
#print(myList)

for name in myList:
    currentImg = cv2.imread(f'{path}/{name}')
    images.append(currentImg)
    classNames.append(os.path.splitext(name)[0])
#print(classNames)

def findEncodings (images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            time = datetime.now()
            dtstring = time.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtstring}')

encodeListKnown = findEncodings(images)
print('Encoding Complete.')

cap = cv2.VideoCapture(1)

window.mainloop()

