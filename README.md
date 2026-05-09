# talk-to-site

Export your static site content as a single plain-text file for AI editing, then ingest changes back automatically via GitHub Actions.

**The idea:** tap the download button on your phone, upload the file to any AI, share an idea, get a FILE block back, commit it to `_inbox/` — the site updates itself.

---

## How it works

| | |
|---|---|
| `/out.txt` | Your entire site content in one plain-text file, with instructions for the AI |
| `_inbox/` | Drop FILE blocks here — GitHub Actions applies them to your source files |

### Full workflow

1. Tap the **Export IA** button on your site → downloads `out.txt`
2. Upload the file to Claude, ChatGPT, or any AI
3. Share an idea → the AI reads the existing content, finds where it fits, drafts a FILE block
4. Commit the FILE block to `_inbox/` → GitHub Actions writes the file and rebuilds the export

Partial updates are accepted — the inbox only needs the files you're adding or changing.

---

## Installation (Jekyll)

### 1. Run the install script

From the root of your Jekyll repo:

```bash
curl -fsSL https://raw.githubusercontent.com/periggouanvic/talk-to-site/main/install.sh | bash
```

This copies the following files without overwriting anything that already exists:

```
scripts/generate_export.py
scripts/ingest.py
.github/workflows/generate-export.yml
.github/workflows/ingest.yml
_inbox/.gitkeep
_includes/tts-button.html
```

### 2. Customize `scripts/generate_export.py`

Edit the two sections at the top:

```python
# Your Jekyll collection folders
COLLECTIONS = [
    ('_posts',      'Posts'),
    ('_definitions', 'Definitions'),
    # ...
]

SITE_URL = 'https://yoursite.com'
```

Then replace the `# CUSTOMIZE` instruction block with a description of your site: its thesis, what each section is for, and the editorial voice you want the AI to maintain.

### 3. Customize `scripts/ingest.py`

Update `ALLOWED_PREFIXES` to match your collection folders:

```python
ALLOWED_PREFIXES = (
    '_posts/',
    '_definitions/',
    # ...
)
```

### 4. Customize `.github/workflows/generate-export.yml`

Update the `paths:` trigger to match your collection folders:

```yaml
paths:
  - '_posts/**'
  - '_definitions/**'
```

### 5. Exclude `scripts/` from Jekyll

In `_config.yml`:

```yaml
exclude:
  - scripts/
```

### 6. Add the download button (optional)

Copy `_includes/tts-button.html` into your site, then drop it wherever you want the button to appear — typically in your navigation or header:

```liquid
{% include tts-button.html %}
```

This renders a simple `<a href="/out.txt" download>` link. Style it with `.tts-button` in your CSS, or replace the label with whatever fits your site.

### 7. Push and merge

The export generates automatically on first push. Your content will be live at `/out.txt`.

---

## FILE block format

```
====FILE: _posts/my-new-post.md====
---
title: "My New Post"
date: 2026-01-01
---

Content in Markdown...
====END: _posts/my-new-post.md====
```

- Works for both **new** and **existing** files
- Include multiple FILE blocks in a single inbox submission
- The inbox file is deleted automatically after processing

## Security

The ingest script only writes to folders listed in `ALLOWED_PREFIXES`. Path traversal attempts (`..`, absolute paths) are blocked.

---

## Other static site generators

The scripts are plain Python and read/write Markdown files — they work with Hugo, Eleventy, or any generator. Adapt `COLLECTIONS` to your folder structure.
