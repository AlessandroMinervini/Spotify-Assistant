import os,sys
import numpy
import cv2
import face_recognition
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import *

class Face_Thread(QThread):
    reco = pyqtSignal(str)
    #unreco = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.active = False
        # Get a reference to webcam #0 (the default one)
        self.known_face_encodings,self.known_face_names = self.make_encoding()

    def run(self):
        video_capture = cv2.VideoCapture(0)

        try:
            while self.active:
                # Grab a single frame of video
                ret, frame = video_capture.read()

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_frame = frame[:, :, ::-1]

                # Find all the faces and face enqcodings in the frame of video
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                # Loop through each face in this frame of video
                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)

                    name = "Unknown"

                    # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = self.known_face_names[first_match_index]

                    # Draw a box around the face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                    # Draw a label with a name below the face
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                    if (name != "Unknown"):
                        self.reco.emit(name)
                        self.deactivate()
                        video_capture.release()
                        cv2.destroyAllWindows()
                        break
                    else:
                        #self.unreco.emit()
                        self.deactivate()
                        video_capture.release()
                        cv2.destroyAllWindows()
                        break
                # Display the resulting image
                # cv2.imshow('Video', frame)
                # Hit 'q' on the keyboard to quit!
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except:
            print("error while recognize")

    def deactivate(self):
        """Method called to stop and deactivate the face recognition Thread"""
        self.active = False
        self.quit()
        if self.isRunning():
            self.quit()

    def face_rec_loop(self):
        try:
            self.active = True
            self.known_face_encodings, self.known_face_names = self.make_encoding()
            self.start()
        except:
            print('')

    def make_encoding(self):
        import os
        root, dirs, files = next(os.walk('spotyPeople'))
        person_encoding=[]
        person_name=[]
        for file in files:
            try:
                person_image = face_recognition.load_image_file('spotyPeople/'+file)
                person_face_encoding = face_recognition.face_encodings(person_image)[0]
                person_encoding.append(person_face_encoding)
                name = file.split('.')
                person_name.append(name[0])
            except:
                print('')
        return person_encoding, person_name

