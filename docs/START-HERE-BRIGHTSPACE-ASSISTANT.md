# Your local Brightspace assistant

Open **brightspace-d2l-assistant.html** in a browser. It is a single offline file: no installation, extension, login, API key, or server is needed. Keep this file in a stable location so the browser can retain its local notes and sample edits.

The Course Administration layout follows your screenshot. The D2L page remains the main surface; there is no permanent coaching sidebar.

## Use it in two ways

- **Explain clicks: On** — selecting a course tool or a supported setting shows a red explanation: its purpose, workflow, important distinction, and a typical ticket. Turn it off to clear these cards. During a walkthrough, that sequence’s cards take priority.
- **Walkthroughs** — paste a ticket or search a topic. Open **Diagnosis and verification** for the checks and distinctions, then choose **Open walkthrough** or **Open captured screen**. Results are local keyword matches, not an AI diagnosis.

Under **Browse all walkthroughs and recordings**, you can play Claude’s recorded MSU gradebook session, select any of the ten interactive sequences, or load another compatible tour JSON. Recorded playback advances saved screens. Working sequences let you edit synthetic examples at your own pace; Next advances the explanation and does not save a form.

The course selector is the grid icon in the top bar. **Same Playground** is the empty captured-course starting point. **Faculty Support Practice** and **Department Training** hold example data. Relevant working tours select a populated sample course when needed.

## Start with this ticket

“The student sees assessment scores but cannot see the final grade.”

1. Open Walkthroughs and search **cannot see final grade**.
2. Open the result **Assessment grades are visible, but the course total is missing**. Its diagnostic notes distinguish calculating a total from releasing it.
3. Open the walkthrough. Check **Calculation Options → Final Grade Released** to identify the selected final type.
4. Next opens **Final Grades**. In real navigation, the captured path is **Enter Grades → Final Calculated Grade column menu → Enter Grades**. Tick the intended learner’s **Released** box and **Save**.
5. Next shows the simulated learner result. In the untouched sample, Demo Learner’s calculated grade is **82.00%**. On a real ticket, verify through your institution’s approved learner-access method.

## Reuse it with AI

Give the AI this HTML and **brightspace-reference/index.json**. The index points to compact ticket, workflow, tool, and captured-screen records. A browser assistant can use the page’s optional WebMCP tools when supported, or its visible controls otherwise.

A useful instruction is:

> Use the local Brightspace reference for this ticket. Identify the likely settings, distinguish similar options, and open the matching local walkthrough or captured screen. Match the depth of Claude’s recorded cards; skip obvious interface instructions. Show one meaningful step at a time with red highlights. Tell me when a screen or saved behavior is not represented, and use official documentation for gaps. Preserve the difference between a practice result and verification in our actual course.

Use **Help → My learning notes** to record useful findings. **Export notebook** saves notes and practice state as JSON to attach to a future AI session. This is reusable reference memory; the HTML does not train an AI or automatically learn from your real D2L account.

## What is faithful, and what is approximate

- **Course Administration:** all 44 tools, seven categories, order, blue links, and Category/Name control follow your screenshot. Icons and fonts are approximations.
- **Captured library:** all 47 screen records, 759 controls, 17 menus, and 13 dialogs are included as text reconstructions. The capture supplied no screenshots of these destinations. Recorded transitions open the next captured screen when one exists.
- **Working subset:** numeric gradebooks, common settings, wizard, release/display, selected item/category operations, simple content and assignment availability, quiz timing, and limited administrative examples.
- **Other tools:** their menu position and explanation are present, but the destination is not falsely recreated as fully functional. Top-level organization administration was not captured; those exercises are explicitly approximate.

See **BRIGHTSPACE-REVIEW-AND-LIMITS.md** for validation and important source corrections. The original Claude tour remains in the reference folder for provenance; use the HTML’s reviewed cards when learning.
