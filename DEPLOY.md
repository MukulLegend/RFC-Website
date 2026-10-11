# Deploying for free: Render (website) + Neon (database)

Why this combo: Render runs the Django site free (no credit card). Render's own free
database is deleted after 30 days, so the data lives in Neon's free Postgres instead.

Free-tier things to know:
- Render's free site **sleeps after 15 minutes without visitors**; the next visit takes ~1 minute to wake it.
- Neon's free database also naps when idle and wakes automatically.
- Free limits change over time - check render.com/pricing and neon.com/pricing if something surprises you.

## 0. Do this first (security)
1. Go to https://platform.openai.com/api-keys and **delete the old key** (it was in the code you shared).
2. Create a **new** key and keep it somewhere private. Never paste it into code or GitHub.

## 1. Put the project on GitHub
Create an empty **private** repository on github.com, then in this folder:
```
git init
git add .
git commit -m "RFC website"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```
(`.gitignore` already keeps `.env` and `db.sqlite3` out.)

## 2. Create the database on Neon
1. Sign up at https://neon.com (free, no card) -> **Create project**.
2. Copy the **connection string** (starts with `postgresql://...`). Keep it for step 3.

## 3. Create the website on Render
1. Sign up at https://render.com with GitHub.
2. **New +  ->  Blueprint** -> choose your repo. Render reads `render.yaml`.
3. It asks you for these values:

| Variable | What to enter |
|---|---|
| `DATABASE_URL` | the Neon connection string from step 2 |
| `OPENAI_API_KEY` | your **new** OpenAI key |
| `DJANGO_SUPERUSER_USERNAME` | the admin username you want |
| `DJANGO_SUPERUSER_EMAIL` | your email |
| `DJANGO_SUPERUSER_PASSWORD` | a strong admin password |

4. Click **Apply**. The first build takes a few minutes. When it says "Live", open the URL
   shown at the top (like `https://ramos-fc.onrender.com`).

If you create the service manually instead of using the Blueprint: runtime Python, build command
`bash build.sh`, start command `gunicorn CU.wsgi:application --workers 1 --threads 4`, health check
path `/healthz/`, plus the variables above and `DEBUG=False`, `DJANGO_SECRET_KEY=<long random string>`,
`PYTHON_VERSION=3.12.3`.

## 4. Fill in your club's content
Go to `https://YOUR-SITE.onrender.com/admin/`, log in with the admin account from step 3 and add:
**Players**, **Matches** (leave scores empty for upcoming games, fill them in afterwards), **Announcements**.
Messages from the Contact page appear under **Contacts**.

## 5. Optional extras
- **Password-reset emails.** Without setup, reset links only appear in Render's *Logs* tab. To send real
  emails with Gmail: turn on 2-step verification, create an *App password*, then add Render variables
  `EMAIL_HOST_USER` (your Gmail address) and `EMAIL_HOST_PASSWORD` (the app password).
- **Stop the site sleeping.** A free uptime monitor (e.g. UptimeRobot) can request
  `https://YOUR-SITE.onrender.com/healthz/` every 5 minutes. This uses your free monthly instance hours.
- **Your own domain.** Render -> your service -> Settings -> Custom Domains, follow the DNS steps, then add a
  variable `EXTRA_HOSTS=yourdomain.com,www.yourdomain.com`.
- **AI model.** The chat uses `gpt-4o-mini`. If OpenAI retires it, set `OPENAI_MODEL` to a current model.
  The chat only works if your OpenAI account has credit.

## 6. Updating the site later
Change files, then `git add . && git commit -m "update" && git push` - Render redeploys automatically.
Content changes (players, matches, news) don't need code - use `/admin/`.

## Troubleshooting
- **"Bad Request (400)"** -> the hostname isn't allowed. Add it in `EXTRA_HOSTS`.
- **"CSRF verification failed"** on login/forms -> same cause: use the Render URL or add your domain to `EXTRA_HOSTS`.
- **Build fails** -> open the Render *Logs* tab; the last red line says why.
- **Pages look unstyled** -> check the build log shows `collectstatic` ran (it's in `build.sh`).
- **AI chat says "unavailable"** -> check `OPENAI_API_KEY`, your OpenAI credit, and the Render logs.
- **Admin login doesn't work** -> the superuser is created only on a deploy where the three
  `DJANGO_SUPERUSER_*` variables exist; set them and click *Manual Deploy*.
