import face_recognition
import pickle
if __name__!="__main__":
    from .camera import WebCamVideoStream
from itertools import chain
import cv2
import numpy as np

def compare_encoding(image,authorized_encodings):
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    result=[]
    for encoding in authorized_encodings:
        result.append(face_recognition.compare_faces(encoding,face_encodings))
    return np.argmax(np.bincount(list(chain(*result))))

def create_encoding(image_bytes,path):
    authorized_encodings=[]
    for image in image_bytes:
        # Convert the image to RGB if needed
        # image_rgb = image.convert("RGB").tobytes()
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        authorized_encodings.extend(face_encodings)
    save_encoding(authorized_encodings)

def load_authorized_encoding(encoding_file_path):
    try:
        with open(encoding_file_path, 'rb') as file:
            authorized_face_encodings = pickle.load(file)
        return authorized_face_encodings
    except FileNotFoundError:
        print("File not found. No authorized face encodings loaded.")
        return []

def save_encoding(authorized_encodings):
    with open("/Users/abirallamsal/ai/users.txt", 'wb') as file:
        pickle.dump(authorized_encodings,file)

def take_register_user():
    stream=WebCamVideoStream()
    image_frames=[]
    for i in range(100):
        print(i)
        rgb_frame = cv2.cvtColor(stream.read_frame(), cv2.COLOR_BGR2RGB)
        image_frames.append(rgb_frame)
    create_encoding(image_frames,"users.pk1")

def compare_face():
    stream=WebCamVideoStream()    
    authorized_encoding=load_authorized_encoding("/Users/abirallamsal/ai/users.txt")
    rgb_frame = cv2.cvtColor(stream.read_frame(), cv2.COLOR_BGR2RGB)
    return compare_encoding(rgb_frame,authorized_encoding)


if __name__=="__main__":
    from camera import WebCamVideoStream
    print(take_register_user())