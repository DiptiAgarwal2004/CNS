import socket
import random

def modular_exponentiation(base, exponent, modulus):
    return pow(base, exponent, modulus)

def generate_parameters():
    p = 23  # Prime number
    g = 5   # Primitive root
    return p, g

def client():
    p, g = generate_parameters()
    print(f"Client: Prime number (p): {p}")
    print(f"Client: Primitive root (g): {g}")

    a = random.randint(1, p-1)
    A = modular_exponentiation(g, a, p)

    # Connect to the attacker instead of the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 65431))  # Attacker's port
        print("Client: Connected to the attacker.")
        s.sendall(str(A).encode())
        B = int(s.recv(1024).decode())
        print(f"Client: Received Server's public key (B): {B}")
        shared_secret_client = modular_exponentiation(B, a, p)
        print(f"Client: Shared secret: {shared_secret_client}")

# Uncomment to run the client
client()