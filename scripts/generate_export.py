#!/usr/bin/env python3
"""Generate a single-file export of all site content for AI-assisted editing."""

import os
import glob
import subprocess
from datetime import datetime, timezone

# CUSTOMIZE: list your Jekyll collection folders and their human-readable names
COLLECTIONS = [
    ('_posts',      'Posts'),
    ('_pages',      'Pages'),
]

# CUSTOMIZE: your site URL
SITE_URL = 'https://yoursite.com'

# CUSTOMIZE: allowed folders for the ingest script (should match COLLECTIONS folders)
# Also update ALLOWED_PREFIXES in scripts/ingest.py to match.

SEP = '=' * 72


def get_git_sha():
    try:
        sha = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], stderr=subprocess.DEVNULL
        ).decode().strip()
        return sha[:12]
    except Exception:
        return 'unknown'


def get_file_mtime(filepath):
    try:
        ts = os.path.getmtime(filepath)
        return datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    except Exception:
        return 'unknown'


def generate_export():
    date = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    sha = get_git_sha()

    lines = [
        '---',
        'layout: none',
        'permalink: /out.txt',
        '---',
        f'# {SITE_URL.replace("https://", "").upper()} — CONTENT EXPORT',
        f'# Site:      {SITE_URL}',
        f'# Generated: {date}',
        f'# Commit:    {sha}',
        '#',
        '# IMPORTANT: Before proposing any changes, verify that this export',
        f'# matches the current state of the site (commit {sha}, {date}).',
        '# If you have an older copy, ask for a fresh export before editing.',
        '#',
        SEP,
        '# INSTRUCTIONS FOR THE AI READING THIS FILE',
        SEP,
        '#',
        # CUSTOMIZE: replace the lines below with a description of your site,
        # its purpose, editorial voice, and what each section is for.
        '# You are an editorial assistant for this site.',
        '# [CUSTOMIZE: describe the site thesis and purpose here]',
        '#',
        '# YOUR ROLE:',
        '#   When the user shares an idea, a reference, or a rough thought:',
        '#   1. Read the existing content below to understand what already exists.',
        '#   2. Identify where the idea fits: an existing page to enrich,',
        '#      a new page in an existing section, or a new section.',
        '#   3. Propose additions or modifications using FILE blocks (see format below).',
        '#   4. Preserve the editorial voice of the site.',
        '#',
        '# SITE SECTIONS AND THEIR PURPOSE:',
        # CUSTOMIZE: describe each section/collection
        '#   [CUSTOMIZE: describe each folder and what belongs in it]',
        '#',
        '# HOW TO PROPOSE A CHANGE OR NEW PAGE:',
        '#   Use FILE blocks. Partial updates are accepted — include only the',
        '#   files you are creating or modifying, not the entire export.',
        '#',
        '#   To modify an existing page, use its exact path from the list below.',
        '#   To create a new page, use a new path in the appropriate folder.',
        '#   The site updates automatically when the FILE block is committed to _inbox/.',
        '#',
        '# FILE BLOCK FORMAT:',
        '#',
        '#   ====FILE: _posts/my-new-post.md====',
        '#   ---',
        '#   title: "My New Post"',
        '#   ---',
        '#',
        '#   Content in Markdown...',
        '#   ====END: _posts/my-new-post.md====',
        '#',
        '# NOTE: existing files show "| last modified: <date>" in their header.',
        '# Omit that annotation when writing a FILE block — it is metadata only.',
        '#',
        '# ALLOWED FOLDERS: ' + '  '.join(f'{f}/' for f, _ in COLLECTIONS),
        '#',
        SEP,
        '',
    ]

    for folder, section_title in COLLECTIONS:
        if not os.path.isdir(folder):
            continue
        files = sorted(glob.glob(f'{folder}/*.md'))
        if not files:
            continue

        lines.append(SEP)
        lines.append(f'# {section_title}')
        lines.append(SEP)
        lines.append('')

        for filepath in files:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            mtime = get_file_mtime(filepath)
            lines.append(f'====FILE: {filepath} | last modified: {mtime}====')
            lines.append(content.rstrip('\n'))
            lines.append(f'====END: {filepath}====')
            lines.append('')

    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    os.makedirs('out', exist_ok=True)
    export = generate_export()
    output_path = 'out/index.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(export)
    size_kb = len(export.encode('utf-8')) / 1024
    print(f'Export generated: {output_path} ({size_kb:.1f} KB)')
