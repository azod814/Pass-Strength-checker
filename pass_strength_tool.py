import re
import getpass
import time
import hashlib
import requests
import random
import string
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def print_banner():
    banner = f"""
{Fore.RED}
                        ██╗   ██╗██████╗ ██╗
                        ██║   ██║██╔══██╗██║
                        ██║   ██║██████╔╝██║
                        ██║   ██║██╔══██╗██║
                        ╚██████╔╝██║  ██║███████╗
                         ╚═════╝ ╚═╝  ╚═╝╚══════╝

███████╗████████╗██████╗ ███████╗███╗   ██╗ ██████╗████████╗██╗  ██╗
██╔════╝╚══██╔══╝██╔══██╗██╔════╝████╗  ██║██╔════╝╚══██╔══╝██║  ██║
███████╗   ██║   ██████╔╝█████╗  ██╔██╗ ██║██║  ███╗  ██║   ███████║
╚════██║   ██║   ██╔══██╗██╔══╝  ██║╚██╗██║██║   ██║  ██║   ██╔══██║
███████║   ██║   ██║  ██║███████╗██║ ╚████║╚██████╔╝  ██║   ██║  ██║
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝
{Fore.YELLOW}
            [+] Created by: Nitro Dead
            [+] Tool: Password Strength Checker
{Fore.RESET}
    """
    for line in banner.split('\n'):
        print(line)
        time.sleep(0.01)

def is_password_leaked(password):
    try:
        hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix, suffix = hash[:5], hash[5:]
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url)
        if suffix in response.text:
            return True
        return False
    except:
        return False  # Offline mode

def estimate_brute_force_time(password):
    length = len(password)
    charset_size = 0
    if re.search(r'[a-z]', password):
        charset_size += 26
    if re.search(r'[A-Z]', password):
        charset_size += 26
    if re.search(r'[0-9]', password):
        charset_size += 10
    if re.search(r'[!@#$%^&*]', password):
        charset_size += 10
    if charset_size == 0:
        return "Instant"
    # Estimated time in years (simplified)
    combinations = charset_size ** length
    time_seconds = combinations / (10**12)  # 1 trillion guesses per second
    if time_seconds < 1:
        return "Instant"
    elif time_seconds < 60:
        return f"{time_seconds:.2f} seconds"
    elif time_seconds < 3600:
        return f"{time_seconds/60:.2f} minutes"
    elif time_seconds < 86400:
        return f"{time_seconds/3600:.2f} hours"
    elif time_seconds < 31536000:
        return f"{time_seconds/86400:.2f} days"
    else:
        return f"{time_seconds/31536000:.2f} years"

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

def check_strength(password):
    strength = 0
    suggestions = []

    # Length check
    if len(password) >= 8:
        strength += 1
    else:
        suggestions.append("Make it longer (at least 8 characters).")

    # Uppercase check
    if re.search(r'[A-Z]', password):
        strength += 1
    else:
        suggestions.append("Add uppercase letters (A-Z).")

    # Lowercase check
    if re.search(r'[a-z]', password):
        strength += 1
    else:
        suggestions.append("Add lowercase letters (a-z).")

    # Number check
    if re.search(r'[0-9]', password):
        strength += 1
    else:
        suggestions.append("Add numbers (0-9).")

    # Special character check
    if re.search(r'[!@#$%^&*]', password):
        strength += 1
    else:
        suggestions.append("Add special characters (!@#$%^&*).")

    # Common password check
    common_passwords = ["password", "123456", "qwerty", "letmein", "admin", "welcome"]
    if password.lower() in common_passwords:
        strength = 0
        suggestions.append("Avoid common passwords!")

    # Strength level
    if strength <= 2:
        return "WEAK", suggestions
    elif strength <= 4:
        return "MEDIUM", suggestions
    else:
        return "STRONG", suggestions

def print_progress_bar(percent, strength):
    bar_length = 20
    filled = int(bar_length * percent / 100)
    bar = '█' * filled + '-' * (bar_length - filled)
    color = Fore.RED if strength == "WEAK" else Fore.YELLOW if strength == "MEDIUM" else Fore.GREEN
    print(f"\n{color}Password Strength: [{bar}] {percent}% ({strength}){Fore.RESET}")

def main():
    print_banner()
    while True:
        print(f"\n{Fore.CYAN}[+] Options:{Fore.RESET}")
        print(f"   {Fore.GREEN}1.{Fore.RESET} Check Password Strength")
        print(f"   {Fore.GREEN}2.{Fore.RESET} Generate Strong Password")
        print(f"   {Fore.GREEN}3.{Fore.RESET} Exit")
        choice = input(f"\n{Fore.YELLOW}[>]{Fore.RESET} Enter your choice: ")

        if choice == "1":
            password = getpass.getpass(f"{Fore.YELLOW}[>]{Fore.RESET} Enter password to check: ")
            strength, suggestions = check_strength(password)
            percent = {"WEAK": 30, "MEDIUM": 70, "STRONG": 100}[strength]
            print_progress_bar(percent, strength)
            if is_password_leaked(password):
                print(f"{Fore.RED}[!] Warning: This password has been leaked in a data breach!{Fore.RESET}")
            brute_time = estimate_brute_force_time(password)
            print(f"\n{Fore.BLUE}[+] Brute-Force Time Estimate: {brute_time}{Fore.RESET}")
            if strength != "STRONG":
                print(f"{Fore.YELLOW}[+] Suggestions to improve:{Fore.RESET}")
                for tip in suggestions:
                    print(f"   - {tip}")
            time.sleep(2)

        elif choice == "2":
            length = int(input(f"{Fore.YELLOW}[>]{Fore.RESET} Enter password length (default 12): ") or 12)
            password = generate_password(length)
            print(f"\n{Fore.GREEN}[+] Generated Password: {password}{Fore.RESET}")
            time.sleep(2)

        elif choice == "3":
            print(f"\n{Fore.RED}[!] Exiting...{Fore.RESET}")
            break

        else:
            print(f"\n{Fore.RED}[!] Invalid choice!{Fore.RESET}")

if __name__ == "__main__":
    main()
