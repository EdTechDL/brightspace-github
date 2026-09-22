---
title: Brightspace gradebook — first guided lab
docs_checked: 2026-09-22
institution_verified: null
status: Generic training; navigation and permissions need verification in your sandbox
---

# Your first gradebook lab

Allow **40–45 minutes**. Work in your approved empty sandbox with fictional assessments and an institution-provided test learner. Instructor access does not establish permission to create learner accounts. Without a test learner, build the structure and use the arithmetic below; mark score-entry and learner-view verification as pending.

The tutor should identify the actual screen before each step, explain the setting, let you perform the action, and check the result. The routes below come from documentation; your institution’s navigation may differ. This lab does not authorize changes in faculty courses.

## 0–5 minutes: Find your way around

Open the sandbox and locate **Grades**. Find **Manage Grades** (assessment columns and categories), **Enter Grades** (learner scores), **Settings**, **Setup Wizard**, and **Schemes**. Record the visible route and your role. [D2L: Create a grading system](https://community.d2l.com/brightspace/kb/articles/3519-create-a-grading-system)

Checkpoint: Explain the difference between changing a column’s maximum points and entering a learner’s score.

## 5–12 minutes: Choose the calculation rules

Open **Grades → Setup Wizard**. For this exercise, choose:

- **Weighted** grading.
- **Calculated Final Grade**.
- **Drop ungraded items**.
- **Automatically keep final grade updated**.
- Keep automatic final-grade release off until the visibility exercise.

Review the default scheme and teacher/student display settings. These choices belong to this exercise; faculty grading policies determine real course settings. The choices can also be found under Grades settings. [D2L: Set up your Grade book](https://community.d2l.com/brightspace/kb/articles/3539-set-up-your-grade-book)

Explain the three systems: **Points** uses earned points divided by possible points; **Weighted** applies specified percentages; **Formula** supports custom calculation rules. Weighted items still require maximum points. [D2L: Grading systems types](https://community.d2l.com/brightspace/kb/articles/3521-grading-systems-types)

## 12–22 minutes: Build a small gradebook

Under **Manage Grades**, use **New → Category** and **New → Item → Numeric** to build:

| Component | Maximum points | Weight |
|---|---:|---:|
| Quizzes category | — | 40% of course |
| Q1, inside Quizzes | 10 | 50% of category |
| Q2, inside Quizzes | 10 | 50% of category |
| Project, outside Quizzes | 100 | 60% of course |

Use evenly distributed weights for the two quizzes. Check that Quizzes and Project total 100% of the course and the quizzes total 100% of their category. Item weight inside a category is relative to that category. [D2L: Manage Grades](https://community.d2l.com/brightspace/kb/articles/3553-manage-grades-in-the-grades-tool)

Checkpoint: Q1 contributes 20% of the full course, despite being labelled 50% inside its category.

## 22–31 minutes: Predict and test the result

For the approved test learner, enter Q1 = **8/10**, Q2 = **6/10**, Project = **90/100**. These independently calculated examples are your checks:

| Experiment | Expected total |
|---|---:|
| Weighted, all three scores entered | **82%** |
| Same data in a points system; discuss without changing this book | **86.67%** |
| Weighted, clear Q2; Drop ungraded items | **86%** |
| Weighted, Q2 blank; Treat ungraded items as 0 | **70%** |
| Weighted, record Q2 as zero; Drop ungraded items | **70%** |

Arithmetic: weighted = `((8 + 6) / 20 × 40) + (90 / 100 × 60) = 82`; points = `104 / 120 × 100 = 86.666…`. With Q2 dropped, the quiz category uses `8/10`; with Q2 zero, it uses `8/20`.

**An ungraded item and a recorded zero are different.** Dropping ungraded items ignores blanks; it does not ignore an earned zero. Restore Q2 to 6 and restore this lab’s original calculation settings afterwards. [MSU: Gradebook Tips](https://help.d2l.msu.edu/msu-docs/d2l-grades-at-msu/d2l-gradebook-tips)

## 31–39 minutes: Connect and reveal grades

Create a practice assessment and associate it with the existing Project numeric item, avoiding a duplicate. Locate its evaluation publication controls. Published activity scores synchronize with associated grade items; direct gradebook edits can also affect associated activities. Inspect the actual options before demonstrating. [D2L: Create a grading system](https://community.d2l.com/brightspace/kb/articles/3519-create-a-grading-system)

Inspect the Project grade-item visibility separately from the overall final-grade release. In **Enter Grades**, locate the final-grade controls, release only the approved test learner’s total, and verify what that learner can see using an available, permitted learner view. A calculated total remains invisible until released. [D2L: Enter grades](https://community.d2l.com/brightspace/kb/articles/34125-enter-grades-in-the-grades-tool)

## 39–45 minutes: Explain and save

Solve this practice ticket: “My current percentage became much lower when I changed how ungraded work is handled.” Explain the cause before changing anything. Save the observed route, settings, result, and any unverified learner-view check.

Next lessons:

- **Adjusted final grades and schemes:** adjusted totals require manual updating; schemes provide grading scales, separate from the calculation system. Use institutional thresholds. [MSU: Gradebook Tips](https://help.d2l.msu.edu/msu-docs/d2l-grades-at-msu/d2l-gradebook-tips)
- **Exemptions, missing work, drop lowest:** distinguish excused work from zeros; verify category requirements and whether automatic zero grading is available. [D2L: Missing or excluded work](https://community.d2l.com/brightspace/kb/articles/35446-handle-missing-or-excluded-work)
- **Bonus and Can Exceed:** test extra credit and caps at item, category, and final-total levels. [D2L: Manage Grades](https://community.d2l.com/brightspace/kb/articles/3553-manage-grades-in-the-grades-tool)
- Build a separate points gradebook, then practise quiz synchronization and a “student cannot see a grade” ticket. Leave Formula for a later policy-specific exercise.
