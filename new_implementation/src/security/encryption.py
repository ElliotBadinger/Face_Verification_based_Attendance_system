from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
import os
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

class EncryptionService:
    """Service for handling encryption of sensitive data"""
    
    def __init__(self, key_directory: str = "secure_keys"):
        """Initialize encryption service with key management"""
        self.key_directory = key_directory
        self.current_key_id = None
        self.key_cache = {}
        self._ensure_key_directory()
        self._load_or_generate_key()

    def _ensure_key_directory(self):
        """Ensure key directory exists"""
        if not os.path.exists(self.key_directory):
            os.makedirs(self.key_directory, mode=0o700)  # Secure permissions

    def _load_or_generate_key(self):
        """Load existing key or generate new one"""
        key_files = [f for f in os.listdir(self.key_directory) 
                    if f.endswith('.key')]
        
        if not key_files:
            self._generate_new_key()
        else:
            # Load most recent key
            latest_key = sorted(key_files)[-1]
            self.current_key_id = latest_key.split('.')[0]
            with open(os.path.join(self.key_directory, latest_key), 'rb') as f:
                self.key_cache[self.current_key_id] = f.read()

    def _generate_new_key(self):
        """Generate new encryption key"""
        key = Fernet.generate_key()
        key_id = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        key_path = os.path.join(self.key_directory, f'{key_id}.key')
        
        # Save key with secure permissions
        with open(key_path, 'wb') as f:
            os.chmod(key_path, 0o600)  # Secure permissions
            f.write(key)
        
        self.current_key_id = key_id
        self.key_cache[key_id] = key
        
        # Log key generation (in production, use secure audit logging)
        logger.info(f"Generated new encryption key with ID: {key_id}")

    def encrypt_face_data(self, face_encoding) -> tuple:
        """Encrypt face encoding data"""
        if not isinstance(face_encoding, bytes):
            face_encoding = face_encoding.tobytes()
            
        # Add metadata for verification
        metadata = {
            "timestamp": datetime.utcnow().isoformat(),
            "key_id": self.current_key_id,
            "version": "1.0"
        }
        
        # Combine metadata and face encoding
        data_to_encrypt = json.dumps(metadata).encode() + b"||" + face_encoding
        
        # Get current key
        key = self.key_cache[self.current_key_id]
        f = Fernet(key)
        
        # Encrypt data
        encrypted_data = f.encrypt(data_to_encrypt)
        
        return encrypted_data, self.current_key_id

    def decrypt_face_data(self, encrypted_data: bytes, key_id: str) -> bytes:
        """Decrypt face encoding data"""
        # Get key for decryption
        if key_id not in self.key_cache:
            key_path = os.path.join(self.key_directory, f'{key_id}.key')
            with open(key_path, 'rb') as f:
                self.key_cache[key_id] = f.read()
        
        key = self.key_cache[key_id]
        f = Fernet(key)
        
        # Decrypt data
        decrypted_data = f.decrypt(encrypted_data)
        
        # Split metadata and face encoding
        metadata_json, face_encoding = decrypted_data.split(b"||")
        
        # Verify metadata (in production, implement additional checks)
        metadata = json.loads(metadata_json)
        if metadata["key_id"] != key_id:
            raise ValueError("Key ID mismatch")
            
        return face_encoding

    def rotate_keys(self):
        """Implement key rotation"""
        # Generate new key
        self._generate_new_key()
        
        # In production:
        # 1. Re-encrypt all data with new key
        # 2. Implement secure key deletion
        # 3. Update all relevant database records
        # 4. Log key rotation in secure audit log
        
        logger.info("Completed key rotation")

    def get_key_info(self, key_id: str = None) -> dict:
        """Get information about encryption keys"""
        if key_id is None:
            key_id = self.current_key_id
            
        key_path = os.path.join(self.key_directory, f'{key_id}.key')
        key_stat = os.stat(key_path)
        
        return {
            "key_id": key_id,
            "created_at": datetime.fromtimestamp(key_stat.st_ctime).isoformat(),
            "is_current": key_id == self.current_key_id
        }
