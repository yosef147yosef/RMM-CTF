import socket
import email
from email.parser import Parser
from email.mime.text import MIMEText

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 25  # SMTP port

def send_email(sender_email, recipient_email, subject, body):
    # Create the message
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Connect to the SMTP server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Receive the server's greeting
        data = s.recv(1024)
        print(f"Server response: {data.decode().strip()}")

        # Send the HELO command
        s.sendall(b'HELO localhost\r\n')
        data = s.recv(1024)
        print(f"Server response: {data.decode().strip()}")

        # Send the MAIL FROM command
        s.sendall(f"MAIL FROM:<{sender_email}>\r\n".encode())
        data = s.recv(1024)
        print(f"Server response: {data.decode().strip()}")

        # Send the RCPT TO command
        s.sendall(f"RCPT TO:<{recipient_email}>\r\n".encode())
        data = s.recv(1024)
        print(f"Server response: {data.decode().strip()}")

        # Send the DATA command
        s.sendall(b'DATA\r\n')
        data = s.recv(1024)
        print(f"Server response: {data.decode().strip()}")

        # Send the email message
        s.sendall(msg.as_string().encode())
        s.sendall(b'\r\n.\r\n')
        data = s.recv(1024)
        print(f"Server response: {data.decode().strip()}")

        # Receive the response email from the server
        response_email = b''
        while True:
            data = s.recv(1024)
            if not data:
                break
            response_email += data
            if data.endswith(b'\r\n.\r\n'):
                break

        # Parse and print the response email
        try:
            msg = Parser().parsestr(response_email.decode())
            print('Received response email:')
            print(msg)
        except (UnicodeDecodeError, email.errors.MessageParseError):
            print('Error parsing response email')

        # Send the QUIT command
        s.sendall(b'QUIT\r\n')
        data = s.recv(1024)
        print(f"Server response: {data.decode().strip()}")

# Example usage
send_email("your_email@example.com", "Iran_Misseles@Iranfasdfd.gov.co.il", "Test Email", "This is a test email.")
