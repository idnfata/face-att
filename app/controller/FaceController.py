from app import response, app
from flask import request, jsonify, abort
import cv2, os, fnmatch, base64, numpy as np
import json
from PIL import Image
from io import BytesIO


# Convert Base64 to Image
def b64_2_img(data):
    buff = BytesIO(base64.b64decode(data))
    return Image.open(buff)

def isUserHasFaceStored(client_id, employee_id):
    faceDirOfClient = 'facedata/' + str(client_id)
    if os.path.exists(faceDirOfClient): # masuk ke direktori data wajah milik client
        allImages = os.listdir(faceDirOfClient) #dapatkan semua path file yang ada di folder tersebut
        # dapatkan file dengan awalan employee_id dan berekstensi .jpg
        imagePaths = [os.path.join(faceDirOfClient,f) for f in allImages if f.startswith(employee_id) and f.endswith('.jpg')] 
        if not imagePaths : # jika kosong
            return response.NotFound('Data wajah tidak ditemukan.')
        else :
            # print(imagePaths)
            return response.success('Data wajah ditemukan.')
    else:
        # return 'folder clientID tidak ada'
        return response.NotFound('Data wajah tidak ditemukan. Folder ClientID tidak ada.')

def detectFace(img, client_id):
    faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faceRecognizer = cv2.face.LBPHFaceRecognizer_create()

    trainedFace = 'facetrained/' + str(client_id) + '/training.xml'
    if not os.path.exists(trainedFace):
        faceID = -1
        confidenceTxt = ""
        return faceID, confidenceTxt
        
    faceRecognizer.read(trainedFace)
    font = cv2.FONT_HERSHEY_SIMPLEX

    id = 0
    
    # names = ["Tidak diketahui", "Fatahillah Ibrahim", "Najmi Oktavia"]

    img_array = np.array(img) 
    face = faceDetector.detectMultiScale(img_array, scaleFactor=1.03, minNeighbors=5)
    for (x, y, w, h) in face:
        square = cv2.rectangle(img_array, (x, y), (x + w, y + h), (255, 255, 0), 5)
        id, confidence = faceRecognizer.predict(img_array[y:y+h, x:x+w]) # confidence = 0, artinya wajah sesuai/cocok
        # print(id)
        # print(confidence)
        if confidence <= 52 :
            # faceID = names[id]
            faceID = id
            confidenceTxt = "{0}%".format(round(100-confidence))
        else:
            # faceID = names[0]
            faceID = 0
            confidenceTxt = "{0}%".format(round(100-confidence))
    
    # memberikan label di gambar
    # cv2.putText(img_array, str(faceID), (x+5, y-15), font, 1, (255,255,0), 8)
    # cv2.putText(img_array, str(confidenceTxt), (x+15, y+h-15), font, 1, (255,255,0), 8)

    # cv2.imwrite('hasil.jpg', img_array)
    # hasil = Image.open('hasil.jpg')

    return faceID, confidenceTxt
    

def recogFace(client_id, employee_id, face):
    face = b64_2_img(face).convert('L')
    faceID, confidenceTxt = detectFace(face, client_id) 
    if faceID == 0: 
        return response.NotFound("Wajah tidak dikenali")
    elif faceID == -1: #jika file training tidak ditemukan
        return response.NotFound("File hasil training data wajah tidak ditemukan.") 
    else:
        if int(employee_id) != faceID: #jika wajah yang dikirim bukan wajah asli
            return response.Unauthorized("Bukan wajah dari ID karyawan {0}. Tapi wajah ID karyawan {1}".format(employee_id, faceID))
        else: #jika sesuai
            return response.success("Data wajah sesuai dengan tingkat kemiripan {0}".format(confidenceTxt))


def recognizeFace():
    data = request.get_json()
    client_id = str(data['client_id'])
    employee_id = data['employee_id'] 

     #face data, str base64 image
    face = b64_2_img(data['face']).convert('L')
    faceID, confidenceTxt = detectFace(face, client_id)
    if faceID == 0: 
        return response.NotFound("Wajah tidak dikenali")
    elif faceID == -1: #jika file training tidak ditemukan
        return response.NotFound("File hasil training data wajah tidak ditemukan.") 
    else:
        if employee_id != faceID: #jika wajah yang dikirim bukan wajah asli
            return response.Unauthorized("Bukan wajah dari ID karyawan {0}. Tapi wajah ID karyawan {1}".format(employee_id, faceID))
        else: #jika sesuai
            return response.success("Data wajah sesuai dengan tingkat kemiripan {0}".format(confidenceTxt))


def saveAttFace(client_id, employee_id, date, att_type, in_or_out, face):
    date = date.split("-")
    tahunBulan = date[0]+'-'+ date[1]
    tanggal = date[2]
    faceDirOfClient = 'faceattendances/' + str(client_id) + '/' + att_type + '/' + tahunBulan

    os.makedirs(faceDirOfClient, exist_ok=True)
    img = b64_2_img(face)
    img.save(faceDirOfClient+'/'+str(in_or_out)+'_'+str(tanggal)+'_'+str(employee_id)+'.jpg', 'JPEG')
    return

def saveFace():
    data = request.get_json()
    client_id = str(data['client_id'])
    employee_id = data['employee_id'] 
    faces = data['faces'] #list data of base64 images
    faceDirOfClient = 'facedata/' + client_id
    os.makedirs(faceDirOfClient, exist_ok=True)

    no = 1
    for i in faces:
        #ubah semua base64 ke file image dan ubah jadi grey
        img = b64_2_img(i).convert('L')
        img.save(faceDirOfClient+'/'+str(employee_id)+'_'+str(no)+'.jpg', 'JPEG')
        no += 1
    
    trainFace(client_id)
    return response.success("Berhasil simpan & latih data wajah")
    

def getImageLabel(client_id):
    faceDirOfClient = 'facedata/' + client_id
    faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

     #dapatkan semua file gambar yang ada di faceDirOfClient
    allImages = os.listdir(faceDirOfClient) 
    # dapatkan file berekstensi .jpg
    imagePaths = [os.path.join(faceDirOfClient,f) for f in allImages if f.endswith('.jpg')] 
    faceSamples = []
    faceIDs = []
    for imagePath in imagePaths:
        PILImg = Image.open(imagePath).convert("L")
        imgNum = np.array(PILImg, 'uint8')
        faceID = os.path.split(imagePath)[-1].split('_')[0] #identitasnya itu employee_id
        faces = faceDetector.detectMultiScale(imgNum)
        for (x,y,w,h) in faces :
            faceSamples.append(imgNum[y:y+h, x:x+w])
            faceIDs.append(int(faceID))
    return faceSamples, faceIDs

def trainFace(client_id):
    faceRecognizer = cv2.face.LBPHFaceRecognizer_create()

    trainedFaceDirOfClient = 'facetrained/' + client_id
    os.makedirs(trainedFaceDirOfClient, exist_ok=True)

    print("Mesin sedang melakukan training data wajah.... Tunggu dalam beberapa detik.")

    faces, IDs = getImageLabel(client_id)
    faceRecognizer.train(faces, np.array(IDs))
    #simpan
    faceRecognizer.write(trainedFaceDirOfClient + '/training.xml')
    print("Sebanyak {0} data wajah telah ditrainingkan ke mesin.".format(len(np.unique(IDs))))

    