"""
Banner creator module for TONxDAO bot.
Provides a stylized ASCII art banner with gradient color effects.
"""

class BannerColor:
    """Color constants for banner gradient effects using ANSI color codes."""
    CYAN = '\033[38;5;51m'        # Brightest cyan for top line
    LIGHT_BLUE = '\033[38;5;45m'  # Light blue transition
    BLUE = '\033[38;5;39m'        # Medium blue transition
    MEDIUM_BLUE = '\033[38;5;33m' # Darker blue transition
    DARK_BLUE = '\033[38;5;27m'   # Deep blue transition
    DEEP_BLUE = '\033[38;5;21m'   # Darkest blue for bottom line
    WHITE = '\033[38;5;15m'       # Pure white for contact information
    RESET = '\033[0m'             # Reset color code

def create_banner():
    """
    Creates a stylized ASCII art banner for the TONxDAO bot.
    Uses a gradient color effect from cyan to deep blue for visual appeal.
    
    Returns:
        str: Formatted ASCII art banner with color codes
    """
    return f"""
{BannerColor.CYAN}███████╗██╗     ███████╗██╗  ██╗██╗  ██╗    ██████╗ ██╗ ██████╗██╗  ██╗██╗███████╗
{BannerColor.LIGHT_BLUE}██╔════╝██║     ██╔════╝╚██╗██╔╝╚██╗██╔╝    ██╔══██╗██║██╔════╝██║  ██║██║██╔════╝
{BannerColor.BLUE}█████╗  ██║     █████╗   ╚███╔╝  ╚███╔╝     ██████╔╝██║██║     ███████║██║█████╗  
{BannerColor.MEDIUM_BLUE}██╔══╝  ██║     ██╔══╝   ██╔██╗  ██╔██╗     ██╔══██╗██║██║     ██╔══██║██║██╔══╝  
{BannerColor.DARK_BLUE}██║     ███████╗███████╗██╔╝ ██╗██╔╝ ██╗    ██║  ██║██║╚██████╗██║  ██║██║███████╗
{BannerColor.DEEP_BLUE}╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚══════╝
                   {BannerColor.CYAN}Telegram: {BannerColor.WHITE}@airdrop3arn{BannerColor.RESET}
    """