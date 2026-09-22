---
title: Brightspace gradebook — diagnose a support ticket
docs_checked: 2026-09-22
institution_verified: null
status: Generic diagnostic reference; verify local settings, role, and workflow
---

# Diagnose before changing a gradebook

Start with the requested outcome, course, affected assessment, and scope: one learner, several learners, or everyone. Ask for one expected result and the actual result. Determine whether the ticket concerns **calculation, synchronization, or visibility**. Use anonymized examples in reusable notes. This reference does not authorize grade changes or publication in faculty courses.

## “The total is wrong”

1. Compare the intended syllabus rule with **Grades → Settings → Calculation Options**. Points uses earned/possible totals; Weighted uses assigned percentages; Formula needs its particular expression inspected.
2. Check maximum points, category placement, item weights, and category weights. An item’s weight inside a category is a percentage of that category. Weights that do not total 100% can be normalized proportionally; do not treat a plausible-looking total as proof that configuration matches policy. [D2L: Grading systems types](https://community.d2l.com/brightspace/kb/articles/3521-grading-systems-types)
3. Inspect blanks, recorded zeros, exemptions, and category drop rules. Confirm whether the work should count. Exemption is learner-specific exclusion; automatic zero grading is separate from treating ungraded items as zero. Drop-lowest requires matching maximum points in points categories or evenly distributed category weights in weighted grading. Automatic zeros require organizational enablement and support specific activities, not all tools. [D2L: Missing or excluded work](https://community.d2l.com/brightspace/kb/articles/35446-handle-missing-or-excluded-work)
4. Check bonus status and Can Exceed caps on the item, category, and final total. Bonus adds earned credit without enlarging the normal denominator. [D2L: Manage Grades](https://community.d2l.com/brightspace/kb/articles/3553-manage-grades-in-the-grades-tool)
5. Identify whether the displayed total is Calculated or Adjusted. Adjusted final grades require manual updating; a stale adjusted total may survive newer assessment scores. Confirm the displayed grade scheme and institutional thresholds. [MSU: Gradebook Tips](https://help.d2l.msu.edu/msu-docs/d2l-grades-at-msu/d2l-gradebook-tips)

Reproduce one learner’s arithmetic before proposing a fix. Do not repair a calculation discrepancy by overriding the final total unless that is the intended, authorized grading decision.

## “The activity is graded, but Grades is blank”

Inspect the assessment’s numeric grade-item association, duplicate columns, publication state, and quiz gradebook synchronization settings. A quiz score can remain unsynchronized when the relevant export/update and publication steps have not occurred. Direct gradebook edits can synchronize scores and feedback back to associated tools; they are not an isolated scratchpad. [D2L: Create a grading system](https://community.d2l.com/brightspace/kb/articles/3519-create-a-grading-system)

## “The learner cannot see the grade”

First establish **where**: the activity’s results/feedback page, its gradebook column, or the overall course total. Check the relevant publication, visibility, date/condition, and release controls. For quizzes, inspect Evaluation & Feedback options. A computed final total must be released before learners can see it; releasing one assessment is not the same operation. Verify the intended learner and scope before any release. [D2L: Enter grades](https://community.d2l.com/brightspace/kb/articles/34125-enter-grades-in-the-grades-tool)

Displaying the final-grade calculation breakdown is also distinct from releasing the final grade. [MSU: Gradebook Tips](https://help.d2l.msu.edu/msu-docs/d2l-grades-at-msu/d2l-gradebook-tips)

Finish with the cause, proposed change, affected scope, and a verification check. After an authorized fix, record the observed route, expected and actual outcomes, documentation date, and remaining uncertainty. Mark institution_verified only after checking that workflow in the institution’s actual environment.
