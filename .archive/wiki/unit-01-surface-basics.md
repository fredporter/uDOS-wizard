# Unit 01: Surface Basics

This unit introduces the `uDOS-surface` browser layer and the retained
`Wizard` broker role.

## What You Should Learn

- what Surface owns
- what Wizard still owns
- how to launch the local compatibility host
- how to verify the browser and broker lanes are alive

## Short Practical How-To

1. Validate the repo.

```bash
bash scripts/run-surface-checks.sh
```

2. Start the local host.

```bash
.venv/bin/udos-surface-demo
```

3. Open the main browser lane.

```text
http://127.0.0.1:8787/app
```

4. Verify the broker registry.

```text
http://127.0.0.1:8787/wizard/services
```

## Editable Demo Script

Use this as the smallest repeatable launch script:

```bash
#!/usr/bin/env bash
set -euo pipefail

bash scripts/run-surface-checks.sh
.venv/bin/python -m wizard.main
```

Change the final command to `uvicorn wizard.main:app --host 127.0.0.1 --port 8787`
if you want explicit bind control.

## Outcome Check

You should be able to answer these before moving on:

1. Which component owns browser rendering and operator pages?
   Surface.
2. Which component owns family request brokering?
   Wizard.
3. Which component owns managed OK, MCP, network policy, and host runtime authority?
   Ubuntu.
4. Which route lists broker-visible services?
   `GET /wizard/services`

## Pass Condition

Pass this unit when you can launch the local host, open `/app`, and confirm
that `/wizard/services` returns a service list.
