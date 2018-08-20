import hmac
import json
import binascii
import datetime
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
        return None

    message = auth_data[0].encode()
    signature = auth_data[1]

    v = verify(
        CONF.session_key.encode(),
        message,
        signature
    )

    if not v:
        return None

    payload = json.loads(b64decode(message))

    iat = datetime.datetime.fromtimestamp(payload['iat'])

    if iat < datetime.datetime.now() - datetime.timedelta(hours=CONF.token_duration):
        return None

    return payload
