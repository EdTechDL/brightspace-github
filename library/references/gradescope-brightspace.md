# Gradescope with Brightspace (D2L): integration reference

Documentation-based reference for a D2L Brightspace training simulator. Everything below comes from guides.gradescope.com as read on 2026-09-22. Nothing here was observed in a live course. UI labels are quoted exactly as the guides print them; a label the guides do not print is marked UNCONFIRMED. The guides use the name "Brightspace" throughout and note that an institution may call it D2L or Desire2Learn.

Scope notes from the guides:
- "Gradescope integrations with LMSs, such as Brightspace, are available with an institutional Gradescope license."
- "When you access Gradescope through Brightspace, you and your students won't need to create or use a separate Gradescope password" (authentication is via Brightspace credentials).
- The instructor guide lists seven steps: 1 Add Gradescope to your course-level navbar, 2 Link your courses, 3 Sync your roster, 4 Set up your assignment, 5 Grade submissions, 6 Link your assignment to Brightspace, 7 Post Grades.

Source: https://guides.gradescope.com/hc/en-us/articles/23587619649805-Using-Gradescope-LTI-1-3-with-Brightspace-D2L-as-an-Instructor, checked 2026-09-22

## (a) Instructor workflow with LTI 1.3, step by step

### a1. Launch point: adding Gradescope to the course-level navbar (Brightspace side)
1. "Access your course."
2. "From the dotted menu, select either Edit this Navbar to edit one course navbar or Manage all Course Navbars to edit all your course navbars."
3. "Select Add Links, on the Edit Navbar page."
4. "Select Create Custom Link from the Add Links modal."
5. "Enter a name and for the URL, select Insert Quicklink."
6. "Choose External Learning Tools and then Gradescope from the Insert Quicklink modal."
7. Note in the guide: "Don't see Gradescope? Based on your institution's configuration, you may not see the Gradescope course-level LTI link." (The remainder of this note was not captured verbatim; the parallel LTI 1.0 article continues: if Gradescope is not listed, link the course while linking an assignment instead.)
8. "Select Create to close the Create Custom Link modal."
9. "Make sure the Gradescope link is checked and select Add to close the Add Links modal."
10. "You should now see Gradescope added to your navbar links list back on the Edit Navbar page."
11. "Select Save and Close. Gradescope will now appear in the navigation bar for your course or courses."

The guide also describes a second launch point used in later steps: "log in to Brightspace > Click your course > Click Content > Click the module where you added Gradescope > Click the Gradescope tool link there." Both the navbar link and the Content module link take the instructor to the "Gradescope Course Dashboard". A third route is the Gradescope website itself ("log in to the Gradescope website and click your course").

Source: https://guides.gradescope.com/hc/en-us/articles/23587619649805-Using-Gradescope-LTI-1-3-with-Brightspace-D2L-as-an-Instructor, checked 2026-09-22

### a2. First launch: account creation or linking, and course linking
1. "Log in to Brightspace. Navigate to the homepage of the Brightspace course you'd like to link to Gradescope."
2. "On your Brightspace course homepage, select More at the end of the top navigation bar and then select Gradescope (it may be named slightly differently)."
3. "Once Gradescope launches, you'll see a dialog box with course-linking options. Choose to link to a new or existing course, and then select Link Course to go to the Course Settings page."
4. "On the Gradescope Course Settings page, you can update the course title, description, rubric types, and score bounds."
5. "When you're finished, select Update Course. Your course is now linked and students will be able to access it."
6. "Next, it's recommended that you sync your roster."

Account behaviour on first launch, as the guide states it:
- New users: "At this point, a new Gradescope account will be created for you if you do not already have one" associated with the email address used in Brightspace.
- Existing users: "If you already have a Gradescope account under your school email address" and that is the email on the Brightspace account, "clicking the Gradescope link inside Brightspace will take you to your existing account" and no new account is created.
- Students: "Students are automatically added to the Gradescope roster once they select a Gradescope course or assignment link".

Linking an existing Gradescope course: the same dialog offers the existing-course choice ("Choose to link to a new or existing course"). The exact radio or dropdown labels inside the dialog are UNCONFIRMED; the guide prints only "Link Course" as the confirming button. The LTI 1.0 article additionally describes linking from the Gradescope side ("link it back to Brightspace from the Gradescope Course Settings page"); whether that alternate route exists under LTI 1.3 is UNCONFIRMED.

Multiple Gradescope courses per Brightspace course: "If you have several courses on Gradescope that correspond to a single Brightspace course, it is not recommended that you link your Brightspace course to Gradescope." The LTI 1.0 article gives the reason: linking "would allow students to enroll in any of the Gradescope courses that are associated with the single Brightspace course."

Source: https://guides.gradescope.com/hc/en-us/articles/23587619649805-Using-Gradescope-LTI-1-3-with-Brightspace-D2L-as-an-Instructor (and, for the reason and alternate route, https://guides.gradescope.com/hc/en-us/articles/23587410040717-Using-Gradescope-LTI-1-0-with-Brightspace-D2L-as-an-Instructor), checked 2026-09-22

### a3. Roster sync (Gradescope side)
1. Go to the "Gradescope Course Dashboard" (via the Brightspace link or the Gradescope website).
2. "expand the left sidebar (if it isn't already) and click Roster to get to your Roster page."
3. Button name: "click the Sync Brightspace Roster button." Guide caveat: "If your institution is using the latest version of the Gradescope tool (LTI 1.3), your roster sync button may display a customized name your institution has chosen instead of the word 'Brightspace.'" (The admin guide's "Branded Platform Name" supplies that word.)
4. "A dialog box will appear explaining how accounts will be synced. All names, emails, and IDs will be auto-synced from Brightspace. All roles will be synced depending on how your institution initially configured your Gradescope integration." Also: "ID and section name syncing: If your institution uses the older version of the Gradescope tool (LTI 1.0+API), your IDs and section names will be auto-synced also."
5. Notification checkbox in the dialog: "Let new users know that they were added to the course" (checked by default; "By default, Gradescope will email users to say that they've been added to the course"). Then "click Sync Roster."
6. First-time authorization: "If you haven't already associated your Brightspace account with Gradescope, you will be taken to the Brightspace login screen. After you log in to Brightspace, a message will appear asking if you'd like to authorize Gradescope. Click Continue and then click the Sync Roster button again in Gradescope."
7. Re-sync: "If students add/drop in Brightspace, be sure to re-sync the roster. Existing submissions/grades for dropped students will be preserved."
8. Sections and groups after sync: "click Download Roster (bottom of Gradescope Roster page) > Add a Section and/or Group column with section or group values to the CSV file > Click Add Students or Staff > Upload the CSV back to Gradescope." "Brightspace linking and any existing submissions and grades will be preserved as long as emails stay the same."

What the sync matches on: email address. The guides tie linking to the email ("as long as emails stay the same"), and the troubleshooting article says members without an email address in Brightspace cannot be synced.
What happens to students no longer in D2L: the guide states only that their submissions and grades are preserved; whether a re-sync removes them from the Gradescope roster is UNCONFIRMED. The troubleshooting article notes that after unlinking and relinking, "the initially synced roster will remain on the Roster page".
Section sync under LTI 1.3: UNCONFIRMED. The 1.3 article states names, emails and IDs; the "sections ... also" sentence is scoped to LTI 1.0+API. The admin article describes an optional config variable ("d2l.Tools.Lti.SendLisPersonSourcedId") to send student IDs, so ID sync under 1.3 depends on admin setup.

Source: https://guides.gradescope.com/hc/en-us/articles/23587619649805-Using-Gradescope-LTI-1-3-with-Brightspace-D2L-as-an-Instructor, checked 2026-09-22

### a4. Setting up the assignment (Gradescope side) and the assignment link (Brightspace side)
Gradescope side (Step 4 of the guide):
1. "On your Gradescope Course Dashboard, click an existing Gradescope assignment or click Create Assignment to make a new one. If you're updating an existing assignment, click Settings in the left sidebar, make your changes, and then click Save."
2. "If you're creating a new assignment, next choose the assignment type and settings. When you've chosen your settings, click Create Assignment."
3. "To finalize the assignment link and set up, select the assignment link you just created in Brightspace to go back to Gradescope. You won't be able to post grades until you do this step."
4. "For student-uploaded assignments, once your release date passes in Gradescope, students will be able to submit work via the Gradescope website or by clicking the Gradescope tool link in their Brightspace course module."
5. Guide FAQ: "Do I need to link my Gradescope assignment to Brightspace? Yes, but not until you're ready to post Gradescope grades to your Brightspace Grades page. At that time you will need to connect your Gradescope assignment to a Brightspace grade item that you've set up to have the same overall point value as your Gradescope assignment."
6. Assignment name under LTI 1.3 (from the Assignment Settings Overview): "If the class or assignment is linked via an LTI 1.3 learning management system (LMS) integration, the Gradescope assignment name comes from the LMS and can only be changed within the LMS."

Brightspace side (Step 6 of the guide, "Linking your assignment to Brightspace"):
1. "Log in to Brightspace and access your course."
2. "Select Content and then Add Existing Activities from your Module."
3. "Select the Gradescope 1.3 assignment. You will be taken to a new modal to link the Brightspace assignment to the Gradescope assignment." (The item name in the "Add Existing Activities" dropdown is whatever the admin named the deployment link; the guide calls it "the Gradescope 1.3 assignment".)
4. "In the Gradescope modal, choose how you want to link the assignment and select to either Create a new assignment or Link with an existing assignment."
5. "Select Link Assignment."

Source: https://guides.gradescope.com/hc/en-us/articles/23587619649805-Using-Gradescope-LTI-1-3-with-Brightspace-D2L-as-an-Instructor and https://guides.gradescope.com/hc/en-us/articles/22242992536205-Assignment-Settings-Overview, checked 2026-09-22

### a5. Grading (Gradescope side)
"On your Gradescope Course Dashboard, click the assignment and Grade Submissions in the left sidebar to start grading." The guide states the grading process is the same for Brightspace and non-Brightspace users and points to the Grading Submissions article. "Once you've finished grading, be sure to connect your Gradescope assignment to a Brightspace grade item so you can post grades to Brightspace".

Source: https://guides.gradescope.com/hc/en-us/articles/23587619649805-Using-Gradescope-LTI-1-3-with-Brightspace-D2L-as-an-Instructor, checked 2026-09-22

### a6. Posting grades to Brightspace
1. "First, make sure you've linked your assignment and synced your roster."
2. "With your Gradescope assignment open, expand the left sidebar (if it isn't already) and select Review Grades."
3. "On the Gradescope Review Grades page, select the Post Grades to Brightspace button. When the dialog box appears, select Post Grades."
4. What "post" means: "Posting grades to Brightspace will only post the students' final assignment scores from Gradescope to the linked grade item in Brightspace. Only grades for fully graded submissions (which have a checkmark in the Graded column on the Gradescope Review Grades page) will be posted."
5. Missing button: "If the Post Grades to Brightspace button does not appear on the Review Grades page, launch the Brightspace assignment to open the Gradescope assignment".
6. Student-facing detail is separate from posting: "To allow students to also see their graded, annotated submissions, question-by-question scores, rubrics, and feedback on Gradescope, select the Publish Grades."
7. Email: "To alert students via email that their grades are now visible, select the Compose Email to Students at the bottom of the Review Grades page."

Grade item behaviour and points: the LTI 1.3 guide says the instructor connects the assignment "to a Brightspace grade item that you've set up to have the same overall point value as your Gradescope assignment", and the troubleshooting fix for posting failures is "Ensure the point values are the same for the assignment in Gradescope and the assignment in Brightspace." The admin guide's deployment option "Grades created by LTI will be included in Final Grade (recommended)" is described as "syncs the grades from Gradescope to your D2L gradebook." Whether the LTI 1.3 deep link creates the Brightspace grade item automatically is UNCONFIRMED (the LTI 1.0 article says linking "will automatically add an item to your Brightspace gradebook"; the 1.3 article does not say this). The grade item type is UNCONFIRMED for 1.3 (the 1.0 article recommends "Numeric"). Re-running: the 1.3 article does not say whether posting can be repeated; the 1.0 article's fix "Re-sync the roster in Gradescope > Click Post Grades to Brightspace again" implies it can. Treat as UNCONFIRMED for 1.3.

Source: https://guides.gradescope.com/hc/en-us/articles/23587619649805-Using-Gradescope-LTI-1-3-with-Brightspace-D2L-as-an-Instructor, https://guides.gradescope.com/hc/en-us/articles/21753755447949-Troubleshooting-Brightspace-D2L-Issues-for-Instructors, https://guides.gradescope.com/hc/en-us/articles/21791026788109-Configuring-Gradescope-LTI-1-3-in-Brightspace-D2L-for-Admins, checked 2026-09-22

### a7. Notes on TAs, sections and multiple links
- TAs: "If you are a Brightspace teaching assistant (TA) and you find that you are unable to sync rosters, create assignments, grade submissions, or post grades in Gradescope, ask an instructor to change your role to 'instructor' on the Brightspace course classlist and resync the roster in Gradescope." The generic FAQ adds that roster sync and grade posting "both involve accessing student email addresses" and a role may lack that permission.
- Roles: "All roles will be synced depending on how your institution initially configured your Gradescope integration." (The admin guide's registration step selects "Send Institution Role".)
- Sections: see a3; section names can be added by CSV after sync. LTI 1.3 automatic section sync is UNCONFIRMED.
- Multiple links: one course-level link (navbar, "Basic Launch" in the admin guide) plus one assignment-level link per assignment (Content module, "Deep Linking Quicklink" in the admin guide). Several Gradescope courses linked to one Brightspace course is not recommended (see a2).

Source: https://guides.gradescope.com/hc/en-us/articles/23587619649805-Using-Gradescope-LTI-1-3-with-Brightspace-D2L-as-an-Instructor and https://guides.gradescope.com/hc/en-us/articles/21576876947981-Why-can-t-I-sync-my-LMS-course-roster-or-post-grades-to-my-LMS, checked 2026-09-22

## (b) What a student sees when launching from Brightspace
- Access: "When accessing Gradescope through Brightspace, simply navigate to your course and select the Gradescope tool link in your course module." No separate Gradescope login is needed through the LMS.
- Direct website access options listed by the guide: pick the school from the SAML list and log in with school credentials; use "Forgot your password?" with the Brightspace email if previously accessed via Brightspace; or sign up with a course code if new. The same account is used either way; different email addresses can produce multiple accounts.
- Submitting: 1. "Log in to Brightspace. Select your course." 2. Select "Content". The Gradescope assignment "will either launch directly or direct you to the Gradescope Course Dashboard." 3. Follow the instructor's settings for uploading PDFs, images, linking code repositories, or answering questions online. 4. "Once you've submitted the assignment, if your instructor has allowed it, you can view your submission."
- Viewing grades: 1. Log in to Brightspace, click the course, then select "Grades" (the posted final score). 2. To see the submission and feedback, select "Content" and open the Gradescope assignment or Course Dashboard. 3. "Once your Gradescope assignment launches, if your instructor has published grades to Gradescope, you will be able to see your submission, points breakdown, and any comments your instructor gave you."

Source: https://guides.gradescope.com/hc/en-us/articles/21749752941069-Using-Gradescope-with-Brightspace-D2L-as-a-Student, checked 2026-09-22

## (c) Troubleshooting article, condensed

| Symptom (as titled in the guide) | Cause (as the guide states it) | Fix (as the guide states it) |
| --- | --- | --- |
| "I can only sync part of my roster." | "most likely, these members do not have an email address associated with their account in Brightspace." | "either ask the course members or your Brightspace admin to add the email addresses to the accounts in Brightspace. Then re-sync the roster." |
| "I can't sync my roster at all." | Role permissions (TA role) | "TAs: Ask an instructor to change your role to 'instructor' on the Brightspace course class list and resync the roster in Gradescope. Instructors: Please contact help@gradescope.com." |
| "After I unlink a D2L course from Gradescope, the initially synced roster will remain on the Roster page even after I link a new course." | Unlink does not clear previously synced students | "Please contact help@gradescope.com to have the excess students removed. Alternatively, if there are no assignments within the course, you can delete it and create a new one to link with Gradescope." |
| "I can't post grades to Brightspace" | Point value mismatch | "Ensure the point values are the same for the assignment in Gradescope and the assignment in Brightspace." |
| "Gradescope doesn't appear in the embedded window when I use the Safari browser." | Safari cross-site tracking prevention | "select Preferences from Safari's settings and then ensure Prevent cross-site tracking is unchecked." |
| "Gradescope doesn't appear in the embedded window when I use Chrome in incognito mode." | Third-party cookies blocked | Temporary: eye icon in the URL bar, "Site not working?", then "Allow cookies". Permanent: Chrome privacy settings, "Cookies and other site data", "Allow all cookies". |

Source: https://guides.gradescope.com/hc/en-us/articles/21753755447949-Troubleshooting-Brightspace-D2L-Issues-for-Instructors, checked 2026-09-22

## (d) How to tell LTI 1.0 from LTI 1.3
- "Depending on your institution's configuration, you may be launching Gradescope from Brightspace (D2L) using LTI version 1.3 or using the older version, LTI 1.0 combined with Brightspace's (D2L) custom API."
- Method 1 (recommended): "Contact your institution's Brightspace (D2L) administrator to ask if you're using Gradescope in Brightspace (D2L) with LTI 1.0 + API or LTI 1.3."
- Method 2: "Check your deep-linking capabilities. To do that, on your course site in Brightspace (D2L), select More from the top navigation bar. If Gradescope is listed as an option, you most likely have LTI 1.3. If Gradescope is not listed, you most likely have LTI 1.0 + API." The guide adds this "is not a foolproof method and the best option is to contact either your admin or help@gradescope.com."
- Other differences visible in the two instructor articles: the 1.0 article links the assignment from the Gradescope assignment "Settings" page ("Brightspace Assignment" section, "Link" button, grade item dropdown), while the 1.3 article links from Brightspace "Content" > "Add Existing Activities". The 1.0 article states IDs and section names auto-sync; the 1.3 roster sync button "may display a customized name".

Source: https://guides.gradescope.com/hc/en-us/articles/23734240055565-Determining-your-Brightspace-D2L-LTI-tool-version (and the two instructor articles cited above), checked 2026-09-22

## (e) Admin configuration summary (context only)
1. Prerequisite: email help@gradescope.com so integration permissions are enabled on the admin's Gradescope account; use the same email in both systems.
2. Step One, Gradescope side: "LTI 1.3 Integrations" > "Configure Integration" > "Create new registration" > "Brightspace"; copy the Gradescope details (Domain, Redirect URLs, OpenID Connect Login URL, Target Link URL, Keyset URL).
3. Step One, Brightspace side: settings cog > "Manage Extensibility" > "LTI Advantage" > "Register Tool" > "Standard"; name "Gradescope"; paste the details; extensions "Assignment and Grade Services", "Deep Linking", "Names and Roles Provisioning Services"; roles "Send Institution Role"; "Register".
4. Copy the Brightspace values (Client ID, Keyset URL, OAuth2 Access token URL, OpenID Connect Authentication Endpoint, OAuth2 Audience, Issuer) into Gradescope "LMS Details" and "Save".
5. Optional student ID sync: "Config Variable Browser", variable "d2l.Tools.Lti.SendLisPersonSourcedId" set to "On".
6. Step Two: "View Deployments" > "New Deployment"; all three extensions; all "Security Settings"; "Open as External Resource" (opens in a new tab) and "Grades created by LTI will be included in Final Grade" (syncs grades to the D2L gradebook), both recommended; add org units with descendants; "Create Deployment".
7. Step Three: "View Link" > "New Link"; URL "https://lti.int.turnitin.com/launch/gs"; assignment-level link type "Deep Linking Quicklink" (width and height 800); course-level link type "Basic Launch"; "Save and Close".
8. Course-level link placement options: admin adds it via "Manage All Course Navbars" > "Add Links" > "Create Custom Link" > "External Learning Tools" > "Gradescope"; or instructors add it themselves; or skip the course-level link.
9. Step Four: in a course, "Content" > "Add Existing Activities" > the Gradescope option; log in to Gradescope; enter a "Branded Platform Name" (for example "Brightspace"); select the school.
10. Test from the instructor and student side before rollout.

Source: https://guides.gradescope.com/hc/en-us/articles/21791026788109-Configuring-Gradescope-LTI-1-3-in-Brightspace-D2L-for-Admins, checked 2026-09-22

## (f) Every UI label the guides mention (all tagged (guide): from documentation, not observation)

Brightspace (D2L) side:
"Edit this Navbar" (guide); "Manage all Course Navbars" (guide); "Edit Navbar" page (guide); "Add Links" (guide); "Create Custom Link" (guide); "name" field (guide); "URL" field (guide); "Insert Quicklink" (guide); "External Learning Tools" (guide); "Gradescope" (guide; "it may be named slightly differently"); "Create" (guide); "Add" (guide); "Save and Close" (guide); "More" in the top navigation bar (guide); "Content" (guide); module (guide); "Gradescope tool link" (guide); "Add Existing Activities" (guide); "the Gradescope 1.3 assignment" item (guide); "Grades" (student guide); Brightspace login screen (guide); authorize Gradescope message with "Continue" (guide); classlist role "instructor" (guide); "Edit Properties In-place" and "Open as External Resource" (LTI 1.0 guide only); grade item type "Numeric" (LTI 1.0 guide only); Safari "Preferences" and "Prevent cross-site tracking" (troubleshooting guide); Chrome "Site not working?", "Allow cookies", "Cookies and other site data", "Allow all cookies" (troubleshooting guide). Admin-only: "Manage Extensibility", "LTI Advantage", "Register Tool", "Standard", "Enabled", "Assignment and Grade Services", "Deep Linking", "Names and Roles Provisioning Services", "Send Institution Role", "Register", "Config Variable Browser", "View Deployments", "New Deployment", "Security Settings", "Open as External Resource", "Grades created by LTI will be included in Final Grade", "Create Deployment", "View Link", "New Link", "Deep Linking Quicklink", "Basic Launch", "Manage All Course Navbars" (all guide).

Gradescope side:
course-linking dialog with new or existing course choice (guide); "Link Course" (guide); "Course Settings" (guide); course title, description, rubric types, score bounds fields (guide); "Update Course" (guide); "Gradescope Course Dashboard" (guide); left sidebar (guide); "Roster" (guide); "Sync Brightspace Roster" (guide; name may be customized); "Let new users know that they were added to the course" checkbox (guide); "Sync Roster" (guide); "Download Roster" (guide); "Add Students or Staff" (guide); "Create Assignment" (guide); "Settings" (guide); "Save" (guide); "Grade Submissions" (guide); "Review Grades" (guide); "Post Grades to Brightspace" (guide); "Post Grades" (guide); "Graded" column with checkmark (guide); "Publish Grades" (guide); "Compose Email to Students" (guide); Gradescope modal from Add Existing Activities with "Create a new assignment" and "Link with an existing assignment" (guide); "Link Assignment" (guide); "Brightspace Assignment" section and "Link" button on assignment Settings (LTI 1.0 guide only); "Forgot your password?" (student guide); "Grades" and "Content" as student routes (student guide). Admin-only: "LTI 1.3 Integrations", "Configure Integration", "Create new registration", "Brightspace", "LMS Details", "Save", "Branded Platform Name" (all guide).

Source: all articles cited in sections (a) to (e), checked 2026-09-22
