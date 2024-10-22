import socket
import random

def modular_exponentiation(base, exponent, modulus):
    return pow(base, exponent, modulus)

def generate_parameters():
    p = 23  # Prime number
    g = 5   # Primitive root
    return p, g

def attacker():
    p, g = generate_parameters()
    print(f"Attacker: Prime number (p): {p}")
    print(f"Attacker: Primitive root (g): {g}")

    k = random.randint(1, p-1)
    K = modular_exponentiation(g, k, p)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 65431))  # Listen on a different port
        s.listen()
        print("Attacker: Waiting for a connection...")
        conn, addr = s.accept()
        with conn:
            print(f"Attacker: Connected by {addr}")

            # Send attacker's public key to the client
            conn.sendall(str(K).encode())
            A = int(conn.recv(1024).decode())
            print(f"Attacker: Received Client's public key (A): {A}")

            # Connect to the server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_conn:
                server_conn.connect(('localhost', 65432))
                server_conn.sendall(str(K).encode())  # Send attacker's public key to server
                server_conn.sendall(str(A).encode())  # Forward A to server

                B = int(server_conn.recv(1024).decode())
                print(f"Attacker: Received Server's public key (B): {B}")

                # Calculate shared secret with client
                shared_secret_attacker_client = modular_exponentiation(A, k, p)
                print(f"Attacker: Shared secret with Client: {shared_secret_attacker_client}")

                # Calculate shared secret with server
                shared_secret_attacker_server = modular_exponentiation(B, k, p)
                print(f"Attacker: Shared secret with Server: {shared_secret_attacker_server}")

# Uncomment to run the attacker
attacker()