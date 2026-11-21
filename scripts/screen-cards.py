"""Generate data/help/screens.json: full help cards for the Quizzes, Assignments
and Classlist screens in the screen reference.

Run with: python3 -I scripts/screen-cards.py
Cards are keyed by the same help id the app computes for each control
(screen id . slug(group) . slug(label)), so a click finds its card directly.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUIZ = "https://community.d2l.com/brightspace/kb/articles/3413-create-and-configure-a-quiz"
QUIZ_SA = "https://community.d2l.com/brightspace/kb/articles/3462-set-special-access-for-a-quiz"
QUIZ_TROUBLE = "https://community.d2l.com/brightspace/kb/articles/33420-troubleshoot-issues-with-quizzes"
QUIZ_EVAL = "https://community.d2l.com/brightspace/kb/articles/3533-evaluate-quizzes"
PREVIEW = "https://community.d2l.com/brightspace/kb/articles/35012"
ASSIGN = "https://community.d2l.com/brightspace/kb/articles/2776-create-an-assignment"
ASSIGN_SUBMIT = "https://community.d2l.com/brightspace/kb/articles/18122-submit-and-manage-assignments"
ASSIGN_EVAL = "https://community.d2l.com/brightspace/kb/articles/3529-evaluate-assignments-using-the-assignments-tool"
CLASSLIST = "https://community.d2l.com/brightspace/kb/articles/3680-use-classlist-to-manage-course-participants"
ACCOM = "https://community.d2l.com/brightspace/kb/articles/34430-manage-classlist-accomodations"


def slug(text):
    s = re.sub(r"[^a-z0-9]+", "-", str(text or "").lower()).strip("-")[:48]
    return s or "unlabelled"


def hid(screen, group, label):
    return ".".join([screen, slug(group or "other"), slug(label)])


def card(title, where, what, when=None, how=None, verify=None, gotchas=None, tickets=None, source=None, options=None, learner=None):
    if len(where) <= 10:
        where = "Course navigation > " + where
    when = when or "When an instructor asks about this part of the page or reports that it is not working as expected."
    verify = verify or "Reopen the page and confirm the saved setting matches what the instructor asked for."
    c = {"title": title, "where": where, "what": what}
    if options:
        c["options"] = [{"label": a, "effect": b} for a, b in options]
    if when:
        c["when"] = when
    if learner:
        c["learnerSees"] = learner
    if how:
        c["howTo"] = how
    if verify:
        c["verify"] = verify
    if gotchas:
        c["gotchas"] = gotchas
    if tickets:
        c["tickets"] = tickets
    if source:
        c["source"] = source
    c["evidence"] = "documented"
    return c


CARDS = {}


INVENTORY = json.load(open(ROOT / "data/capture/d2l-ui-inventory.json", encoding="utf-8"))
KINDS = {}
for _s in INVENTORY["screens"]:
    for _c in _s["controls"]:
        KINDS.setdefault((_s["id"], _c.get("group"), _c["label"]), set()).add(_c.get("kind"))
BUTTON_KINDS = {"button", "link", "tab", "menu"}


def add(screen, group, labels, c):
    # The app keys buttons, links, tabs and menus under the group "control", and every
    # other control under its own group, so register each card under the key it is looked up by.
    for label in labels if isinstance(labels, list) else [labels]:
        kinds = KINDS.get((screen, group, label))
        if not kinds:
            raise SystemExit(f"No control {label!r} in group {group!r} on {screen}")
        for kind in kinds:
            CARDS[hid(screen, "control" if kind in BUTTON_KINDS else group, label)] = c


def add_menu(screen, labels, c):
    for label in labels if isinstance(labels, list) else [labels]:
        CARDS[hid(screen, "menu", label)] = c


# ---------- Shared cards used by both activity editors ----------
def title_card(kind, tool):
    return card(f"{kind} title", f"{tool} > New {kind}", f"The name learners see in {tool}, the course calendar, the gradebook and notifications.",
                "Always. A clear title is the first thing a learner searches for.",
                ["Replace Untitled with a specific name, such as “Unit 3 Quiz” or “Lab Report 2”.", "Save. The new name appears everywhere the activity is listed."],
                "The list page shows the new name after Save and Close.",
                ["Renaming does not rename a grade item created earlier under a different name in older workflows; check the gradebook if names drift."],
                [f"“Students can’t find the {kind.lower()} I posted.”"], QUIZ if kind == "Quiz" else ASSIGN)


def due_card(kind, tool):
    return card("Due Date", f"{tool} > New {kind}", f"The deadline learners see. It marks work as late after this time but does not by itself stop {'attempts' if kind == 'Quiz' else 'submissions'}.",
                "Whenever the activity has a deadline that should appear in the calendar and on learner to-do lists.",
                ["Pick a date and time.", "Set the End Date under Availability Dates & Conditions if access should close.", "Save."],
                "The date shows on the list page and in the course calendar.",
                ["Due Date and End Date are different. Due marks late; End Date closes access. Most “students submitted after the deadline” tickets come from setting only one of them.",
                 "Times use the time zone shown on the page. Confirm it matches the instructor’s intent."],
                [f"“Why could a student still submit after the due date?”", "“The deadline shows the wrong time.”"], ASSIGN_SUBMIT if kind == "Assignment" else QUIZ)


def start_end_card(which, kind, tool):
    if which == "Start Date":
        what = f"The {kind.lower()} cannot be opened before this time. Depending on display settings, learners may still see it listed."
        tick = [f"“My students can already see the {kind.lower()} before it should open.”"]
    else:
        what = f"Access closes at this time. After it, learners can no longer {'start the quiz' if kind == 'Quiz' else 'submit'}, unless they have special access."
        tick = [f"“A student missed the deadline and needs to submit late.”" if kind == "Assignment" else "“A student could not start the quiz in the evening.”"]
    return card(which, f"{tool} > New {kind} > Availability Dates & Conditions", what,
                "Use with the Due Date to control exactly when work can happen.",
                ["Open Availability Dates & Conditions.", f"Set the {which} date and time.", "Save."],
                "Reopen the activity and check the saved date and time.",
                ["For one learner who needs different dates, use Special Access instead of moving the dates for the whole class."],
                tick, ASSIGN_SUBMIT if kind == "Assignment" else QUIZ)


def release_card(kind, tool):
    return card("Release conditions", f"{tool} > New {kind} > Availability Dates & Conditions", f"Hides the {kind.lower()} until a learner meets a condition, such as completing a content topic or scoring above a threshold on another activity.",
                "Sequencing work, such as unlocking a quiz only after the reading is viewed.",
                ["Open Availability Dates & Conditions.", "Choose Add Release Condition and pick the condition type.", "Set the criteria and save."],
                "Check as a test learner, or confirm the condition is listed under Release Conditions.",
                ["This is the most common cause of “my student cannot see it”. Always check release conditions before anything else.",
                 "Conditions combine. With several conditions, check whether all or any must be met."],
                [f"“One student can’t see the {kind.lower()} but everyone else can.”"], ASSIGN if kind == "Assignment" else QUIZ)


def manage_sa_card(kind, tool, src):
    return card("Manage Special Access", f"{tool} > New {kind} > Availability Dates & Conditions > Special Access", f"Opens the exceptions list for this one {kind.lower()}: different dates{', a different time limit or more attempts' if kind == 'Quiz' else ''} for selected learners, without changing anything for the rest of the class.",
                "One learner needs an extension, a make-up window or extra time on this activity only.",
                ["Click Manage Special Access.", "Choose whether special access adds exceptions or restricts who can see the activity.", "Add Users to Special Access, set their dates or limits, select the learner and save.", f"Save the {kind.lower()} as well."],
                "The learner appears in the special access list with the new dates or limits.",
                ["For extra time on every quiz in the course, use Classlist > Edit Accommodations instead.",
                 "Quiz Preview does not apply special access. Verify with the saved record, not a preview."] if kind == "Quiz" else
                ["Special access dates replace the normal dates for that learner only. Remember to save the assignment after adding them."],
                [f"“Can you give one student until Monday?”", "“A student was sick and needs a make-up window.”"], src)


def notify_card(kind, tool):
    return card("Notification email", f"{tool} > New {kind}", f"Sends an email to the addresses entered whenever a learner {'completes an attempt' if kind == 'Quiz' else 'submits'}.",
                "An instructor or TA wants to know the moment work arrives.",
                ["Enter one or more addresses separated by commas.", "Save."],
                "A test submission sends an email to the address.",
                ["For a large class this can mean hundreds of emails. Suggest it only for small classes or important deadlines."],
                [f"“I want an email when students {'finish the quiz' if kind == 'Quiz' else 'hand in the assignment'}.”"], QUIZ if kind == "Quiz" else ASSIGN)


def category_card(kind, tool):
    return card("Category", f"{tool} > New {kind}", f"Groups this {kind.lower()} with others on the {tool} list page, such as “Midterms” or “Weekly Labs”. This is a display category in {tool}, separate from gradebook categories.",
                "Keeping a long list of activities tidy for instructors and learners.",
                [f"Pick an existing category, or create one with Edit Categories on the {tool} page.", "Save."],
                f"The {kind.lower()} appears under that heading on the list page.",
                [f"This does not change grade weighting. Weighting comes from the gradebook category in Grades."],
                [f"“Why doesn’t moving the {kind.lower()} to a category change the weighting?”"], QUIZ if kind == "Quiz" else ASSIGN)


def objectives_card(kind, tool):
    return card("Learning objectives", f"{tool} > New {kind} > Evaluation & Feedback", f"Aligns this {kind.lower()} to course outcomes or standards so achievement can be reported against them.",
                "Programs that report on outcomes or competencies.",
                ["Click Manage Learning Objectives.", "Select the outcomes this activity assesses.", "Save."],
                "The outcomes are listed under Learning Objectives.",
                ["Alignment alone does not record achievement. Instructors still evaluate against the outcome."],
                ["“How do I connect this to our program outcomes?”"], QUIZ if kind == "Quiz" else ASSIGN)


def hidden_card(kind, tool):
    return card("Visibility (Hidden switch)", f"{tool} > New {kind} > bottom bar", f"Controls whether learners can see the {kind.lower()} at all. Hidden activities do not appear for learners regardless of dates.",
                f"Keeping a {kind.lower()} out of sight while it is being built.",
                ["Use the switch in the bottom bar.", "Save."],
                f"The list page shows the {kind.lower()} as hidden or visible.",
                [f"A hidden {kind.lower()} looks “broken” to learners. Check this switch early in any “students can’t see it” ticket."],
                [f"“None of my students can see the {kind.lower()}.”"], QUIZ if kind == "Quiz" else ASSIGN)


def back_card(kind, tool):
    return card(f"Back to Manage {tool}", f"{tool} > New {kind}", f"Returns to the {tool} list.",
                None, ["Save first if you want to keep changes."], None,
                ["Leaving without saving asks whether to discard changes."], None, QUIZ if kind == "Quiz" else ASSIGN)


def sa_dates(tool, src):
    has_due = card("Has Due Date (special access)", f"{tool} > Special Access > Properties", "Gives the selected learners their own due date for this activity. Everyone else keeps the normal due date.",
                   "An extension for one learner or a small group.",
                   ["Check Has Due Date.", "Pick the new date and time.", "Select the learners and save, then save the activity."],
                   "The learner’s row in special access shows the new due date.",
                   ["Move the End Date too if the extension goes past it, otherwise access still closes at the original end date."],
                   ["“Can you extend the due date for just one student?”"], src)
    has_start = card("Has Start Date (special access)", f"{tool} > Special Access > Properties > Availability", "Lets the selected learners open the activity from a different time, earlier or later than the class.",
                     "Make-up sittings and early access for planned absences.",
                     ["Check Has Start Date.", "Set the date and time.", "Save."],
                     "The special access record lists the new start date.", None,
                     ["“A student will be away and needs to write it early.”"], src)
    has_end = card("Has End Date (special access)", f"{tool} > Special Access > Properties > Availability", "Keeps the activity open longer for the selected learners only.",
                   "Late work allowed for one learner without reopening the activity for everyone.",
                   ["Check Has End Date.", "Set the new date and time.", "Save."],
                   "The learner can still open the activity after the class end date.",
                   ["If the activity is hidden or blocked by a release condition, new dates alone will not make it reachable."],
                   ["“A student got an extension but still can’t submit.”"], src)
    return has_due, has_start, has_end


def users_cards(tool, src):
    search = card("Search for learners", f"{tool} > Special Access > Users", "Filters the learner list so you can find the right person in a large class.",
                  None, ["Type part of a name or ID.", "Press Enter or the search icon."], "The table narrows to matching learners.",
                  ["Confirm the exact learner with the instructor. Classes often have people with similar names."], None, src)
    table = card("Learner list", f"{tool} > Special Access > Users", "Every learner who can receive special access. Check the box next to each learner the exception should apply to.",
                 None, ["Select one or more learners.", "Save."], "Only the selected learners show in the special access list.",
                 ["The settings above apply to everyone selected in this one save. Add learners with different needs separately."], None, src)
    return search, table


# ---------- Quizzes ----------
Q, QT = "Quiz", "Quizzes"
add("quizzes-list", "tool tabs", "Manage Quizzes", card("Manage Quizzes", "Quizzes", "The list of every quiz in the course, with each quiz’s actions menu for editing, previewing, grading and special access.", "Starting point for almost every quiz ticket.", ["Find the quiz.", "Open its menu for Edit, Preview, Grade or Statistics."], None, None, ["“Where do I go to change my quiz?”"], QUIZ))
add("quizzes-list", "tool tabs", "Question Library", card("Question Library", "Quizzes > Question Library", "A course bank of reusable questions and sections. Questions here can be pulled into many quizzes or drawn at random.", "Building question pools so each learner gets a different set of questions.", ["Create sections by topic.", "Add or import questions.", "In a quiz, use Add Existing to pull them in, or a random section to draw from a pool."], "The quiz shows the pulled questions or the random section.", ["Editing a question in the library can update every quiz that uses it. Check before changing a live question."], ["“How do I give each student different questions?”"], QUIZ))
add("quizzes-list", "tool tabs", "Statistics", card("Quiz statistics", "Quizzes > Statistics", "Class averages, score distributions and per-question results for each quiz.", "Spotting a broken question (everyone got it wrong) or reviewing how a class did.", ["Open Statistics.", "Pick the quiz.", "Switch between user, question and question detail views."], None, ["A question that nearly everyone missed is often a wrong answer key rather than a hard question."], ["“Is something wrong with question 7? Nobody got it.”"], QUIZ_EVAL))
add("quizzes-list", "tool tabs", "LockDown Browser", card("LockDown Browser", "Quizzes > LockDown Browser", "Settings for Respondus LockDown Browser, which locks the learner’s computer to the quiz while it is open.", "High-stakes exams that require a secure browser, where the institution licenses it.", ["Open the LockDown Browser tab.", "Choose the quiz and require LockDown Browser.", "Save."], "Learners are prompted to open the quiz in LockDown Browser.", ["Learners need the app installed first. Most failures are students on Chromebooks or tablets without it."], ["“My students say the quiz won’t open.”"], QUIZ_TROUBLE))
add("quizzes-list", "button row", "New Quiz", card("New Quiz", "Quizzes", "Opens the quiz editor to build a new quiz.", None, ["Click New Quiz.", "Add a title and questions.", "Set availability, timing and attempts.", "Save and Close."], "The quiz appears on the list.", None, None, QUIZ))
add("quizzes-list", "button row", "Edit Categories", card("Edit quiz categories", "Quizzes", "Creates the headings that group quizzes on the list page.", "Organizing a course with many quizzes.", ["Click Edit Categories.", "Add or rename categories.", "Assign quizzes to them in each quiz’s settings."], None, ["These categories only organize the list. They do not affect grades."], None, QUIZ))
add("quizzes-list", "view", "View:", card("View quizzes by", "Quizzes", "Sorts the list by availability dates or by category.", None, ["Pick a view.", "Click Apply."], None, None, None, QUIZ))

add("quiz-new", "header", "Back to Manage Quizzes", back_card(Q, QT))
add("quiz-new", "left column", "Quiz Title", title_card(Q, QT))
add("quiz-new", "left column", "Grade Out Of", card("Grade Out Of", "Quizzes > New Quiz", "The quiz total, calculated from the point values of its questions. It updates as questions are added.", None, ["Add questions and set their points; the total follows."], "The total matches the sum of question points.", ["A quiz worth 0 points will not affect any grade even if it is in the gradebook."], ["“Why is my quiz out of 0?”"], QUIZ))
add("quiz-new", "left column", "Not in Grade Book", card("Grade book link", "Quizzes > New Quiz", "Connects the quiz to a gradebook item so scores flow into Grades. Not in Grade Book means scores stay in Quizzes only.", "Any quiz that counts toward the final grade.", ["Open the grade book menu.", "Add to the grade book, or link to an existing grade item.", "Save."], "The quiz score appears in Grades after an attempt is published.", ["“Quiz grade missing from Grades” is usually this being left as Not in Grade Book, or results not being published."], ["“My quiz scores aren’t showing in the gradebook.”"], QUIZ_EVAL))
add("quiz-new", "left column", "Due Date", due_card(Q, QT))
add("quiz-new", "left column", "Description", card("Description", "Quizzes > New Quiz", "Instructions learners see before starting: rules, allowed materials, time limit reminders.", None, ["Write the instructions.", "Save."], None, None, None, QUIZ))
add("quiz-new", "Questions", "Preview", card("Preview quiz", "Quizzes > New Quiz > Questions", "Shows the quiz as a learner would see it, without recording an attempt.", "Checking questions and layout before releasing the quiz.", ["Click Preview.", "Work through the questions.", "Close the preview."], None, ["Preview does not apply special access or accommodations. Do not use it to verify extra time."], None, PREVIEW))
add("quiz-new", "Questions", "Add Existing", card("Add existing questions", "Quizzes > New Quiz > Questions", "Pulls questions from the Question Library or another source into this quiz.", "Reusing a question bank.", ["Click Add Existing.", "Choose the source and select questions.", "Add, then save."], "The questions appear in the quiz list.", None, None, QUIZ))
add("quiz-new", "Questions", "Create New", card("Create a new question", "Quizzes > New Quiz > Questions", "Writes a new question directly in this quiz: multiple choice, true or false, written response, and more. Also adds sections.", None, ["Click Create New and pick a question type.", "Write the question, answers and points.", "Save the question, then save the quiz."], None, ["Written response questions need manual grading, so the quiz score stays incomplete until they are marked."], ["“Why does the quiz show no score yet?”"], QUIZ))
add("quiz-new", "Availability Dates & Conditions", "Start Date", start_end_card("Start Date", Q, QT))
add("quiz-new", "Availability Dates & Conditions", "End Date", start_end_card("End Date", Q, QT))
add("quiz-new", "Availability Dates & Conditions > Release Conditions", ["Add Release Condition", "Users are not able to access or view the quiz unless they meet the release conditions."], release_card(Q, QT))
add("quiz-new", "Availability Dates & Conditions > Special Access", ["Manage Special Access", "Special Access allows quizzes to be available to only a select group of users or individualized due dates for certain users."], manage_sa_card(Q, QT, QUIZ_SA))
add("quiz-new", "Availability Dates & Conditions", "Password", card("Quiz password", "Quizzes > New Quiz > Availability Dates & Conditions", "Learners must type this password to start the quiz. Often used for in-room exams where the instructor reads the password aloud.", "Supervised sittings.", ["Enter a password.", "Save.", "Share it with learners at the start of the sitting."], "Starting the quiz asks for the password.", ["A forgotten or mistyped password is a frequent “quiz won’t start” ticket. Check this field first."], ["“The quiz is asking my students for a password.”"], QUIZ))
add("quiz-new", "Availability Dates & Conditions > IP Restrictions", "Manage IP Restrictions", card("IP restrictions", "Quizzes > New Quiz > Availability Dates & Conditions", "Limits the quiz to computers on specific network addresses, such as a testing lab.", "Lab-only exams.", ["Click Manage IP Restrictions.", "Add the allowed address ranges.", "Save."], None, ["Learners on home or mobile networks will be blocked. Check this when only remote students report the quiz is unavailable."], ["“Students at home can’t open the exam.”"], QUIZ))
add("quiz-new", "Availability Dates & Conditions > Session Restrictions", "Lock each attempt to a single login session", card("Lock attempt to one session", "Quizzes > New Quiz > Availability Dates & Conditions", "An attempt can only continue in the browser session where it started.", "Reducing sharing of a quiz session.", ["Check the box.", "Save."], None, ["If a learner’s browser crashes or they switch devices, they may be locked out mid-attempt and need help from the instructor."], ["“My browser crashed and now I can’t get back into the quiz.”"], QUIZ))
add("quiz-new", "Timing & Display", "Set time limit", card("Set time limit", "Quizzes > New Quiz > Timing & Display", "Gives the quiz a time limit. Use Timer Settings to choose when the clock starts and what happens when it runs out.", "Timed quizzes and exams.", ["Check Set time limit.", "Enter the minutes.", "Open Timer Settings to choose the expiry behaviour.", "Save."], "The panel summary shows the time limit.", ["Learners with accommodations get their extra time from Classlist automatically. Do not create a second quiz for them."], ["“How do I make the quiz 60 minutes?”"], QUIZ))
add("quiz-new", "Timing & Display", "Time Limit", card("Time limit (minutes)", "Quizzes > New Quiz > Timing & Display", "The number of minutes each learner gets for an attempt.", None, ["Enter the minutes.", "Save."], None, ["Accommodation multipliers apply to this number, so a 1.5 multiplier on 40 minutes gives 60."], None, QUIZ))
add("quiz-new", "Timing & Display", "Asynchronous", card("Asynchronous timer", "Quizzes > New Quiz > Timing & Display", "Each learner’s clock starts when they open the quiz, so everyone gets the full time limit whenever they start.", None, None, None, None, None, QUIZ))
add("quiz-new", "Timing & Display", "Auto-submit when time is up", card("Auto-submit when time is up", "Quizzes > New Quiz > Timing & Display", "When the time limit runs out the attempt is submitted automatically with the answers saved so far.", None, None, None, ["Answers are saved as learners move through the quiz. An answer typed but not saved in the last seconds may be lost."], ["“The quiz submitted itself before I finished.”"], QUIZ))
add("quiz-new", "Timing & Display", "Timer Settings", card("Timer settings", "Quizzes > New Quiz > Timing & Display", "Chooses when the clock starts and what happens when time runs out.", None, ["Click Timer Settings.", "Choose asynchronous or synchronous start.", "Choose the expiry behaviour.", "OK, then save."], None, None, None, QUIZ))
add("quiz-new", "Timing & Display", "Paging", card("Paging", "Quizzes > New Quiz > Timing & Display", "How many questions appear per page: all together, one per page, or a page per section.", "One question per page suits long quizzes and limits lost work if a connection drops.", ["Pick a paging option.", "Save."], None, ["With one question per page, check whether learners may move back to earlier pages."], None, QUIZ))
add("quiz-new", "Timing & Display > Shuffle Quiz", "Shuffle questions and sections within the quiz. Does not cascade to sub-sections.", card("Shuffle questions", "Quizzes > New Quiz > Timing & Display", "Shows the questions in a different order for each learner.", "Reducing answer sharing.", ["Check the box.", "Save."], None, ["It does not shuffle inside sub-sections. Set shuffling on each section too if needed."], None, QUIZ))
add("quiz-new", "Timing & Display > Display", "Allow hints", card("Allow hints", "Quizzes > New Quiz > Timing & Display", "Shows the hints written on individual questions.", "Practice quizzes.", ["Check the box.", "Add hints to the questions.", "Save."], None, None, None, QUIZ))
add("quiz-new", "Timing & Display > Display", "Hide question annotation tools", card("Hide annotation tools", "Quizzes > New Quiz > Timing & Display", "Removes the highlighting and strike-through tools learners can use while answering.", None, None, None, ["Some learners rely on these tools as an accessibility aid. Check before hiding them."], None, QUIZ))
add("quiz-new", "Timing & Display > Display", "Hide question point values", card("Hide point values", "Quizzes > New Quiz > Timing & Display", "Learners do not see how many points each question is worth while answering.", None, None, None, None, None, QUIZ))
add("quiz-new", "Timing & Display > Display", "Disable Email, Instant Messages, and Alerts within Brightspace", card("Disable messages during the quiz", "Quizzes > New Quiz > Timing & Display", "Blocks Brightspace email, instant messages and alerts while a learner has an attempt open.", "Exams where outside communication should be limited.", ["Check the box.", "Save."], None, ["It only affects Brightspace. Learners can still use other apps and devices."], None, QUIZ))
add("quiz-new", "Timing & Display > Header and Footer", "Manage Header and Footer", card("Header and footer", "Quizzes > New Quiz > Timing & Display", "Adds text above or below the questions, such as a formula sheet or academic integrity statement.", None, ["Click Manage Header and Footer.", "Write the text.", "Save."], None, None, None, QUIZ))
add("quiz-new", "Attempts & Completion > Attempts", ["Manage Attempts", "1 attempt allowed"], card("Attempts allowed", "Quizzes > New Quiz > Attempts & Completion", "How many times each learner may take the quiz, and which attempt counts: highest, lowest, average, first or last.", "Practice quizzes with retakes, or exams with one attempt.", ["Click Manage Attempts.", "Set the number of attempts.", "Choose which attempt is kept as the grade.", "Save."], "The panel summary shows the attempt count.", ["To give one learner an extra attempt, use Special Access with Override attempts allowed, or reset their attempt in Grade. Do not raise attempts for the whole class."], ["“A student’s internet died. Can they try again?”"], QUIZ))
add("quiz-new", "Attempts & Completion", "Category", category_card(Q, QT))
add("quiz-new", "Attempts & Completion", "Notification Email", notify_card(Q, QT))
add("quiz-new", "Evaluation & Feedback", "Auto-publish attempt results immediately upon completion", card("Auto-publish results", "Quizzes > New Quiz > Evaluation & Feedback", "Learners see their result as soon as they submit, and the score is published.", "Auto-graded quizzes where instant feedback helps.", ["Check the box.", "Choose what learners see under When published, display to learners.", "Save."], "A test attempt shows its result right after submission.", ["With written response questions the score shown is incomplete until those are marked."], ["“Students can see their marks immediately. Can I stop that?”"], QUIZ_EVAL))
add("quiz-new", "Evaluation & Feedback", "Synchronize to grade book on publish", card("Sync to grade book on publish", "Quizzes > New Quiz > Evaluation & Feedback", "When results are published, the score is sent to the linked gradebook item.", None, ["Link the quiz to a grade item first; the option becomes available.", "Check the box.", "Save."], "Published scores appear in Grades.", ["Greyed out means the quiz is not in the gradebook yet."], ["“The quiz is graded but the mark is not in Grades.”"], QUIZ_EVAL))
add("quiz-new", "Evaluation & Feedback > When published, display to learners:", ["Attempt grade", "No questions"], card("What learners see after publishing", "Quizzes > New Quiz > Evaluation & Feedback", "Controls how much a learner sees after their attempt is published: the grade, and whether questions, their answers and correct answers are shown.", "Balancing feedback against keeping questions secure for later sittings.", ["Choose whether the attempt grade shows.", "Choose which questions are shown: none, incorrect only, or all.", "Use Customize Quiz Results Displays for more control.", "Save."], None, ["Showing correct answers while some learners have not yet written the quiz can leak the answers."], ["“Students want to see which questions they got wrong.”"], QUIZ_EVAL))
add("quiz-new", "Evaluation & Feedback", "Customize Quiz Results Displays", card("Customize results displays", "Quizzes > New Quiz > Evaluation & Feedback", "Adds extra result views, for example showing correct answers only after the quiz end date.", "Releasing answers to everyone once the quiz has closed.", ["Click Customize Quiz Results Displays.", "Add a display with a release date or condition.", "Save."], None, None, None, QUIZ_EVAL))
add("quiz-new", "Evaluation & Feedback > Learning Objectives", ["Manage Learning Objectives", "No learning objectives"], objectives_card(Q, QT))
add("quiz-new", "bottom bar", "Hidden", hidden_card(Q, QT))

add("quiz-timing-dialog", "Quiz Start", "Asynchronous: Timer starts when the learner launches the quiz", card("Asynchronous start", "Quizzes > New Quiz > Timer Settings", "Each learner gets the full time limit from the moment they open the quiz.", "Quizzes learners can take any time within a window.", None, None, None, None, QUIZ))
add("quiz-timing-dialog", "Quiz Start", "Synchronous: Timer starts on the start date", card("Synchronous start", "Quizzes > New Quiz > Timer Settings", "The clock starts for everyone at the quiz start date. A learner who joins late gets less time.", "Exams everyone writes at the same time.", None, None, ["Late joiners lose time. Explain this before an instructor chooses it."], ["“A student started 10 minutes late and only got 50 minutes.”"], QUIZ))
expire_auto = card("Automatically submit", "Quizzes > Timer Settings > When the time limit expires", "The attempt is submitted as soon as time runs out.", "Strict timed exams.", None, None, None, ["“The quiz submitted itself before I finished.”"], QUIZ)
expire_flag = card("Flag and allow to continue", "Quizzes > Timer Settings > When the time limit expires", "Learners can keep working after time runs out, but the attempt is flagged as exceeding the time limit so the instructor can decide what to do.", "Low-stakes quizzes, or when a hard cut-off would be unfair.", None, None, ["Flagged answers still count unless the instructor adjusts the grade."], None, QUIZ)
expire_none = card("Do not enforce the limit", "Quizzes > Timer Settings > When the time limit expires", "The time limit is shown as a guide only. Nothing happens when it runs out.", "Practice quizzes.", None, None, None, None, QUIZ)
for scr, grp in [("quiz-timing-dialog", "When The Time Limit Expires"), ("quiz-add-special-access-dialog", "Timing > When The Time Limit Expires")]:
    add(scr, grp, "Automatically submit the quiz attempt", expire_auto)
    add(scr, grp, 'Flag as "exceeded time limit" and allow the learner to continue working', expire_flag)
    add(scr, grp, "Do nothing: the time limit is not enforced", expire_none)
add("quiz-timing-dialog", "dialog buttons", "OK", card("Apply timer settings", "Quizzes > New Quiz > Timer Settings", "Keeps the timer choices. They are only stored when the quiz itself is saved.", None, ["Click OK.", "Save the quiz."], None, None, None, QUIZ))

sa_choice_q = card("Special access type", "Quizzes > New Quiz > Manage Special Access", "Chooses what special access does for this quiz.", "Every special access request starts here.", ["Pick the option.", "Add users and their settings.", "Save and Close, then save the quiz."], None, ["Restricting the quiz to special-access users hides it from the whole class. Choose this only when the quiz is meant for a few learners."], ["“After I gave one student extra time, nobody else could see the quiz.”"], QUIZ_SA,
                   options=[("Allow selected users special access", "The quiz stays available to everyone; the selected learners get their own dates, time limit or attempts."), ("Allow only users with special access to see this quiz", "Only the selected learners can see the quiz at all. Use it for make-up exams.")])
add("quiz-special-access-dialog", "dialog", ["Allow selected users special access to this quiz", "Allow only users with special access to see this quiz"], sa_choice_q)
add("quiz-special-access-dialog", "dialog", "Add Users to Special Access", card("Add users to special access", "Quizzes > New Quiz > Manage Special Access", "Opens the form where you set the exception and pick the learners it applies to.", None, ["Click Add Users to Special Access.", "Set dates, time limit or attempts.", "Select learners and save."], "The learners appear in the special access list.", None, None, QUIZ_SA))
qd, qs, qe = sa_dates(QT, QUIZ_SA)
add("quiz-add-special-access-dialog", "Properties > Due Date", ["Has Due Date", "Has Due Date (date)", "Has Due Date (time)"], qd)
add("quiz-add-special-access-dialog", "Properties > Availability", ["Has Start Date", "Has Start Date (date)", "Has Start Date (time)"], qs)
add("quiz-add-special-access-dialog", "Properties > Availability", ["Has End Date", "Has End Date (date)", "Has End Date (time)"], qe)
add("quiz-add-special-access-dialog", "Timing", ["Override time limit", "Original time limit: No time limit"], card("Override time limit", "Quizzes > Special Access > Timing", "Gives the selected learners a different time limit on this quiz only.", "Extra time on one quiz.", ["Check Override time limit.", "Choose Set time limit and enter the new total minutes.", "Choose what happens when time expires.", "Select learners and save."], "The special access list shows the new limit for that learner.", ["Enter the new total, not the extra. For 50% more on a 30-minute quiz, enter 45.", "For extra time on every quiz, use Classlist > Edit Accommodations instead, which uses a multiplier.", "Preview does not apply special access."], ["“Give Sam time and a half on the midterm only.”"], QUIZ_SA))
add("quiz-add-special-access-dialog", "Timing", ["Set time limit", "New Time Limit"], card("New time limit", "Quizzes > Special Access > Timing", "The total minutes the selected learners get on this quiz.", None, ["Choose Set time limit.", "Enter the total minutes.", "Save."], None, ["This replaces the quiz time limit for these learners. It is a total, not an addition."], None, QUIZ_SA))
add("quiz-add-special-access-dialog", "Timing", "No time limit", card("No time limit", "Quizzes > Special Access > Timing", "Removes the time limit for the selected learners on this quiz.", "An accommodation that calls for untimed assessment.", None, None, None, None, QUIZ_SA))
add("quiz-add-special-access-dialog", "Attempts", ["Override attempts allowed", "Attempts Allowed", "Optional Advanced Attempt Conditions will appear if a number of attempts from 2 to 10 is applied."], card("Override attempts allowed", "Quizzes > Special Access > Attempts", "Gives the selected learners a different number of attempts on this quiz.", "A learner whose attempt failed for a technical reason, or who is approved for a retake.", ["Check Override attempts allowed.", "Choose the number and click Apply.", "Select learners and save."], "The learner can start a new attempt.", ["If the learner only needs their broken attempt cleared, resetting that attempt may be simpler than adding attempts."], ["“A student’s laptop died mid-quiz. Can they try again?”"], QUIZ_SA))
qsearch, qtable = users_cards(QT, QUIZ_SA)
add("quiz-add-special-access-dialog", "Users", "Search For...", qsearch)
add("quiz-add-special-access-dialog", "Users", ["Users table", "Learner", "Demo Student (Id: DemoStudent_<ou>_<hash>)"], qtable)

# ---------- Assignments ----------
A, AT = "Assignment", "Assignments"
add("assignments-list", "button row", "New Assignment", card("New Assignment", "Assignments", "Opens the editor to create a submission folder where learners hand in work.", None, ["Click New Assignment.", "Add a title, instructions and points.", "Set dates and submission rules.", "Save and Close."], "The assignment appears on the list.", None, None, ASSIGN))
add("assignments-list", "button row", "Edit Categories", card("Edit assignment categories", "Assignments", "Creates the headings that group assignments on the list page.", None, ["Click Edit Categories.", "Add or rename categories."], None, ["These only organize the list. Grade weighting lives in Grades."], None, ASSIGN))
add("assignments-list", "empty state", "Click New Assignment to start.", card("No assignments yet", "Assignments", "This course has no assignments. Create one with New Assignment.", None, None, None, None, None, ASSIGN))

add("assignment-new", "header", "Back to Manage Assignments", back_card(A, AT))
add("assignment-new", "left column", "Assignment Title", title_card(A, AT))
add("assignment-new", "left column", "Grade Out Of", card("Grade Out Of", "Assignments > New Assignment", "The points the assignment is marked out of. Leaving it Ungraded means it collects work without a score.", None, ["Type the points.", "Use the grade book menu to add it to Grades.", "Save."], "The grade book link appears once a number is entered.", ["Changing the points after marking changes what existing scores mean. Check with the instructor before editing."], ["“I changed the assignment to be out of 50 but scores still show out of 100.”"], ASSIGN))
add("assignment-new", "left column", "In Grade Book", card("Grade book link", "Assignments > New Assignment", "Connects the assignment to a gradebook item so published marks flow to Grades.", "Any assignment that counts toward the final grade.", ["Open the grade book menu.", "Add to the grade book or link to an existing grade item.", "Save."], "Published marks appear in Grades.", ["Marks appear in Grades only after they are published from the assignment."], ["“I marked everything but Grades is empty.”"], ASSIGN_EVAL))
add("assignment-new", "left column", "Due Date", due_card(A, AT))
add("assignment-new", "left column", "Instructions", card("Instructions", "Assignments > New Assignment", "What learners see when they open the assignment: the task, requirements and any rubric expectations.", None, ["Write the instructions.", "Attach files or links with the bar below if needed.", "Save."], None, None, None, ASSIGN))
attach = card("Attachments for learners", "Assignments > New Assignment > Instructions", "Adds files, links, cloud files or an audio recording to the instructions, such as a template or rubric sheet.", None, ["Use the attachment bar under the instructions.", "Upload or link the material.", "Save."], "Learners see the attachment when they open the assignment.", ["Files linked from personal cloud storage need sharing permissions, or learners will not be able to open them."], ["“Students say the template link doesn’t work.”"], ASSIGN)
add("assignment-new", "left column > attachment bar", ["icon:upload file", "icon:link", "icon:cloud sources", "Record Audio"], attach)
add("assignment-new", "right column", "Availability Dates & Conditions", card("Availability Dates & Conditions", "Assignments > New Assignment", "Start and end dates, release conditions and special access for this assignment.", "Any question about when, or whether, learners can reach the assignment.", None, None, None, None, ASSIGN))
add("assignment-new", "Availability Dates & Conditions", "Start Date", start_end_card("Start Date", A, AT))
add("assignment-new", "Availability Dates & Conditions", "End Date", start_end_card("End Date", A, AT))
add("assignment-new", "Availability Dates & Conditions > Release Conditions", ["Add Release Condition", "Users are not able to access or view the assignment unless they meet the release conditions."], release_card(A, AT))
add("assignment-new", "Availability Dates & Conditions > Special Access", ["Manage Special Access", "Special Access allows activities to be available to only a select group of users or individualized due dates for certain users."], manage_sa_card(A, AT, ASSIGN))
add("assignment-new", "right column", "Submission & Completion", card("Submission & Completion", "Assignments > New Assignment", "Who submits, what they submit, and how many submissions are kept.", None, None, None, None, None, ASSIGN))
add("assignment-new", "Submission & Completion", "Assignment Type", card("Assignment type", "Assignments > New Assignment > Submission & Completion", "Individual means each learner submits their own work. Group means one submission per group, shared by its members.", "Group projects.", ["Create groups in the Groups tool first.", "Choose Group assignment and pick the group category.", "Save."], None, ["The type cannot be changed once submissions exist. Decide before the assignment opens."], ["“I need one submission per project team.”"], ASSIGN))
add("assignment-new", "Submission & Completion", "Category", category_card(A, AT))
add("assignment-new", "Submission & Completion", "Submission Type", card("Submission type", "Assignments > New Assignment > Submission & Completion", "What learners hand in: a file upload, text typed into Brightspace, an on-paper submission, or an observed in person activity.", None, ["Pick the type.", "Set the file rules if it is a file submission.", "Save."], None, ["On-paper and observed types have no upload box. Learners who expect to upload will report it as broken."], ["“There’s no button to upload my work.”"], ASSIGN))
files = card("Files allowed per submission", "Assignments > New Assignment > Submission & Completion", "Whether each submission can contain many files or exactly one.", None, None, None, ["With One File, a learner with several parts must combine them first."], ["“It only lets me upload one file.”"], ASSIGN,
             options=[("Unlimited", "Learners can attach several files in one submission."), ("One File", "Each submission holds exactly one file.")])
add("assignment-new", "Submission & Completion > Files Allowed Per Submission", ["Unlimited", "One File"], files)
add("assignment-new", "Submission & Completion", "Allowable File Extensions", card("Allowed file types", "Assignments > New Assignment > Submission & Completion", "Limits uploads to certain file types, such as PDF only.", "When the instructor needs a specific format for marking or annotation.", ["Choose a restriction.", "Save."], "Uploading another type is refused.", ["Students on phones often produce HEIC or Pages files. A strict PDF-only rule creates tickets unless learners are told how to convert."], ["“It won’t accept my file.”"], ASSIGN))
subs = card("Which submissions are kept", "Assignments > New Assignment > Submission & Completion", "Controls what happens when a learner submits more than once.", None, None, None, ["With Only one submission allowed, a learner who uploads the wrong file cannot fix it themselves. The instructor has to delete the submission or allow another."], ["“I uploaded the wrong file and can’t resubmit.”"], ASSIGN_SUBMIT,
            options=[("All submissions are kept", "Every upload is saved; the instructor sees them all."), ("Only one submission allowed", "The first submission is final."), ("Only the most recent submission is kept", "Each new upload replaces the previous one.")])
add("assignment-new", "Submission & Completion > Submissions", ["All submissions are kept", "Only one submission allowed", "Only the most recent submission is kept"], subs)
add("assignment-new", "Submission & Completion", "Notification Email", notify_card(A, AT))
add("assignment-new", "right column", "Evaluation & Feedback", card("Evaluation & Feedback", "Assignments > New Assignment", "Rubrics, outcomes, annotation, anonymous marking and similarity checking for this assignment.", None, None, None, None, None, ASSIGN_EVAL))
add("assignment-new", "Evaluation & Feedback > Rubrics", "Add Rubric", card("Add rubric", "Assignments > New Assignment > Evaluation & Feedback", "Attaches a rubric so marking uses consistent criteria and learners can see how they will be assessed.", None, ["Click Add Rubric.", "Choose an existing rubric or create one.", "Save."], "The rubric opens in the evaluation screen.", ["A rubric’s visibility setting decides whether learners see it before marking. Check it when learners say they can’t find the rubric."], ["“Students can’t see the rubric.”"], ASSIGN_EVAL))
add("assignment-new", "Evaluation & Feedback > Learning Objectives", ["Manage Learning Objectives", "No learning objectives"], objectives_card(A, AT))
add("assignment-new", "Evaluation & Feedback > Annotation Tools", "Make annotation tools available for assessment", card("Annotation tools", "Assignments > New Assignment > Evaluation & Feedback", "Lets the instructor mark up submitted files directly: highlights, comments and drawings on the document.", None, ["Check the box.", "Save."], "Opening a submission shows the annotation toolbar.", ["Annotations only work on supported file types. Unusual formats open without the toolbar."], ["“I can’t write comments on the student’s PDF.”"], ASSIGN_EVAL))
add("assignment-new", "Evaluation & Feedback > Anonymous Marking", "Hide student names during assessment", card("Anonymous marking", "Assignments > New Assignment > Evaluation & Feedback", "Hides learner names while marking to reduce bias. Names are revealed when marks are published.", None, ["Check the box before submissions arrive.", "Save."], None, ["Marks are published together for everyone, not one at a time."], ["“Why can’t I publish one student’s mark?”"], ASSIGN_EVAL))
add("assignment-new", "Evaluation & Feedback > Turnitin Integration", ["Manage Turnitin", "Turnitin(TM) adds additional functionality to evaluation."], card("Turnitin", "Assignments > New Assignment > Evaluation & Feedback", "Turns on similarity checking for submissions, where the institution licenses Turnitin.", None, ["Click Manage Turnitin.", "Enable similarity checking and choose its options.", "Save."], "Submissions show a similarity score after processing.", ["Reports take time to generate, so a fresh submission may show no score yet."], ["“The similarity score isn’t showing.”"], ASSIGN))
add("assignment-new", "bottom bar", "Hidden", hidden_card(A, AT))

sa_choice_a = card("Special access type", "Assignments > New Assignment > Manage Special Access", "Chooses what special access does for this assignment.", "Every extension or private-folder request starts here.", ["Pick the option.", "Add users and their dates.", "Save and Close, then save the assignment."], None, ["Restricting the folder to special-access users hides it from the whole class."], ["“After I extended one student, the assignment disappeared for everyone.”"], ASSIGN,
                   options=[("Allow users with special access to submit outside the normal availability dates", "The assignment stays open to everyone; the selected learners get their own dates."), ("Allow only users with special access to see this folder", "Only the selected learners can see the assignment.")])
add("assignment-manage-special-access-dialog", "dialog", ["Allow users with special access to submit outside the normal availability dates for this folder", "Allow only users with special access to see this folder"], sa_choice_a)
add("assignment-manage-special-access-dialog", "dialog", "Add Users to Special Access", card("Add users to special access", "Assignments > New Assignment > Manage Special Access", "Opens the form where you set new dates and pick the learners they apply to.", None, ["Click Add Users to Special Access.", "Set the due, start or end dates.", "Select learners and save."], None, None, None, ASSIGN))
ad, as_, ae = sa_dates(AT, ASSIGN_SUBMIT)
add("assignment-special-access-user-dialog", "Properties > Due Date", ["Has Due Date", "Has Due Date (date)", "Has Due Date (time)"], ad)
add("assignment-special-access-user-dialog", "Properties > Availability", ["Has Start Date", "Has Start Date (date)", "Has Start Date (time)"], as_)
add("assignment-special-access-user-dialog", "Properties > Availability", ["Has End Date", "Has End Date (date)"], ae)
asearch, atable = users_cards(AT, ASSIGN)
add("assignment-special-access-user-dialog", "Users", "Search For...", asearch)
add("assignment-special-access-user-dialog", "Users", ["Users table", "Learner", "Demo Student"], atable)

# ---------- Classlist ----------
add("classlist", "button row", "Add Participants", card("Add participants", "Classlist", "Enrols people into this course, one at a time or in bulk, where the role allows it.", "Adding a TA or guest. Student enrolment usually comes from the student system instead.", ["Open Add Participants.", "Choose to add existing users or create new ones.", "Pick the role and save."], "The person appears in the Classlist with the chosen role.", ["Manually added students may be removed by the next student-system sync. Check how enrolment is managed before adding learners by hand."], ["“Can you add my TA to the course?”"], CLASSLIST))
add("classlist", "button row", "Class Engagement", card("Class engagement", "Classlist", "Shows how recently and how often learners have been active in the course.", "Spotting learners who have not logged in.", None, None, ["Activity shows access, not understanding or completed work."], ["“Which students haven’t logged in yet?”"], CLASSLIST))
add("classlist", "button row", "Enrollment Statistics", card("Enrollment statistics", "Classlist", "Counts of participants by role.", None, None, None, None, None, CLASSLIST))
add("classlist", "button row", "Email Classlist", card("Email the class", "Classlist", "Sends an email to everyone in the course, or to selected people.", None, ["Click Email Classlist, or select learners and email them.", "Write and send."], None, ["Messages go to learners’ institutional addresses. Learners who do not check them will miss it."], ["“How do I email the whole class?”"], CLASSLIST))
add("classlist", "search", "Search For...", card("Search the classlist", "Classlist", "Finds a participant by name, username or ID.", None, ["Type part of a name.", "Press Enter."], None, None, None, CLASSLIST))
add("classlist", "row actions", "Email", card("Email selected", "Classlist", "Emails the participants whose boxes are checked.", None, ["Check the participants.", "Click Email."], None, None, None, CLASSLIST))
add("classlist", "row actions", "Instant Message", card("Instant message", "Classlist", "Sends a Brightspace instant message to the selected participants.", None, None, None, None, None, CLASSLIST))
add("classlist", "row actions", "Enrollment", card("Change enrolment", "Classlist", "Changes the role of the selected participants in this course, such as Learner to TA.", None, ["Check the participant.", "Click Enrollment and pick the new role.", "Save."], "The Role column shows the new role.", ["Roles control what someone can see and do. A wrong role is a common cause of “I can’t see the gradebook”."], ["“My TA can’t see the submissions.”"], CLASSLIST))
add("classlist", "row actions", "Unenroll", card("Unenrol", "Classlist", "Removes the selected participants from this course.", "Removing a TA or a test account. Student drops usually come from the student system.", ["Check the participant.", "Click Unenroll and confirm."], None, ["Treat this as hard to undo. Re-enrolling restores access, but double-check the right person is selected before confirming."], ["“A student dropped but is still in my course.”"], CLASSLIST))
add("classlist", "table", ["Classlist table", "[instructor row: real name withheld]", "Student, Demo"], card("Participant list", "Classlist", "Everyone enrolled in the course with their role and last access. Each name has a menu with actions for that person.", None, ["Find the person.", "Use the arrow beside their name for email, progress, groups or accommodations."], None, None, ["“Is this student actually enrolled in my course?”"], CLASSLIST))
add("classlist", "table", "icon:chevron beside Student, Demo", card("Participant menu", "Classlist", "Actions for one person: send email, view progress, view groups, and Edit Accommodations.", "Opening a learner’s progress or setting their quiz accommodations.", ["Click the arrow beside the name.", "Choose the action."], None, None, ["“Where do I set extra time for a student?”"], CLASSLIST))
add("classlist", "footer", ["10 per page", "Total Users: 2"], card("Page size", "Classlist", "How many people show per page, and the total enrolled.", None, None, None, None, None, CLASSLIST))

add("classlist-edit-accommodations", "dialog header", "Demo Student", card("Accommodations for this learner", "Classlist > Edit Accommodations", "The learner these accommodations apply to. Settings here apply across every quiz in this course.", None, None, None, ["Confirm the exact learner before saving. Accommodation details are private; do not include the reason in tickets or notes."], None, ACCOM))
add("classlist-edit-accommodations", "Quizzes > Timing", "Modify Time Limit", card("Modify time limit", "Classlist > Edit Accommodations > Quizzes > Timing", "Gives this learner more time on every timed quiz in the course, automatically.", "A learner with an approved extra-time accommodation.", ["Open the learner’s menu in Classlist and choose Edit Accommodations.", "Check Modify Time Limit.", "Choose a multiplier or extra minutes.", "Save."], "Reopen the dialog and confirm the saved value.", ["Quiz Preview does not show accommodations. Verify from this dialog, or with a demo learner.", "Special access on one quiz can override the accommodation for that quiz."], ["“Give this student time and a half on all quizzes.”"], ACCOM))
mult = card("Multiplier of original quiz time", "Classlist > Edit Accommodations > Quizzes > Timing", "Multiplies each quiz’s time limit. 1.5 gives time and a half, 2 gives double time.", "Most extra-time accommodations, since they scale with each quiz’s length.", ["Choose Multiplier.", "Enter the multiplier, such as 1.5.", "Save."], "A 20-minute quiz becomes 30 minutes and a 40-minute quiz becomes 60.", ["Enter 1.5, not 50. The number multiplies the time."], ["“The student should get 50% extra time.”"], ACCOM)
add("classlist-edit-accommodations", "Quizzes > Timing", ["Multiplier of original quiz time", "Multiplier of original quiz time (value)"], mult)
extra = card("Extra time", "Classlist > Edit Accommodations > Quizzes > Timing", "Adds a fixed number of minutes to every timed quiz.", "An accommodation stated as a set number of minutes.", ["Choose Extra time.", "Enter the minutes.", "Save."], None, ["The same minutes are added to short and long quizzes alike. A multiplier is usually fairer when quiz lengths vary."], None, ACCOM)
add("classlist-edit-accommodations", "Quizzes > Timing", ["Extra time", "Extra time (value)"], extra)
add("classlist-edit-accommodations", "dialog header", "icon:close", card("Close without saving", "Classlist > Edit Accommodations", "Closes the dialog. Nothing changes unless you clicked Save.", None, None, None, None, None, ACCOM))

# ---------- Panel headers, menus and remaining controls ----------
add("quiz-new", "header", "New Quiz", card("Quiz editor", "Quizzes > New Quiz", "The page for building one quiz: questions on the left, settings in the panels on the right.", None, ["Add a title and questions.", "Work down the panels on the right.", "Save and Close."], None, None, None, QUIZ))
add("assignment-new", "header", "New Assignment", card("Assignment editor", "Assignments > New Assignment", "The page for building one assignment: details on the left, settings in the panels on the right.", None, ["Add a title, points and instructions.", "Work down the panels on the right.", "Save and Close."], None, None, None, ASSIGN))
add("quiz-new", "Questions", "Ready to begin adding quiz content?", card("No questions yet", "Quizzes > New Quiz > Questions", "This quiz has no questions. Add some from the library or write new ones.", None, ["Click Add Existing or Create New."], None, None, None, QUIZ))
add("quiz-new", "right column", "Availability Dates & Conditions", card("Availability Dates & Conditions", "Quizzes > New Quiz", "Start and end dates, release conditions, special access, password and network limits for this quiz.", "Any question about when, or whether, learners can open the quiz.", ["Click the panel header to open it.", "Adjust the setting.", "Save."], None, None, ["“My student can’t open the quiz.”"], QUIZ))
add("quiz-new", "right column", "Timing & Display", card("Timing & Display", "Quizzes > New Quiz", "Time limit, timer behaviour, paging, shuffling and what learners see while answering.", None, ["Click the panel header to open it.", "Adjust the setting.", "Save."], None, None, None, QUIZ))
add("quiz-new", "right column", "Attempts & Completion", card("Attempts & Completion", "Quizzes > New Quiz", "Number of attempts, which attempt counts, the list category and completion emails.", None, ["Click the panel header to open it.", "Adjust the setting.", "Save."], None, None, None, QUIZ))
add("quiz-new", "right column", "Evaluation & Feedback", card("Evaluation & Feedback", "Quizzes > New Quiz", "Publishing, grade book sync, what learners see after the quiz, and learning objectives.", None, ["Click the panel header to open it.", "Adjust the setting.", "Save."], None, None, ["“Students can’t see their quiz results.”"], QUIZ_EVAL))
close_card = card("Close without saving", "Special Access dialog", "Closes the dialog. Nothing changes unless you saved.", None, ["Click the X, or Cancel."], None, None, None, QUIZ_SA)
add("quiz-special-access-dialog", "dialog header", "icon:close", close_card)
add("assignment-manage-special-access-dialog", "dialog header", "icon:close", close_card)
per_page = card("Learners per page", "Special Access > Users", "How many learners show per page in the list.", None, ["Choose a page size, or search to find one learner."], None, None, None, QUIZ_SA)
add("quiz-add-special-access-dialog", "Users", "20 per page", per_page)
add("assignment-special-access-user-dialog", "Users", "20 per page", per_page)
add_menu("classlist", "Add existing users", card("Add existing users", "Classlist > Add Participants", "Enrols someone who already has an account at the institution.", "Adding a TA, co-instructor or guest.", ["Open Add Participants, then Add existing users.", "Search for the person.", "Pick their role and enrol."], "They appear in the Classlist with that role.", ["Choose the role carefully. It decides what they can see and change."], ["“Can you add my TA?”"], CLASSLIST))
add_menu("classlist", "Send Email", card("Send email", "Classlist > participant menu", "Emails this one person.", None, ["Open the arrow beside the name.", "Choose Send Email."], None, None, None, CLASSLIST))
add_menu("classlist", "Impersonate", card("Impersonate", "Classlist > participant menu", "Signs you in as this person to see exactly what they see. Available only to roles with that permission.", "Reproducing what a learner reports, such as a missing activity.", ["Open the arrow beside the name.", "Choose Impersonate.", "Look, but do not submit or change anything.", "End impersonation from your profile menu."], "You see the course as that person.", ["Actions taken while impersonating are recorded as that person. Look, do not act."], ["“The student says the quiz isn’t there. Can you see what they see?”"], CLASSLIST))
add_menu("classlist", "View progress", card("View progress", "Classlist > participant menu", "One learner’s activity in the course: grades, content visited, submissions, quiz attempts and logins.", "Checking whether a learner actually submitted or opened something.", ["Open the arrow beside the name.", "Choose View progress.", "Pick the area to review."], None, ["Progress shows access, not understanding."], ["“The student says they submitted. Did they?”"], CLASSLIST))
add_menu("classlist", "View groups", card("View groups", "Classlist > participant menu", "Which groups this learner belongs to.", "Group assignment problems, such as a learner who cannot see their group’s submission folder.", ["Open the arrow beside the name.", "Choose View groups."], None, ["A learner outside the group category cannot submit to a group assignment."], ["“I can’t see my group’s assignment.”"], CLASSLIST))
add_menu("classlist", "Edit Accommodations", card("Edit accommodations", "Classlist > participant menu", "Opens this learner’s quiz accommodations, such as extra time on every quiz in the course.", "An approved accommodation that applies to all quizzes.", ["Open the arrow beside the name.", "Choose Edit Accommodations.", "Set the time change and save."], "Reopen the dialog and confirm the saved value.", ["For one quiz only, use that quiz’s Special Access instead."], ["“This student gets time and a half on all quizzes.”"], ACCOM))
add_menu("assignment-new", ["Edit or Link to Existing", "Not in Grade Book", "Reset to Ungraded"], card("Grade book options", "Assignments > New Assignment > grade book menu", "Chooses how the assignment connects to Grades: a new grade item, an existing one, not in the grade book, or back to ungraded.", None, ["Open the grade book menu under Grade Out Of.", "Pick the option.", "Save."], "The label under Grade Out Of shows the choice.", ["Unlinking from the grade book stops new marks flowing to Grades. Existing grades stay where they are."], ["“Marks aren’t going into the gradebook.”"], ASSIGN_EVAL))
add("quizzes-list", "empty state", "You haven't created any quizzes. Click New Quiz to add a new quiz.", card("No quizzes yet", "Quizzes", "This course has no quizzes. Create one with New Quiz.", None, ["Click New Quiz."], None, None, None, QUIZ))

STEPS = {'Asynchronous timer': ['Check Set time limit.', 'Open Timer Settings and choose the asynchronous start.', 'Save.'], 'Auto-submit when time is up': ['Open Timer Settings.', 'Under When the time limit expires, choose Automatically submit.', 'Save.'], 'Hide annotation tools': ['Check Hide question annotation tools.', 'Save.'], 'Hide point values': ['Check Hide question point values.', 'Save.'], 'Asynchronous start': ['Select this option.', 'Click OK.', 'Save the quiz.'], 'Synchronous start': ['Make sure the quiz has a Start Date.', 'Select this option.', 'Click OK, then save the quiz.'], 'Automatically submit': ['Select this option.', 'Click OK or Save.', 'Save the quiz.'], 'Flag and allow to continue': ['Select this option.', 'Click OK or Save.', 'After the quiz, review flagged attempts in Grade.'], 'Do not enforce the limit': ['Select this option.', 'Click OK or Save.', 'Save the quiz.'], 'No time limit': ['Check Override time limit.', 'Choose No time limit.', 'Select the learners and save, then save the quiz.'], 'No assignments yet': ['Click New Assignment.', 'Fill in the title, instructions and dates.', 'Save and Close.'], 'Availability Dates & Conditions': ['Click the panel header to open it.', 'Set start and end dates, release conditions or special access.', 'Save.'], 'Submission & Completion': ['Click the panel header to open it.', 'Set the assignment type, submission type and file rules.', 'Save.'], 'Files allowed per submission': ['Choose Unlimited or One File.', 'Save.'], 'Which submissions are kept': ['Choose the submission rule.', 'Save.'], 'Evaluation & Feedback': ['Click the panel header to open it.', 'Add a rubric, outcomes, annotation or similarity checking.', 'Save.'], 'Class engagement': ['Click Class Engagement.', 'Sort by last access to find learners who have not been active.'], 'Enrollment statistics': ['Click Enrollment Statistics.', 'Read the counts by role.'], 'Instant message': ['Check the participants.', 'Click Instant Message.', 'Write and send.'], 'Page size': ['Choose how many people to show per page.'], 'Accommodations for this learner': ['Check the name matches the learner in the request.', 'Set the accommodation below.', 'Save.'], 'Close without saving': ['Click the X, or Cancel.']}
for _c in CARDS.values():
    if not _c.get("howTo"):
        _c["howTo"] = STEPS[_c["title"]]


def main():
    out = ROOT / "data/help/screens.json"
    json.dump(CARDS, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(out, "a", encoding="utf-8").write("\n")
    distinct = len({id(c) for c in CARDS.values()})
    print(f"wrote {len(CARDS)} control entries ({distinct} distinct cards) to {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
