import json, subprocess
from pathlib import Path
import nbformat
files = subprocess.check_output(['git', 'ls-files', '-z']).decode().split('\0')
checked = 0
for name in filter(None, files):
    p = Path(name)
    if not p.is_file():
        raise SystemExit(f'Missing tracked file: {name}')
    if p.suffix == '.ipynb':
        nbformat.validate(nbformat.read(p, as_version=4))
        checked += 1
    elif p.suffix == '.json':
        json.loads(p.read_text(encoding='utf-8-sig'))
    elif p.suffix == '.pdf' and p.read_bytes()[:5] != b'%PDF-':
        raise SystemExit(f'Invalid PDF header: {name}')
print(f'Archive integrity passed; {checked} notebooks validated, not executed.')
