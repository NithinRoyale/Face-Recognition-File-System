import cv2
import os
import glob
import numpy as np
import face_recognition
# import serial
   
# ser = serial.Serial('COM6', 9600, timeout=1)
   
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
    
  
# Initialize the SimpleFacerec instance
sfr = SimpleFacerec()
  
# Load known face encodings
sfr.load_encoding_images("images")
  
# Define the base folder where the authorized folders are located
# Replace with the actual path to the base folder
base_folder = "C:\psg\college-project\iot\source-code-face-recognition\source code\sample"
   
# Load Camera
cap = cv2.VideoCapture(0)
   
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
            # Access the folder for authorized persons
            authorized_folder = os.path.join(base_folder, name)
            # ser.write(b'1')
            if os.path.exists(authorized_folder):
                files = os.listdir(authorized_folder)
                print(f"Accessing folder for {name}: {files}")
                # You can perform any desired operations on the folder here
    
            else:
                print(f"Folder for {name} does not exist.")    
   
        # Print information every time an unknown face is detected
        if new_face_detected and name == "Unknown":
            print("Unknown face detected.")
            # ser.write(b'2')
    
    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
   
cap.release()
cv2.destroyAllWindows()
  