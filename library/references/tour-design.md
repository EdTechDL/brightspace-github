# Guided-tour implementation contract

This is a design for a future tour renderer. It is not an installed extension, an executable adapter, or a format the Claude extension is known to consume automatically.

Use the same workflow ID for the written guide, real-page tour, and optional HTML exercise. Keep the explanation text and checks synchronized. The AI selects and interprets a workflow; a small renderer, if supported and institution-approved, can draw boxes and advance known steps without asking the AI to reconstruct the whole interface every time.

## Live-page tour

Each step needs a page guard, an observed target, a short title/explanation, and an expected resulting state. Resolve the target again after navigation or layout changes. An absent target or more than one match requires fresh inspection, not a coordinate fallback guessed from an old screenshot.

The renderer should draw a temporary red outline around the visible target and a readable explanation card with Back, Next, and Close controls. Keep keyboard focus usable, avoid covering the target, and remove the overlay on close. Reposition it on scroll and resize. Advance only after the required user action or observed transition. Drawing a box must not alter saved D2L content or submit a setting.

Automatic clicking is a separate capability and scope from displaying a tour. Begin with user-driven clicks. If the user asks for a demonstration, the browser assistant can perform permitted actions and narrate them while the renderer displays the matching step.

Complex components, nested frames, page transitions, and the browser's available tools must be checked against the actual D2L instance. Do not promise that a generic CSS script will handle all screens.

## HTML practice companion

Build selected, resettable exercises from the same workflow records. Label it a practice simulation with a list of supported behaviours and a comparison date. It cannot establish real permissions, real grade synchronization, or server-side outcomes. Use synthetic records and explicitly model the intended calculation rules. A local HTML copy of a saved D2L page does not include the operational LMS.

## Draft interchange example

The following JSON is intentionally not ready to execute. A browser adapter and actual target observation are missing.

```json
{
  "workflow_id": "quiz-special-access",
  "step_id": "open-special-access",
  "runtime_ready": false,
  "evidence": "official-docs",
  "institution_verified_at": null,
  "page_guard": {"course": null, "quiz": null, "section_text": "Availability Dates & Conditions"},
  "target": {"visible_label": "Manage Special Access", "observed_role": null, "observed_selector": null},
  "card": {"title": "An exception for this quiz", "text": "Open special access to set different dates, time limits, or attempts for selected learners."},
  "decoration": {"outline_color": "#c92323", "temporary": true},
  "advance": "user-action-and-state-check",
  "expected_next_text": "Add Users to Special Access",
  "on_missing_or_ambiguous_target": "reinspect"
}
```

Do not install a new extension or introduce a new service without the user's chosen institutional deployment route. The current user is limited to institution-approved extensions. Start with the existing browser assistant's supported capabilities and ordinary files.


## Implemented 2026-09-22 (MSU sandbox)

Live-page tour: the browser assistant's JavaScript tool injects `tutor-overlay.js` (this folder) on each page, drawing a temporary red outline and note card around a control found by visible text (light DOM and shadow DOM, including d2l-button-subtle `text` attributes). Verified by zoomed screenshots. Cleared before each click and lost on navigation, so re-inject per page. Nothing is saved to D2L.

Replay: `tours/gradebook-lab-msu.tour.json` plus `tours/player-template.html` and `tours/build_player.py` give an offline player with Play/Pause/Back/Next and a speed slider. Labelled a practice simulation. Tour JSON format is described in `tours/README.md`. The Codex pack (`d2l-capture/`) holds the observed UI inventory for a fuller simulator.
