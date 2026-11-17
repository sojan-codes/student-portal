import hashlib
import secrets
import hmac

class PasswordHasher:
    def generate_salt(self):
        salt = secrets.token_hex(16)
        return salt
    
    def hash_password(self, password, salt):
        hashed_password = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt.encode(),
            100000
        ).hex()
        return hashed_password
    
    def verify_password(self, password, salt, stored_hash):
        hashed_password = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt.encode(),
            100000
        ).hex()
        return hmac.compare_digest(hashed_password, stored_hash)