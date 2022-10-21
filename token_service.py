import base64
import hashlib
import hmac
import os
import time
from urllib.parse import quote as url_parse_quote

FULLY_QUALIFIED_NAMESPACE = os.environ["EVENT_HUB_HOSTNAME"]
EVENTHUB_NAME = os.environ["EVENT_HUB_NAME"]

SAS_POLICY = os.environ["EVENT_HUB_SAS_POLICY"]
SAS_KEY = os.environ["EVENT_HUB_SAS_KEY"]

TOKEN_EXPIRY_IN_SECONDS = os.environ.get("TOKEN_EXPIRY_IN_SECONDS", 60)


def get_expiry():
    return TOKEN_EXPIRY_IN_SECONDS


def get_token(publisher_id):
    uri = (f"sb://{FULLY_QUALIFIED_NAMESPACE}/{EVENTHUB_NAME}"
           f"/publishers/{publisher_id}")
    token_ttl = get_expiry()
    sas_name = SAS_POLICY
    sas_value = SAS_KEY
    sas = sas_value.encode("utf-8")
    expiry = str(int(time.time() + token_ttl))
    string_to_sign = (uri + "\n" + expiry).encode("utf-8")
    signed_hmac_sha256 = hmac.HMAC(sas, string_to_sign, hashlib.sha256)
    signature = url_parse_quote(base64.b64encode(signed_hmac_sha256.digest()))
    return (f"SharedAccessSignature sr={uri}&sig={signature}"
            f"&se={expiry}&skn={sas_name}")
