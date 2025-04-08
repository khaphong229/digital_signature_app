from cryptography.hazmat.primitives.asymmetric import rsa, dsa
from cryptography.hazmat.primitives import serialization
import os

class KeyGenerator:
    def __init__(self):
        self.public_key = None
        self.private_key = None
    
    def generate_rsa_keys(self, key_size=2048):
        """Generate a new RSA key pair"""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )
        self.public_key = self.private_key.public_key()
        return self.private_key, self.public_key
    
    def generate_dsa_keys(self, key_size=2048):
        """Generate a new DSA key pair"""
        self.private_key = dsa.generate_private_key(
            key_size=key_size
        )
        self.public_key = self.private_key.public_key()
        return self.private_key, self.public_key
    
    def save_private_key(self, filename, password=None):
        """Save private key to file"""
        if not self.private_key:
            raise ValueError("No private key to save")
        
        encryption = serialization.NoEncryption()
        if password:
            encryption = serialization.BestAvailableEncryption(password.encode())
        
        pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption
        )
        
        with open(filename, 'wb') as f:
            f.write(pem)
    
    def save_public_key(self, filename):
        """Save public key to file"""
        if not self.public_key:
            raise ValueError("No public key to save")
        
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        with open(filename, 'wb') as f:
            f.write(pem)
    
    def load_private_key(self, filename, password=None):
        """Load private key from file"""
        with open(filename, 'rb') as f:
            key_data = f.read()
        
        if password:
            self.private_key = serialization.load_pem_private_key(
                key_data,
                password=password.encode()
            )
        else:
            self.private_key = serialization.load_pem_private_key(
                key_data,
                password=None
            )
        return self.private_key
    
    def load_public_key(self, filename):
        """Load public key from file"""
        with open(filename, 'rb') as f:
            key_data = f.read()
        
        self.public_key = serialization.load_pem_public_key(key_data)
        return self.public_key
