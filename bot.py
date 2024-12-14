import sys
import time
from typing import List

sys.dont_write_bytecode = True

from smart_airdrop_claimer import base
from core.token import get_token, get_centrifugo_token
from core.info import get_info
from core.task import process_check_in, process_do_task
from core.ws import process_farm
from core.banner import create_banner

class TerminalStyle:
    """Terminal styling constants for enhanced visual feedback"""
    # Basic colors
    GREEN = '\033[38;5;82m'      # Bright lime green for success
    YELLOW = '\033[38;5;220m'    # Warm yellow for warnings/processing
    RED = '\033[38;5;196m'       # Bright red for errors
    WHITE = '\033[38;5;255m'     # Pure white for normal text
    BLUE = '\033[38;5;51m'       # Cyan blue for info
    PURPLE = '\033[38;5;183m'    # Light purple for statistics
    
    # Text styles
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    
    # Background colors for highlights
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'

class TONxDAO:
    """Main bot class for TONxDAO automation"""
    
    def __init__(self):
        """Initialize bot configuration and styling"""
        # File paths
        self.data_file = base.file_path(file_name="data.txt")
        self.config_file = base.file_path(file_name="config.json")
        
        # Visual elements
        self.line = "─" * 50  # Using Unicode box drawing character
        self.banner = create_banner()
        
        # Load configuration
        self.auto_check_in = self._get_config("auto-check-in")
        self.auto_do_task = self._get_config("auto-do-task")
        self.auto_farm = self._get_config("auto-farm")

    def _get_config(self, name: str) -> bool:
        """Get configuration value with error handling"""
        try:
            return base.get_config(self.config_file, name)
        except Exception as e:
            self._print_error(f"Failed to load config {name}: {str(e)}")
            return False

    def _print_status(self, message: str, status: bool = None):
        """Print status message with appropriate styling"""
        if status is None:
            print(f"{TerminalStyle.BLUE}{message}{TerminalStyle.RESET}")
        elif status:
            print(f"{TerminalStyle.GREEN}✓ {message}{TerminalStyle.RESET}")
        else:
            print(f"{TerminalStyle.RED}✗ {message}{TerminalStyle.RESET}")

    def _print_error(self, message: str):
        """Print error message with styling"""
        print(f"{TerminalStyle.BG_RED}{TerminalStyle.WHITE} ERROR {TerminalStyle.RESET} {TerminalStyle.RED}{message}{TerminalStyle.RESET}")

    def _print_warning(self, message: str):
        """Print warning message with styling"""
        print(f"{TerminalStyle.YELLOW}⚠ {message}{TerminalStyle.RESET}")

    def _print_info(self, message: str):
        """Print info message with styling"""
        print(f"{TerminalStyle.BLUE}ℹ {message}{TerminalStyle.RESET}")

    def _print_stats(self, label: str, value: str):
        """Print statistics with styling"""
        print(f"{TerminalStyle.PURPLE}{label}: {TerminalStyle.WHITE}{value}{TerminalStyle.RESET}")

    def _print_separator(self):
        """Print separator line with styling"""
        print(f"{TerminalStyle.BLUE}{self.line}{TerminalStyle.RESET}")

    def _process_account(self, account_data: str, account_num: int, total_accounts: int):
        """Process a single account with error handling"""
        try:
            self._print_info(f"Processing Account {account_num}/{total_accounts}")
            
            # Get authentication token
            token = get_token(data=account_data)
            if not token:
                self._print_error("Failed to get authentication token")
                return

            # Get account information
            dao_id = get_info(token=token)
            if not dao_id:
                self._print_error("Failed to get account information")
                return

            # Get centrifugo token
            centrifugo_token = get_centrifugo_token(token=token)
            if not centrifugo_token:
                self._print_error("Failed to get centrifugo token")
                return

            # Process automated tasks
            self._handle_automated_tasks(token, centrifugo_token, dao_id)
            
            # Final account info update
            get_info(token=token)
            
        except Exception as e:
            self._print_error(f"Account processing failed: {str(e)}")

    def _handle_automated_tasks(self, token: str, centrifugo_token: str, dao_id: str):
        """Handle all automated tasks for an account"""
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
        """Main bot execution loop"""
        while True:
            try:
                base.clear_terminal()
                print(self.banner)
                
                # Load account data
                with open(self.data_file, "r") as f:
                    accounts = f.read().splitlines()
                
                total_accounts = len(accounts)
                self._print_stats("Total Accounts", str(total_accounts))
                self._print_separator()

                # Process each account
                for idx, account_data in enumerate(accounts, 1):
                    self._process_account(account_data, idx, total_accounts)
                    self._print_separator()

                # Wait before next cycle
                wait_time = 60 * 60  # 1 hour
                self._print_warning(f"Waiting {int(wait_time/60)} minutes until next cycle")
                time.sleep(wait_time)
                
            except KeyboardInterrupt:
                self._print_warning("Bot stopped by user")
                sys.exit(0)
            except Exception as e:
                self._print_error(f"Main loop error: {str(e)}")
                time.sleep(5)  # Brief pause before retry

if __name__ == "__main__":
    try:
        txd = TONxDAO()
        txd.main()
    except KeyboardInterrupt:
        print(f"\n{TerminalStyle.YELLOW}Bot terminated by user{TerminalStyle.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{TerminalStyle.BG_RED}{TerminalStyle.WHITE} CRITICAL ERROR {TerminalStyle.RESET} {str(e)}")
        sys.exit(1)