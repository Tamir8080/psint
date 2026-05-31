"""Banner display for PSINT tool."""
from .utils import Colors

def print_banner():
    banner = f"""
{Colors.CYAN}
██████╗ ███████╗██╗███╗   ██╗████████╗
██╔══██╗██╔════╝██║████╗  ██║╚══██╔══╝
██████╔╝███████╗██║██╔██╗ ██║   ██║   
██╔═══╝ ╚════██║██║██║╚██╗██║   ██║   
██║     ███████║██║██║ ╚████║   ██║   
╚═╝     ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
{Colors.RESET}{Colors.BOLD}
███████╗ ██████╗ █████╗ ███╗   ██╗
██╔════╝██╔════╝██╔══██╗████╗  ██║
███████╗██║     ███████║██╔██╗ ██║
╚════██║██║     ██╔══██║██║╚██╗██║
███████║╚██████╗██║  ██║██║ ╚████║
╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
{Colors.RESET}
{Colors.GREEN}  Passive Open Source Intelligence Gatherer v1.0{Colors.RESET}
{Colors.YELLOW}  For authorized security research & education only{Colors.RESET}
{Colors.DIM}  github.com/yourusername/psint{Colors.RESET}
"""
    print(banner)
