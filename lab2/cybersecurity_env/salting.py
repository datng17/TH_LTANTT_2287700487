import os 
import hashlib
def hash_with_salt(data):
    salt = os.urandom(16)  # Tạo một salt ngẫu nhiên
    hasher = hashlib.pbkdf2_hmac('sha256', data.encode(), salt, 100000)
    return salt + hasher
print("Hash with salt:", hash_with_salt("secure_password"))