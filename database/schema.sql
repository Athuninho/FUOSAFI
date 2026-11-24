-- FUOSAFI Database Schema
-- Community-Based Coastal and Marine Pollution Reporting System

PRAGMA foreign_keys = ON;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone_number TEXT,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('Resident', 'Mzee wa Mtaa', 'Authority Representative', 'Administrator')),
    location TEXT,
    account_status TEXT NOT NULL DEFAULT 'Active' CHECK(account_status IN ('Active', 'Inactive', 'Suspended')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- 2. Reports Table
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reference_number TEXT UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN (
        'Coastal and marine litter',
        'Improperly dumped solid garbage',
        'Sewage and wastewater entering coastal or marine environments'
    )),
    description TEXT NOT NULL,
    date_observed DATE NOT NULL,
    location_name TEXT NOT NULL,
    county TEXT,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'Submitted' CHECK(status IN (
        'Submitted',
        'Under Community Review',
        'Awaiting Additional Information',
        'Referred to Authority',
        'Acknowledged by Authority',
        'In Progress',
        'Resolved (Recorded)',
        'Closed'
    )),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_reports_ref ON reports(reference_number);
CREATE INDEX IF NOT EXISTS idx_reports_user ON reports(user_id);
CREATE INDEX IF NOT EXISTS idx_reports_status ON reports(status);
CREATE INDEX IF NOT EXISTS idx_reports_category ON reports(category);

-- 3. Photographs Table
CREATE TABLE IF NOT EXISTS photographs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    original_filename TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_photos_report ON photographs(report_id);

-- 4. Report History Table (Audit Trail)
CREATE TABLE IF NOT EXISTS report_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER NOT NULL,
    previous_status TEXT,
    new_status TEXT NOT NULL,
    updated_by INTEGER NOT NULL,
    remarks TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE,
    FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_history_report ON report_history(report_id);

-- 5. Referrals Table
CREATE TABLE IF NOT EXISTS referrals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER NOT NULL,
    referred_by INTEGER NOT NULL,
    institution_name TEXT NOT NULL,
    referral_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    referral_remarks TEXT NOT NULL,
    referral_status TEXT NOT NULL DEFAULT 'Pending' CHECK(referral_status IN ('Pending', 'Acknowledged', 'Action Taken', 'Closed')),
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE,
    FOREIGN KEY (referred_by) REFERENCES users(id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_referrals_report ON referrals(report_id);
