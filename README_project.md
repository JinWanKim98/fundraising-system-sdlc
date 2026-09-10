# CSIT314-SDM Online Fundraising System

This project is a Flask and SQLite web application for an online fundraising platform. It supports four main user roles:

- User Admin
- Fundraiser
- Donor
- Platform Management

The codebase follows a BCE-style structure:

- `boundary/`: Flask route files and access control.
- `control/`: Controller classes that coordinate application logic.
- `entity/`: Entity classes that interact with the SQLite database.
- `templates/`: HTML/Jinja templates rendered by Flask.
- `tests/`: Python `unittest` test cases.
- `reference_files/`: CSV seed/reference data used during development.

## Requirements

- Python 3.12 or compatible Python 3 version
- Flask
- SQLite database file included as `fundraising.db`

Install Flask with:

```bash
pip install flask
```

If your environment uses `python3` and `pip3`, use:

```bash
pip3 install flask
```

## How To Run

From the project root:

```bash
cd /Users/kaungkhantkyaw/Documents/GitHub/CSIT314-SDM
python3 app.py
```

Then open:

```text
http://127.0.0.1:5000/login
```

The root URL `/` redirects users to the login page if they are not logged in. After login, users are redirected to the correct dashboard based on their selected profile role.

## Seeded Login Accounts

Use these accounts for testing the main roles:

| Role | Username | Password | Profile ID |
| --- | --- | --- | --- |
| User Admin | `aaronlim` | `pass101` | `1` |
| Fundraiser | `alextan` | `pass106` | `2` |
| Donor | `leahtan` | `pass169` | `3` |
| Platform Management | `ivanlee` | `pass192` | `4` |

When logging in, select the matching profile role from the dropdown. Login will fail if the selected profile does not match the account's stored profile.

## Main Features

### User Admin

- Create user profiles.
- View user profiles.
- Update user profiles.
- Delete user profiles.
- Search user profiles.
- Create user accounts.
- View user accounts.
- Update user accounts.
- Suspend user accounts.
- Search user accounts.
- Login and logout.

### Fundraiser

- Create fundraising activities.
- View own fundraising activities.
- Update fundraising activities.
- Delete fundraising activities.
- Search fundraising activities.
- View completed fundraising activity history.
- Search completed fundraising activity history.
- View activity view counts.
- View activity favourite counts.
- Login and logout.

### Donor

- Browse fundraising activities.
- Search fundraising activities.
- View fundraising activity details.
- Add fundraising activities to favourites.
- View favourite activities.
- Search favourite activities.
- View donation history.
- Search donation history.
- Login and logout.

### Platform Management

- Create fundraising activity categories.
- View fundraising activity categories.
- Update fundraising activity categories.
- Delete fundraising activity categories.
- Search fundraising activity categories.
- Generate daily reports.
- Generate weekly reports.
- Generate monthly reports.
- Login and logout.

## Running Tests

The current TDD/unit test file covers login and logout behaviour.

Run tests from the project root:

```bash
python3 -m unittest tests.test_login_logout -v
```

Expected result:

```text
Ran 7 tests in ...
OK
```

The test creates a temporary copy of `fundraising.db`, so the main database is not modified by the login/logout tests.

## Database

The application uses SQLite through `fundraising.db`.

Important tables include:

- `user_profile`
- `user_account`
- `user_session`
- `category`
- `fundraising_activity`
- `favourite_list`
- `donation`
- `activity_view`

The database schema is also available in:

```text
fundraising.sql
```

## Notes For Developers

- Keep HTML templates inside `templates/`. Flask expects templates to be there unless the app template folder is reconfigured.
- The route files in `boundary/` act as the boundary layer in the BCE structure.
- Controller files in `control/` should contain coordination logic and call entity methods.
- Entity files in `entity/` should contain database interaction logic.
- Do not commit `__pycache__/` files or local IDE/cache files.

