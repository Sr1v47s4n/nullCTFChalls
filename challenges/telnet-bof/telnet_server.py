import socket
import threading
import time

def handle_client(client_socket, address):
    try:
        client_socket.send(b"\n  Welcome to The Matrix Telnet Server \n")
        client_socket.send(b"Neo says: 'Follow the white rabbit...'\n")
        client_socket.send(b"Enter a number to test our ultra-secure buffer: ")

        while True:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break
            # Check for "buffer overflow" simulation
            if data.isdigit():
                number = int(data)
                if number > 1337:
                    # Simulate buffer overflow
                    client_socket.send(b"\nBUFFER OVERFLOW DETECTED!\n")
                    client_socket.send(b"You've broken into the Matrix. Neo is impressed.\n")
                    client_socket.send(b"Morpheus: 'There is no spoon... or buffer limit!'\n")
                    client_socket.send(b"\nRed Pill Taken! Here's your flag:\n")
                    client_socket.send(b"nulleec{buff3r_0v3rfl0w_w0w}\n")
                    client_socket.send(b"\nAgent Smith: 'Mr. Anderson... you've done well.'\n")
                    break
                elif number > 255:
                    client_socket.send(b"\nBuffer getting full... Try a bigger number!\n")
                    client_socket.send(b"Cat fact: Cats have 9 lives, buffers have limits!\n")
                    client_socket.send(b"Enter another number: ")
                else:
                    client_socket.send(b"\nNumber stored safely in buffer!\n")
                    client_socket.send(b"'That's cute. Try harder!' - Trinity\n")
                    client_socket.send(b"Enter another number: ")
            elif data.lower() in ['help', 'hint']:
                client_socket.send(b"\nHints:\n")
                client_socket.send(b"- Try numbers bigger than 1337\n")
                client_socket.send(b"- The Matrix has no limits... or does it?\n")
                client_socket.send(b"- Even cats can overflow buffers!\n")
                client_socket.send(b"Enter a number: ")
            elif data.lower() in ['exit', 'quit']:
                client_socket.send(b"\nGoodbye from The Matrix!\n")
                break
            else:
                client_socket.send(b"\nInvalid input! Numbers only, please.\n")
                client_socket.send(b"Keanu Reeves says: 'Whoa... that's not a number!'\n")
                client_socket.send(b"Enter a number: ")
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 2323))
    server.listen(5)
    print("Matrix Telnet Server started on port 2323")
    print("Waiting for connections...")
    while True:
        client_socket, address = server.accept()
        print(f"Connection from {address}")
        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, address)
        )
        client_thread.daemon = True
        client_thread.start()

if __name__ == "__main__":
    start_server()