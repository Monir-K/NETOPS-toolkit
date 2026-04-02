# NetOps Toolkit

> A professional-grade, single-file browser-based network support toolkit for IT & infrastructure engineers.  
> **By M Kamjo** — v3.0

---

## 🚀 Quick Start

1. Download `index.html`
2. Open with **Microsoft Edge** (double-click or right-click → Open with → Edge)
3. The tool auto-requests fullscreen on load
4. Click **▶ LAUNCH** on the splash screen

No installation. No server. No dependencies. Everything runs locally in your browser.

---

## 🔧 Features (16 Tabs)

| Tab | Description |
|---|---|
| 📡 Dashboard | Public IP, LAN IP, ISP, ASN, Location, Timezone — quick check bar |
| 🔐 Vault | Hidden credential/config storage with advanced regex search |
| 🔗 URL Check | urlscan.io threat intelligence for URLs and domains |
| 🌍 IP Lookup | Full geo/ASN/proxy/hosting/mobile detection via ip-api.com |
| 🌐 DNS | DNS lookup (Google DNS), WHOIS (rdap.org), SSL cert (crt.sh) |
| 📧 Email Hdrs | Full email header analyzer — SPF/DKIM/DMARC, routing hops |
| 🧮 Subnet | CIDR subnet calculator — network, broadcast, hosts, binary mask |
| 📊 Ports | Searchable local database of 60+ common ports |
| 🔌 MAC | MAC vendor lookup + formatter (colon/dash/Cisco/plain) |
| 🧹 Extractor | Auto-extract IPs, emails, URLs, MACs, hashes from any text |
| ⚙️ Netsh | Netsh command builder — static IP, DNS, reset, flush, etc. |
| 📦 Encoder | Base64, URL encode, HEX, IP ↔ Integer |
| 🔑 Password | Strength analyzer + default credential checker (25 pairs) |
| 📡 IP Range | Range generator + ping/tracert command builder |
| 📝 Notes | Session-persistent scratchpad |
| 🖥️ Windows | ms-settings: links + .cpl / .msc quick launch |

---

## 🖥️ UI Features

- **Splash screen** — fullscreen matrix animation, auto-requests F11 on load
- **Taskbar** — Windows-style bottom bar: green start menu, network status, live clock
- **Lock screen** — PIN `1234` (change `LOCK_PIN` in source to customise)
- **Radar** — animated scanning radar in bottom-right corner
- **Tab animations** — each tab has a unique mini canvas animation themed to its function
- **Power button** — top-right, closes the tool

---

## ⚙️ Configuration

Open `index.html` in any text editor or VS Code and search for these lines to customise:

```js
const LOCK_PIN = '1234';       // Change lock screen PIN
```

---

## 🌐 APIs Used (all free, no key required)

| API | Usage |
|---|---|
| [ip-api.com](https://ip-api.com) | IP geolocation, ISP, ASN, proxy/VPN detection |
| [ipify.org](https://api.ipify.org) | Public IP detection |
| [urlscan.io](https://urlscan.io) | URL/domain threat intelligence |
| [dns.google](https://dns.google) | DNS record lookups |
| [rdap.org](https://rdap.org) | WHOIS / RDAP domain info |
| [crt.sh](https://crt.sh) | SSL certificate transparency logs |
| [macvendors.com](https://api.macvendors.com) | MAC address vendor lookup |

---

## 📁 Project Structure

```
netops-toolkit/
├── index.html          # Entire application (single file)
├── README.md           # This file
├── .gitignore          # Git ignore rules
└── .vscode/
    └── settings.json   # VS Code recommended settings
```

---

## 🛠️ Development

Open in VS Code:
```bash
code netops-toolkit/
```

Recommended VS Code extensions:
- **Live Preview** (ms-vscode.live-server) — instant browser refresh on save
- **HTML CSS Support** (ecmel.vscode-html-css)
- **Prettier** — code formatter

> The entire app is a single HTML file. No build step, no npm, no framework.

---

## 📤 Deploy to GitHub Pages

```bash
git init
git add .
git commit -m "Initial commit — NetOps Toolkit v3.0"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/netops-toolkit.git
git push -u origin main
```

Then in GitHub → Settings → Pages → Source: `main` / `/ (root)` → Save  
Your tool will be live at: `https://YOUR_USERNAME.github.io/netops-toolkit/`

🔐 Default Login
Admin
Username: admin
Password: 
User
Username: user
Password: User@NetOps26

---

## 📜 License

MIT — free to use, modify and distribute.  
**By M Kamjo**
