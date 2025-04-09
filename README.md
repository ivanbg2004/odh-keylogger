# OD&H Keylogger - Ethical Educational Resource

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This repository contains a Python-based keylogger developed by Oblivion Development & Hosting (OD&H) for **ethical and educational purposes only**. It is intended to demonstrate the potential risks associated with keylogging and to provide insights into how such tools work.

**Important Disclaimer:** This tool should **never** be used for malicious purposes or without explicit consent. OD&H is not responsible for any misuse of this software. By using this code, you agree to use it responsibly and ethically.

## Features

*   **Keylogging:** Records keystrokes and saves them to a log file.
*   **System Information Gathering:** Collects basic system information (OS, hostname, IP address, etc.) for analysis.
*   **Screenshot Capture:** Periodically captures screenshots of the active desktop.
*   **Clipboard Monitoring:** Monitors clipboard contents for potentially sensitive data.
*   **Active Window Tracking:**  Logs the title of the active window.
*   **Email Reporting (Optional):** Can send reports via email at specified intervals (requires configuration).
*   **Configurable:** Settings (reporting interval, file paths, email settings) can be customized via a configuration file (`config.ini`).

## Ethical Considerations

OD&H emphasizes the importance of ethical considerations when working with security tools. This keylogger is provided solely for:

*   **Security Awareness Training:** Demonstrating the risks of keylogging to end-users.
*   **Educational Purposes:** Understanding how keyloggers function and how to defend against them.
*   **Research:**  Studying security vulnerabilities in controlled environments.

**Unethical uses are strictly prohibited.**

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/ivanbg2004/odh-keylogger.git
    cd odh-keylogger
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
    (Ensure you have Python and pip installed)

3.  **Configuration:**

    *   Edit the `config.ini` file to configure settings such as the reporting interval, file paths, and email settings (if email reporting is desired).
    *   **Important:** Ensure that email settings are properly configured with a dedicated email account to prevent misuse.

## Usage

1.  **Run the keylogger:**

    ```bash
    python main.py
    ```

2.  **Stopping the keylogger:**

    *   Press `Ctrl+C` in the terminal window.

## Important Files

*   `main.py`: The main script to start the keylogger.
*   `keylogger.py`: Contains the Keylogger class with all the core keylogging functionality.
*   `config.ini`: Configuration file for customizing settings.
*   `requirements.txt`: Lists the required Python packages.
*   `odh_keylog.txt`: (Default) The log file where keystrokes are recorded.
*   `odh_system_info.json`: (Default) File containing system information.
*   `odh_screenshots/`: (Default) Directory where screenshots are saved.

## Configuration Options (`config.ini`)


| Setting                 | Description                                                                   | Default Value         |
| ----------------------- | ----------------------------------------------------------------------------- | --------------------- |
| `report_interval`       | Time interval (in seconds) between reports.                                   | `120`                 |
| `persistence`           | Whether to attempt to establish persistence (auto-start on boot).             | `True`                |
| `log_file`              | Path to the log file where keystrokes are saved.                              | `odh_keylog.txt`      |
| `system_info_file`      | Path to the file where system information is saved.                           | `odh_system_info.json`|
| `screenshot_dir`        | Path to the directory where screenshots are saved.                            | `odh_screenshots`     |
| `obfuscate`             | Whether to obfuscate the code (not fully implemented).                        | `False`               |
| `enable_email_reporting`| Enable or disable email reporting.                                            | `False`               |
| `email`                 | Email address to send reports to (if email reporting is enabled).             | `''`                  |
| `password`              | Password for the email account (if email reporting is enabled).               | `''`                  |

## Contributing

Contributions are welcome, but please ensure that all contributions align with the ethical and educational goals of this project. Submit pull requests with clear descriptions of the changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## About Oblivion Development & Hosting (OD&H)

Oblivion Development & Hosting helps individuals and businesses succeed in the digital world with top-tier web development, hosting, and cybersecurity services. We deliver secure, reliable, and innovative tech solutions with transparency and trust.

*   **Website:** [odh.ivan-vcard.xyz](https://odh.ivan-vcard.xyz)

## OD&H Support

For support or inquiries, please contact OD&H Customer Support via [OD&H Discord](https://discord.gg/na8gqhQYJR).
