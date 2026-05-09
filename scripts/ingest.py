#!/usr/bin/env python3
"""Process files from _inbox/ and update site content."""

import os
import re
import sys
import glob

# CUSTOMIZE: list the folders the ingest script is allowed to write to.
# Should match the COLLECTIONS folders in generate_export.py.
ALLOWED_PREFIXES = (
    '_posts/',
    '_pages/',
)


def parse_file_blocks(content):
    """Extract (filepath, file_content) pairs from FILE block markers."""
    blocks = []
    pos = 0
    start_re = re.compile(r'^====FILE: (.+?)====\n', re.MULTILINE)

    while pos < len(content):
        start_match = start_re.search(content, pos)
        if not start_match:
            break

        filepath = start_match.group(1).strip()
        content_start = start_match.end()

        end_marker = f'====END: {filepath}===='
        end_pos = content.find(end_marker, content_start)

        if end_pos == -1:
            print(f'  WARNING: no END marker found for {filepath}, skipping')
            pos = content_start
            continue

        file_content = content[content_start:end_pos]
        blocks.append((filepath, file_content))
        pos = end_pos + len(end_marker)

    return blocks


def ingest():
    inbox_files = glob.glob('_inbox/*.md') + glob.glob('_inbox/*.txt')

    if not inbox_files:
        print('No inbox files found.')
        return []

    changes = []

    for inbox_file in inbox_files:
        print(f'Processing: {inbox_file}')

        with open(inbox_file, 'r', encoding='utf-8') as f:
            content = f.read()

        blocks = parse_file_blocks(content)

        if not blocks:
            print(f'  No FILE blocks found, skipping.')
            continue

        for filepath, file_content in blocks:
            if not any(filepath.startswith(p) for p in ALLOWED_PREFIXES):
                print(f'  BLOCKED (unauthorized path): {filepath}')
                continue

            if '..' in filepath or filepath.startswith('/'):
                print(f'  BLOCKED (unsafe path): {filepath}')
                continue

            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(file_content.rstrip('\n') + '\n')

            changes.append(filepath)
            print(f'  Written: {filepath}')

        os.remove(inbox_file)
        print(f'  Deleted: {inbox_file}')

    return changes


if __name__ == '__main__':
    changes = ingest()
    if not changes:
        print('No changes applied.')
        sys.exit(1)
    print(f'\n{len(changes)} file(s) updated:')
    for c in changes:
        print(f'  {c}')
