from hashlib import sha256

def hash_value(text: str):
    return sha256(text.encode()).hexdigest()