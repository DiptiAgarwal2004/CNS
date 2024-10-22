import socket
import random

# Function to calculate modular exponentiation (x^y) % p
def power_mod(base, exponent, mod):
    return pow(base, exponent, mod)

# Generating random prime p and base g
p = random.randint(10, 100)  # Prime number (in a realistic scenario, use a large prime)
g = random.randint(2, p-1)    # Base (g should be a primitive root modulo p)

# Server's private key (b)
server_private_key = random.randint(1, 100)

# Server's public key (B = g^b mod p)
server_public_key = power_mod(g, server_private_key, p)

# Display server-side values
print(f"Server: p = {p}, g = {g}, b (private key) = {server_private_key}")
print(f"Server: Public key (B) = {server_public_key}")

# Create a socket and bind it to a host and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 65432))
server_socket.listen(1)

print("Waiting for client connection...")
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

# Send p, g, and server's public key to the client
conn.send(f"{p},{g},{server_public_key}".encode())

# Receive client's public key
client_public_key = int(conn.recv(1024).decode())

# Calculate the shared secret key (S = A^b mod p)
shared_secret = power_mod(client_public_key, server_private_key, p)
print(f"Shared secret key (Server): {shared_secret}")

# Close connection
conn.close()
server_socket.close()
