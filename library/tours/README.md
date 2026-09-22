# Tour kit: replayable Brightspace walkthroughs

Purpose: turn a live tutoring session (red boxes and note cards drawn on the real D2L page) into a file you can replay offline, like a video with a pause button, as many times as you like. Everything in this folder is a **practice simulation**. It proves nothing about D2L on its own; the tour JSON records which steps were verified live and on what date.

## Files

- `gradebook-lab-msu.tour.json`: the tour. Screens (simplified rebuilds of the D2L pages seen) plus steps (control label, note card, action, expected next screen, evidence).
- `player-template.html`: the player. Renders any tour JSON: Play / Pause / Back / Next / Restart, seconds-per-step slider, progress bar, transcript, keyboard shortcuts (Space, arrows, R). Also has "Load another tour file" so one player serves every tour.
- `build_player.py`: inlines a tour JSON into the template so the result opens by double-click with no server. `python3 build_player.py gradebook-lab-msu.tour.json gradebook-lab-player.html`
- `gradebook-lab-player.html`: the built, ready-to-open result.
- `../references/tutor-overlay.js`: the script the browser assistant injects on the real D2L page to draw the same red box and card (temporary, page-local, saves nothing). Kept here so live and local visuals match.

## Tour JSON format (schema_version 1)

Top level: `tour_id`, `title`, `recorded` (date), `environment` (institution, origin, course, ui, role label), `evidence` (sentence), `limitations` (list), `screens`, `steps`.

`screens`: an object keyed by screen id. Each screen has `blocks`, or `extends` another screen with optional `add` (extra blocks appended) and `patch` (edit the nth block of a type, e.g. `"radios:0": {"selected": "Points"}`).

Block types the player understands: `tooltabs` (items, active, right), `tabs` (items, active), `h1`, `h2`, `label`, `text`, `kv` (items: [[key, value]]), `buttons` (items: [{label, primary, caret}]), `note`, `link`, `table` (columns, rows, checkbox), `radios` (options, selected, descriptions), `checkbox` (label, checked), `field` (label, value, wide), `linklist` (items), `menu` (anchor, items: an open dropdown under a button in the last buttons row), `dialog` (title, text, buttons), `toast` (text).

`steps`: an ordered list. Each step: `id`, `section`, `screen`, `target` (the exact visible label; use `dialog:Label` for a dialog button and `menu:Label` for a menu item when the same label also exists on the page), `title`, `card` (lines starting with WHAT:, WHY:, TICKET:, NEXT:, CAUTION:, CHECK: are bolded), `action` (click | look | type), `actionLabel`, `next` (screen id or null), `evidence` (live | official-docs | proposed).

## Adding a new tour

1. During a live session, record each step as it is performed: exact label, page, card text, and what the screen showed next.
2. Describe each screen with the block types above. Reuse `extends` for small state changes (a menu opened, a dialog shown, a radio changed).
3. Run `build_player.py`. Open the HTML. Step through with Next and fix any card that says "target not found".
4. Mark evidence honestly. A step that was never performed in the real course stays `official-docs` or `proposed`.

## Why not Remotion, and when it would help

Remotion renders React components to MP4. It needs a Node project, a build step and a re-render for every edit. The player gives the same "watch it like a video" experience with a pause on every card, opens offline, and updates by editing JSON. If a real video file is ever required (for an LMS help page, say), either screen-record the player at the chosen speed, or write a small Remotion composition that reads the same tour JSON and animates the box and card per step. The JSON is the reusable part.

## Would a Claude Project help

Only as a home for this kit and the reference library, so future conversations produce tours in the same format without re-explaining it. Put in it: SKILL.md, the references folder, this README, the template, the build script and the existing tour JSON files. No further documentation is needed.
