import os
import base64
import hashlib

def get_file_hash(file_path, algorithm='sha256'):
    """Calculate hash of a file"""
    hash_algorithms = {
        'sha256': hashlib.sha256(),
        'sha384': hashlib.sha384(),
        'sha512': hashlib.sha512(),
        'md5': hashlib.md5()  # Not recommended for security purposes
    }
    
    hasher = hash_algorithms.get(algorithm.lower(), hashlib.sha256())
    
    with open(file_path, 'rb') as f:
        # Read in chunks to handle large files
        chunk = f.read(8192)
        while chunk:
            hasher.update(chunk)
            chunk = f.read(8192)
    
    return hasher.hexdigest()

def ensure_directory_exists(path):
    """Ensure that directory exists, create if not"""
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def display_signature_info(signature):
    """Return a string with basic info about the signature"""
    if not signature:
        return "No signature available"
    
    # Return signature size and a preview (first 16 bytes as hex)
    size = len(signature)
    preview = signature[:16].hex()
    return f"Signature size: {size} bytes\nPreview: {preview}..."

def get_base64_signature(signature):
    """Convert signature bytes to base64 string"""
    if not signature:
        return ""
    return base64.b64encode(signature).decode('ascii')

def decode_base64_signature(base64_string):
    """Convert base64 string back to signature bytes"""
    if not base64_string:
        return None
    return base64.b64decode(base64_string)
