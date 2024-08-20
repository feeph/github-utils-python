#!/usr/bin/env python3
"""

update environment secrets for GitHub Actions

usage:
  update_github-secrets
  update_github-secrets -c config/config.yaml -s config/secrets.yaml
  update_github-secrets -h
"""

import argparse
import logging
import os
import subprocess
import sys

import yaml

import feeph.github_utils

LH = logging.getLogger('main')


def read_yaml_file(filename):
    try:
        LH.debug("Trying to read  file '%s'.", filename)
        with open(filename, 'r', encoding='UTF-8') as fh:
            return yaml.safe_load(fh)
    except FileNotFoundError as e:
        LH.error("Unable to read file '%s': %s", filename, e.strerror)
        sys.exit(1)
    except yaml.parser.ParserError as e:
        LH.error("Unable to parse YAML file '%s'! Please verify syntax.", filename)
        LH.error("%s", e)
        sys.exit(1)


def update_gha(gha: feeph.github_utils.Actions, config: list[str], secrets: dict[str, str]):
    try:
        for secret_name in config:
            is_success, error_msg = gha.update_secret(name=secret_name, value=secrets[secret_name])
            if is_success:
                LH.info("Successfully updated GitHub Actions secret '%s'.", secret_name)
            else:
                LH.warning("Failed to update GitHub Actions secret '%s': %s", secret_name, error_msg)
    except (AttributeError, TypeError) as e:
        LH.debug("Unable to process GitHub Actions config: %s", e)


def update_ghc(ghc: feeph.github_utils.Codespaces, config: list[str], secrets: dict[str, str]):
    try:
        for secret_name in config:
            is_success, error_msg = ghc.update_secret(name=secret_name, value=secrets[secret_name])
            if is_success:
                LH.info("Successfully updated GitHub Codespaces secret '%s'.", secret_name)
            else:
                LH.warning("Failed to update GitHub Codespaces secret '%s': %s", secret_name, error_msg)
    except (AttributeError, TypeError) as e:
        LH.debug("Unable to process GitHub Codespaces config: %s", e)


def update_ghd(ghd: feeph.github_utils.Dependabot, config: list[str], secrets: dict[str, str]):
    try:
        for secret_name in config:
            is_success, error_msg = ghd.update_secret(name=secret_name, value=secrets[secret_name])
            if is_success:
                LH.info("Successfully updated GitHub Dependabot secret '%s'.", secret_name)
            else:
                LH.warning("Failed to update GitHub Dependabot secret '%s': %s", secret_name, error_msg)
    except (AttributeError, TypeError) as e:
        LH.debug("Unable to process GitHub Dependabot config: %s", e)


def update_ghe(ghe: feeph.github_utils.Environments, config: list[str], secrets: dict[str, str], environment: str):
    try:
        for secret_name in config:
            is_success, error_msg = ghe.update_secret(environment=environment, name=secret_name, value=secrets[secret_name])
            if is_success:
                LH.info("Successfully updated GitHub Environment secret '%s' in environment '%s'.", secret_name, environment)
            else:
                LH.warning("Failed to update GitHub Environment secret '%s' in environment '%s': %s", secret_name, environment, error_msg)
    except (AttributeError, TypeError) as e:
        LH.debug("Unable to process GitHub Environment config for environment '%s': %s", environment, e)


def main():
    logging.basicConfig(format='%(levelname).1s: %(message)s', level=logging.INFO)

    parser = argparse.ArgumentParser(prog='update_github-secrets', description='update GitHub secrets from the command line')
    parser.add_argument('-c', '--config-file', type=str, default='config/config.yaml')
    parser.add_argument('-s', '--secrets-file', type=str, default='config/secrets.yaml')
    parser.add_argument('-v', '--verbose', action='store_true', help='raise log verbosity')
    args = parser.parse_args()

    if args.verbose:
        LH.setLevel(level=logging.DEBUG)

    github_pat = None
    if 'GITHUB_PAT' in os.environ:
        LH.info("Using environment variable 'GITHUB_PAT'.")
        github_pat = os.environ['GITHUB_PAT']
    else:
        LH.debug("Trying to acquire Personal Access Token using 'gh auth token'.")
        result = subprocess.run(['gh', 'auth', 'token'], check=True, stdout=subprocess.PIPE)
        LH.info("Using Personal Access Token provided by 'gh auth token'.")
        github_pat = result.stdout.rstrip().decode('utf-8')

    if github_pat is None:
        LH.error("Unable to acquire a GitHub Personal Access Token! Aborting.")
        LH.error("(please provide environment variable 'GITHUB_PAT' or use 'gh auth login')")
        sys.exit(1)

    config = read_yaml_file(args.config_file)
    LH.info("Using configuration file '%s'.", args.config_file)

    secrets = read_yaml_file(args.secrets_file)
    LH.info("Using secrets file '%s'.", args.secrets_file)

    for record in config:
        owner = record['owner']
        repository = record['repository']

        LH.info("Processing repository '%s/%s'.", owner, repository)
        if 'actions' in record:
            gha = feeph.github_utils.Actions(owner=owner, repository=repository, github_pat=github_pat)
            cfg = record['actions'].get('secrets', [])
            update_gha(gha, config=cfg, secrets=secrets)
        if 'codespaces' in record:
            ghc = feeph.github_utils.Codespaces(owner=owner, repository=repository, github_pat=github_pat)
            cfg = record['codespaces'].get('secrets', [])
            update_ghc(ghc, config=cfg, secrets=secrets)
        if 'dependabot' in record:
            ghd = feeph.github_utils.Dependabot(owner=owner, repository=repository, github_pat=github_pat)
            cfg = record['dependabot'].get('secrets', [])
            update_ghd(ghd, config=cfg, secrets=secrets)
        if 'environments' in record:
            for ev_name, ev_record in record['environments'].items():
                ghe = feeph.github_utils.Environments(owner=owner, repository=repository, github_pat=github_pat)
                cfg = ev_record.get('secrets', [])
                update_ghe(ghe, config=cfg, secrets=secrets, environment=ev_name)


if __name__ == '__main__':
    main()
