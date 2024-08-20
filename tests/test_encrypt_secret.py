#!/usr/bin/env python3
# pylint: disable=missing-class-docstring,missing-function-docstring,missing-module-docstring

import base64
import unittest


import feeph.github_utils.api.secrets as sut  # sytem under test


# pylint: disable=protected-access
class TestEncryptSecret(unittest.TestCase):

    def setUp(self) -> None:
        data = {
            'key_id': '3380204578043523366',
            'key': 'p1x4yLjvlEWW0CgbCMQOWJteDdbIIVn200eQVjmfDA0=',
        }
        self.key_id = data['key_id']
        self.key = base64.b64decode(data['key'])
        return super().setUp()

    # ---------------------------------------------------------------------

    # the encrypted value changes with each iteration and can't be compared
    def test_encrypt_secret(self):
        enc_key = sut.EncryptionKey(key_id=self.key_id, key=self.key)
        # -----------------------------------------------------------------
        computed = sut.encrypt_secret(encryption_key=enc_key, secret='dummyvalue')
        expected = sut.EncryptedSecret(encrypted_value='bevKcOj3FVITuhP0UtGRtcUs4E9o3SFCkcgWrOUMPTUTSoiQOWAS8y1pymgtCTVW9lA=', key_id=self.key_id)
        # -----------------------------------------------------------------
        self.assertEqual(len(computed.encrypted_value), len(expected.encrypted_value))
        self.assertEqual(computed.key_id, expected.key_id)
