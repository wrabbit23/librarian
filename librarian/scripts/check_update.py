#!/usr/bin/env python3
"""Check Librarian's public release using anonymous curl; never install updates."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
URL = 'https://raw.githubusercontent.com/wrabbit23/librarian/main/release.json'


def version(value):
    if not isinstance(value, str) or not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', value):
        raise ValueError('invalid release version')
    return tuple(map(int, value.split('.')))


def check(local, release):
    installed = version(local)
    if not isinstance(release, dict) or release.get('name') != 'librarian' or release.get('skill_path') != 'librarian':
        raise ValueError('unexpected release identity or skill path')
    available = version(release.get('version'))
    if not isinstance(release.get('commit'), str) or not re.fullmatch(r'[0-9a-fA-F]{40}', release['commit']):
        raise ValueError('invalid payload commit')
    status = 'update_available' if available > installed else 'current' if available == installed else 'upstream_older'
    return dict(status=status, installed_version=local, available_version=release['version'], commit=release['commit'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('installed_version', nargs='?', help='override installed version; otherwise read references/updates.md')
    parser.add_argument('--boolean', action='store_true', help='print true if newer, false otherwise; failure exits 2')
    args = parser.parse_args()
    try:
        local = args.installed_version
        if local is None:
            text = (ROOT / 'references/updates.md').read_text()
            match = re.search(r'^- Version: ([0-9]+\.[0-9]+\.[0-9]+)$', text, re.M)
            if not match:
                raise ValueError('installed version missing')
            local = match.group(1)
        version(local)
        # Ignore user curl configuration; send no credentials, cookies, or local data.
        result = subprocess.run(['curl', '--disable', '--fail', '--silent', '--show-error',
            '--proto', '=https', '--connect-timeout', '10', '--max-time', '25', URL],
            capture_output=True, text=True, timeout=30)
        if result.returncode:
            raise RuntimeError(f'curl exit {result.returncode}: {result.stderr.strip()}')
        outcome = check(local, json.loads(result.stdout))
        print(json.dumps(outcome['status'] == 'update_available') if args.boolean else json.dumps(outcome))
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(json.dumps(dict(status='unavailable', method='curl', reason=str(exc))), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
