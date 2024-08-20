#!/usr/bin env

from attrs import define

@define(frozen=True)
class EncryptionKey:
    key_id: str
    key: str
