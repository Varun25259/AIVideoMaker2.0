import os, json, base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from pathlib import Path
STOREFILE = Path(__file__).parent.parent / 'keys_upgraded.enc'
def _derive_key(passphrase: str, salt: bytes):
    return scrypt(passphrase.encode('utf-8'), salt, 32, N=2**14, r=8, p=1)
def save_keys_securely(data: dict, passphrase: str):
    salt = os.urandom(16)
    key = _derive_key(passphrase, salt)
    cipher = AES.new(key, AES.MODE_GCM)
    plaintext = json.dumps(data).encode('utf-8')
    ct, tag = cipher.encrypt_and_digest(plaintext)
    blob = salt + cipher.nonce + tag + ct
    with open(STOREFILE, 'wb') as f:
        f.write(base64.b64encode(blob))
def load_keys_securely(passphrase: str):
    if not STOREFILE.exists():
        return None
    blob = base64.b64decode(open(STOREFILE,'rb').read())
    salt = blob[:16]; nonce = blob[16:32]; tag = blob[32:48]; ct = blob[48:]
    key = _derive_key(passphrase, salt)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    pt = cipher.decrypt_and_verify(ct, tag)
    return json.loads(pt.decode('utf-8'))
