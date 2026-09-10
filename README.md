## Online Fundraising Platform — one SDLC cycle, six people

**Six-person group project (CSIT 314 Software Development Methodologies).** The team split into a
programming team and a documentation team, and I was on the documentation side. **My part: user
stories #37–42; BCE class and sequence diagrams for 14 of the 42 use cases (#27–37 and #40–42); use
case diagrams and descriptions; wireframes; and the Gantt chart.**

The split was not front end versus back end in the usual sense. **The screens came from our side —
the HTML wireframes in `wireframes/` and the Jinja templates in `templates/`. The Python behind them
— routes, controllers, entities — was written by the programming team.**

That is what makes this repository different from the rest of my portfolio. The others are code I
wrote alone. **This one is a record of requirements I defined, screens my side drew, and what the
two became together** — which file, which route, which query, which test.

The signed contribution table in `docs/` records the division as it was agreed. In practice the two
sides crossed it in both directions, which is the subject of *How the team actually worked* below.

### Overview

A Flask + SQLite fundraising platform with four roles — User Admin, Fundraiser, Donor, Platform
Management — built over four sprints by six people, in a BCE (Boundary–Control–Entity) structure.

| | |
|---|---|
| User stories | 42, tracked on a Taiga board across 4 sprints |
| Code | 48 Python files (3,426 lines) · 27 Jinja templates (3,029 lines) · 32 routes |
| Structure | `boundary/` 8 · `control/` 31 · `entity/` 8 |
| Front end | 16 HTML wireframes (1,932 lines) → 27 templates, both from the documentation team |
| Tests | `tests/test_login_logout.py` — 7 cases against a temporary copy of the database |
| Team record | 5 minuted meetings, signed contribution table, Taiga sprint boards |

### 1. Two assignments, not one

The documentation work was divided twice, on two different axes, and I was given a different slice
each time.

| Assignment | My slice | Count |
|---|---|---|
| **User stories** — write the story and its use case description | **#37–42**, all Platform Management | 6 of 42 |
| **BCE class + sequence diagrams** — one pair per use case, split evenly three ways | **#27–37 and #40–42** | **14 of 42** |

The second one is the larger contribution and the less obvious one, so it goes first.

#### The 14 use cases I diagrammed

BCE diagrams are the step between a use case description and a file layout: they name the boundary,
the control and the entity a use case needs, and the sequence diagram orders the calls between them.
**The repository's folder structure is those diagrams** — `boundary/`, `control/`, `entity/`, with
one controller file per use case, because that is one controller box per diagram.

My 14 cover a coherent slice of the system — everything that reads and reports, plus category
master data:

| Use cases | What they are | Where they live |
|---|---|---|
| #27–28 | Fundraiser: activity view counts, favourite counts | `fundraising_activity_view_record_controller.py`, `entity/fundraising_activity.py` |
| #29–30 | Fundraiser: search and view completed activity history | `search_completed_activity_controller.py`, `view_completed_activity_controller.py` |
| #31–32 | Donor: view and search donation history | `view_my_donation_controller.py`, `search_my_donation_controller.py`, `entity/donation.py` |
| #33–37 | Platform Management: category create, view, update, delete, search | 5 controllers + `entity/fundraising_category.py` + `boundary/fundraising_category_routes.py` |
| #40–42 | Platform Management: daily, weekly, monthly reports | `view_platform_report_controller.py`, `entity/platform_report.py`, `boundary/report_routes.py` |

Those fourteen use cases reach roughly a dozen of the 31 controllers — the three report stories
share one — and five of the eight entity classes.

#### The six user stories I wrote

Stories **#37–42** were mine to define — the search, the session and the reporting end of Platform
Management. **I wrote the story and the full use case description for all six**, including log in
and log out, whose BCE diagrams went to the two members who took every role's session use cases.
Four of the six (#37, #40–42) fall in my diagram block as well, so for those I wrote the requirement
and drew the structure that answers it. This is the trace:

| # | User story | Boundary | Control | Entity | Template |
|---|---|---|---|---|---|
| **37** | Search for a fundraising activity category | `fundraising_category_routes.py` → `main_page()` (`/categories?search=`) | `search_fundraising_category_controller.py` | `fundraising_category.py` → `searchCategories()` | `categories/category_main_page.html` |
| **38** | Log in to the platform management dashboard | `auth_routes.py` → `login()` | `login_controller.py` | `user_account.py` → `authenticateUser()`, `user_session.py` | `auth/login.html` |
| **39** | Log out and end the session | `auth_routes.py` → `logout()` | `logout_controller.py` | `user_session.py` | — |
| **40** | Generate a daily report | `report_routes.py` → `view_reports()` | `view_platform_report_controller.py` → `generateDailyReport()` | `platform_report.py` | `reports/platform_reports.html` |
| **41** | Generate a weekly report | same route, `?type=weekly` | `generateWeeklyReport()` | `platform_report.py` | same |
| **42** | Generate a monthly report | same route, `?type=monthly` | `generateMonthlyReport()` | `platform_report.py` | same |

Stories #38 and #39 are also the worked example in the project report's CI/CD chapter, which traces
the same path the table above does — requirement, then boundary / control / entity, then the
automated test, then the merge commit that shipped it.

#### The report feature, end to end

`entity/platform_report.py` is where my three report stories land. One method,
`generateReportInDateRange()`, answers five questions against a date window:

```sql
SELECT COALESCE(SUM(donation_amount), 0) FROM donation WHERE donation_date BETWEEN ? AND ?
SELECT COUNT(*) FROM user_session WHERE DATE(login_at) BETWEEN ? AND ?
SELECT COUNT(*) FROM fundraising_activity WHERE activity_status = 'ongoing' AND start_date <= ? AND end_date >= ?
SELECT COUNT(*) FROM fundraising_activity WHERE activity_status = 'completed' AND end_date BETWEEN ? AND ?
SELECT c.category_name, COALESCE(SUM(d.donation_amount), 0) AS total_amount
  FROM donation d JOIN fundraising_activity fa ON d.activity_id = fa.activity_id
  JOIN category c ON fa.category_id = c.category_id
  WHERE d.donation_date BETWEEN ? AND ? GROUP BY c.category_id, c.category_name
  ORDER BY total_amount DESC, c.category_name ASC LIMIT 1
```

Three things in there came out of writing the use case description first rather than the code first.
**The "ongoing activities" window is inverted on purpose** — `start_date <= endDate AND end_date >=
startDate` counts an activity that was running *at any point during* the period, not one that
started and finished inside it. **`COALESCE` on both sums** is what makes an empty period report
`$0` instead of a blank. And **the tie-break on category name** means the "most active category"
is stable when two categories draw the same amount, instead of changing between runs.

Daily, weekly and monthly are the same method with three different windows: a single date, a
supplied range, and a month expanded to its first and last day with `calendar.monthrange`. The
validation sits one layer up in the controller — a missing date, a reversed range, a non-numeric or
out-of-range month are all rejected before the entity is called.

### The screens, before and after

`wireframes/` is a small standalone Flask app with 16 HTML pages — the wireframe deliverable my side
of the team produced before the real system existed. It is not a discarded prototype; it is the
artefact the use case descriptions were drawn against, and the templates in `templates/` are what it
turned into once there was a database behind it.

The three screens that carry my user stories can be read either way round:

| Wireframe | Final template | Stories |
|---|---|---|
| `wireframes/templates/pm_main_categories.html` | `templates/categories/category_main_page.html` | #37 search category |
| `wireframes/templates/login.html` | `templates/auth/login.html` | #38 · #39 log in / log out |
| `wireframes/templates/pm_reports.html` | `templates/reports/platform_reports.html` | #40–42 reports |

The wireframe versions hold their data in Python lists in `auth_routes.py`; the final ones receive it
from a controller. **The layout survives the trip almost unchanged, which is the point of drawing it
first.**

### 2. How the team actually worked

The first meeting split the group into a programming team and a documentation team and assigned
user stories in blocks of six per person. Four sprints followed, each opened and closed with a
minuted meeting, each with its own Taiga board snapshot at start and end.

| Sprint | Scope |
|---|---|
| 1 | User Admin (profiles, accounts), and log in / log out for all four roles — 18 stories |
| 2 | Fundraiser activity CRUD and search; Donor browse and view — 7 stories |
| 3 | Favourites, view counts, completed-activity history, donation history — 9 stories |
| 4 | Platform Management categories and reports — 8 stories. Four were mine to write (#37, #40–42); **all eight were mine to diagram** |

**The formal split held on paper and leaked everywhere in practice.** The minutes assign the test
plan and test cases to the programming team in all four sprints; close to the deadline that work
moved across to the documentation side, and I took a share of it — test cases for User Admin
stories that were nowhere near my block. That is not in the contribution table, and it is not the
only thing that is not.

So the table in `docs/` should be read for what it is: **the division as it was agreed, not a
transcript of who touched what.** Six people worked on one system for two months and covered for
each other at the edges; the table is the part of that which can be signed.

`docs/SDM_Report.pdf` is the full 230-page project report: 42 user stories, five sets of meeting
minutes, a use case description with BCE class and sequence diagrams and a wireframe for every
story, test plans, Taiga board snapshots at the start and end of each sprint, and the signed
contribution table. `docs/user_stories_and_assignment.docx` is the working document that assigned
the stories in blocks of six, which is where #37–42 are recorded as mine.

Two links from the last page of the report:

- [Demo recording](https://drive.google.com/file/d/1OYmXwJ3rjCA6FSy77S3lpcyCjugkHag9/view?usp=sharing) — the system being walked through.
- [Team repository](https://github.com/Anythingsaf22/CSIT314-SDM) — where the programming team pushed.

**Teammates are named throughout, because who did what is the entire point of a contribution
table.** What is removed is the part that carries no credit and identifies a person outside this
project: university student ID numbers and handwritten signatures, on the two pages that held them.
Images in the report are downsampled to 150 dpi to keep the repository a reasonable size.

### 3. Notes on the implementation

I did not write the Python back end, so this section is description rather than defence — but a
reader will notice these before anything else, and they are worth naming.

**Passwords are stored and compared in plaintext.** `entity/user_account.py` inserts the password as
given and authenticates with `WHERE LOWER(username) = LOWER(?) AND password = ?`. There is no
hashing anywhere in the codebase. For a coursework build assessed on process this was never
challenged, but it is the first thing that would have to change before this ran anywhere real:
store a salted hash (`werkzeug.security` ships one) and compare hashes, never the password itself.
The seeded accounts in `README_project.md` exist because of this — they are demo credentials for a
demo database, not secrets.

**Every query is parameterised.** All 8 entity files use `?` placeholders — 114 of them — and there
is no string-built SQL anywhere, including the `LIKE` searches, where the `%term%` pattern is
assembled in Python and passed as a bound parameter. So the code is exposed on authentication and
not on injection, which is a more specific thing to say than "it is a student project".

**Access control is a decorator, applied unevenly.** `boundary/access_control.py` defines
`roles_required(*profile_ids)` and `login_required`; the report route carries
`@roles_required(PLATFORM_MANAGEMENT)`, and so do category create, update and delete. The category
list-and-search route does not. Reading a category list is not sensitive, so this may well be
deliberate — but it is the kind of asymmetry a use case description is supposed to settle in
writing, before it becomes a decision made by omission.

### Repository Structure

```
fundraising-system-sdlc/
├── README.md                  # this file
├── README_project.md          # the team's own README, unchanged
├── app.py  db.py              # Flask app factory, SQLite connection
├── fundraising.db             # seeded SQLite database
├── fundraising.sql            # schema
├── boundary/                  # 8 route modules + access_control.py
├── control/                   # 31 controllers, one per use case
├── entity/                    # 8 entity classes, all SQL lives here
├── templates/                 # 27 Jinja templates
├── wireframes/                # the HTML wireframes these templates came from
├── tests/                     # test_login_logout.py — 7 cases
├── reference_files/           # CSV seed data used during development
└── docs/                      # project report (student IDs and signatures covered)
```

The controller-per-use-case count is not an accident of style: the BCE diagrams were drawn one
diagram per use case, and the code follows them one file per use case.

### How to Run

```bash
git clone https://github.com/JinWanKim98/fundraising-system-sdlc.git
cd fundraising-system-sdlc
pip install flask
python3 app.py
```

Then open `http://127.0.0.1:5000/login`. The database ships seeded with 102 accounts. One per role:

| Role | Username | Password |
|---|---|---|
| User Admin | `aaronlim` | `pass101` |
| Fundraiser | `alextan` | `pass106` |
| Donor | `leahtan` | `pass169` |
| **Platform Management** — the screens behind my stories | `ivanlee` | `pass192` |

These are the four the team's own `README_project.md` documents.

The role selected in the dropdown must match the account's stored profile, or the login is rejected;
that check is the reason the login use case has a sequence diagram of its own. Passwords are stored
and compared in plain text — see the note in §3.

```bash
python3 -m unittest tests.test_login_logout -v   # 7 tests
```

The test creates a temporary copy of `fundraising.db`, so running it does not touch the committed
database.

### Provenance

Group project, six members, CSIT 314 at UOW (SIM Singapore), Semester 2 2026. The code was developed
in the team's shared repository at
[github.com/Anythingsaf22/CSIT314-SDM](https://github.com/Anythingsaf22/CSIT314-SDM); this
repository is my copy of the submitted deliverable, published with the documentation, with my own
contribution identified. The demo recording is linked above rather than committed; the file is 131 MB.

### Limitations

- **I am not the author of the Python back end.** The traceability above is a claim about
  requirements and screens, not about controller or entity code. For questions about how a
  particular method was written, the person who wrote it is the right one to ask.
- **`wireframes/` and `templates/` are the documentation team's work, three people including me.**
  The repository does not attempt to split those two directories per person. The BCE diagram split
  (#27–37, #40–42) is recorded because the team agreed it in writing; the screens were not divided
  that cleanly.
- The four report figures are computed at request time by scanning the tables; there is no
  aggregation table or cache. On this dataset that is instant, and on a real one it would not be.
- `tests/` covers login and logout only. Test plans and test cases for the rest of the system exist
  in the project report as documents, not as automated tests.
- The database ships seeded and the application writes to it directly. There is no migration path;
  `fundraising.sql` is the schema, and re-seeding means rebuilding the file.
- Student ID numbers and signatures in `docs/` are covered on the two pages that carried them. Names
  are not, so the contribution table and the minutes still read as a record of who did what.
