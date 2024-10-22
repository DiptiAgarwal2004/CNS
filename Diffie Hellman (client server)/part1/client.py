import socket
import random

# Function to calculate modular exponentiation (x^y) % p
def power_mod(base, exponent, mod):
    return pow(base, exponent, mod)

# Create a socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 65432))

# Receive p, g, and server's public key from the server
received_data = client_socket.recv(1024).decode()
p, g, server_public_key = map(int, received_data.split(','))

# Client's private key (a)
client_private_key = random.randint(1, 100)

# Client's public key (A = g^a mod p)
client_public_key = power_mod(g, client_private_key, p)

# Display client-side values
print(f"Client: p = {p}, g = {g}, a (private key) = {client_private_key}")
print(f"Client: Public key (A) = {client_public_key}")

# Send client's public key to the server
client_socket.send(str(client_public_key).encode())

# Calculate the shared secret key (S = B^a mod p)
shared_secret = power_mod(server_public_key, client_private_key, p)
print(f"Shared secret key (Client): {shared_secret}")

# Close connection
client_socket.close()
