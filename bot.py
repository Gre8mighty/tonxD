import sys
import time
from typing import List
from datetime import datetime
import json

sys.dont_write_bytecode = True

from smart_airdrop_claimer import base
from core import (
    get_token,
    get_centrifugo_token,
    get_info,
    process_check_in,
    process_do_task,
    process_farm,
    create_banner
)

class TerminalStyle:
    """Enhanced terminal styling with rich colors and formatting"""
    # Basic Colors
    BLACK = '\033[38;5;0m'
    RED = '\033[38;5;196m'
    GREEN = '\033[38;5;82m'
    YELLOW = '\033[38;5;220m'
    BLUE = '\033[38;5;51m'
    MAGENTA = '\033[38;5;201m'
    CYAN = '\033[38;5;39m'
    WHITE = '\033[38;5;255m'
    
    # Bright Colors
    BRIGHT_RED = '\033[38;5;203m'
    BRIGHT_GREEN = '\033[38;5;118m'
    BRIGHT_YELLOW = '\033[38;5;227m'
    BRIGHT_BLUE = '\033[38;5;81m'
    BRIGHT_MAGENTA = '\033[38;5;207m'
    BRIGHT_CYAN = '\033[38;5;87m'
    
    # Pastel Colors
    PASTEL_RED = '\033[38;5;211m'
    PASTEL_GREEN = '\033[38;5;157m'
    PASTEL_YELLOW = '\033[38;5;229m'
    PASTEL_BLUE = '\033[38;5;117m'
    PASTEL_MAGENTA = '\033[38;5;219m'
    PASTEL_CYAN = '\033[38;5;159m'
    
    # Special Colors
    ORANGE = '\033[38;5;214m'
    PURPLE = '\033[38;5;141m'
    PINK = '\033[38;5;218m'
    GOLD = '\033[38;5;220m'
    SILVER = '\033[38;5;247m'
    BRONZE = '\033[38;5;172m'
    
    # Background Colors
    BG_RED = '\033[48;5;196m'
    BG_GREEN = '\033[48;5;82m'
    BG_YELLOW = '\033[48;5;220m'
    BG_BLUE = '\033[48;5;51m'
    BG_MAGENTA = '\033[48;5;201m'
    BG_CYAN = '\033[48;5;39m'
    
    # Text Styles
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    RESET = '\033[0m'
    
    # Compound Styles
    SUCCESS = f"{BRIGHT_GREEN}{BOLD}"
    ERROR = f"{BRIGHT_RED}{BOLD}"
    WARNING = f"{BRIGHT_YELLOW}{BOLD}"
    INFO = f"{BRIGHT_BLUE}{BOLD}"
    CRITICAL = f"{BG_RED}{WHITE}{BOLD}"
    HIGHLIGHT = f"{BG_YELLOW}{BLACK}{BOLD}"

class TONxDAO:
    """Main bot class for TONxDAO automation with enhanced visual feedback"""
    
    def __init__(self):
        self.data_file = base.file_path(file_name="data.txt")
        self.config_file = base.file_path(file_name="config.json")
        self.line = "─" * 60
        self.banner = create_banner()
        self.style = TerminalStyle()
        
        # Load configuration with proper parsing
        self.load_config()

    def load_config(self):
        """Load and validate all configuration values"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            # Parse boolean configs
            self.auto_check_in = self._parse_bool_value(config.get('auto-check-in', 'false'))
            self.auto_do_task = self._parse_bool_value(config.get('auto-do-task', 'false'))
            self.auto_farm = self._parse_bool_value(config.get('auto-farm', 'false'))
            
            # Parse wait time
            wait_time = int(config.get('wait-time', '360'))
            if wait_time <= 0:
                raise ValueError("Wait time must be positive")
            self.wait_time = wait_time * 60  # Convert to seconds
            
        except Exception as e:
            self._print_error(f"Failed to load config: {str(e)}")
            # Set default values
            self.auto_check_in = True
            self.auto_do_task = True
            self.auto_farm = True
            self.wait_time = 360 * 60  # 360 minutes in seconds

    def _parse_bool_value(self, value: str) -> bool:
        """Parse string boolean value"""
        if isinstance(value, str):
            return value.lower() == 'true'
        return bool(value)

    def _print_header(self, text: str):
        """Print stylized header with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n{self.style.PURPLE}{self.line}")
        print(f"{self.style.GOLD}[{timestamp}] {self.style.BRIGHT_CYAN}{text}")
        print(f"{self.style.PURPLE}{self.line}{self.style.RESET}\n")

    def _print_status(self, message: str, status: bool = None):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if status is None:
            print(f"{self.style.SILVER}[{timestamp}] {self.style.INFO}{message}{self.style.RESET}")
        elif status:
            print(f"{self.style.SILVER}[{timestamp}] {self.style.SUCCESS}✓ {message}{self.style.RESET}")
        else:
            print(f"{self.style.SILVER}[{timestamp}] {self.style.ERROR}✗ {message}{self.style.RESET}")

    def _print_error(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{self.style.SILVER}[{timestamp}] {self.style.CRITICAL} ERROR {self.style.RESET} {self.style.ERROR}{message}{self.style.RESET}")

    def _print_warning(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{self.style.SILVER}[{timestamp}] {self.style.WARNING}⚠ {message}{self.style.RESET}")

    def _print_info(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{self.style.SILVER}[{timestamp}] {self.style.INFO}ℹ {message}{self.style.RESET}")

    def _print_stats(self, label: str, value: str):
        print(f"{self.style.PASTEL_BLUE}{label}: {self.style.PASTEL_YELLOW}{value}{self.style.RESET}")

    def _print_separator(self):
        print(f"{self.style.PURPLE}{self.line}{self.style.RESET}")

    def _process_account(self, account_data: str, account_num: int, total_accounts: int):
        try:
            self._print_header(f"Processing Account {account_num}/{total_accounts}")
            
            token = get_token(data=account_data)
            if not token:
                self._print_error("Failed to get authentication token")
                return

            dao_id = get_info(token=token)
            if not dao_id:
                self._print_error("Failed to get account information")
                return

            centrifugo_token = get_centrifugo_token(token=token)
            if not centrifugo_token:
                self._print_error("Failed to get centrifugo token")
                return

            self._handle_automated_tasks(token, centrifugo_token, dao_id)
            get_info(token=token)
            
        except Exception as e:
            self._print_error(f"Account processing failed: {str(e)}")

    def _handle_automated_tasks(self, token: str, centrifugo_token: str, dao_id: str):
        # Check-in processing
        if self.auto_check_in:
            self._print_status("Auto Check-in", True)
            process_check_in(token=token)
        else:
            self._print_status("Auto Check-in Disabled", False)

        # Task processing
        if self.auto_do_task:
            self._print_status("Auto Task Processing", True)
            process_do_task(token=token)
        else:
            self._print_status("Auto Task Processing Disabled", False)

        # Farming
        if self.auto_farm:
            self._print_status("Auto Farming", True)
            process_farm(token=centrifugo_token, dao_id=dao_id)
        else:
            self._print_status("Auto Farming Disabled", False)

    def main(self):
        while True:
            try:
                base.clear_terminal()
                print(f"{self.style.GOLD}{self.banner}{self.style.RESET}")
                
                with open(self.data_file, "r") as f:
                    accounts = f.read().splitlines()
                
                total_accounts = len(accounts)
                self._print_header("TONxDAO Bot Status")
                self._print_stats("Total Accounts", str(total_accounts))
                self._print_stats("Auto Check-in", "Enabled" if self.auto_check_in else "Disabled")
                self._print_stats("Auto Task", "Enabled" if self.auto_do_task else "Disabled")
                self._print_stats("Auto Farm", "Enabled" if self.auto_farm else "Disabled")
                self._print_stats("Wait Time", f"{int(self.wait_time/60)} minutes")
                self._print_separator()

                for idx, account_data in enumerate(accounts, 1):
                    self._process_account(account_data, idx, total_accounts)
                    self._print_separator()

                self._print_warning(f"Waiting {int(self.wait_time/60)} minutes until next cycle")
                time.sleep(self.wait_time)
                
            except KeyboardInterrupt:
                self._print_warning("Bot stopped by user")
                sys.exit(0)
            except Exception as e:
                self._print_error(f"Main loop error: {str(e)}")
                time.sleep(5)

if __name__ == "__main__":
    try:
        txd = TONxDAO()
        txd.main()
    except KeyboardInterrupt:
        print(f"\n{TerminalStyle.WARNING}Bot terminated by user{TerminalStyle.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{TerminalStyle.CRITICAL}CRITICAL ERROR {TerminalStyle.RESET} {str(e)}")
        sys.exit(1)