---
name: cron-bash-script-syntaxerror
description: Fix cron jobs that fail running bash scripts as if they were Python
category: devops
---

# Cron Job: Running Bash Scripts vs Python Scripts

## Problem
When a cron job runs a `.sh` script that has `#!/bin/bash` shebang, the system may try to parse it as Python and throw:
```
File "/path/to/script.sh", line 7
    TIMESTAMP=$(date '+%Y-%m-%d_%H%M')
              ^
SyntaxError: invalid syntax
```

## Root Cause
The cron runner (`hermes-scripts`) defaults to `python3` when executing script files, regardless of the shebang line. Bash scripts with command substitutions like `$(...)` are valid bash but invalid Python syntax.

## Solution

**Option A — Use `bash` explicitly** (preferred if script is straightforward bash):

In the cron job `prompt`, invoke bash explicitly:
```bash
bash /home/agentuser/.hermes/scripts/cuwa-2026-watch.sh 2>&1
```

**Do NOT** use:
- `python3 /path/to/script.sh` — will parse bash as Python
- `/path/to/script.sh` (unqualified) — depends on runner implementation

**Option B — Rewrite as pure Python** (when bash heredocs or complex bash-isms are involved):

If the script embeds Python via bash heredocs (`<< 'PYEOF'`), rewriting as pure Python avoids the interpreter conflict entirely:

```python
#!/usr/bin/env /home/agentuser/.camoufox-venv/bin/python3
"""Script description"""
import sys
sys.path.insert(0, '/home/agentuser/.camoufox-venv/lib/python3.12/site-packages')
from camoufox.sync_api import Camoufox
# ... rest of script
```

Key fixes when converting:
1. Change shebang to the correct venv Python: `#!/usr/bin/env /home/agentuser/.camoufox-venv/bin/python3`
2. Remove all bash command substitutions `$(...)` — convert to Python `os.popen()` or inline Python
3. Use Python's own heredoc equivalent or write the Python code directly at the top level
4. Replace `echo "..." >> "$LOGFILE"` with Python file writes

## Verification
```bash
# Check shebang
head -1 /path/to/script.sh
# Should show: #!/bin/bash

# Confirm it's valid bash
file /path/to/script.sh
# Should show: Bourne-Again shell script

# Run correctly
bash /path/to/script.sh
```

## Actual Error Encountered (2026-04-24)
```
File "/home/agentuser/.hermes/scripts/cuwa-2026-watch.sh", line 7
    TIMESTAMP=$(date '+%Y-%m-%d_%H%M')
              ^
SyntaxError: invalid syntax
```
The script had a bash heredoc embedding Python (`<< 'PYEOF'`), with bash `$(...)` command substitution on line 7 — Python couldn't parse the bash syntax inside the heredoc. Fixed by rewriting as pure Python with correct venv shebang.

## Applies To
- All `.sh` scripts with `#!/bin/bash` shebang
- Scripts using bash-isms: `$()`, `[[]]`, `source`, pipe to python heredoc
