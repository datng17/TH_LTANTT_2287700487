import hashlib
def hash_string(data):
    return hashlib.sha256(data.encode()).hexdigest()
input_data = "secure_password"   
hashed_data = hash_string(input_data)
print(f"Original Data: {input_data}")
print(f"SHA-256 Hash: {hashed_data}")
#thêm chức năng so sánh hash
def verify_hash(data, hash):
    return hash_string(data) == hash
correct_data = "secure_password"
incorrect_data = "wrong_password"
print("Verification (correct): ",verify_hash(correct_data, hashed_data)) 
print("Verification (incorrect): ",verify_hash(incorrect_data, hashed_data))

def hash_file(file_path):
    hasher = hashlib.sha256()
    with open(file_path,'rb') as file:
        while chunk :=file.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()
file_hash = hash_file(r"e:\DEMO-ANTT\lab2\cybersecurity_env\sample.txt")
print (f"File_Hash: {file_hash}")

def hash_string_md5(data):
    return hashlib.md5(data.encode()).hexdigest()
def hash_string_sha1(data):
    return hashlib.sha1(data.encode()).hexdigest()
print(f"MD5 hash: {hash_string_md5(input_data)}")
print(f"SHA-1 hash: {hash_string_sha1(input_data)}")