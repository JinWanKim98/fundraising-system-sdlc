DROP TABLE IF EXISTS activity_view;
DROP TABLE IF EXISTS favourite_list;
DROP TABLE IF EXISTS donation;
DROP TABLE IF EXISTS fundraising_activity;
DROP TABLE IF EXISTS user_account;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS user_profile;
DROP TABLE IF EXISTS user_session;
PRAGMA foreign_keys = ON;

create TABLE user_profile (
    profile_id INTEGER PRIMARY KEY ,
    profile_name TEXT NOT NULL UNIQUE,
    profile_desc TEXT NOT NULL
);

Create TABLE user_account(
    account_id INTEGER PRIMARY KEY ,
    full_name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    DOB DATE,
    address TEXT,
    contact_num TEXT NOT NULL,
    profile_id INTEGER NOT NULL,
    account_status TEXT NOT NULL check(account_status in ('ACTIVE', 'SUSPENDED', 'EXPIRED')),
    account_created_date TEXT,
    FOREIGN KEY (profile_id) REFERENCES user_profile(profile_id)

);

CREATE TABLE user_session(
    session_id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL,
    login_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    logout_at TEXT,
    session_status TEXT NOT NULL CHECK( session_status in ('active', 'logged_out', 'suspended', 'expired')),
    FOREIGN KEY (account_id) REFERENCES user_account(account_id)
);
CREATE INDEX idx_user_sessions_account_id ON user_session(account_id);
CREATE INDEX idx_user_sessions_status ON user_session(session_status);
CREATE INDEX idx_user_sessions_login_at ON user_session(login_at);

CREATE TABLE category(
    category_id INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL UNIQUE
);

Create TABLE fundraising_activity(
    activity_id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL,
    activity_name TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    activity_desc TEXT NOT NULL,
    funding_current REAL NOT NULL DEFAULT 0,
    funding_goal REAL NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    activity_status TEXT NOT NULL CHECK (activity_status in ('completed', 'expired', 'cancelled', 'ongoing')),
    FOREIGN KEY (account_id) REFERENCES user_account(account_id),
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);

CREATE TABLE donation(
    donation_id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL,
    activity_id INTEGER NOT NULL,
    donation_amount REAL NOT NULL CHECK (donation_amount > 0),
    donation_date TEXT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES user_account(account_id),
    FOREIGN KEY (activity_id) REFERENCES fundraising_activity(activity_id)
);

CREATE TABLE favourite_list(
    favourite_id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL,
    activity_id INTEGER NOT NULL,
    FOREIGN KEY (account_id) REFERENCES user_account(account_id),
    FOREIGN KEY (activity_id) REFERENCES fundraising_activity(activity_id),
    UNIQUE (account_id, activity_id)
);

CREATE TABLE activity_view(
    viewing_id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL,
    activity_id INTEGER NOT NULL,
    viewing_date TEXT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES user_account(account_id),
    FOREIGN KEY (activity_id) REFERENCES fundraising_activity(activity_id)

);
