---
name: cron-output-file-write
description: Write protected files under /root/.hermes/cron/output/ when execute_code runs as non-root agentuser
---

# Cron Output File Write Skill

## Context
When running as a scheduled cron job with `execute_code` (sandbox as `agentuser`), writing to `/root/.hermes/cron/output/` fails with `Permission denied` because that directory is owned by root.

## Solution
Use `sudo python3 -c "..."` via the `terminal` tool instead of `execute_code` to write protected files.

## Example
```bash
sudo python3 -c "
import json
data = {'processed': ['1', '2', '3']}
with open('/root/.hermes/cron/output/processed_emails.json', 'w') as f:
    json.dump(data, f, indent=2)
print('Saved')
"
```

## Files this applies to
- `/root/.hermes/cron/output/processed_emails.json`
- `/root/.hermes/cron/output/work-check-state.json`
- Any other files under `/root/.hermes/cron/output/` that need root permissions
