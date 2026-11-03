# NetOps Toolkit v3.1 — By M Kamjo

## Quick Start
1. Double-click **START_PING_SERVER.bat** — keep terminal open
2. Double-click **launch-edge.bat** — opens Edge in fullscreen using a regular profile
3. Login with: `admin` / `Admin@NetOps26` (or `user` / `User@NetOps26`)
4. New users can enter a username and password on the login screen and select **START 1-MONTH FREE TRIAL**

## Files
- `index.html` — full single-file application
- `ping_server.py` — Python backend (ping, email, DNS proxy, cmd runner)
- `START_PING_SERVER.bat` — starts the backend on port 5199
- `launch-edge.bat` — opens Edge in fullscreen using a regular browser profile

## Default Login Credentials
| Role  | Username | Password         |
|-------|----------|------------------|
| Admin | admin    | Admin@NetOps26   |
| User  | user     | User@NetOps26    |

**Change passwords:** Login as admin → click ADMIN badge in topbar → Admin Settings panel

## One-Month Trial
New users can create an account from the login screen. Trial access expires one calendar month after signup. Trial accounts are stored in the browser's local storage, so they are limited to that browser profile and can be reset if its site data is cleared; this is not centralized account or subscription enforcement. Use a regular browser window (not InPrivate/Incognito) to preserve trial access between sessions.

## Features
- 📡 Asset Monitor — ICMP ping + HTTP reachability + email alerts
- 🔐 Credential Vault — hidden text storage with multi-field live search
- 🔗 URL/Domain Threat Intelligence (urlscan.io)
- 🌍 IP Geolocation + ASN (ip-api.com, fallback via backend proxy)
- 🌐 DNS Lookup — Cloudflare DoH → Google DoH → local proxy fallback
- 📧 Email Header Analyzer — local, SPF/DKIM/DMARC check
- 🔧 Net Tools — Subnet Calculator + Netsh Builder + IP Range + Ping/Tracert
- 📊 Ports — color-coded dangerous ports (HIGH RISK in red)
- 🔑 Password — strength checker, generator, HIBP breach checker
- 💻 Inline CMD Runner — safe commands run from dashboard
- 🖨️ Printer — saved printers with one-click web interface access
- 🌙/☀️ Dark/Light theme toggle
- Navigation grouped into Network, Security & Analysis, and Workspace menus
- Click **Show/Hide** on panel headings to expand or collapse dense feature sections
- ↕️ Drag-to-reorder tools within each navigation menu; order saved to localStorage

## Email Alerts
1. Go to Google Account → Security → App Passwords
2. Dashboard → Email Alerts row → fill Gmail, App Password, Recipients → Save

## Lock / Logout
Click the 🔒 button in taskbar to log out and return to login screen.

## Notes
- Tool designed to run from localhost:5199 (via ping_server.py)
- Lock screen PIN (legacy): 1234 — customise LOCK_PIN in index.html
- All data stored in localStorage — nothing sent to external servers except:
  - ip-api.com (geolocation), dns.cloudflare.com (DNS queries)
  - macvendors.com (MAC lookup), urlscan.io (URL threat intel)
  - api.pwnedpasswords.com (HIBP — only first 5 chars of hash, k-anonymity)


🔐 Default Login
Admin
Username: admin
Password: 
User
Username: user
Password: User@NetOps26
