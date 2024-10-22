import socket
import random

def modular_exponentiation(base, exponent, modulus):
    return pow(base, exponent, modulus)

def generate_parameters():
    p = 23  # Prime number
    g = 5   # Primitive root
    return p, g

def server():
    p, g = generate_parameters()
    print(f"Server: Prime number (p): {p}")
    print(f"Server: Primitive root (g): {g}")

    b = random.randint(1, p-1)
    B = modular_exponentiation(g, b, p)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 65432))
        s.listen()
        print("Server: Waiting for a connection...")
        conn, addr = s.accept()
        with conn:
            print(f"Server: Connected by {addr}")
            conn.sendall(str(B).encode())
            A = int(conn.recv(1024).decode())
            print(f"Server: Received Client's public key (A): {A}")
            shared_secret_server = modular_exponentiation(A, b, p)
            print(f"Server: Shared secret: {shared_secret_server}")
# Uncomment to run the server
server()