# Unit 01: Wizard Basics

## What This Module Is

`uDOS-wizard` is the **orchestration and browser operator** lane: MCP adapters,
workflow execution, and the dev-time HTTP surface that presents operator UI. It
is **not** the long-running command-centre host (that is **`uDOS-ubuntu`**).

## What You Should Learn

By the end of this unit you should be able to:

- separate **Wizard broker / operator UI** from **Ubuntu runtime host**
- point to where preview vs controlled execution is documented
- find how Wizard delegates to host surfaces per family contracts

## Practical How-To

1. Read the doc index and architecture.

```text
docs/README.md
docs/architecture.md
docs/getting-started.md
```

2. Read the Core boundary for Wizard vs host (in the **`uDOS-core`** checkout).

```text
docs/wizard-surface-delegation-boundary.md
```

3. Run the repo checks from the Wizard root (see `docs/README.md` for the exact commands your checkout documents).

## Quick Check

You pass this unit if you can answer:

- Which repo owns **primary** command-centre uptime on a workstation?
- What does Wizard own that Ubuntu does not?
- Where is **delegation** to a host surface described?

## See Also

- **`uDOS-surface`** `wiki/unit-01-surface-basics.md` — browser-facing Surface layer
- **`docs/gui-system-family-contract.md`** (in `uDOS-dev`) — shared GUI vocabulary
