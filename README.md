## Enhanced Audio Steganography using Dynamic Compression and Encryption

## Overview
This project implements an advanced **audio steganography system** that securely hides data within audio files using a combination of **LSB-based steganography, modern encryption (AES-256 & ChaCha20), and lossless compression techniques (Zstandard, Brotli, LZMA, Bzip2)** with **random algorithm selection** for enhanced security. The system ensures **high security, efficient data hiding, and adaptability** for real-world applications like **secure communication and watermarking**.  

## Features
- **Strong Encryption:** AES-256 & ChaCha20 ensure data confidentiality.  
- **Lossless Compression:** Multiple compression algorithms optimize storage and transmission.  
- **LSB-based Steganography:** Ensures imperceptibility of hidden data.  
- **Random Key Generation:** Each session uses a unique encryption key. 
- **Random Algorithm Selection:** Each session uses a different random combination of compression and encryption algorithms.
- **Modular Design:** Independent components for encryption, compression, and steganography.

1. Clone the repository:
   ```bash
   git clone https://github.com/Shashank0409/DynamicStego.git
   cd DynamicStego
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the main script:
   ```bash
   python Start.py
   ```

## Usage
1. **Embedding a Secret Message**
   - Input an audio file and a secret message.
   - The system compresses and encrypts the message.
   - The encrypted message is embedded into the audio file.
   - The output is a stego-audio file and a secret key.
   - The secret key can be shared via email directly from the system or saved as a text file and shared through another channel.

2. **Extracting a Hidden Message**
   - Input the stego-audio file and the secret key.
   - The system extracts the hidden data, decrypts, and decompresses it.
   - The original secret message is retrieved.

## Dependencies
Ensure Python 3.8+ is installed and install the dependencies using:
```bash
pip install -r requirements.txt
```

## **Technologies Used**  
- **Python** (Core development)  
- **Cryptography Library** (AES-256 & ChaCha20)  
- **Zstandard, Brotli, LZMA, Bzip2** (Compression)  
- **PyAudio & Pydub** (Audio processing)  
- **CustomTkinter** (GUI for user-friendly interaction)  

📌 **Use Cases:** Secure messaging, watermarking, data protection, and confidential communication. 
