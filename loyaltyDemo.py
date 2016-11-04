from SimpleCV import Image, Camera
from time import strftime
import pickle
from faceAPI import *
import random
import numpy as np
import cv2


subscription_key = "" ##Enter your own subscription key from Cognitive Services Subscription
base_path = 'C:\Users\deku\Downloads'
faceListId = "mytestset037"


giftList = ["$10 Amazon gift card", "5 Percent discount on purchase of new Titan watch",
"15 percent discount on BookmyShow Ticket", "Uber Free Ride", "Cheetos", "PokemonGo gift card", "No gift this time",
"Thank You Card"]


pidHash = {} # PID -> ["persistedId1", "persistedId2", "persistedId3", "persistedId4"]
persistedIdHash = {} # persistedId -> PID
timeStampHash = {}

# pidHash = pickle.load(open("C:\Users\deku\Downloads\pidHash", "rb"))
# persistedIdHash = pickle.load(open("C:\Users\deku\Downloads\persistedIdHash", "rb"))
# timeStampHash = pickle.load(open("C:\Users\deku\Downloads\stamptime", "rb"))



def initialize():
    cam = Camera(1)
    return cam

def getRandomString():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))


def captureImage(cam, fileName):
    # fileName = "C:\Users\deku\Downloads\CamPics\pic" + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) + str(".jpg")
    img = cam.getImage()
    img.save(fileName)
    return fileName

def getImageContent(fileName):
    with open(fileName, "rb") as f:
        content = f.read()
        print content
    return content

def getTimeStamp():
    return strftime("%d_%m_%Y_%H_%M_%S")

def getConfidence(data):
    try:
        jsonParsed = jsonParsed = json.loads(data.decode('utf-8'))
        if(len(jsonParsed)  >0):
            persistedId = jsonParsed[0]["persistedFaceId"]
            confidence = jsonParsed[0]["confidence"]
            return persistedId, str(confidence)
        else:
                # print "Error in Json Parsing in getConfidence"
                return "err"+getRandomString(), str(0.0)
    except Exception as e:
        print "Exception caught in function getConfidence"


def performProcess(img):
    fileName = base_path + getTimeStamp() + ".jpg"
    cv2.imwrite(fileName, img)
    imgContent = getImageContent(fileName)

    faceId, detectStatus = faceDetectOctetStream(imgContent, subscription_key)
    if (detectStatus == 0):
        print "Face Not Detected in this pic\n\n\n"
        return
    data, similarityStatus = faceSimilarity(faceId, faceListId, 1, subscription_key)
    if (similarityStatus == 0):
        print "Error with Similarity Status Function\n\n\n"
        return
    persistedId, confidence = getConfidence(data)
    # print "Confidence", confidence
    if (float(confidence) > 0.50):
        print "Match Found"
        #Adding this face to our dataset as well
        updatedPersistedId, addStatus = addFaceToListOctetStream(imgContent, faceListId, subscription_key)
        if(addStatus == 0):
            print "Error in Adding\n\n\n"
            return
        userPID = persistedIdHash[persistedId]
        pidHash[userPID].append(updatedPersistedId)
        timeStampHash[userPID].append(getTimeStamp())
        persistedIdHash[updatedPersistedId] = userPID
        # print pidHash
        # print persistedIdHash
        # print timeStampHash
        print "Number of times of visits: ", len(timeStampHash[userPID])
        print "Last Visit Timing: ", timeStampHash[userPID][-2]
        print "Reward Points for visiting Us: $", random.randint(1,9)
        print "Gift for you this week: ", random.choice(giftList)
        print "\n\n\n"
        pickle.dump(pidHash, open("C:\Users\deku\Downloads\pidHash", "wb"))
        pickle.dump(persistedIdHash, open("C:\Users\deku\Downloads\persistedIdHash", "wb"))
        pickle.dump(timeStampHash, open("C:\Users\deku\Downloads\stamptime", "wb"))

    else:
        print "No Match Found"
        PID = getRandomString()
        updatedPersistedId, addStatus = addFaceToListOctetStream(imgContent, faceListId, subscription_key)
        if(addStatus == 0):
            print "Error in Adding"
            return
        newList = []
        newList.append(updatedPersistedId)
        pidHash[PID] = newList
        timeStampHash[PID] = [getTimeStamp()]
        persistedIdHash[updatedPersistedId] = PID
        print "New Customer / Unknown Customer"
        print "Visit Us Again"
        print "\n\n\n"
        # print pidHash
        # print persistedIdHash
        # print timeStampHash
        pickle.dump(pidHash, open("C:\Users\deku\Downloads\pidHash", "wb"))
        pickle.dump(persistedIdHash, open("C:\Users\deku\Downloads\persistedIdHash", "wb"))
        pickle.dump(timeStampHash, open("C:\Users\deku\Downloads\stamptime", "wb"))










createFaceList(faceListId, subscription_key)
fileName = "C:\Users\deku\Downloads\sallu3.jpg"
with open(fileName, "rb") as f:
    content = f.read()
faceId, detectStatus = faceDetectOctetStream(content, subscription_key)
print(addFaceToListOctetStream(content, faceListId, subscription_key))
print "\n\n\n"



cap = cv2.VideoCapture(1)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Display the resulting frame
    cv2.imshow('DisplayWindow', frame)
    if cv2.waitKey(1) & 0xFF == ord('y'):
        performProcess(frame)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()










# cam = initialize()
# fileName = "C:\Users\deku\Downloads\CamPics\pic" + getTimeStamp() + ".jpg"
# captureImage(cam, fileName)



# fileName = "C:\Users\deku\Downloads\CamPics\pic2016_07_27_16_15_22.jpg"
# fileName = "C:\Users\deku\Downloads\myPic.jpg"
# createFaceList("mytestlist007", subscription_key)
# with open(fileName, "rb") as f:
#     content = f.read()


### TESTING FUNCTIONS #####
# createFaceList("mytestlist008", subscription_key)

# facesToAdd = ["amir1", "amir3", "amir4", "sallu1", "sallu2", "sallu3", "shah1", "shah2", "shah3"]
# for face in facesToAdd:
#     nameFile = "C:\Users\deku\Downloads\set\\" + face + ".jpg"
#     with open(nameFile, "rb") as f:
#         content = f.read()
#     print(addFaceToListOctetStream(content, "mytestlist008", subscription_key))


# nameFile = "C:\Users\deku\Downloads\set\\amir2.png"
# with open(nameFile, "rb") as f:
#     content = f.read()
# faceId = faceDetectOctetStream(content, subscription_key)
# print(faceSimilarity(faceId, "mytestlist008", 3, subscription_key))


# faceId = faceDetectOctetStream(content, subscription_key)
# print(faceSimilarity(faceId, "mytestlist007", 2, subscription_key))
# addFaceToListOctetStream(content, "mytestlist007", subscription_key)
# print(faceDetectOctetStream(content, subscription_key))





