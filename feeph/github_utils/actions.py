#!/usr/bin/env python3

import base64
import logging

import requests
from feeph.github_utils.api.secrets import EncryptionKey, encrypt_secret

LH = logging.getLogger('feeph.github')


class Actions:

    def __init__(self, owner: str, repository: str, github_pat: str):
        self.base_url = f"https://api.github.com/repos/{owner}/{repository}"
        self.enc_key: EncryptionKey | None = None
        self.session = requests.Session()
        self.session.headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f"Bearer {github_pat}",
            'X-GitHub-Api-Version': '2022-11-28',
        }

    def get_encryption_key(self) -> EncryptionKey:
        # https://docs.github.com/en/rest/actions/secrets?apiVersion=2022-11-28#get-a-repository-public-key
        response = self.session.get(f"{self.base_url}/actions/secrets/public-key")
        key_id = response.json()['key_id']
        key    = base64.b64decode(response.json()['key'])
        LH.debug("Using KeyID %s to encrypt the GitHub Actions/Environments secrets.", key_id)
        return EncryptionKey(key_id=key_id, key=key)

    def update_secret(self, name: str, value: str) -> tuple[bool, str | None]:
        """
        create or update a GitHub Actions secret
        - required permission: Codespaces user secrets (r/w)

        https://github.com/<owner>/<repo>/settings/secrets/actions
        """
        # https://docs.github.com/en/rest/actions/secrets?apiVersion=2022-11-28#create-or-update-a-repository-secret
        if self.enc_key is None:
            self.enc_key = self.get_encryption_key()
        encrypted = encrypt_secret(encryption_key=self.enc_key, secret=value)
        response = self.session.put(f"{self.base_url}/actions/secrets/{name}", json={'encrypted_value': encrypted.encrypted_value, 'key_id': encrypted.key_id})
        if response.status_code in [201, 204]:
            return (True, None)
        elif response.status_code in [403, 404, 422]:
            # 403 - permission error
            # 404 - resource not found
            # 422 - outdated key version
            return (False, response.json()['message'])
        else:
            raise RuntimeError(f"Unexpected status code '{response.status_code}': {response.text}")
