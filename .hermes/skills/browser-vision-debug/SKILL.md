---
name: browser-vision-debug
description: Diagnose and fix browser_vision failures in Hermes Agent — "No LLM provider configured for task=vision"
---

# Browser Vision Debug Skill

## Trigger
`browser_vision` fails with `"No LLM provider configured for task=vision provider=auto"`, or image analysis tools return empty/None results.

## Diagnostic Workflow

### Step 1: Verify browser itself works
Python check (run in hermes-agent venv):
```python
import sys; sys.path.insert(0, '/home/agentuser/.hermes/hermes-agent')
from tools.browser_tool import browser_navigate
result = browser_navigate('https://www.baidu.com')
print(result[:300] if isinstance(result, str) else result)
```
- If this succeeds → browser backend (camoufox) is fine
- If this fails → fix browser backend first

### Step 2: Check camoufox service is running
```bash
curl -s http://localhost:9377/health
ps aux | grep camouf | grep -v grep
```

### Step 3: Check vision provider availability
Python check (run in hermes-agent venv):
```python
import sys; sys.path.insert(0, '/home/agentuser/.hermes/hermes-agent')
from agent.auxiliary_client import (
    _strict_vision_backend_available,
    resolve_vision_provider_client,
)

for p in ['minimax-cn', 'openrouter', 'google', 'nous', 'codex']:
    print(f'{p}: {_strict_vision_backend_available(p)}')

prov, client, model = resolve_vision_provider_client()
print(f'resolve_vision_provider_client: prov={prov}, client={type(client)}, model={model}')
```

### Step 4: Check credential pool
```python
import json
print(json.load(open('/home/agentuser/.hermes/auth.json')))
```
- Empty `credential_pool` → no API keys configured
- MiniMax API key not in pool → vision won't work even if main chat works

### Step 5: Check config
Read file `/home/agentuser/.hermes/config.yaml` directly (do NOT pipe to grep in shell — security scan blocks it). Look for:
- `model:` setting
- `auxiliary:` section with `vision:` config

## Known Root Causes

| Cause | Symptom | Fix |
|-------|---------|-----|
| No API key configured | credential pool empty, all `_strict_vision_backend_available` return False | Run `hermes setup` |
| Wrong provider | MiniMax in pool but no vision endpoint | Use OpenRouter+Gemini or Google AI Studio |
| hermes setup never run | Fresh install, providers: {} in config | Run `hermes setup` |

## Fix

Run interactive setup to configure a vision-capable provider:
```bash
cd /home/agentuser/.hermes/hermes-agent && source venv/bin/activate && hermes setup
```

Choose a provider with vision support:
- **OpenRouter** + `google/gemini-3-flash-preview` (free tier available)
- **Google AI Studio** + Gemini API key
- **Nous** (if OAuth configured)

## Verification
After fix, run this Python check:
```python
import sys; sys.path.insert(0, '/home/agentuser/.hermes/hermes-agent')
from tools.browser_tool import browser_navigate, browser_vision
browser_navigate('https://www.baidu.com')
result = browser_vision('What is on this page?')
print(result[:200])
```
Should return JSON with `success: true` and vision analysis.

## Key Code Paths
- `tools/browser_tool.py` — `browser_vision()` calls `call_llm()` via `agent/auxiliary_client.py`
- `agent/auxiliary_client.py` — `_resolve_strict_vision_backend()` checks all backends; `_strict_vision_backend_available()` for probe
- `tools/vision_tools.py` — `vision_analyze_tool` also uses `resolve_vision_provider_client()`
- Camoufox at `http://localhost:9377` (xvfb + Firefox in headless mode)
- Config: `/home/agentuser/.hermes/config.yaml`
- Auth: `/home/agentuser/.hermes/auth.json`
