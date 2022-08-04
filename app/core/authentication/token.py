from typing import Any, Optional

import datetime
import jwt
import uuid
import dataclasses

from app.bootstrap.config import config

@dataclasses.dataclass
class TokenDecodeResult:
    class FailureReason:
        EXPIRED = 1
        INVALID = 2

    success: bool
    payload: dict[str, Any]
    fail_reason: int


def issue_token(claims):
    return jwt.encode(claims, config.get('main.token_key'), algorithm="HS256")

def decode_token(token) -> TokenDecodeResult:
    try:
        payload = jwt.decode(token, config.get('main.token_key'), algorithms=["HS256"], verify=True)
        return TokenDecodeResult(True, payload, 0)
    except jwt.ExpiredSignatureError:
        return TokenDecodeResult(False, {}, TokenDecodeResult.FailureReason.EXPIRED)
    except:
        return TokenDecodeResult(False, {}, TokenDecodeResult.FailureReason.INVALID)


def new_access_token(userid):
    return issue_token({
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45),
        'jti': str(uuid.uuid4()),
        'userid': userid,
        'tk_type': 'acs'
    })

def new_ref_token(userid, expires_at):
    tkid = f'ref-{str(uuid.uuid4())}'
    token = issue_token({
        'exp': expires_at,
        'jti': tkid,
        'userid': userid,
        'tk_type': 'ref',
    })

    return token, tkid