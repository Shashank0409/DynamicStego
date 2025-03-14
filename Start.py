from customtkinter import *
from typing import Any
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import wave
import pyaudio
import threading
import os
import time
from pathlib import Path
import subprocess
import random
import string
from datetime import datetime

from Compression_module import Compression
from Encryption_module import Encryption
from Steganography_module import Audio_Steganography
from darkdetect import theme
from Key_Exchange import send_email_with_attachment
from matplotlib.pyplot import autoscale

# Initialize customtkinter appearance
set_appearance_mode("dark" if theme() == "Dark" else "light")
set_default_color_theme("blue")

# Get the Downloads folder
DOWNLOADS_PATH = str(Path.home() / "Downloads")

# Global variable for audio file path
audio_file_path = None
recording = False

class MainModule:
    def __init__(self):
        self.compressor = Compression()
        self.encrypter = Encryption()
        filename = ''.join(random.choices(string.digits, k=10)) + '.wav'
        self.save_at_location = Path.home() / 'Downloads' / filename

    def embed(self, audio_file_location, message):
        message = message.encode()
        messagebox.showinfo("Step 1", f"Encoding the message")

        compressed_message, compression_code = self.compressor.compressor(message)
        messagebox.showinfo("Step 2", f"Compressing the message. Compression code chosen is {compression_code}")

        encrypted_message, encryption_code, encryption_key = self.encrypter.encrypt(compressed_message)
        messagebox.showinfo("Step 3", f"Encrypting the message. Encryption code chosen is {encryption_code}")

        Audio_Steganography.steganography(audio_file_location, encrypted_message, self.save_at_location)
        messagebox.showinfo("Success", f"Steganography completed successfully\nFile saved at: {self.save_at_location}")
        return compression_code + encryption_code + encryption_key

    def extract(self, audio_file_location, key):
        if len(key) < 6:  # Ensure key is long enough
            raise ValueError("Invalid key length.")

        messagebox.showinfo("Step 1", f"Performing desteganography on the audio")

        encrypted_message = Audio_Steganography.desteganography(audio_file_location)
        compression_code, encryption_code, encryption_key = key[:2], key[2:4], key[4:]

        decrypted_message = self.encrypter.decrypt(encrypted_message, encryption_code, encryption_key)
        messagebox.showinfo("Step 2", f"Decrypting the message using Encryption code {encryption_code}")

        message = self.compressor.decompressor(decrypted_message, compression_code)
        messagebox.showinfo("Step 3", f"Decompressing the message using Compression code {compression_code}")
        return message.decode()

def record_audio():
    global audio_file_path, recording
    def record():
        global audio_file_path, recording
        chunk: Any = 1024
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 44100
        filename = "recorded_audio.wav"
        audio_file_path = os.path.join(DOWNLOADS_PATH, filename)

        p = pyaudio.PyAudio()

        try:
            stream = p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize recording: {e}")
            p.terminate()
            return
        frames = []
        max_seconds = 300
        recording = True

        def update_timer():
            elapsed_time = 0
            while recording and elapsed_time < max_seconds:
                timer_label.configure(text=f"Recording: {elapsed_time}s")
                for _ in range(10):
                    if not recording:
                        timer_label.configure(text="Recording stopped.")
                        return
                    time.sleep(0.1)
                elapsed_time += 1
            stop_recording()
            timer_label.configure(text="Recording stopped.")

        threading.Thread(target=update_timer, daemon=True).start()

        try:
            while recording:
                data = stream.read(chunk)
                frames.append(data)
                if len(frames) >= (rate // chunk) * max_seconds:  # Stop after max_seconds
                    break
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during recording: {e}")
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
            recording = False

            with wave.open(audio_file_path, 'wb') as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(p.get_sample_size(audio_format))
                wf.setframerate(rate)
                wf.writeframes(b''.join(frames))

            messagebox.showinfo("Recording Saved", f"Audio recorded and saved to: {audio_file_path}")
            update_audio_display(audio_file_path)

    threading.Thread(target=record).start()

def stop_recording():
    global recording
    if recording:  # Check if recording is in progress
        recording = False

def play_audio(file_path):
    if os.path.exists(file_path):
        try:
            # For Windows
            if os.name == 'nt':
                subprocess.Popen(['start', file_path], shell=True)
            # For macOS
            elif os.name == 'posix':
                subprocess.Popen(['open', file_path])
            # For Linux
            else:
                subprocess.Popen(['xdg-open', file_path])

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while opening audio player: {e}")
    else:
        messagebox.showerror("Error", "Audio file not found!")

def update_audio_display(file_path):
    audio_path_label.configure(text=f"Audio File: {file_path}")
    play_button.configure(command=lambda: play_audio(file_path))
    play_button.pack(side=tk.BOTTOM, padx=5)

def go_back():
    main_frame.pack(expand=True)
    encode_frame.pack_forget()
    decode_frame.pack_forget()

def on_encode():
    main_frame.pack_forget()
    encode_frame.pack(expand=True)

def on_decode():
    main_frame.pack_forget()
    decode_frame.pack(expand=True)

def update_time():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_label.configure(text=current_time)  # Use configure instead of config
    root.after(1000, update_time)


def toggle_theme():
    if theme_switch.get():
        set_appearance_mode("light")
    else:
        set_appearance_mode("dark")



def import_audio():
    global audio_file_path
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        audio_file_path = file_path
        messagebox.showinfo("Audio Imported", f"Audio file imported: {file_path}")
        update_audio_display(file_path)

def start_steganography():
    if secret_message.get() and audio_file_path:
        main = MainModule()
        key = main.embed(audio_file_path, secret_message.get())

        # Show success message
        messagebox.showinfo("Success", f"Key: {key}")

        # Save the key to a text file
        file_path = DOWNLOADS_PATH + "\\key.txt"
        if file_path:
            with open(file_path, 'w') as file:
                file.write(key)
            messagebox.showinfo("Saved", f"Key has been saved at {file_path}")

            mail_choice = messagebox.askyesno("Key Exchange", "Do you want to share the key as a text file?")
            if mail_choice:
                send_email_with_attachment(file_path) ################ For Key Exchange


    else:
        messagebox.showerror("Error", "Please input correct details!")

def decode_steganography():
    media_path = decode_media_path.get()
    secret_key = decode_secret_key.get()

    if not os.path.exists(media_path):
        messagebox.showerror("Error", "Media path not found! Please select a valid .wav file.")
        return

    if not secret_key:
        messagebox.showerror("Error", "Please provide a valid secret key or select a .txt file!")
        return

    try:
        if os.path.exists(secret_key):
            with open(secret_key, 'r') as key_file:
                secret_key = key_file.read().strip()

        main = MainModule()
        decoded_message = main.extract(media_path, secret_key)
        messagebox.showinfo("Decoded Message", decoded_message)

        save_choice = messagebox.askyesno("Decoded Message", "Do you want to save the Message to a text file?")
        if save_choice:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(decoded_message)
                messagebox.showinfo("Saved", "Message has been saved to the file!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during decoding: {e}")

def import_key():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        decode_secret_key.delete(0, tk.END)
        decode_secret_key.insert(0, file_path)

def import_media_path():
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        decode_media_path.delete(0, tk.END)
        decode_media_path.insert(0, file_path)

def refresh_encode():
    # Reset fields in the encode frame
    secret_message.delete(0, tk.END)
    audio_path_label.configure(text="Audio File: None")
    timer_label.configure(text="")
    play_button.pack_forget()

def refresh_decode():
    # Reset fields in the decode frame
    decode_media_path.delete(0, tk.END)
    decode_secret_key.delete(0, tk.END)

# Create the main window
root = CTk()
root.title("Steganography")
root.geometry("600x600")
root.configure(bg="white")

# Main frame for Encode/Decode options
main_frame = CTkFrame(root, border_color="grey", border_width=1 ,height=400,width=350)
main_frame.pack(expand=True)


encode_button = CTkButton(main_frame, text="  Encode  ", font=("Arial",20) ,command=on_encode, width=15, border_color="grey", border_width=1)
encode_button.grid(row=0, column=0, padx=15, pady=15)

decode_button = CTkButton(main_frame, text="  Decode  ", font=("Arial",20),command=on_decode, width=15, border_color="grey", border_width=1)
decode_button.grid(row=0, column=1, padx=15, pady=15)

# Theme Toggle at top right
theme_frame = CTkFrame(root)
theme_frame.pack(anchor="ne", padx=10, pady=5)


theme_switch = CTkSwitch(theme_frame, command=toggle_theme,text="  Mode")
theme_switch.pack(side=tk.LEFT, padx=15 , pady=10)

# Time display at bottom right
time_label = CTkLabel(root, text="", font=("Arial", 12))
time_label.pack(anchor="se", padx=10, pady=5)
update_time()

# Encode frame
encode_frame = CTkFrame(root, border_color="grey", border_width=1 , height=500,width=400)

CTkLabel(encode_frame, text="1. Record or Import Audio", font=("Arial", 16)).pack(pady=15)

audio_frame = CTkFrame(encode_frame)
audio_frame.pack(pady=5)

record_button = CTkButton(audio_frame, text="Record Audio", command=record_audio, border_color="grey", border_width=1)
record_button.pack(side=tk.LEFT, padx=1)

stop_button = CTkButton(audio_frame, text="Stop Recording", command=stop_recording, border_color="grey", border_width=1)
stop_button.pack(side=tk.LEFT, padx=1)

import_button = CTkButton(audio_frame, text="Import Audio", command=import_audio, border_color="grey", border_width=1)
import_button.pack(side=tk.LEFT, padx=2)

audio_path_label = CTkLabel(encode_frame, text="Audio File: None", font=("Arial", 14))
audio_path_label.pack(pady=5)

timer_label = CTkLabel(encode_frame, text="", font=("Arial", 10))
timer_label.pack(pady=5)


play_button = CTkButton(encode_frame, text="Play Audio", border_color="grey", border_width=1)
play_button.pack(pady=5 ,side=tk.BOTTOM)



CTkLabel(encode_frame, text="2. Enter Secret Message", font=("Arial", 16)).pack(pady=10)

secret_message = CTkEntry(encode_frame, width=180, font=("Arial", 14), border_color="grey", border_width=1)
secret_message.pack(pady=5)

start_button = CTkButton(encode_frame, text="Start Steganography", command=start_steganography, font=("Arial", 14), border_color="grey", border_width=1)
start_button.pack(pady=20)

refresh_button_encode = CTkButton(encode_frame, text="Refresh", command=refresh_encode,font=("Arial", 12), border_color="grey", border_width=1)
refresh_button_encode.pack(side=tk.BOTTOM, pady=10)

back_button_encode = CTkButton(encode_frame, text="Back", command=go_back,font=("Arial", 12) ,border_color="grey", border_width=1)
back_button_encode.pack(side=tk.BOTTOM, pady=10)

# Decode frame
decode_frame = CTkFrame(root, border_color="grey", border_width=1 , height=500 , width=400)

CTkLabel(decode_frame, text="1. Select Media File (.wav)", font=("Arial", 16)).pack(pady=5)

decode_media_path = CTkEntry(decode_frame, width=180, font=("Arial", 14), border_color="grey", border_width=1)
decode_media_path.pack(pady=2)

media_path_button = CTkButton(decode_frame, text="Browse", command=import_media_path, border_color="grey", border_width=1)
media_path_button.pack(pady=2)

play_audio_button = CTkButton(decode_frame, text="Play Selected Audio", command=lambda: play_audio(decode_media_path.get()), border_color="grey", border_width=1)
play_audio_button.pack(pady=5 ,side=tk.BOTTOM)

CTkLabel(decode_frame, text="2. Enter Secret Key", font=("Arial", 16)).pack(pady=10)

decode_secret_key = CTkEntry(decode_frame, width=180, font=("Arial", 14), border_color="grey", border_width=1)
decode_secret_key.pack(pady=5)

key_button = CTkButton(decode_frame, text="Import Key", command=import_key, border_color="grey", border_width=1)
key_button.pack(pady=5)

decode_button = CTkButton(decode_frame, text="Start Decoding", command=decode_steganography, font=("Arial", 14), border_color="grey", border_width=1)
decode_button.pack(pady=20)

refresh_button_decode = CTkButton(decode_frame, text="Refresh", command=refresh_decode,font=("Arial", 12), border_color="grey", border_width=1)
refresh_button_decode.pack(side=tk.BOTTOM, pady=5)

back_button_decode = CTkButton(decode_frame, text="Back", command=go_back, font=("Arial", 12),border_color="grey", border_width=1)
back_button_decode.pack(side=tk.BOTTOM, pady=5)

# Run the application
root.mainloop()