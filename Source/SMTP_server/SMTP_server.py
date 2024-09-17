import socket
import email
from email.parser import Parser
from email.mime.text import MIMEText
import smtplib

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 25  # SMTP port

# Custom message to be sent back
RESPONSE_MESSAGE = "Ok Mohamad, You got to the end. \n Flag{Who_Dares_Winds}\n"

def handle_client(conn, addr):
    print(f'New connection from {addr}')

    # Send greeting
    conn.sendall(b'220 localhost Simple SMTP Server ready\r\n')

    recipient_email = None

    while True:
        data = conn.recv(1024)
        if not data:
            break

        # Parse the SMTP command
        command, *args = data.decode().strip().split(None, 1)
        print(f'Received command: {command} {" ".join(args)}')

        if command.upper() == 'HELO':
            conn.sendall(b'250 localhost\r\n')
        elif command.upper() == 'MAIL':
            conn.sendall(b'250 OK\r\n')
        elif command.upper() == 'RCPT':
            recipient_email = args[0].strip('<>')
            conn.sendall(b'250 OK\r\n')
        elif command.upper() == 'DATA':
            conn.sendall(b'354 Enter message, end with "." on a line by itself\r\n')
            message = b''
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message += data
                if data.endswith(b'\r\n.\r\n'):
                    break
            try:
                msg = Parser().parsestr(message.decode())
                print('Received message:')
                print(msg)
                conn.sendall(b'250 OK\r\n')
                if recipient_email.endswith('Iran_Misseles@Iran.gov.co.il'):
                    send_response_email(msg,conn)
                    print('Response email sent')
            except (UnicodeDecodeError, email.errors.MessageParseError):
                conn.sendall(b'451 Error parsing message\r\n')
        elif command.upper() == 'QUIT':
            conn.sendall(b'221 Bye\r\n')
            break
        else:
            conn.sendall(b'502 Command not implemented\r\n')

    print(f'Connection closed with {addr}')
    conn.close()

def send_response_email(original_message, client_socket):
    # Create the response email message
    msg = f"From: Iran_Misseles@Iran.gov.co.il\r\n"
    msg += f"To: {original_message['From']}\r\n"
    msg += f"Subject: Response: {original_message['Subject']}\r\n"
    msg += "\r\n"
    msg += RESPONSE_MESSAGE
    msg+='\r\n.\r\n'
    client_socket.sendall(msg.encode())

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'SMTP server listening on {HOST}:{PORT}')

        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)

main()
