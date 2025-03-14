from aes_ed import AES
from chacha20_ed import ChaCha20
import random

class Encryption:
    def __init__(self):
        self.algorithms = {
            "00": AES,
            "01": ChaCha20
        }

    #Returns encrypted data and encyption code and key
    def encrypt(self, data):
        #chooses a random algorithm and encrypt the data
        encryption_code=random.choice(tuple(self.algorithms.keys()))
        encrypted_data, key=self.algorithms[encryption_code].encrypt(data)

        return encrypted_data, encryption_code, key

    #Return decrypted data
    def decrypt(self, encrypted_data, encryption_code, key):
        decrypted_data=self.algorithms[encryption_code].decrypt(encrypted_data, key)
        return decrypted_data

'''
def sample_encryption():
    encryption_module = Encryption()

    data = b"This is a compressed text string example."
    
    encrypted_data, encryption_code, key = encryption_module.encrypt(data)
    print(f"Encrypted data: {encrypted_data}\n")
    print(f"Encryption code: {encryption_code}\n")
    print(f"key: {key}\n")

    decrypted_data=encryption_module.decrypt(encrypted_data, encryption_code, key)
    print(f"Decrypted data: {decrypted_data}\n")

sample_encryption()
'''