import cv2
import os
import glob
import numpy as np
import face_recognition
# import serial
import atexit
from cryptography.fernet import Fernet

# ser = serial.Serial('COM6', 9600, timeout=1)

# Key : [Path,Encryption]
DetailDict = {"Nithin": [r"C:\psg\college-project\iot\source-code-face-recognition\source code\images\Nithin.jpeg", r'IXc_TOPeqQFwl2Q3hC4sJIPpW586Uiv-R4GVXcVP68c='],
              'RishiKhanna': [r'C:\psg\college-project\iot\source-code-face-recognition\source code\Folders\RishiKhanna', r'-4Ra1RuIvdI5MaQwFtG3qfOc4wAqgMA0bVeV41dlAmI=']}

DetectedFace = ''


class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.frame_resizing = 0.25
        self.detected_faces = set()  # To keep track of detected faces

    def load_encoding_images(self, images_path):
        # Load Images
        images_path = glob.glob(os.path.join(images_path, "*.*"))

        print("{} encoding images found.".format(len(images_path)))

        # Store image encoding and names
        for img_path in images_path:
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Get the filename only from the initial file path.
            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)
            # Get encoding
            img_encoding = face_recognition.face_encodings(rgb_img)[0]

            # Store file name and file encoding
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)
        print("Encoding images loaded")

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(
            frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        # Find all the faces and face encodings in the current frame of video
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

        face_names = []
        new_face_detected = False  # Initialize a flag for new face detection

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(
                self.known_face_encodings, face_encoding)
            name = "Unknown"

            if self.known_face_encodings:  # Check if known_face_encodings is not empty
                face_distances = face_recognition.face_distance(
                    self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
            face_names.append(name)

            # Check if the face is new and hasn't been detected before
            if name not in self.detected_faces:
                new_face_detected = True
                # Add to the set to indicate that the face has been detected
                self.detected_faces.add(name)

        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names, new_face_detected


def on_exit_handler():
    if DetectedFace != '':
        EncrytFiles(DetectedFace)


def DecrytFiles(NameOfOwner):

    folder_path = DetailDict[NameOfOwner][0]
    key = DetailDict[NameOfOwner][1]

    cipher_suite = Fernet(key)

    # Walk through the folder and decrypt its contents
    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)

            with open(file_path, "rb") as file:
                file_data = file.read()
                decrypted_data = cipher_suite.decrypt(file_data)

            with open(file_path, "wb") as file:
                file.write(decrypted_data)

    print("Folder decrypted successfully.")


def EncrytFiles(NameOfOwner):

    folder_path = DetailDict[NameOfOwner][0]
    key = DetailDict[NameOfOwner][1]

    cipher_suite = Fernet(key)

    # Walk through the folder and encrypt its contents
    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)

            with open(file_path, "rb") as file:
                file_data = file.read()
                encrypted_data = cipher_suite.encrypt(file_data)

            with open(file_path, "wb") as file:
                file.write(encrypted_data)

    print("Folder encrypted successfully.")


# Initialize the SimpleFacerec instance
sfr = SimpleFacerec()

# Load known face encodings
sfr.load_encoding_images("images")

# Load Camera
cap = cv2.VideoCapture(0)

# Registering on exit handler
atexit.register(on_exit_handler)

bflag = False

while True:
    ret, frame = cap.read()

    # Detect Faces and check for new face detection
    face_locations, face_names, new_face_detected = sfr.detect_known_faces(
        frame)

    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        cv2.putText(frame, name, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        if new_face_detected and name != "Unknown":
            if bflag and name != DetectedFace:
                print("Another Authorized user detected, closing...")
                # ser.write(b'2')
                exit()
            if os.path.exists(DetailDict[name][0]) and not bflag:
                bflag = True
                DetectedFace = name
                print("Decryting contents of the folder")
                DecrytFiles(name)
                # ser.write(b'1')

        # Print information every time an unknown face is detected
        if new_face_detected and name == "Unknown":
            print("Unknown face detected, Closing Immediately")
            # ser.write(b'2')
            exit()

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
