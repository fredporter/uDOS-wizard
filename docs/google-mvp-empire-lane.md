# Wizard Google MVP Empire Lane

## Purpose

Define Wizard's provider-entry contract for the first Google MVP lane owned by
`uDOS-empire`.

Wizard does not own the remote service itself. Wizard owns:

- provider selection
- prompt generation
- extraction expectations
- budget-aware routing into the Google-backed generation lane

## Named Lane

- `Google MVP A: Firestore mirror + Cloud Run binder + gameplay world export`

## Wizard-Owned Entry Point

Primary route surfaces:

- `GET /ok/lanes/google-mvp-a`
- `GET /ok/lanes/google-mvp-a/prompt-template`
- `GET /ok/lanes/google-mvp-a/extraction-checklist`
- `GET /ok/lanes/google-mvp-a/generated-output-example`
- MCP tool: `ok.google_mvp.bundle`

Recommended provider path:

- `wizard.gemini`

Reason:

- multimodal and long-context support fit the bounded Google AI Studio planning
  and extraction lane

## Wizard Guardrails

- Firestore remains mirror storage only
- generated output must be extracted into repo-owned artifacts
- Ubuntu fallback and local cache behavior must remain intact
- provider ownership does not move into Empire or Ubuntu

## Required Extracted Outputs

- route list
- Firestore collection and field summary
- environment variable list
- auth model summary
- budget profile
- mirror-eligibility rules

## First Extracted Example

Wizard now publishes a first inspectable extracted-output example for this lane.

That example includes:

- route list
- Firestore collection summary
- environment variable list
- auth model
- budget profile
- uDOS mapping notes

## Repo Alignment

- `uDOS-empire` owns `Firestore mirror + Cloud Run binder supervision`
- `uDOS-gameplay` owns `multiplayer crypt-placement world`
- `uDOS-ubuntu` owns `always-on local mirror/cache host`
