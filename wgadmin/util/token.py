import hmac
from base64 import b64encode
from base64 import b64decode
from hashlib import sha512

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

    return hmac.compare_digest(
        h.digest(),
        b64decode(signature.encode())
    )
