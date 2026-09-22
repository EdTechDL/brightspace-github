# Brightspace assistant — review and limits

Reviewed 22 September 2026. Independent offline simulation, not a D2L product or an institution-certified replica.

## Evidence and coverage

The user-provided Course Administration screenshot is the visual reference for the 44-tool directory. Claude’s supplied pack provides 47 screen records, 759 controls, 17 menus, 13 dialogs, 200 transitions, and 114 explicitly unobserved entries. Of the transitions, 103 specify another captured screen. The records contain no destination screenshots, so their geometry, fonts, icons, and uncaptured behavior cannot be reproduced exactly.

The assistant includes 25 ticket references: 12 linked to a working tour, eight to captured-screen references, and five documentation-only cases. These are curated examples, not a claim of exhaustive ticket coverage. Ten working tours contain 32 steps. The recorded gradebook tour contains 20 steps.

The Course Administration screenshot corrects the original inventory grouping: Tools is a link under Administration; Learning Repository is the heading for Manage Repositories, Publish, and Search.

## Corrected source claims

- Eligible deleted Numeric, Selectbox, Pass/Fail, and Text grade items can be restored via **Manage Grades → More Actions → View Event Log → Restore**, subject to permissions. Deleting a category leaves its items outside that category. An associated item may need to be unlinked before deletion. [D2L event-log guidance](https://community.d2l.com/brightspace/kb/articles/34138-managing-event-logs-in-grade-book), [deletion guidance](https://community.d2l.com/brightspace/kb/articles/5190-delete-grade-items-or-categories).
- Numeric grading schemes map display values, while Selectbox Assigned Value percentages affect calculations. [D2L grading schemes](https://community.d2l.com/brightspace/kb/articles/34122-create-grading-schemes-using-the-grades-tool).
- A denominator such as /240 is not enough to diagnose the wrong grading system. Review course design, item structure, and display choices.
- Two grading-system save confirmations were reported at MSU; this is not a universal guarantee. The setting is reversible.
- Quiz special access uses the specific full time limit; course accommodations offer a multiplier or added minutes. The local model applies a quiz timing override first. Real Quiz Preview does not apply individual special access/accommodations.

The HTML replaces the affected recorded lesson text with reviewed wording. Original imported JSON is retained for traceability, not presented as unquestioned truth.

## Working-model boundaries

Numeric Points/Weighted calculations support blanks, entered zeros, exemptions, visibility versus exclusion, completed equal-item drops, supported bonus cases, caps, and adjusted-versus-calculated finals. Partial/unequal drop cases and incomplete weighted-bonus combinations explicitly report a limitation. Formula, Selectbox calculation, other grade types, activity grade transfer, registrar submission, automatic overdue zeros, real quizzes, uploads, and background tasks are not implemented.

Automatic release is implemented as a default for new local final records; existing release choices are preserved. Explicit Released checkboxes / Release All are available for existing learners. The wizard stages changes until Finish as a local implementation. Neither behavior is asserted as independently observed real-system persistence.

Module and assignment visibility/dates, assignment per-learner dates, and quiz timing are simplified. Full release conditions, sections/groups, rubric evaluation, content file trees, integrations, analytics, repository services, SSO, and backend authorization are not reproduced. Organization-wide admin exercises were not captured at MSU and must not be used to infer the user's real permissions.

## Validation

- 26 numeric model checks: points/weighted examples, blanks/zero, exemptions, hidden items, drops, bonus cases, caps, and unsupported-case reporting.
- 20 supplied calculation examples passed the UI self-check in the simulator.
- All 47 captured screens rendered in the Codex in-app browser.
- All 20 recorded targets resolved against their reconstructed HTML; the first ten were also exercised through the browser tool.
- Invalid tour version, missing screen, cyclic inheritance, unsupported block, and malformed structure were rejected. Captured text is escaped rather than executed.
- All 25 ticket IDs and referenced tour/screen/tool names validated; all 44 tool explanations match the menu directory. Example ticket matching checked.
- Browser checks covered optional explanation cards, ticket search, paired grading-system save confirmations, a 45-minute quiz exception, the corresponding simulated learner result, preserving a +15-minute accommodation across an enrollment save, and releasing an 82% calculated final followed by learner-view verification. Explanation placement was corrected so it did not cover the release checkbox or Save button.

Testing in the Codex in-app browser does not establish compatibility with every institutional browser policy or real Brightspace configuration. The artifact uses no external scripts, fonts, or network service. Documentation links open the web only when selected.

The in-app browser blocked direct file:// navigation, so a double-click launch was not verified there. Browser verification used the existing localhost development preview. The saved HTML is self-contained and contains no external script or stylesheet dependency.
