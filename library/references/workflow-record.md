# Record and maintain a reusable workflow

Read this when saving a new procedure or correcting an existing one. Reuse its ID when the intent is unchanged. Keep a distinct variant if a course layout or role changes the steps. Maintain the existing package format.

Record these fields in the workflow file:

- Stable ID, title, and a few natural-language ticket aliases.
- Intended outcome and parameters: activity/course scope, learner scope, dates/time zone or requested values. Use example values, not retained student records.
- Environment: relevant institution, course/UI variant, and observed permissions.
- Prerequisites and diagnostic checks, including other causes the symptom could have.
- Each step: visible label, page context, action, explanation, and expected next state. Store selectors only if actually observed; prefer semantic labels and scope over coordinates.
- Saved-state verification and separate learner-outcome verification, each marked performed/pending/not applicable with evidence.
- Source links and dates checked; institution verification date or null.
- Known differences, limitations, and relevant escalation conditions.
- A short reusable reply pattern and sandbox practice/reset method when useful.

Use evidence states deliberately:

- **proposed:** a new idea or untested local variant.
- **official-docs:** supported by documentation, not yet tested in this institution.
- **institution-verified:** the applicable steps and recorded result checks succeeded in an identified institutional context. Preserve partial verification limits.
- **stale:** observed mismatch or changed relevant configuration requires rechecking.

Do not automatically downgrade a workflow just because a date elapsed; freshness depends on current UI evidence, product changes, and the importance of the operation. A simulator has separate verification and cannot promote a real D2L workflow to institution-verified.

When write access exists, update the procedure, then its index entry and learning memory. Read the changed files back. Keep only concise reusable discoveries in memory. A correction should preserve evidence for any still-valid variant rather than silently overwriting it.

When write access is missing, produce the complete updated file or a precise patch and tell the user where it belongs. State that the master library and uploaded copies still need updating. A successful browser session or remembered conversation is not proof that these files were persisted.
