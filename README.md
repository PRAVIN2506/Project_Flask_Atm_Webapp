# ATM Demo — Flask + MySQL

A simple web-based ATM simulation built with Python Flask, MySQL, and vanilla HTML/CSS. Supports login, balance check, deposit, withdrawal, and transaction history.

This version has all the fixes from the code review applied — see [What Was Fixed](#what-was-fixed).

## Tech Stack

- **Backend:** Python 3, Flask, Flask-WTF (CSRF protection)
- **Database:** MySQL (via `mysql-connector-python`)
- **Frontend:** Jinja2 templates, plain CSS (no framework)

## Project Structure

```
.
├── app.py              # Flask routes (login, dashboard, balance, deposit, withdraw, transactions)
├── atm.py              # ATM class — balance/deposit/withdraw/transaction DB logic
├── database.py         # MySQL connection helper (reads config from .env)
├── seed_user.py         # CLI helper to create new users with hashed PINs
├── schema.sql            # Database + table creation, with a sample login
├── requirements.txt    # Python dependencies
├── .env.example         # Template for local environment config
├── .gitignore
├── static/
│   └── style.css
└── templates/
    ├── login.html
    ├── dashboard.html
    ├── balance.html
    ├── deposit.html
    ├── withdraw.html
    └── transactions.html
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create the database

```bash
mysql -u root -p < schema.sql
```

This creates the `atm_db` database, the `users` and `transactions` tables, and a sample login:

- **Account number:** `1234567890`
- **PIN:** `1234`

(The PIN is stored hashed in the table, not in plaintext — the raw value `1234` is what you type in at login.)

### 3. Configure environment variables

```bash
cp .env.example .env
```

Then edit `.env` with your own MySQL credentials and a random `SECRET_KEY`:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Run the app

```bash
python app.py
```

Visit `http://localhost:5000` and log in with the sample account above.

### 5. (Optional) Add more users

There's no in-app registration flow, so use the helper script to add accounts with correctly hashed PINs:

```bash
python seed_user.py
```

## Features

- Login with account number + PIN (PINs hashed with Werkzeug's `scrypt`-based hasher)
- CSRF-protected forms (login, deposit, withdraw)
- Dashboard with quick links to all actions
- Check balance
- Deposit money
- Withdraw money (blocks overdraw)
- Transaction history (deposits/withdrawals, newest first)
- Logout (clears session)
- In-page error messages (invalid login, invalid amount, insufficient balance)

## What Was Fixed

Compared to the original upload, this version addresses:

| Issue | Fix |
|---|---|
| No database schema shipped | Added `schema.sql` with `users`/`transactions` tables and a working sample login |
| `mysql-connector-python==26.7.0` doesn't exist on PyPI | Pinned to `mysql-connector-python==9.2.0`, verified installable |
| PINs stored and compared as plaintext | PINs are now hashed with `werkzeug.security.generate_password_hash` / `check_password_hash`; `pin` column widened to `VARCHAR(255)` |
| Hardcoded DB credentials and Flask `secret_key` | Moved to environment variables via `python-dotenv` and `.env` (see `.env.example`) |
| `debug=True` always on | Now controlled by `FLASK_DEBUG` env var, defaults to `False` |
| No CSRF protection on forms | Added `Flask-WTF`'s `CSRFProtect`; all POST forms include a CSRF token |
| Deposit/withdraw errors returned as raw text | Errors now render inline in the page via an `error` template variable |
| No way to create additional users | Added `seed_user.py` CLI helper that hashes PINs correctly |

## Known Limitations (still demo-scope)

- No self-service registration flow (by design — use `seed_user.py`).
- No rate limiting on login attempts.
- No HTTPS/session-cookie hardening configured (`SESSION_COOKIE_SECURE`, etc.) — add this before deploying anywhere public.
- Amounts use `DECIMAL(12,2)` in MySQL but `float` in Python route handlers; fine for a demo, but a production version should use `Decimal` throughout to avoid floating-point rounding issues.

## License

Demo / educational project — no license specified.
