# Ramos Football Club (RFC) website

Django 5.2 site: home, about, squad, matches, news, contact, member accounts
(register / login / email password-reset / profile) and a members-only AI chat.
Club content (players, fixtures, results, news) is managed from the admin panel at `/admin/`.

## Preview it on your own computer

You need Python 3.10 or newer (https://www.python.org/downloads/ - tick "Add Python to PATH" on Windows).

**Windows (Command Prompt or PowerShell), inside this folder:**
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py runserver
```

**Mac / Linux:**
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py runserver
```

Then open http://127.0.0.1:8000 - and the admin panel at http://127.0.0.1:8000/admin/

- `seed_demo` adds sample players / fixtures / news so the pages aren't empty. Delete or edit them in the admin.
- To try the AI chat locally, put your **new** OpenAI key in `.env` (`OPENAI_API_KEY=...`) and restart.
- Password-reset emails are printed in the terminal window locally - copy the link from there.
- Want your old accounts and contact messages locally? Copy your old `db.sqlite3` into this folder and run `python manage.py migrate`.

## What changed from your original version

| Area | Before | Now |
|---|---|---|
| OpenAI key | hard-coded in `views.py` | read from `OPENAI_API_KEY` environment variable |
| Password reset | anyone could reset **any** user's password by typing their username | proper emailed one-time link |
| AI chat API | open to anyone, CSRF disabled, leaked error details | login required, CSRF on, 20 msgs/hour/user, no internals leaked, club-specific assistant |
| Settings | DEBUG on, fixed secret key, no allowed hosts | environment-driven, production-safe (HTTPS, secure cookies) |
| Database | SQLite only | SQLite locally, Postgres in production via `DATABASE_URL` |
| Home page | login required | public (visitors can see the club) |
| New | - | Squad, Matches (fixtures + results), News, contact message box, shared nav/footer |
| Removed | 5 unused images/videos (~11 MB) | smaller, faster deploys |

Deployment guide: see **DEPLOY.md**.
