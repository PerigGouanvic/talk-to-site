#!/usr/bin/env bash
set -e

REPO="periggouanvic/talk-to-site"
BASE="https://raw.githubusercontent.com/${REPO}/main"

FILES=(
  "scripts/generate_export.py"
  "scripts/ingest.py"
  ".github/workflows/generate-export.yml"
  ".github/workflows/ingest.yml"
  "_inbox/.gitkeep"
  "_includes/tts-button.html"
)

echo "Installing talk-to-site into $(pwd)"
echo ""

for file in "${FILES[@]}"; do
  dir=$(dirname "$file")
  mkdir -p "$dir"

  if [ -f "$file" ]; then
    echo "  SKIP (already exists): $file"
  else
    curl -fsSL "${BASE}/${file}" -o "$file"
    echo "  OK: $file"
  fi
done

echo ""
echo "Done. Next steps:"
echo ""
echo "  1. Edit scripts/generate_export.py"
echo "       — set SITE_URL"
echo "       — set COLLECTIONS (your Jekyll folder names)"
echo "       — describe your site in the AI instructions block"
echo ""
echo "  2. Edit scripts/ingest.py"
echo "       — set ALLOWED_PREFIXES to match your COLLECTIONS folders"
echo ""
echo "  3. Edit .github/workflows/generate-export.yml"
echo "       — set paths: to match your COLLECTIONS folders"
echo ""
echo "  4. Add to _config.yml:"
echo "       exclude:"
echo "         - scripts/"
echo ""
echo "  5. Add the download button to your navigation:"
echo "       {% include tts-button.html %}"
