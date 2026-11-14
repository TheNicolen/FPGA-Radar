"""Validate local inline Markdown links; skip external URLs and code blocks."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
errors = []
count = 0
files = list(ROOT.rglob('*.md'))
for path in files:
    if '.git' in path.parts:
        continue
    text = path.read_text(encoding='utf-8')
    text = re.sub(r'```.*?```', '', text, flags=re.S)
    for raw in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', text):
        target = raw.strip().split(' "', 1)[0].strip('<>')
        url = urlsplit(target)
        if url.scheme or url.netloc or not url.path:
            continue
        resolved = (path.parent / unquote(url.path)).resolve()
        if not resolved.is_relative_to(ROOT):
            errors.append(f'{path.relative_to(ROOT)}: outside repository: {target}')
        elif not resolved.exists():
            errors.append(f'{path.relative_to(ROOT)}: missing: {target}')
        count += 1
if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'OK: {len(files)} Markdown files, {count} local links. '
      'External URLs and anchors not checked.')
