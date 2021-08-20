from tkinter import *
import cv2
import numpy as np
import face_recognition

root = Tk()

def myClick():
    myLabel = Label(root, text ="hello world")
    myLabel.pack()

def onClick():
    cv2.imshow('Praveen', img_praveen)
    cv2.imshow('Praveen Test', img_test)
    cv2.waitKey(0)

myButton = Button(root, text = "Click me", command=onClick)

myButton.pack()

img_praveen = face_recognition.load_image_file('Images/praveen.jpg')
img_praveen = cv2.cvtColor(img_praveen, cv2.COLOR_BGR2RGB)
img_test = face_recognition.load_image_file('Images/praveen.jpg')
img_test = cv2.cvtColor(img_test, cv2.COLOR_BGR2RGB)

faceLoc = face_recognition.face_locations(img_praveen)[0]
encodeFace = face_recognition.face_encodings(img_praveen)[0]
cv2.rectangle(img_praveen, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)

faceLocTest = face_recognition.face_locations(img_test)[0]
encodeFaceTest = face_recognition.face_encodings(img_test)[0]
cv2.rectangle(img_test, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (0, 255, 0), 2)

results = face_recognition.compare_faces([encodeFace], encodeFaceTest)
faceDis = face_recognition.face_distance([encodeFace], encodeFaceTest)
print(results, faceDis)
cv2.putText(img_test, f'{results} {round(faceDis[0], 2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)


root.mainloop()