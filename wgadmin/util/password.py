from base64 import b64encode
from hashlib import scrypt
from wgadmin.common.config import CONF

def encode_hash_pw(password, salt):    
    encoded_hashed_pw = b64encode(
        scrypt(
            password=password.encode(),
            salt=salt.encode(),
            n=CONF.scrypt_n,
            r=CONF.scrypt_r,
            p=CONF.scrypt_p
        )
    ).decode()

    return encoded_hashed_pw
