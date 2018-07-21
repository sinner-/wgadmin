import hmac
import binascii
from base64 import b64encode
from base64 import b64decode
from hashlib import sha512
from wgadmin.common.config import CONF

def sign(key, message):
    signature = b64encode(
        hmac.new(
            key=key,
            msg=message,
            digestmod=sha512
        ).digest()
    ).decode()

    return signature

def verify(key, message, signature):
    h = hmac.new(
        key=key,
        msg=message,
        digestmod=sha512
    )

    try:
        sig = b64decode(signature.encode())
    except binascii.Error:
        return False

    return hmac.compare_digest(
        h.digest(),
        sig
    )

def check_auth(token):
    auth_data = token.split('.')

    if len(auth_data) != 2:
        return False

    message = auth_data[0].encode()
    signature = auth_data[1]

    return verify(
        CONF.session_key.encode(),
        message,
        signature
    )
