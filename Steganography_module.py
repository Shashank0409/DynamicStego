import pydub
import numpy as np

class Audio_Steganography:
    
    #Saves the result audio file at save_at location
    @staticmethod
    def steganography(input_audio_location, message, save_at):
        # Load the audio file
        audio = pydub.AudioSegment.from_file(input_audio_location)
        audio_samples = np.array(audio.get_array_of_samples())
        
        # Embed the message length (4 bytes, 32-bit integer)
        message_length = len(message).to_bytes(4, byteorder='big')
        full_message = message_length + message  # Prepend length to the message

        # Convert the message to a binary string
        binary_message = ''.join(format(byte, '08b') for byte in full_message)
        
        # Embed the message in the least significant bit (LSB)
        for i in range(len(binary_message)):
            audio_samples[i] = (audio_samples[i] & ~1) | int(binary_message[i])
        
        # Save the stego audio
        stego_audio = audio._spawn(audio_samples.tobytes())
        stego_audio.export(save_at, format="wav")

    @staticmethod
    def desteganography(input_audio_location):
        # Load the stego audio
        stego_audio = pydub.AudioSegment.from_file(input_audio_location)
        audio_samples = np.array(stego_audio.get_array_of_samples())

        # Extract the first 32 bits for the message length
        binary_length = ''.join(str(audio_samples[i] & 1) for i in range(32))
        message_length = int(binary_length, 2)

        # Extract the remaining bits for the message
        binary_message = ''.join(str(audio_samples[i] & 1) for i in range(32, 32 + message_length * 8))
        binary_bytes = [binary_message[i:i + 8] for i in range(0, len(binary_message), 8)]
        extracted_message = bytes([int(byte, 2) for byte in binary_bytes])

        return extracted_message

'''
def sample_steganography():

    # Test data (binary payloads as example)
    message_to_embed = b"This is an encrypted message"

    # Path to your input audio file
    audio_file = "audio.wav"  # Replace this with your actual audio file
    save_at= "stego_audio.wav"     
    audio_steg=Audio_Steganography()
    # Perform audio steganography with the example audio and message
    Audio_Steganography.steganography(audio_file, message_to_embed, save_at)

    print("\noriginal msg: ",message_to_embed,"\n")
    # Perform audio de-steganography to extract the hidden message
    extracted_msg=Audio_Steganography.desteganography(save_at)
    print("extracted msg: ",extracted_msg,"\n")
    print(message_to_embed==extracted_msg)

sample_steganography()
'''