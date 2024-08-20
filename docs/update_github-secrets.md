# update_github-secrets

manage all types of GitHub secrets in multiple repositories

## Purpose

The script `update_github-secrets` has been written because
  - updating the GitHub Actions secrets using GitHub CLI ('gh secret ...')
    is possible only at the repository and organizational level. Managing
    secrets in environments is not possible.
  - updating the secrets using the low level API('gh api ...') is possible
    but actually quite hard since the secret must be encrypted with the
    repository's public key before we can upload it. 

We now have a utility that makes it convenient to manage GitHub Actions,
Codespaces, Dependabot and Environments secrets in multiple repositories.

## Usage

```
# use defaults
update_github-secrets

# customize file locations
update_github-secrets -c ~/my/config.yaml -s ~/my/secrets.yaml -v

# need help?
update_github-secrets -h
```

## Configuration files

This scripts expects 2 config file with the following format:

configuration file (default location: `config/config.yaml`)
```
---
config:
  - owner: feeph
    repository: libtesta1-python
    environments:
      publish-to-pypi:
        secrets:
          - secret1
      publish-to-testpypi:
        secrets:
          - secret1
  - owner: feeph
    repository: libtesta2-python
    environments:
      publish-to-testpypi:
        secrets:
          - secret1
          - secret2
```

secrets file (default location: `config/secrets.yaml`)
```
---
secrets:
  secret1: "value1"
  secret2: "value2"
```
