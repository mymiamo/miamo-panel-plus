import requests
import time
import os
import re
import signal
import sys

# Console colors
ORANGE = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


clear()
print(ORANGE + r"""
░███     ░███ ░██                                         ░█████████                                   ░██            
░████   ░████                                             ░██     ░██                                  ░██            
░██░██ ░██░██ ░██ ░██████   ░█████████████   ░███████     ░██     ░██  ░██████   ░████████   ░███████  ░██      ░██   
░██ ░████ ░██ ░██      ░██  ░██   ░██   ░██ ░██    ░██    ░█████████        ░██  ░██    ░██ ░██    ░██ ░██    ░██████ 
░██  ░██  ░██ ░██ ░███████  ░██   ░██   ░██ ░██    ░██    ░██          ░███████  ░██    ░██ ░█████████ ░██      ░██   
░██       ░██ ░██░██   ░██  ░██   ░██   ░██ ░██    ░██    ░██         ░██   ░██  ░██    ░██ ░██        ░██            
░██       ░██ ░██ ░█████░██ ░██   ░██   ░██  ░███████     ░██          ░█████░██ ░██    ░██  ░███████  ░██            
                                                                                                                      
""" + RESET)

# -------------------------------------------------------------------
# Miamo Panel + Proxy list (HTTP first, then SOCKS4 / SOCKS5)
# -------------------------------------------------------------------

MIAMO_PROXIES = [
    # HTTP proxies (try these first)

    {"ip": "15.160.181.77", "port": 8090, "protocol": "https"},
    {"ip": "15.160.181.77", "port": 8090, "protocol": "http"},

]

# Global configuration
url = ""
request_count = 0
proxy_mode = 3        # 1 = Miamo Panel, 2 = custom, 3 = no proxy
custom_proxy = None   # e.g. "socks4://ip:port" or "http://ip:port"


def extract_title_and_description(html: str):
    """Extract <title> and <meta name="description"> from HTML."""
    title = "Not found"
    description = "Not found"

    # Extract <title>...</title>
    title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if title_match:
        title = title_match.group(1).strip()

    # Try <meta name="description" content="...">
    meta_desc_match = re.search(
        r'<meta[^>]+name=["\']description["\'][^>]*>',
        html,
        re.IGNORECASE | re.DOTALL,
    )
    if meta_desc_match:
        tag = meta_desc_match.group(0)
        content_match = re.search(
            r'content=["\'](.*?)["\']',
            tag,
            re.IGNORECASE | re.DOTALL,
        )
        if content_match:
            description = content_match.group(1).strip()
    else:
        # Fallback: try og:description
        og_match = re.search(
            r'<meta[^>]+property=["\']og:description["\'][^>]*>',
            html,
            re.IGNORECASE | re.DOTALL,
        )
        if og_match:
            tag = og_match.group(0)
            content_match = re.search(
                r'content=["\'](.*?)["\']',
                tag,
                re.IGNORECASE | re.DOTALL,
            )
            if content_match:
                description = content_match.group(1).strip()

    return title, description


# --------------------------
# URL INPUT VALIDATION
# --------------------------
pattern = r"^https?://.+"

while True:
    url_input = input(ORANGE + "Enter target URL: " + RESET).strip()

    if re.match(pattern, url_input):
        url = url_input
        print(GREEN + "URL format is valid." + RESET)
        break
    else:
        print(RED + "Invalid URL format. Example: https://example.com" + RESET)


# --------------------------
# REQUEST COUNT INPUT VALIDATION
# --------------------------
while True:
    count_input = input(ORANGE + "How many requests should be sent?: " + RESET).strip()

    if count_input.isdigit() and int(count_input) > 0:
        request_count = int(count_input)
        print(GREEN + f"Request count set to {request_count}." + RESET)
        break
    else:
        print(RED + "Please enter a valid positive integer. Example: 5" + RESET)


# --------------------------
# PROXY MODE SELECTION
# --------------------------
while True:
    print()
    print(ORANGE + "Proxy mode selection:" + RESET)
    print(ORANGE + "[1] Use Miamo Panel + Proxy" + RESET)
    print(ORANGE + "[2] Use your own proxy" + RESET)
    print(ORANGE + "[3] Continue without proxy (Not recommended + VPN Use Is Recommended)" + RESET)

    choice = input("Select an option (1-3): ").strip()

    if choice in ("1", "2", "3"):
        proxy_mode = int(choice)
        break
    else:
        print(RED + "Invalid selection. Please choose 1, 2 or 3." + RESET)

# If user selected custom proxy, ask for it
if proxy_mode == 2:
    while True:
        custom_input = input(
            ORANGE + "Enter your proxy (example: socks4://ip:port or http://ip:port): " + RESET
        ).strip()

        if custom_input:
            custom_proxy = custom_input
            print(GREEN + f"Custom proxy set to: {custom_proxy}" + RESET)
            break
        else:
            print(RED + "Proxy cannot be empty. Please enter a valid proxy string." + RESET)


# --------------------------
# REQUEST SENDER FUNCTION
# --------------------------
def send_request(i: int):
    print(ORANGE + f"[{i}] Connecting to server..." + RESET)

    # No proxy
    if proxy_mode == 3:
        try:
            response = requests.get(url, timeout=1)
            title, description = extract_title_and_description(response.text)
            print(GREEN + f"[{i}] Request succeeded. Status code: {response.status_code}" + RESET)
            print(GREEN + f"[{i}] Page title: {title}" + RESET)
            print(GREEN + f"[{i}] Meta description: {description}" + RESET)
        except Exception as e:
            print(RED + f"[{i}] Request failed (no proxy)." + RESET)
            print(RED + f"[ERROR]: {str(e)}" + RESET)

    # Custom proxy
    elif proxy_mode == 2:
        proxies = {
            "http": custom_proxy,
            "https": custom_proxy
        }
        print(ORANGE + f"[{i}] Using custom proxy: {custom_proxy}" + RESET)
        try:
            response = requests.get(url, proxies=proxies, timeout=40)
            title, description = extract_title_and_description(response.text)
            print(GREEN + f"[{i}] Request succeeded. Status code: {response.status_code}" + RESET)
            print(GREEN + f"[{i}] Page title: {title}" + RESET)
            print(GREEN + f"[{i}] Meta description: {description}" + RESET)
        except Exception as e:
            print(RED + f"[{i}] Request failed with custom proxy." + RESET)
            print(RED + f"[ERROR]: {str(e)}" + RESET)

    # Miamo Panel + Proxy
    elif proxy_mode == 1:
        last_error = None
        success = False

        for p in MIAMO_PROXIES:
            proxy_url = f"{p['protocol']}://{p['ip']}:{p['port']}"
            proxies = {
                "http": proxy_url,
                "https": proxy_url
            }

            print(ORANGE + f"[{i}] Trying Miamo Panel proxy: {proxy_url}" + RESET)

            try:
                response = requests.get(url, proxies=proxies, timeout=40, verify=False)
                title, description = extract_title_and_description(response.text)
                print(GREEN + f"[{i}] Request succeeded with Miamo proxy: {proxy_url}" + RESET)
                print(GREEN + f"[{i}] Status code: {response.status_code}" + RESET)
                print(GREEN + f"[{i}] Page title: {title}" + RESET)
                print(GREEN + f"[{i}] Meta description: {description}" + RESET)
                success = True
                break
            except Exception as e:
                print(RED + f"[{i}] Proxy failed: {proxy_url}" + RESET)
                last_error = e

        if not success:
            print(RED + f"[{i}] All Miamo Panel proxies failed. Request could not be sent." + RESET)
            if last_error is not None:
                print(RED + f"[LAST ERROR]: {str(last_error)}" + RESET)

    print(ORANGE + "-" * 1 + RESET)
    time.sleep(1)


# Prevent console pause/freeze on CTRL + C
def handle_interrupt(signum, frame):
    print(RED + "\n\n[!] Process interrupted by user (CTRL + C)." + RESET)
    time.sleep(1)
    clear()
    os.system("python main.py")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_interrupt)

# --------------------------
# RUN REQUESTS
# --------------------------
try:
    for i in range(1, request_count + 1):
        send_request(i)

    print(GREEN + "\n[+] All requests completed successfully." + RESET)

    # Wait for Enter and return to menu when finished normally
    input(ORANGE + "\nPress Enter to return to the main menu..." + RESET)
    clear()
    os.system("python main.py")

except Exception as e:
    print(RED + f"\n[ERROR]: {str(e)}" + RESET)
    input(ORANGE + "\nPress Enter to exit..." + RESET)
    clear()
    os.system("python main.py")