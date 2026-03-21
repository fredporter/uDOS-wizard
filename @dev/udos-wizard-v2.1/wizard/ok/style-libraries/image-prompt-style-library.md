# Image Prompt Style Library

## Purpose

This library defines reusable visual prompt families for Wizard-managed OK Diagrammer and OK Publisher outputs.

It supports deterministic prompt packing for:

- promotional scenes
- binder story scenes
- technical cutaways
- shell or kiosk visuals
- teletext-inspired layouts
- hybrid diagrammatic illustration

## Required prompt fields

Every prompt pack should declare:

- `style_id`
- `mode` (`diagrammatic` | `decorative`)
- `subject`
- `purpose`
- `composition`
- `viewpoint`
- `visual_era`
- `medium`
- `palette`
- `line_quality`
- `detail_level`
- `background_treatment`
- `text_policy`
- `reconstructable`
- `output_ratio`
- `transparency`
- `negative_constraints`
- `binder_tags`

## Global rules

- Prefer diagram output before decorative image output.
- If the output is technical, keep it reconstructable.
- Avoid unreadable embedded text unless the renderer explicitly supports it.
- Treat decorative images as secondary to text and SVG truth.
- Use concise prompt tags and stable style identifiers.

## Style families

### udos-technical-clean

Purpose:
- architecture diagrams
- clean technical concepts
- cutaways
- system illustrations

Defaults:
- mode: `diagrammatic`
- medium: `vector technical illustration`
- palette: `muted grayscale with restrained accent`
- line_quality: `precise uniform strokes`
- text_policy: `minimal labels only`
- reconstructable: `true`

Tags:
- `technical`
- `clean`
- `vector`
- `diagram`
- `cutaway`

### udos-teletext-retro

Purpose:
- retro info pages
- kiosk page concepts
- broadcast menu screens
- panel title cards

Defaults:
- mode: `diagrammatic`
- medium: `teletext block graphic`
- palette: `high-contrast retro limited palette`
- line_quality: `blocky grid edges`
- text_policy: `large block-safe headings only`
- reconstructable: `true`

Tags:
- `teletext`
- `retro`
- `grid`
- `broadcast`
- `panel`

### udos-shell-panel

Purpose:
- shell UI mockups
- terminal overlays
- system dashboard visualisation

Defaults:
- mode: `diagrammatic`
- medium: `flat panel interface graphic`
- palette: `dark shell tones with restrained signal accents`
- line_quality: `sharp UI edges`
- text_policy: `UI labels allowed`
- reconstructable: `true`

Tags:
- `shell`
- `ui`
- `panel`
- `dashboard`
- `terminal`

### udos-binder-atlas

Purpose:
- binder maps
- world overlays
- artifact map pages
- mission routing visuals

Defaults:
- mode: `diagrammatic`
- medium: `atlas page illustration`
- palette: `paper, ink, restrained highlight colours`
- line_quality: `map-grade linework`
- text_policy: `labels allowed`
- reconstructable: `true`

Tags:
- `binder`
- `atlas`
- `map`
- `routing`
- `world`

### udos-kiosk-broadcast

Purpose:
- home kiosk views
- broadcast info screens
- stream menu graphics

Defaults:
- mode: `decorative`
- medium: `broadcast-style flat poster`
- palette: `vivid controlled accent palette`
- line_quality: `clean bold poster edges`
- text_policy: `headline only`
- reconstructable: `false`

Tags:
- `kiosk`
- `broadcast`
- `poster`
- `stream`
- `display`

### udos-diagrammatic-cutaway

Purpose:
- exploded systems
- layer breakdowns
- spatial technical views

Defaults:
- mode: `diagrammatic`
- medium: `technical cutaway illustration`
- palette: `soft neutral base with selective coded accents`
- line_quality: `fine engineered linework`
- text_policy: `small technical labels`
- reconstructable: `true`

Tags:
- `cutaway`
- `exploded`
- `system`
- `layered`
- `technical`

### udos-story-scene

Purpose:
- binder atmosphere
- gameplay/world scenes
- promo narrative frames

Defaults:
- mode: `decorative`
- medium: `cinematic concept art`
- palette: `story-driven`
- line_quality: `scene appropriate`
- text_policy: `no embedded text`
- reconstructable: `false`

Tags:
- `story`
- `scene`
- `atmospheric`
- `concept`
- `narrative`

## Prompt pack template

```yaml
style_id: udos-technical-clean
mode: diagrammatic
subject: "Wizard provider routing control plane"
purpose: "Explain managed provider routing in uDOS v2.1"
composition: "front-on technical layout with labeled routing stages"
viewpoint: "orthographic"
visual_era: "contemporary technical manual"
medium: "vector technical illustration"
palette: "muted grayscale with restrained accent"
line_quality: "precise uniform strokes"
detail_level: "medium"
background_treatment: "plain light background"
text_policy: "minimal labels only"
reconstructable: true
output_ratio: "16:9"
transparency: false
negative_constraints:
  - "no photorealism"
  - "no clutter"
  - "no ornamental gradients"
binder_tags:
  - wizard
  - routing
  - control-plane
```
