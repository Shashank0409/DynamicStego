from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import base64

class AES:

    @staticmethod
    def encrypt(data):
        # Generate a random 256-bit key and 128-bit initialization vector.
        key = os.urandom(32)
        iv = os.urandom(16)

        # Create a new AES-CBC cipher object with the given key and IV.
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Pad the data to a multiple of the block size.
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()

        # Encrypt the padded data.
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        encoded_key = base64.b64encode(key).decode('utf-8')
        return (iv + encrypted_data,encoded_key)
        
    @staticmethod
    def decrypt(encrypted_data, key):
        # Extract IV and ciphertext
        key = base64.b64decode(key)
        iv = encrypted_data[:16]  # First 16 bytes are the IV
        ciphertext = encrypted_data[16:]  # Remaining bytes are the ciphertext

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt and remove PKCS7 padding
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(padded_data) + unpadder.finalize()
        return decrypted_data

'''
def sample_aes_encryption():
    compressed_text = b"This is a compressed text string example."

    # Encrypt the compressed text (returns IV + ciphertext)
    encrypted_data,aes_key = AES.encrypt(compressed_text)
    print("Encrypted Data (IV + Ciphertext):", encrypted_data,'\n')
    print("AES Key:", aes_key,'\n')

    # Decrypt the encrypted data
    decrypted_text = AES.decrypt(encrypted_data, aes_key)
    print("Decrypted Text:", decrypted_text,'\n')

    # Ensure the original and decrypted text match
    assert compressed_text == decrypted_text, "Decryption failed!"
    print("\nDecryption successful! The original and decrypted text match.")


sample_aes_encryption()
'''