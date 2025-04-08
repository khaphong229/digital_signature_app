from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, utils
from cryptography.exceptions import InvalidSignature
import os

class DigitalSignature:
    def __init__(self):
        self.hash_algorithms = {
            'SHA256': hashes.SHA256(),
            'SHA384': hashes.SHA384(),
            'SHA512': hashes.SHA512()
        }
    
    def sign_message(self, message, private_key, hash_algorithm='SHA256'):
        """
        Sign a message using private key
        :param message: Message to sign (bytes or string)
        :param private_key: Private key object
        :param hash_algorithm: Hash algorithm to use
        :return: Signature bytes
        """
        if isinstance(message, str):
            message = message.encode('utf-8')
        
        # Choose hash algorithm
        hash_algo = self.hash_algorithms.get(hash_algorithm, self.hash_algorithms['SHA256'])
        
        # Different signing process for RSA and DSA
        if private_key.__class__.__name__ == 'RSAPrivateKey':
            signature = private_key.sign(
                message,
                padding.PSS(
                    mgf=padding.MGF1(hash_algo),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hash_algo
            )
        elif private_key.__class__.__name__ == 'DSAPrivateKey':
            signature = private_key.sign(
                message,
                hash_algo
            )
        else:
            raise ValueError("Unsupported key type")
        
        return signature
    
    def verify_signature(self, message, signature, public_key, hash_algorithm='SHA256'):
        """
        Verify a signature using public key
        :param message: Original message (bytes or string)
        :param signature: Signature bytes
        :param public_key: Public key object
        :param hash_algorithm: Hash algorithm used
        :return: True if signature is valid, False otherwise
        """
        if isinstance(message, str):
            message = message.encode('utf-8')
        
        # Choose hash algorithm
        hash_algo = self.hash_algorithms.get(hash_algorithm, self.hash_algorithms['SHA256'])
        
        try:
            # Different verification process for RSA and DSA
            if public_key.__class__.__name__ == 'RSAPublicKey':
                public_key.verify(
                    signature,
                    message,
                    padding.PSS(
                        mgf=padding.MGF1(hash_algo),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hash_algo
                )
            elif public_key.__class__.__name__ == 'DSAPublicKey':
                public_key.verify(
                    signature,
                    message,
                    hash_algo
                )
            else:
                raise ValueError("Unsupported key type")
            return True
        except InvalidSignature:
            return False
    
    def sign_file(self, file_path, private_key, hash_algorithm='SHA256'):
        """
        Sign a file using private key
        :param file_path: Path to file
        :param private_key: Private key object
        :param hash_algorithm: Hash algorithm to use
        :return: Signature bytes
        """
        # Choose hash algorithm
        hash_algo = self.hash_algorithms.get(hash_algorithm, self.hash_algorithms['SHA256'])
        
        # Calculate file hash
        hasher = hashes.Hash(hash_algo)
        with open(file_path, 'rb') as f:
            # Read in chunks to handle large files
            chunk = f.read(8192)
            while chunk:
                hasher.update(chunk)
                chunk = f.read(8192)
        
        digest = hasher.finalize()
        
        # Sign the digest
        if private_key.__class__.__name__ == 'RSAPrivateKey':
            signature = private_key.sign(
                digest,
                padding.PSS(
                    mgf=padding.MGF1(hash_algo),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                utils.Prehashed(hash_algo)
            )
        elif private_key.__class__.__name__ == 'DSAPrivateKey':
            # DSA doesn't support prehashed, so we need to sign whole file
            with open(file_path, 'rb') as f:
                content = f.read()
            signature = private_key.sign(
                content,
                hash_algo
            )
        else:
            raise ValueError("Unsupported key type")
        
        return signature
    
    def verify_file_signature(self, file_path, signature, public_key, hash_algorithm='SHA256'):
        """
        Verify a file signature using public key
        :param file_path: Path to file
        :param signature: Signature bytes
        :param public_key: Public key object
        :param hash_algorithm: Hash algorithm used
        :return: True if signature is valid, False otherwise
        """
        hash_algo = self.hash_algorithms.get(hash_algorithm, self.hash_algorithms['SHA256'])
        
        try:
            if public_key.__class__.__name__ == 'RSAPublicKey':
                # Calculate file hash
                hasher = hashes.Hash(hash_algo)
                with open(file_path, 'rb') as f:
                    chunk = f.read(8192)
                    while chunk:
                        hasher.update(chunk)
                        chunk = f.read(8192)
                
                digest = hasher.finalize()
                
                # Verify the signature
                public_key.verify(
                    signature,
                    digest,
                    padding.PSS(
                        mgf=padding.MGF1(hash_algo),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    utils.Prehashed(hash_algo)
                )
            elif public_key.__class__.__name__ == 'DSAPublicKey':
                # DSA doesn't support prehashed, so we need to verify whole file
                with open(file_path, 'rb') as f:
                    content = f.read()
                public_key.verify(
                    signature,
                    content,
                    hash_algo
                )
            else:
                raise ValueError("Unsupported key type")
            return True
        except InvalidSignature:
            return False
    
    def save_signature(self, signature, filename):
        """Save signature to file"""
        with open(filename, 'wb') as f:
            f.write(signature)
    
    def load_signature(self, filename):
        """Load signature from file"""
        with open(filename, 'rb') as f:
            return f.read()
