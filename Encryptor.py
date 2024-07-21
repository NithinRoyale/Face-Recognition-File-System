from cryptography.fernet import Fernet
import os

# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet('-4Ra1RuIvdI5MaQwFtG3qfOc4wAqgMA0bVeV41dlAmI=')

# Path to the folder you want to encrypt
folder_path = r"C:\psg\college-project\iot\source-code-face-recognition\source code\Folders\RishiKhanna"

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