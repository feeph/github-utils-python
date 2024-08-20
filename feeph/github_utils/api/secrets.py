#!/usr/bin/env python
"""
https://docs.github.com/en/rest/guides/encrypting-secrets-for-the-rest-api?apiVersion=2022-11-28#example-encrypting-a-secret-using-python
please note: the example provided on this page does NOT work and will
result in the following error:

{"message":"Bad request - validation failed due to an improperly encrypted secret","documentation_url":"https://docs.github.com/rest/reference/actions#create-or-update-an-environment-secret","status":"422"}

https://pynacl.readthedocs.io/en/latest/secret/#example-with-secretbox provides
a slightly different example and this works
"""

import base64
from attrs import define

import nacl.secret


@define(frozen=True)
class EncryptionKey:
    key_id: str
    key: bytes


@define(frozen=True)
class EncryptedSecret:
    encrypted_value: str
    key_id: str


def encrypt_secret(encryption_key: EncryptionKey, secret: str) -> EncryptedSecret:
    box = nacl.secret.SecretBox(encryption_key.key)
    encrypted_secret = box.encrypt(secret.encode("utf-8"))
    encrypted_secret_b64 = base64.b64encode(encrypted_secret).decode("utf-8")
    return EncryptedSecret(encrypted_value=encrypted_secret_b64, key_id=encryption_key.key_id)
