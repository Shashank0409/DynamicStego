import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog  # Import simpledialog
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email_with_attachment( file_path):
    sender_email = "your_email_address"  # Replace with your email
    sender_password = "your_email_app_password"  # Replace with your email password

    receiver_email = simpledialog.askstring("Input", "Please enter the receiver's email address:")   ##Receiver mail input
    if receiver_email:

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Key Exchange"

    # Attach the file
        with open(file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={file_path.split("/")[-1]}')
            msg.attach(part)

        # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Use your email provider's SMTP server
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
                messagebox.showinfo("Sent", "Key has been sent successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {str(e)}")
'''
def key_exchange(key):
    mail_choice = messagebox.askyesno("Key Exchange", "Do you want to share the key as a text file?")
    if mail_choice:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(key)
                send_email_with_attachment(file_path)

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    key = "your_secret_key"  # Replace with your actual key
    key_exchange(key)
'''