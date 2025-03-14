from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64

class ChaCha20:

    @staticmethod
    def encrypt(data):
        key = os.urandom(32)  # generate a random 256-bit key
        nonce = os.urandom(16)  # ChaCha20 requires a 128-bit nonce

        chacha = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
        encryptor = chacha.encryptor()
        encrypted_data = encryptor.update(data) + encryptor.finalize()
        encoded_key = base64.b64encode(key).decode('utf-8')
        return (nonce + encrypted_data, encoded_key)  

    @staticmethod
    def decrypt(encrypted_data, key):
        # Extract nonce and ciphertext
        key = base64.b64decode(key)
        nonce = encrypted_data[:16]  # First 16 bytes are the nonce
        ciphertext = encrypted_data[16:]  # Remaining bytes are the ciphertext

        chacha = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
        decryptor = chacha.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()

'''
def sample_chacha20_encryption():
    # Example usage
    compressed_text = b"This is a compressed text string example."

    chacha20=ChaCha20()
    # Encrypt the compressed text (returns nonce + ciphertext)
    encrypted_data, chacha_key = ChaCha20.encrypt(compressed_text)
    print("Encrypted Data (Nonce + Ciphertext):", encrypted_data,'\n')
    print("ChaCha20 Key:", chacha_key,'\n')

    # Decrypt the encrypted data
    decrypted_text = ChaCha20.decrypt(encrypted_data, chacha_key)
    print("Decrypted Text:", decrypted_text,  '\n')

    # Ensure the original and decrypted text match
    assert compressed_text == decrypted_text, "Decryption failed!"
    print("\nDecryption successful! The original and decrypted text match.")

sample_chacha20_encryption()
'''