import os
import shutil
from cryptography.fernet import Fernet
import base64
import hashlib
import json
import sys




def main(argv):
    FPath = argv[1]
    for item in os.listdir(FPath):
        s = os.path.join(FPath, item)
        if not s.endswith(".calc"):
            print(f'file: {s} is not encrypted')
        elif s.endswith("DS_Store") or s.endswith("DS_Store.calc"):
            print(f'file: {s} is not encrypted')
        else:
            with open(s ,'r') as EncrypedFile:
                FContent = EncrypedFile.read()
            ParsedContent = json.loads(FContent)
            BS64FileContent = ParsedContent["filecontents"]
            DecodedFileBS64 = DecodeContentBS64(BS64FileContent)
            DecryptedFile = DecryptData(DecodedFileBS64)
            with open(s, 'w')as ReadyToDecrypt:
                ReadyToDecrypt.write(DecryptedFile)
            os.rename(s,s.rpartition('.')[0])
            print(f'Data is Decrypted')
            
            


def DecodeContentBS64(file):
    decoded_content = base64.b64decode(file)
    return decoded_content
    

def DecryptData(decoded_data):
    with open(keyFile, 'rb') as filekey:
        key = filekey.read()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(decoded_data).decode()
    return decrypted
    



if __name__=="__main__":
    if len(sys.argv) != 3:
        print(50 * "-")
        print("ERROR: Incorrect number of arguments!")
        print("Enter the correct path to decrypt and the path+filename for the decryption key.")
        print("Example: python3 ProjectP1.py /Users/kb/test/ /Users/bk/TestKey/KEY.txt")
        print(50 * "-")
        sys.exit(1)
    
    keyFile = sys.argv[2]
    print(f"Encryption Key File: {keyFile}")
    print(f"Target Directory: {sys.argv[1]}")
    main(sys.argv)