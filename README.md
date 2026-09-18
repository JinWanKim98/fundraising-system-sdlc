# Online Fundraising Platform — requirements and SDLC

Six-person CSIT 314 group project at UOW (SIM Singapore), built with Flask and SQLite across four sprints. **My original role was on the documentation team**, not the Python back-end team.

## Tech stack

![HTML](https://img.shields.io/badge/HTML-E34F26?style=flat&logo=html5&logoColor=white) ![CSS](https://img.shields.io/badge/CSS-663399?style=flat&logo=css&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-333333?style=flat&logo=flask&logoColor=white) ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)

**My contribution:** requirements, BCE diagrams and shared HTML/CSS wireframes/templates. Flask and SQLite describe the team application; the original Python back end was implemented by the programming team.

## My contribution

| Deliverable | My scope |
|---|---|
| User stories and use case descriptions | #37–42: category search, Platform Management login/logout, daily/weekly/monthly reports |
| BCE class and sequence diagrams | 14 use cases: #27–37 and #40–42 |
| Shared documentation work | Use case diagrams, wireframes/templates and Gantt chart, with the documentation team |

The project had 42 user stories and four roles: User Admin, Fundraiser, Donor and Platform Management. The [project report](docs/SDM_Report.pdf) contains the contribution table, requirements, diagrams, wireframes, test plans and meeting records. [Working story assignments](docs/user_stories_and_assignment.docx) record the six-story allocation.

Wireframes and templates were shared work by three documentation-team members; this repository does not attribute every screen to me. The original Python routes, controllers and entities were written by the programming team.

## Following a requirement into the system

| Story | Implementation to inspect |
|---|---|
| #37 category search | `boundary/fundraising_category_routes.py` → `control/search_fundraising_category_controller.py` → `entity/fundraising_category.py` |
| #38–39 login/logout | `boundary/auth_routes.py`, login/logout controllers, user account/session entities |
| #40–42 reports | `boundary/report_routes.py` → `control/view_platform_report_controller.py` → `entity/platform_report.py` |

The reporting stories share a date-range calculation for donation totals, login sessions, currently ongoing activities overlapping the period, completed activities and the category receiving the most donations. A login count measures sessions, not unique users; “most active” means the largest donation total in this implementation.

The ongoing count uses **current status** plus date overlap. It does not reconstruct which activities were ongoing at a historical date, because there is no status-history table. This distinction matters when interpreting past-period reports.

The BCE folders follow the design's separation of screens/routes, coordination and stored data. Some use cases share controllers, including all three reporting periods; there is not one controller file for every story.

## Run and test

```bash
pip install -r requirements.txt
python3 app.py
# in another terminal, from the repository root:
python3 -m unittest discover -s tests -v
```

Open `http://127.0.0.1:5000/login`. Demo credentials are in [the original team README](README_project.md); Platform Management uses `ivanlee` / `pass192` with that role selected. The application writes to the supplied SQLite database, so use a copy if you want to preserve the seeded state. The login tests use a temporary database copy.

## Portfolio maintenance

After submission, category home/list/search/view routes were given the same Platform Management guard as category create/update/delete. Report input now rejects impossible dates, reversed ranges and invalid years before querying the database. The ongoing-activity label was clarified to match the current-status calculation. Automated checks cover these cases alongside the seven original login/logout tests.

These are later maintenance changes, not a claim that I wrote the team's original back end. The submitted report and wireframes remain historical artifacts and may use the older report label.

## Team record and limits

- [Team repository](https://github.com/Anythingsaf22/CSIT314-SDM)
- [Demo recording](https://drive.google.com/file/d/1OYmXwJ3rjCA6FSy77S3lpcyCjugkHag9/view?usp=sharing)

This is a local coursework demo. Passwords remain plaintext and the app uses development configuration; it is not a production authentication implementation. Entity queries use bound parameters, but that is not a complete security review. Reporting scans the underlying tables, and there is no migration system or historical status tracking. Automated tests cover selected behaviour, not all 42 stories.

The contribution record retains teammate names. University IDs and signatures were covered in the shared report. The repository demonstrates requirements, metric definitions and collaboration, rather than sole authorship of the complete application.
