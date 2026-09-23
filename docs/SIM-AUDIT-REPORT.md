# Brightspace Practice Simulator: Audit and Improvement Brief

**For:** the coding agent maintaining `EdTechDL/brightspace-github` (deployed at brightspace-github.vercel.app)
**Audited:** 2026-09-23, against repo HEAD `daf9c6c` and the live deployment, compared read-only with the real MSU sandbox course "Same Playground" (d2l.msu.edu, org unit 2747167)
**Method:** (1) read the source, (2) ran a headless browser coverage audit that calls `explanationFor()` on every visible control of every route, grade tab, dialog and captured screen, (3) clicked through Explain clicks and Walkthroughs by hand, (4) compared page layouts with the live D2L course (view only, nothing saved).

---

## 0. What the product must become (the definition of done)

The person using this is a **new learning technology support hire** who will answer tickets from professors about any D2L menu or setting. They know a general LMS at a basic level but not D2L.

The owner's requirement, in her words: *they should be able to click on anything and see what its purpose is and how it can be used, so that by the end of their exploration, regardless of which path they take, they are experts in all D2L settings.*

Translate that into five testable rules:

1. **Every visible control is teachable.** With Explain clicks on, clicking ANY button, link, tab, menu item, radio option, checkbox, select option, text field, chevron, or icon on ANY page, dialog, or menu shows a red-outlined explanation card anchored to that element. No dead clicks. No disabled controls that swallow the click.
2. **Cards teach at option level.** A radio group explains the specific option clicked (Weighted vs Points vs Formula), not the group in general.
3. **The interface matches Same Playground.** Same page structure, button order, labels, tabs, menus, and dialogs as the real MSU course, so muscle memory transfers.
4. **Walkthroughs are hand-held.** Step by step, one element at a time, including inside dialogs and menus, advancing when the learner performs the click, the way a person sitting beside them would teach.
5. **Coverage is enforced by a test.** The build fails if any control lacks a teaching card.

Writer's note for all in-app text: assume the reader has basic LMS familiarity and define every D2L-specific term (org unit, release conditions, special access, grade item vs grade category, etc.). **Do not mention any other LMS by name in the UI.**

---

## 1. Headline findings

| # | Finding | Evidence | Severity |
|---|---|---|---|
| F1 | **Live site is stale.** Vercel is serving an older build. | Live page: 47 captured screens, 510,802-byte script, no `CAPTURE_GS` / `TOOL_NOTES`. Repo HEAD builds 752,424 bytes with 85 screens and the Gradescope library. | P0 |
| F2 | **Explain clicks only teaches about 28% of controls outside the captured library.** | 463 visible controls across all routes, grade tabs, and dialogs: 131 taught, 18 capture-note only, 314 nothing. Even on the course-tool pages alone (excluding Admin Tools and training pages) it is 130 of 236 (55%), and most of those 130 are the Grades settings and the 44 Course Admin links. | P0 |
| F3 | **Captured MSU screens teach about 9%.** | 883 controls across the 85 captured screen bodies: 83 taught, 292 capture-note only, 508 nothing. **0 of 82 radio buttons and 0 of 170 text fields** are taught. | P0 |
| F4 | **87% of captured-screen controls are `disabled`.** Disabled elements never dispatch `click`, so Explain mode cannot fire even if help existed. | 764 of 883 captured controls have `disabled=true`. Same on practice pages (Import, Export, Switch to Spreadsheet View, More Actions, Change Role, Bookmarks, Formula radio, Auto zero checkbox, and more). | P0 |
| F5 | **The "capture-note" fallback is not teaching.** It shows capture metadata such as "home icon; accessible name not captured", "menu not opened", "control type not recorded", with generic steps "Read the recorded control and its notes on this reference screen." | `explain.js`, last branch of `explanationFor()`. Median note length 38 characters. | P0 |
| F6 | **38 of 44 Course Admin tools are dead ends.** Clicking Rubrics, Discussions, Groups, etc. opens "The destination and its behavior have not been modeled", although the repo now contains captured screens for those 38 destinations. | `mappedTools` in `grade-ui.js` maps only Assignments, Grades, Quizzes, Classlist. | P0 |
| F7 | **Practice pages do not look like Same Playground.** Quizzes, Assignments, Classlist, Content, and Home are simplified card layouts with different buttons, columns, and order. Captured screens render as grouped text blocks with "Capture note" toggles, not as D2L pages. | Side-by-side comparison, section 4. | P0 |
| F8 | **Walkthroughs are narrative, not hand-held.** 10 walkthroughs, 32 steps total. Each step outlines a whole region (for example the entire quiz list) and puts several instructions in one paragraph. The learner never clicks the real control; Next teleports to another page. Steps never enter a dialog or menu. | `data/workflows.json`; step 1 of "Give one learner extra quiz time" tells the learner to open Manage Special Access, add users, set 45 minutes and save, all in one card, and step 2 jumps to Classlist. | P1 |
| F9 | **Explain clicks is switched off during a walkthrough.** | `showClickExplanation` returns early when `activeWalkthrough()` is true. | P1 |
| F10 | **Several UI bugs in the explanation card.** | Section 7. | P1 |
| F11 | **Admin Tools pages (Users, Roles, Org Units, Config Variables) have zero teaching cards** and are invented, not captured at MSU. | 0 taught of 129 controls across those routes and their dialogs. | P1 |

---

## 2. P0-1: Fix the deployment

1. In Vercel, open the project for brightspace-github and check **Deployments**. Confirm the production deployment's commit is `daf9c6c` (or later). If it is not:
   - check that the project is connected to `EdTechDL/brightspace-github` and the production branch is `main`;
   - check whether recent builds failed (`npm run build` succeeds locally at HEAD and `npm test` passes);
   - redeploy.
2. Add a visible build stamp to the footer of the training launcher (commit short SHA and build date injected by `scripts/build.mjs`) so anyone can see which version is live.

**Acceptance:** live Captured screen library says "Explore all 85 screens", the Gradescope library appears in the Screen library select, and the footer shows the current SHA.

---

## 3. P0-2: Rebuild Explain clicks for 100% coverage

### 3.1 Root causes in the current engine (`src/explain.js`)

- `explanationFor(el)` only returns a card when one of these matches: an input `name` in `FIELD_HELP` (27 keys), a title in `TOOL_HELP` (44 Course Admin tools) or `PAGE_HELP`, a handful of hard-coded `data-action` values, or a captured control with `notes`. Everything else returns `null` and the click shows nothing.
- Lookup is by visible text (`el.textContent`), which breaks when a label contains extra text (see bug B1) and cannot distinguish two controls with the same label on different screens.
- Radio help is keyed by the group `name` (`mode`, `finalType`, ...), so every option in a group shows the same card.
- Captured screens render reference controls as `disabled`, so the capture-phase click listener never receives the event.
- `<select>` options and menu items inside dropdowns have no per-item help.

### 3.2 Required architecture

1. **Stable help IDs on every control.** Every rendered control gets `data-help="<screen>.<section>.<control>[.<option>]"`, for example `quiz-new.timing.time-limit`, `grades-settings-calculation.grading-system.weighted`, `classlist.row-menu.impersonate`. Generate the IDs in the renderers (`captureScreen` render path in `capture.js`, `grade-ui.js`, `app.js` views) from the inventory `id` plus a slug of the control label. The same real-world control appearing on the capture screen and the practice page should share one ID so both show the same card.
2. **One help registry** `data/help/*.json` (split by tool: `grades.json`, `quizzes.json`, `assignments.json`, `classlist.json`, `content.json`, `course-admin/*.json`, `navbar.json`, `home.json`, `admin-tools.json`) keyed by help ID. Keep `FIELD_HELP`, `PAGE_HELP`, and `TOOL_HELP` only as migration sources, then remove them.
3. **Lookup order:** exact help ID, then help ID without the option suffix (group card plus a generic "this option" line), then a **visible authoring gap card** (see 3.4). Never return `null`.
4. **No dead disabled controls.** Replace `disabled` on reference-only controls with `aria-disabled="true"` plus a `.reference-only` style. Intercept the click in the capture phase, `preventDefault()` the action, and still show the card. For controls that are truly disabled in D2L itself (for example Selectbox item type before a scheme exists), render them disabled-looking but clickable in Explain mode, and have the card explain **why D2L disables it and how to enable it**.
5. **Option-level help.** Radios: one card per option. Selects: when the learner changes or focuses a select in Explain mode, show the card for the chosen option plus a compact table of all options. Menus: every dropdown item (navbar menus, More Actions, row chevron menus, New menu, title chevrons) gets its own card.
6. **Icons and chevrons count.** Chevron context menus, magnifier, pencil, trash, flag, avatar, waffle, alerts, gear, Help links, pagination, sort headers, checkboxes in table headers: all get cards.
7. **Explain inside walkthroughs.** Allow Explain cards during a walkthrough for controls other than the current target (show them in a secondary, smaller card) so curious learners can still explore.

### 3.3 Card content standard (what a "hand-hold" card contains)

Replace the current four-field `simpleHelp(what, steps, result, ticket)` with this schema. All fields except `options` and `msu` are required.

```json
{
  "id": "grades-settings-calculation.grading-system.weighted",
  "title": "Grading System: Weighted",
  "where": "Grades > Settings (gear) > Calculation Options > Grading System",
  "what": "Plain-language purpose in 1 to 2 sentences.",
  "when": "When a professor would choose this, tied to how syllabi are written.",
  "options": [{"label": "Weighted", "effect": "..."}, {"label": "Points", "effect": "..."}, {"label": "Formula", "effect": "..."}],
  "learnerSees": "What changes on the student side, if anything.",
  "howTo": ["Click-by-click steps using the exact MSU labels."],
  "verify": "How support confirms the change worked (e.g. View as student / Preview / check a learner's Final Calculated Grade).",
  "gotchas": ["Common mistakes and side effects, e.g. switching systems asks two confirmations; weights are ignored in Points."],
  "tickets": ["2 to 3 realistic professor ticket phrasings this control answers."],
  "related": ["help IDs of settings that interact with this one"],
  "msu": "Anything specific to the MSU instance observed in the capture.",
  "source": "D2L Community or MSU help URL",
  "evidence": "captured | documented | simulated"
}
```

Card layout order: title, where-breadcrumb, what, options (if any), when, learner sees, how to, verify, gotchas, tickets, related (as clickable chips that jump to and flash that control), source link. Keep the red outline on the target element. Collapse gotchas/tickets/related under a "More" toggle so the first view stays short.

**Quality bar, one filled example** (a radio that currently shows nothing):

```json
{
  "id": "quiz-special-access-dialog.mode.only-special",
  "title": "Allow only users with special access to see this quiz",
  "where": "Quizzes > quiz > Edit > Manage Special Access (Availability Dates & Conditions panel)",
  "what": "Turns the quiz into a private quiz: only the learners you add under Special Access can see and take it. Everyone else in the course no longer sees it at all.",
  "when": "Make-up tests, alternate versions for a few students, or a deferred exam sitting.",
  "options": [
    {"label": "Allow selected users special access to this quiz", "effect": "Everyone still sees the quiz; the added learners get their own dates, time limit or attempts."},
    {"label": "Allow only users with special access to see this quiz", "effect": "Only the added learners see the quiz; it disappears for everyone else."}
  ],
  "learnerSees": "Learners not on the list do not see the quiz in Quizzes, Content links, or the calendar.",
  "howTo": ["Open Manage Special Access.", "Choose this option.", "Click Add Users to Special Access, set any overrides, tick the learners, click Add Special Access.", "Save and Close the quiz."],
  "verify": "Check the Special Access list shows the right learners, then confirm with the professor which students should see it. Remember Preview does not apply special access.",
  "gotchas": ["Choosing this by accident hides the quiz from the whole class; this is a common cause of 'my students cannot see the quiz' tickets.", "The assignment version of this dialog says 'folder' instead of 'quiz'."],
  "tickets": ["\"Half my class says the midterm is missing.\"", "\"I need a make-up quiz only two students can see.\""],
  "related": ["quiz-special-access-dialog.mode.allow-selected", "quiz-add-special-access.new-time-limit", "classlist.row-menu.edit-accommodations"],
  "msu": "Labels observed at MSU on 2026-09-22.",
  "source": "https://community.d2l.com/brightspace/kb/articles/3462-set-special-access-for-a-quiz",
  "evidence": "captured"
}
```

(Verify the source URL resolves before shipping; replace with the current D2L Community article if it has moved.)

### 3.4 Authoring gap card

If a help ID has no entry yet, show a grey card: "Not written yet: `<help id>`" with the label and screen. This keeps the gap visible in the product and the coverage test catches it before release.

### 3.5 Coverage gate

Add `scripts/audit-explain-coverage.cjs` (supplied alongside this report) and a CI step:

```sh
npm run build && node scripts/audit-explain-coverage.cjs
```

It opens every route, grade tab, dialog reachable from a button, and every captured screen, and classifies every visible control as `taught`, `capture-note`, or `none`. It exits 1 unless every control is `taught`. Mark library chrome (the screen picker, search box, "Replay recorded tour") with `data-audit-ignore` or give it cards too. Current baseline at HEAD: **220 of 2,928 visible controls taught (7.5%)** including library chrome.

Extend it so it also opens every dropdown menu and every row chevron menu before classifying.

### 3.6 Priority order for writing cards

Write in the order professors actually file tickets, finishing each tool end to end before moving on:

1. Grades (all tabs, settings, wizard, New Item forms for every item type, category form, schemes, final grades, event log, exemptions, import/export)
2. Quizzes (list page and tabs, the full new activity editor, Timing, Attempts, Special Access, Question Library, Statistics, Manage Attempts, LockDown Browser tab)
3. Assignments (list, editor, submission types, availability and release conditions, special access, rubric attachment, evaluation and publishing feedback, Quick Eval)
4. Content (Classic Content tree, module and topic menus, visibility, dates, release conditions, upload and create, the New Content Experience prompt)
5. Classlist (Add Participants, row chevron menu: Send Email, Impersonate, View progress, View groups, Edit Accommodations; enrollment statistics; unenroll)
6. Course Admin: Course Offering Information, Import / Export / Copy Components, Manage Dates, Navigation & Themes, Homepages, Widgets, Groups, Rubrics, Discussions, Announcements, Intelligent Agents, Release conditions everywhere, External Learning Tools (LTI links such as Gradescope, Packback, Perusall, MATLAB), Course Reset, Awards, Checklists, Surveys, Self Assessments, Calendar, Attendance, Class Progress, Manage Files, Tool Status
7. Course Home widgets, Role Switch, navbar, alerts, avatar menu, course selector
8. Admin Tools (clearly labelled as organization-level practice, not observed at MSU)

---

## 4. P0-3: Make the interface match Same Playground

Observed live in Same Playground on 2026-09-23 (view only). Use the capture inventory for exact labels; the notes below are the visible layout differences.

### 4.1 Global shell

- **Typography and scale:** real D2L uses a smaller, denser type scale (navbar items and buttons roughly 14 px, page headings roughly 28 px, table text roughly 13 px). The simulator uses larger text throughout. Sample exact values from the live page's computed styles.
- **Navbar dropdown indicators:** real uses a thin chevron icon after Course Tools, Assessments, Communication, More. Simulator uses the ▾ glyph.
- **Avatar:** real shows initials in a dark square badge followed by the display name, no caret. Simulator shows a round grey "SU" badge with a caret.
- **Help:** real pages carry a small "? Help" link at the top right of most tools; add it everywhere with a card.
- **Buttons:** real primary buttons are compact blue, secondary buttons are compact light grey filled (not outlined).

### 4.2 Course Home

- Real: full-width **banner image** with course name overlaid; widget headers are **dark green bars with white text and a collapse chevron** (MSU theme); left column Announcements, Updates, Content Browser, Role Switch; right column **Need Help?** (MSU IT Service Desk phone numbers, D2L Contact Form, D2L Help Site, MSU IT Service Status, Subscribe, Educational Technology Training) then Calendar.
- Simulator: plain grey banner, white card widgets, Role Switch in the right column above Need Help, Need Help reduced to two lines.

### 4.3 Manage Quizzes

- Real: tab strip **Manage Quizzes | Question Library | Statistics | LockDown Browser**; buttons **New Quiz** (primary), **Edit Categories**, **More Actions ▾**; right side **View: By Availability ▾** and **Apply**; empty state "You haven't created any quizzes. Click New Quiz to add a new quiz."; Help link.
- Simulator: heading, single New Quiz button, explanatory callout, quiz cards with Edit quiz / Manage Special Access buttons.
- Required: rebuild as the real list table (checkbox, quiz name with chevron context menu, availability, status icons), keep practice data behind it. Every tab and button explained, Question Library and Statistics at least as explained static pages from the capture.

### 4.4 New Quiz editor

- Real (captured screen `quiz-new`, 51 controls): the new activity editor with left column (title, grade out of, questions area, description) and right collapsible panels (Availability Dates & Conditions, Timing & Display, Attempts & Completion, Evaluation & Feedback) plus Save and Close, Save, Cancel with a "Discard changes?" dialog.
- Simulator: 5 fields in a modal.
- Required: render the full editor from the capture inventory, every control present and explained; keep only the modelled ones functional.

### 4.5 Assignments

- Real: heading **Assignments**, Help link, **New Assignment** (primary), **Edit Categories**, **More Actions ▾**; empty state "Click New Assignment to start."
- Simulator: heading and one button. Required: add the missing buttons and the list table with row chevrons (Edit, Submissions, Manage Special Access, Hide, Delete, etc. per documentation, labelled "documented" where not captured).

### 4.6 Classlist

- Real: heading **Classlist** with **Export / Print / Help** links; **Add Participants ▾** (primary), **Class Engagement**, **Enrollment Statistics**, **Email Classlist**; search box with **Show Search Options**; action bar **Email, Instant Message, Print, Export, Enrollment, Unenroll**; table columns checkbox, flag, Image, **Name** (sortable, chevron context menu under the name), Username, Email, Role, Last Accessed; **10 per page** selector; "Total Users: 2".
- Simulator: columns Name / Role in this course / Quiz timing accommodation / Account and an **Edit Accommodations** button per row.
- Required: rebuild the real table. Edit Accommodations must be reached the real way: **name chevron > Edit Accommodations** (row menu observed: Send Email, Impersonate, View progress, View groups, Edit Accommodations). Show accommodation status as D2L does, not as an extra column.

### 4.7 Content

- Real: first visit shows the full-page prompt "A new Content Experience is available!" with two choices; behind it, Classic Content with the left Table of Contents panel (Overview, Bookmarks, Course Schedule, Table of Contents, modules) and the Overview page.
- Simulator: "Classic Content · simplified module layout" and a New Module button.
- Required: reproduce the prompt (explain both choices and what an instructor loses or gains), then the Classic Content layout with module and topic context menus, Upload / Create, visibility toggles, dates, release conditions.

### 4.8 Grades

- Enter Grades in the simulator shows only final-grade columns. Real Enter Grades shows one column per grade item plus Final Calculated and Final Adjusted, per-learner chevrons (including Bulk edit exemptions), column chevrons, Import / Export / Switch to Spreadsheet View / More Actions, Hide/Show Columns, View Statistics, Preview. Make these enabled-for-explain.
- Settings, wizard, schemes, final grades are the closest to real and the best-taught area; keep them and fill the remaining gaps listed in Appendix A.

### 4.9 Course Admin

- The directory layout matches well. Wire all 44 links to real destinations: use the 38 captured screens (`availability-date-defaults`, `homepages`, `navigation-themes`, `widgets`, `calendar`, `course-builder-welcome`, `course-design-accelerator`, `external-learning-tools`, `forms`, `faq`, `glossary`, `import-export-copy`, `instructional-design-wizard-resume`, `learning-activity-library`, `links`, `manage-files`, `attendance-registers`, `class-progress`, `groups`, `awards`, `checklists`, `competencies-home`, `quick-eval`, `rubrics`, `self-assessments`, `standards`, `surveys`, `announcements`, `discussions-list`, `intelligent-agents`, `course-reset`, `insights-portal`, `sharing-groups`, `tools-status`, `lor-manage`, `lor-publish`, `lor-search`, `course-offering-information`) instead of the "not modelled" dialog. Same for navbar menu items.

### 4.10 Captured screens must look like D2L pages

Currently each captured screen renders as grouped text sections ("Properties > Due Date") with "Capture note" and "state unobserved" tags. For training, render each captured screen **as the D2L page** (same shell, headings, button rows, tables, panels) using the inventory's `controls[].group` and order. Move provenance ("state unobserved", capture notes, route, observation date) into a small "Evidence" drawer that is closed by default. The learner should feel they are inside Same Playground, not reading a capture log.

---

## 5. P1: Walkthroughs that hold the learner's hand

### 5.1 Engine changes (`src/experience.js`, `data/workflows.json`)

1. **One action per step.** A step targets one element (`data-help` ID), says what to click, why, and what will happen. Split every current step into its atomic clicks.
2. **Advance on the learner's click.** Default mode waits for the learner to click the highlighted element (or to change the highlighted field to an accepted value), then advances. Keep Back, Skip, and Restart. Keep the 18-second autoplay only as an optional "watch" mode.
3. **Reach inside dialogs and menus.** Steps must be able to target controls in `<dialog>`, dropdown menus, row chevron menus, and collapsible panels. The step box repositions next to the target and never covers it.
4. **Checkpoints.** After a sequence, ask a quick check question ("The professor wants 15 extra minutes for one student on one quiz that is 30 minutes long. What do you type in New Time Limit?") before marking the walkthrough complete.
5. **Ticket framing.** Every walkthrough opens with a realistic professor ticket, ends with "How to reply to the professor" (a short template) and "How to verify".
6. **Allow Explain during walkthroughs** (F9).

### 5.2 Rewrite example: "Give one learner extra quiz time"

| Step | Target (help ID) | Learner does | Card says |
|---|---|---|---|
| 1 | `navbar.assessments` | Click Assessments | Assessments groups Assignments, Grades, Quizzes, Rubrics, ... |
| 2 | `navbar.assessments.quizzes` | Click Quizzes | Manage Quizzes lists every quiz in the course. |
| 3 | `quizzes-list.row.quiz-1.chevron` | Click the chevron beside Quiz 1 | Row menu: what each item does. |
| 4 | `quizzes-list.row-menu.edit` | Click Edit | Opens the new activity editor. |
| 5 | `quiz-new.timing` | Expand Timing & Display | Where the base time limit lives. |
| 6 | `quiz-new.special-access` | Click Manage Special Access | Special access = exceptions for named learners on this quiz only. |
| 7 | `quiz-special-access-dialog.mode.allow-selected` | Choose "Allow selected users special access to this quiz" | Difference from "Allow only users with special access to see this quiz". |
| 8 | `quiz-special-access-dialog.add-users` | Click Add Users to Special Access | ... |
| 9 | `quiz-add-special-access.override-time-limit` | Tick Override time limit | ... |
| 10 | `quiz-add-special-access.new-time-limit` | Type 45 | Total minutes, not extra minutes, no multiplier here. |
| 11 | `quiz-add-special-access.when-expires.*` | Read the three options | Explain each option. |
| 12 | `quiz-add-special-access.users.demo-student` | Tick the learner | ... |
| 13 | `quiz-add-special-access.save` | Click Add Special Access | ... |
| 14 | `quiz-new.save-and-close` | Save and Close | ... |
| 15 | Checkpoint | Answer the check question | Contrast with Classlist > Edit Accommodations (course-wide multiplier or extra time). |

### 5.3 Walkthrough catalogue to add

Current 10 walkthroughs cover grades, visibility, dates, quiz time, enrolment, roles, content config. Add at least these ticket walkthroughs (each built as in 5.2):

1. Student cannot see a quiz or assignment (dates, visibility, release conditions, special access "see this folder/quiz only")
2. Reset or add an attempt for one student on a quiz (Manage Attempts / special access attempts)
3. Extend an assignment deadline for one student (assignment special access)
4. Grade column empty although the assignment is graded (grade item association, publish evaluations)
5. Publish feedback and scores in bulk from Assignments / Quick Eval
6. Attach a rubric to an assignment and grade with it
7. Create a weighted category with drop lowest
8. Exempt one learner from an item
9. Import grades from a CSV (format, Org Defined ID, common errors)
10. Export grades
11. Copy course components from last semester (Import / Export / Copy Components, what copies and what does not)
12. Hide or show a module or topic; set start/end dates; add a release condition
13. Upload a file and create a topic; replace a file
14. Post an announcement and schedule it
15. Create a discussion forum and topic; restrict to a group
16. Create groups and group-restricted assignments
17. Make the course active or inactive, change course start/end dates (Course Offering Information)
18. Add a TA or guest to the course (Add Participants, Create a MSU Guest Account, Batch Enroll)
19. Impersonate or View as Student to verify what a learner sees, and the limits of Preview
20. Add or fix an external tool link (Gradescope, Packback, Perusall, Zoom) and why a tool shows an error
21. Recover a deleted grade item (event log)
22. Set up Intelligent Agents for missing work reminders
23. Change the navbar or homepage (Navigation & Themes, Homepages, Widgets)
24. Course accessibility report (Ally)
25. Course Reset: what it deletes, when to never use it

Tag each walkthrough with the tools and help IDs it touches so the learner's progress map (section 6) updates as they go.

---

## 6. P2: Make "expert by the end" measurable

1. **Exploration tracker.** Record every help ID the learner opens (local storage, wrapped in try/catch). Show a progress panel: per tool, "Seen 37 of 112 settings", with unseen controls listed and clickable (jumps there and flashes the control).
2. **Tool mastery badges** when every card in a tool has been opened and the tool's walkthroughs and checkpoints are completed.
3. **Setting search.** A search box in the launcher: type "late submissions" or "extra time" and get matching cards with a "Show me where" button that navigates and highlights.
4. **Ticket simulator.** Random realistic professor ticket, learner finds and fixes it in the sandbox, app checks the resulting state (reuse `runPackChecks` style checks).
5. **Glossary cards** for D2L terms, linked from card text (org unit, release condition, special access, exemption, grade scheme, drop ungraded, bonus, can exceed, org defined ID, impersonate, LTI).

---

## 7. Bugs found

| ID | Bug | Where | Fix |
|---|---|---|---|
| B1 | Card title concatenates the option label and its description: "WeightedEach item or category contributes a percentage of the final grade." | `explanationFor()` uses `el.closest('label').textContent` | Use the help registry title, or only the label's first text node. |
| B2 | Every option in a radio group shows the same card (keyed by `name`). | `FIELD_HELP[name]` | Option-level help IDs (3.2.5). |
| B3 | Explain card for a Grades settings radio renders at the top-left of the page over the header, far from the radio. | `positionWalkthroughBox` | Anchor next to the target; never cover the target or the Save button. |
| B4 | Clicking a disabled control shows nothing (no event). | Captured screens and practice pages | 3.2.4. |
| B5 | Course Admin tools with captured screens still open "not modelled". | `mappedTools` | 4.9. |
| B6 | Walkthrough "Next" needed two clicks once in manual testing on the live site (first click did not advance). Could not reproduce reliably; verify focus and pointer handling on the step box. | Walkthrough box | Check click target overlap and `pointer-events`. |
| B7 | When a walkthrough navigates, the top bar scrolls partly out of view on the live site (course name hidden). | `highlight(true)` `scrollIntoView` | Scroll with an offset for the fixed header. |
| B8 | Explain toggle state persists across sessions, but the toast text says "Click a course tool or grade setting", which undersells the goal. | `toggle-explanations` handler | Change to "Click anything to learn what it does." once coverage is 100%. |
| B9 | The password is visible in the page source, so the gate only deters casual visitors (the code comment says so too). | `gate.js` | If the site must be private, use Vercel Deployment Protection. |

---

## 8. Acceptance checklist

- [ ] Production deployment matches `main` HEAD; build stamp visible.
- [ ] `node scripts/audit-explain-coverage.cjs` exits 0 (every visible control on every route, tab, dialog, menu, and captured screen is taught).
- [ ] No control in any view uses the HTML `disabled` attribute purely as "reference only".
- [ ] Every radio option, select option, and menu item has its own card.
- [ ] Every card has where, what, when, learner sees, how to, verify, gotchas, tickets, source.
- [ ] Quizzes, Assignments, Classlist, Content, Course Home, and Enter Grades match the real Same Playground layouts described in section 4.
- [ ] All 44 Course Admin links and all navbar menu items open a page, never a "not modelled" dialog.
- [ ] Captured screens render as D2L pages with provenance tucked into an Evidence drawer.
- [ ] Walkthroughs advance on the learner's click and reach into dialogs and menus; at least the 25 walkthroughs in 5.3 exist.
- [ ] Progress tracker shows seen vs unseen settings per tool.
- [ ] No in-app text names another LMS.
- [ ] `npm test` still passes (calculation checks, replay targets, build checks).

---

## Appendix A: Untaught controls on the practice pages (repo HEAD)

Counts are visible controls; "untaught" means Explain shows nothing or only capture metadata.

| View | Total | Untaught | Untaught controls |
|---|---|---|---|
| Course Home | 11 | 10 | Bookmarks, Recently Visited, Create some content, Change Role, Current Role select, Class Engagement, Course Access, Tool Access, D2L Help Site, Library Search (8 are disabled) |
| Grades: Enter | 19 | 11 | Import, Export, Switch to Spreadsheet View, More Actions (disabled), Help, Recalculate, Transfer calculated to adjusted, adjusted final inputs, Save grades, Open learner view |
| Grades: Manage | 12 | 6 | New, More Actions, Bulk Edit, Final Calculated Grade link, Help, Supported calculation boundaries |
| Grades: Personal Display | 14 | 7 | Username, Org Defined ID, Grade scheme color (disabled), three number fields, Save |
| Grades: Org Unit Display | 14 | 5 | Display how final grade was calculated, Grade scheme color, Allow users to add grades to ePortfolio, characters field, Save |
| Grades: Calculation | 16 | 3 | Formula radio (disabled), Automatic zero checkbox (disabled), Save |
| Grades: Wizard landing | 7 | 2 | Start, Help |
| Grades: Schemes | 9 | 4 | New Scheme, Default Scheme select, Save default scheme, Help |
| Grades: Final Grades | 12 | 4 | adjusted final inputs, Save, Help |
| Content + New Module dialog | 9 | 6 | New Module, Module title, Module text, Save, Cancel, Close |
| Assignments + New Assignment | 12 | 7 | New Assignment, Title, Instructions, Availability panel, Save and Close, Cancel, Close |
| Quizzes + New Quiz | 11 | 8 | New Quiz, Quiz Title, Timing & Display, Attempts & Completion, Attempts Allowed, Save and Close, Cancel, Close |
| Classlist + Edit Accommodations | 11 | 9 | Edit Accommodations, Manage enrollments, Modify Time Limit, Multiplier radio, Extra time radio, Save, Cancel, Close |
| Course Admin | 46 | 2 | Category / Name ordering toggle (the 44 tools are taught at tool level, but their destinations are dead ends) |
| Course Offering Information | 6 | 4 | Name, Code, Course is active, Save |
| Learner preview | 1 | 1 | View as select |
| Admin Tools (all 5 pages + 9 dialogs) | 129 | 129 | Everything |
| Resources, Library, Replay, Self-check | 98 | 97 | Mostly training chrome; give each a short card or mark `data-audit-ignore` |

## Appendix B: Captured screens (85) coverage at HEAD

Taught / total visible controls on the screen body. Every screen below needs full cards; the worst offenders are the busiest and most ticket-heavy screens.

- Largest screens: external-learning-tools 0/39, navbar-menus 20/33, quiz-new 0/32, grades-new-item-numeric 0/30, assignment-new 0/30, course-home 1/28, grades-enter-grades 1/27, grades-final-grades 0/27, quiz-add-special-access-dialog 0/21, classlist 0/21, course-design-accelerator 0/19, grades-new-scheme 0/18, import-export-copy 0/17, grades-settings-personal 1/16, manage-dates 7/15, grades-manage-with-item 3/15, grades-edit-item-restrictions 0/15, availability-date-defaults 0/15
- Every one of the 38 Course Admin destination screens: 0 to 3 taught.
- Radios across all captured screens: 0 of 82 taught. Checkboxes: 7 of 98. Text fields: 0 of 170.

Full per-control detail is produced by the supplied audit script in `coverage-report.json`.

## Appendix C: Files to touch

| Change | File |
|---|---|
| Build stamp, help registry bundling | `scripts/build.mjs` |
| Help IDs on rendered controls | `src/capture.js`, `src/grade-ui.js`, `src/app.js` |
| Explain engine, disabled handling, option help, positioning | `src/explain.js`, `src/app.css` |
| Walkthrough engine | `src/experience.js` |
| Walkthrough content | `data/workflows.json` |
| Help content | new `data/help/*.json` (migrate `FIELD_HELP`, `PAGE_HELP`, `data/tool-help.json`, `data/tool-notes.json`) |
| Course Admin and navbar routing | `src/grade-ui.js` (`mappedTools`), `src/capture.js` |
| Coverage gate | new `scripts/audit-explain-coverage.cjs`, `package.json` script `audit:explain` |
