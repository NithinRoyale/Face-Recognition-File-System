# Face-Activated File Encryption and Decryption System

## Overview

This project is a comprehensive security solution that integrates facial recognition with file encryption and decryption. It is designed to secure sensitive data by automatically encrypting or decrypting files based on the identity of detected faces using a webcam.

## Key Components

### 1. Facial Recognition System

- **Objective**: Identify and authenticate users based on facial features.
- **Technology**: Utilizes the `face_recognition` library to detect and encode facial features. The system captures images from a webcam, compares detected faces against a database of known faces, and identifies users.
- **Features**:
  - Loads and encodes facial images from a specified directory.
  - Detects and recognizes faces in real-time using a webcam.
  - Flags new or previously unrecognized faces.

### 2. File Encryption and Decryption

- **Objective**: Protect files by encrypting them for authorized users and decrypting them upon recognition.
- **Technology**: Employs the `cryptography` library to encrypt and decrypt files using the Fernet symmetric encryption algorithm.
- **Features**:
  - **Encryption**: Encrypts files stored in a designated folder using a unique key associated with each user.
  - **Decryption**: Decrypts files when the authorized user is detected.
  - **Key Management**: Stores encryption keys securely and utilizes them for both encryption and decryption processes.

## Workflow

1. **Initialization**:
   - Loads facial encodings for authorized users from specified image paths.
   - Sets up a webcam feed for real-time face detection.

2. **Real-Time Face Detection**:
   - Captures video frames and processes them to identify faces.
   - Compares detected faces against the stored encodings to recognize users.
   - If a known face is detected, the system decrypts the corresponding user’s files; if an unknown face is detected, it triggers an alert and terminates the session.

3. **File Management**:
   - **Encryption**: Encrypts files in a user-specific directory upon recognition of a new authorized user.
   - **Decryption**: Decrypts files when the authorized user is detected again.

4. **Security Measures**:
   - Ensures data protection by encrypting files associated with detected users.
   - Utilizes key-based encryption to manage access to sensitive files.

## Tools

Python 3.x
face_recognition
opencv-python
cryptography
git
GitHub (or similar platform)
Webcam
Code Editor (e.g., Visual Studio Code, PyCharm)

## Applications

- **Secure Data Access**: Provides a layer of security for accessing sensitive files based on user authentication.
- **Automated Security**: Enhances security by automating the encryption and decryption process based on real-time facial recognition.

## Future Enhancements

- **Scalability**: Extend support for multiple users and integrate with larger databases.
- **Improved Accuracy**: Enhance facial recognition accuracy and reduce false positives/negatives.
- **Additional Security Features**: Incorporate additional authentication methods and encryption algorithms for increased security.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install face_recognition cryptography opencv-python

## Contributors

- [Nithin](https://github.com/NithinRoyale/)