import cv2
import numpy as np
import sqlite3

faceDetect = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)


def insertOrUpdate(Id, Name, Age):
    conn = sqlite3.connect("database.db")
    cmd = "SELECT * FROM students WHERE ID="+str(Id)
    cursor = conn.execute(cmd)
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if (isRecordExist == 1):
        # cmd="UPDATE Peoples SET Name="+str(Name)+"WHERE id="+str(Id)
        conn.execute("UPDATE students SET Name=? WHERE id=?", (Name, Id,))
        conn.execute("UPDATE students SET Age=? WHERE id=?", (Age, Id))
    else:
        # cmd="INSERT INTO Peoples(id,Name,Age,Gender) Values("+str(Id)+","+str(Name)+","+str(Age)+","+str(Gen)+")"
        conn.execute(
            "INSERT INTO students(id,Name,Age) Values(?,?,?)", (Id, Name, Age))
        # cmd2=""
        # cmd3=""
    conn.commit()
    conn.close()


Id = input('Enter User Id:')
name = input('Enter User Name:')
age = input('Enter User Age:')
insertOrUpdate(Id, name, age)
sampleNum = 0
while (True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        sampleNum = sampleNum+1
        cv2.imwrite("dataSet/User."+str(Id)+"." +
                    str(sampleNum)+".jpg", gray[y:y+h, x:x+w])
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.waitKey(400)
    cv2.imshow("Face", img)
    cv2.waitKey(1)
    if (sampleNum > 20):
        print("Done")
        break
cam.release()
cv2.destroyAllWindows()
