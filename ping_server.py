#!/usr/bin/env python3
"""
NetOps Toolkit — Ping + Email Backend
By M Kamjo — serves index.html AND handles ping/email API
Run: python ping_server.py  (or double-click START_PING_SERVER.bat)
Then open: http://localhost:5199
"""

import subprocess, json, platform, threading, smtplib, os, mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

PORT     = 5199
IS_WIN   = platform.system() == 'Windows'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CFG_FILE = os.path.join(BASE_DIR, 'email_config.json')

email_cfg = {"from_email":"","app_password":"","to_emails":[]}

def load_email_cfg():
    global email_cfg
    try:
        if os.path.exists(CFG_FILE):
            with open(CFG_FILE) as f: email_cfg.update(json.load(f))
    except Exception as e: print(f'  [email] Config load error: {e}')

def save_email_cfg(data):
    global email_cfg
    email_cfg.update(data)
    try:
        with open(CFG_FILE,'w') as f: json.dump(email_cfg,f,indent=2)
    except Exception as e: print(f'  [email] Config save error: {e}')

def send_email_alert(asset_name, asset_ip, is_down):
    if not email_cfg.get('from_email') or not email_cfg.get('app_password'):
        return False,'Email not configured'
    if not email_cfg.get('to_emails'):
        return False,'No recipients configured'
    status  = 'OFFLINE' if is_down else 'BACK ONLINE'
    subject = f'[NETOPS ALERT] {asset_name} is {status}'
    now     = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    color   = '#ff4f6e' if is_down else '#00ff9d'
    icon    = '🔴' if is_down else '🟢'
    body    = f"""<html><body style="font-family:Arial,sans-serif;background:#0a0f0a;color:#e0e0e0;padding:24px;">
<div style="max-width:520px;margin:0 auto;background:#0d1a0d;border:2px solid {color};border-radius:8px;padding:24px;">
  <div style="font-size:1.4rem;font-weight:bold;color:{color};margin-bottom:16px;">{icon} ASSET {'OFFLINE' if is_down else 'RECOVERED'}</div>
  <table style="width:100%;border-collapse:collapse;">
    <tr><td style="color:#888;padding:6px 0;width:100px;">Asset</td><td style="color:#fff;font-weight:bold;">{asset_name}</td></tr>
    <tr><td style="color:#888;padding:6px 0;">IP/Host</td><td style="color:#00c8ff;">{asset_ip}</td></tr>
    <tr><td style="color:#888;padding:6px 0;">Status</td><td style="color:{color};font-weight:bold;">{status}</td></tr>
    <tr><td style="color:#888;padding:6px 0;">Time</td><td style="color:#fff;">{now}</td></tr>
  </table>
  <div style="margin-top:16px;padding-top:12px;border-top:1px solid #1a2a1a;font-size:0.75rem;color:#444;">
    NetOps Toolkit · Automated Alert · By M Kamjo
  </div>
</div></body></html>"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From']    = email_cfg['from_email']
        msg['To']      = ', '.join(email_cfg['to_emails'])
        msg.attach(MIMEText(body,'html'))
        with smtplib.SMTP_SSL('smtp.gmail.com',465,timeout=10) as s:
            s.login(email_cfg['from_email'],email_cfg['app_password'])
            s.sendmail(email_cfg['from_email'],email_cfg['to_emails'],msg.as_string())
        print(f'  [email] ✓ Sent: {asset_name} → {email_cfg["to_emails"]}')
        return True,'Sent'
    except smtplib.SMTPAuthenticationError:
        return False,'Gmail auth failed — check App Password'
    except Exception as e:
        return False,str(e)

def ping(host, count=5, timeout=3, threshold=100):
    import re
    host = host.strip()
    if not host:
        return {'online':False,'ms':None,'loss':100,'sent':0,'recv':0,'error':'No host'}
    try:
        cmd = ['ping','-n',str(count),'-w',str(timeout*1000),host] if IS_WIN else ['ping','-c',str(count),'-W',str(timeout),host]
        r   = subprocess.run(cmd,capture_output=True,text=True,timeout=timeout*count+5)
        out = r.stdout+r.stderr
        sent=count; recv=0; loss_pct=100
        if IS_WIN:
            m = re.search(r'Sent\s*=\s*(\d+),\s*Received\s*=\s*(\d+)',out)
            if m: sent,recv=int(m.group(1)),int(m.group(2)); loss_pct=round((sent-recv)/sent*100) if sent else 100
            lm = re.search(r'\((\d+)%\s*loss\)',out)
            if lm: loss_pct=int(lm.group(1))
        else:
            m = re.search(r'(\d+) packets transmitted,\s*(\d+) received',out)
            if m: sent,recv=int(m.group(1)),int(m.group(2)); loss_pct=round((sent-recv)/sent*100) if sent else 100
        online = loss_pct < threshold
        ms=None
        if recv>0:
            m = re.search(r'Average\s*=\s*(\d+)ms',out) if IS_WIN else re.search(r'rtt .+?=\s*[\d.]+/([\d.]+)/',out)
            if m: ms=int(float(m.group(1)))
        return {'online':online,'ms':ms,'loss':loss_pct,'sent':sent,'recv':recv,'error':None}
    except subprocess.TimeoutExpired:
        return {'online':False,'ms':None,'loss':100,'sent':count,'recv':0,'error':'Timeout'}
    except Exception as e:
        return {'online':False,'ms':None,'loss':100,'sent':0,'recv':0,'error':str(e)}

class Handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200); self._cors(); self.end_headers()

    def do_GET(self):
        p  = urlparse(self.path)
        qs = parse_qs(p.query)

        # ── Serve index.html and static files ──
        if p.path == '/' or p.path == '/index.html':
            self._file('index.html','text/html')
            return
        # serve any other file in BASE_DIR (css, js, etc.)
        fpath = os.path.join(BASE_DIR, p.path.lstrip('/'))
        if os.path.isfile(fpath) and not p.path.startswith('/email_config'):
            mime,_ = mimetypes.guess_type(fpath)
            self._file(p.path.lstrip('/'), mime or 'application/octet-stream')
            return

        # ── API endpoints ──
        if p.path == '/ping':
            import ipaddress as _ipa2
            host      = qs.get('host',[''])[0]
            count     = int(qs.get('count',['5'])[0])
            threshold = int(qs.get('thresh',['81'])[0])  # 81 = online if loss<81% = 1/5 ok
            # Adaptive per-packet timeout: 6s external (VPN/Radmin/Internet), 5s local
            timeout = 5
            try:
                ip = _ipa2.ip_address(host.strip())
                if not ip.is_private and not ip.is_loopback:
                    timeout = 6
            except: timeout = 6  # hostname — unknown, be generous
            self._json(ping(host,count=count,timeout=timeout,threshold=threshold))

        elif p.path == '/ping-all':
            import ipaddress as _ipa
            hosts     = [h.strip() for h in qs.get('hosts',[''])[0].split(',') if h.strip()]
            count     = int(qs.get('count',['5'])[0])
            threshold = int(qs.get('thresh',['81'])[0])  # 81 = online if 1/5 packets reply
            results   = {}
            def _pkt_timeout(h):
                try:
                    ip = _ipa.ip_address(h)
                    return 6 if (not ip.is_private and not ip.is_loopback) else 5
                except: return 6  # hostname — be generous
            def chk(h):
                results[h] = ping(h, count=count, timeout=_pkt_timeout(h), threshold=threshold)
            threads = [threading.Thread(target=chk, args=(h,), daemon=True) for h in hosts]
            for t in threads: t.start()
            # Dynamic join: count × max_per_pkt(6s) + 10s buffer
            join_secs = count * 6 + 10
            for t in threads: t.join(timeout=join_secs)
            for h in hosts:
                if h not in results:
                    results[h] = {'online':False,'ms':None,'loss':100,'sent':count,'recv':0,'error':'Timeout — host unreachable'}
            self._json(results)

        elif p.path == '/email-alert':
            ok,msg = send_email_alert(qs.get('name',['Asset'])[0],qs.get('ip',[''])[0],qs.get('down',['1'])[0]=='1')
            self._json({'ok':ok,'msg':msg})

        elif p.path == '/email-test':
            ok,msg = send_email_alert('TEST ASSET','192.168.0.1',True)
            self._json({'ok':ok,'msg':msg})

        elif p.path == '/email-config':
            data={}
            if qs.get('from'): data['from_email']   = qs['from'][0]
            if qs.get('pass'): data['app_password'] = qs['pass'][0]
            if qs.get('to'):   data['to_emails']    = [e.strip() for e in qs['to'][0].split(',')]
            if data:
                save_email_cfg(data)
                self._json({'ok':True})
            else:
                safe={k:('••••••' if k=='app_password' and v else v) for k,v in email_cfg.items()}
                self._json({'ok':True,'cfg':safe})

        elif p.path == '/run':
            cmd = qs.get('cmd',[''])[0].strip()
            # Whitelist of allowed Windows tools
            ALLOWED_CMDS = [
                'ncpa.cpl','firewall.cpl','devmgmt.msc','services.msc',
                'eventvwr.msc','resmon.exe','compmgmt.msc','gpedit.msc',
                'taskmgr.exe','msconfig.exe','control.exe','diskmgmt.msc',
                'perfmon.msc','secpol.msc','lusrmgr.msc','wmimgmt.msc',
                'mstsc.exe','calc.exe','notepad.exe','explorer.exe',
                'msinfo32.exe','dxdiag.exe','cleanmgr.exe'
            ]
            cmd_lower = cmd.lower()
            allowed = any(cmd_lower == a or cmd_lower.startswith(a.split('.')[0]) for a in ALLOWED_CMDS)
            if not cmd or not allowed:
                self._json({'ok':False,'msg':'Command not in whitelist'})
            elif not IS_WIN:
                self._json({'ok':False,'msg':'Run-cmd only available on Windows'})
            else:
                try:
                    subprocess.Popen(['cmd','/c','start','',cmd], shell=False,
                                     creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess,'CREATE_NO_WINDOW') else 0)
                    self._json({'ok':True,'msg':f'Launched: {cmd}'})
                except Exception as e:
                    self._json({'ok':False,'msg':str(e)})

        elif p.path == '/iplookup':
            ip_target = qs.get('ip',[''])[0].strip()
            import urllib.request
            try:
                fields = 'status,message,continent,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,asname,reverse,mobile,proxy,hosting,query'
                url = f'http://ip-api.com/json/{ip_target}?fields={fields}'
                req = urllib.request.urlopen(url, timeout=6)
                data = json.loads(req.read().decode())
                self._json(data)
            except Exception as e:
                self._json({'status':'fail','message':str(e)})

        elif p.path == '/dns':
            name = qs.get('name',[''])[0]
            qtype = qs.get('type',['A'])[0]
            import urllib.request
            try:
                url = f'https://cloudflare-dns.com/dns-query?name={urllib.parse.quote(name)}&type={urllib.parse.quote(qtype)}'
                req = urllib.request.Request(url, headers={'Accept':'application/dns-json'})
                res = urllib.request.urlopen(req, timeout=5)
                data = json.loads(res.read().decode())
                self._json(data)
            except Exception as e:
                self._json({'Status':2,'Answer':[],'error':str(e)})


        elif p.path == '/run-cmd':
            raw_cmd = qs.get('cmd',[''])[0].strip()
            # Whitelist-based: only safe read-only commands allowed
            ALLOWED_PREFIXES = [
                'ipconfig','arp ','netstat','route print','route print',
                'nslookup','ping ','tracert ','whoami','systeminfo',
                'tasklist','net user','net localgroup','net share',
                'netsh interface ip show','netsh wlan show',
                'netsh advfirewall show','getmac','hostname',
                'wmic nic get','wmic os get','wmic cpu get',
                'dir ','type ','echo ','ver','date /t','time /t',
                'ipconfig /all','ipconfig /displaydns',
                'net statistics','net view',
            ]
            BLOCKED = ['del ','format ','rm ','rmdir','shutdown','reboot','reg ','sc stop','sc delete','net stop','net start','runas','powershell -e','powershell -enc']
            cmd_lower = raw_cmd.lower()
            allowed = any(cmd_lower.startswith(p.lower()) for p in ALLOWED_PREFIXES)
            blocked = any(b in cmd_lower for b in BLOCKED)
            if not allowed or blocked:
                self._json({'ok':False,'output':'','error':f'Command not allowed: "{raw_cmd}". Only safe read-only commands are permitted.'})
                return
            try:
                import subprocess as _sp
                result = _sp.run(raw_cmd, shell=True, capture_output=True, text=True, timeout=15, encoding='utf-8', errors='replace')
                output = (result.stdout or '') + (result.stderr or '')
                self._json({'ok': result.returncode==0, 'output': output[:8000], 'error': ''})
            except _sp.TimeoutExpired:
                self._json({'ok':False,'output':'','error':'Command timed out (15s limit)'})
            except Exception as e:
                self._json({'ok':False,'output':'','error':str(e)})

        elif p.path == '/status':
            self._json({'status':'ok','port':PORT,'os':platform.system(),
                        'email_configured':bool(email_cfg.get('from_email') and email_cfg.get('app_password'))})
        else:
            self.send_response(404); self.end_headers()

    def _file(self, filename, mime):
        fpath = os.path.join(BASE_DIR, filename)
        if not os.path.isfile(fpath):
            self.send_response(404); self.end_headers(); return
        with open(fpath,'rb') as f: data=f.read()
        self.send_response(200)
        self._cors()
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', len(data))
        self.end_headers()
        self.wfile.write(data)

    def _json(self, data):
        body=json.dumps(data).encode()
        self.send_response(200); self._cors()
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',len(body))
        self.end_headers(); self.wfile.write(body)

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods','GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type')

    def log_message(self,fmt,*args):
        print(f'  [{self.address_string()}] {fmt%args}')

def main():
    load_email_cfg()
    print('='*54)
    print('  NetOps Toolkit — Ping + Email Backend')
    print('  By M Kamjo')
    print('='*54)
    print(f'  OS   : {platform.system()} {platform.release()}')
    print(f'  Port : {PORT}')
    if email_cfg.get('from_email'):
        print(f'  Mail : {email_cfg["from_email"]} → {email_cfg.get("to_emails",[])}')
    else:
        print('  Mail : Not configured yet')
    print('='*54)
    print(f'\n  >>> Open NetOps in browser: http://localhost:{PORT}\n')
    print('  Keep this window open. Press Ctrl+C to stop.\n')

    r = ping('127.0.0.1',count=1,timeout=1)
    print(f'  Ping test: {"✓ OK ("+str(r["ms"])+"ms)" if r["online"] else "✗ FAILED — try Run as Administrator"}\n')

    server = HTTPServer(('127.0.0.1',PORT),Handler)
    try: server.serve_forever()
    except KeyboardInterrupt: print('\n  Stopped.'); server.server_close()

if __name__ == '__main__': main()
