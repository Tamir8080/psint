#!/usr/bin/env python3
"""
██████╗ ███████╗██╗███╗   ██╗████████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗
██╔══██╗██╔════╝██║████╗  ██║╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║
██████╔╝███████╗██║██╔██╗ ██║   ██║       ███████╗██║     ███████║██╔██╗ ██║
██╔═══╝ ╚════██║██║██║╚██╗██║   ██║       ╚════██║██║     ██╔══██║██║╚██╗██║
██║     ███████║██║██║ ╚████║   ██║       ███████║╚██████╗██║  ██║██║ ╚████║
╚═╝     ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝

PSINT - Passive OSINT Intelligence Gatherer
For educational purposes and authorized security research only.
Author: CyberSec Student Assignment
"""

import argparse
import sys
import os
from modules.banner import print_banner
from modules.username_search import UsernameSearcher
from modules.profile_builder import ProfileBuilder
from modules.image_search import ImageSearcher
from modules.report import ReportGenerator
from modules.utils import Colors, print_status

def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="PSINT - Passive Open Source Intelligence Gatherer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python osint.py --username johndoe
  python osint.py --name "John Doe" --country "US" --city "New York"
  python osint.py --username johndoe --name "John Doe" --sex male --country "UK"
  python osint.py --email john@example.com
  python osint.py --phone +1234567890
  python osint.py --username johndoe --output report.json

IMPORTANT: Only use on targets you have explicit written authorization to investigate.
        """
    )

    # Target input options
    target_group = parser.add_argument_group("Target Input")
    target_group.add_argument("--username", "-u", metavar="USERNAME",
                              help="Target username to search across platforms")
    target_group.add_argument("--name", "-n", metavar="FULL_NAME",
                              help="Target full name (e.g. 'John Doe')")
    target_group.add_argument("--email", "-e", metavar="EMAIL",
                              help="Target email address")
    target_group.add_argument("--phone", "-p", metavar="PHONE",
                              help="Target phone number (E.164 format: +1234567890)")
    target_group.add_argument("--image", "-i", metavar="IMAGE_PATH",
                              help="Path to target image for reverse lookup info")

    # Narrowing options
    filter_group = parser.add_argument_group("Profile Filters")
    filter_group.add_argument("--sex", choices=["male", "female", "other"],
                              help="Target sex/gender")
    filter_group.add_argument("--country", metavar="COUNTRY",
                              help="Target country (e.g. 'US', 'France')")
    filter_group.add_argument("--city", metavar="CITY",
                              help="Target city")
    filter_group.add_argument("--age", metavar="AGE",
                              help="Target approximate age or range (e.g. '25' or '20-30')")
    filter_group.add_argument("--company", metavar="COMPANY",
                              help="Target company or employer")

    # Module options
    module_group = parser.add_argument_group("Module Selection")
    module_group.add_argument("--all", "-a", action="store_true",
                              help="Run all modules")
    module_group.add_argument("--social", action="store_true",
                              help="Search social media platforms")
    module_group.add_argument("--profile", action="store_true",
                              help="Build intelligence profile")
    module_group.add_argument("--img", action="store_true",
                              help="Search for public images")

    # Output options
    output_group = parser.add_argument_group("Output")
    output_group.add_argument("--output", "-o", metavar="FILE",
                              help="Save report to file (supports .json, .txt, .html)")
    output_group.add_argument("--verbose", "-v", action="store_true",
                              help="Verbose output")
    output_group.add_argument("--no-color", action="store_true",
                              help="Disable colored output")
    output_group.add_argument("--timeout", type=int, default=10,
                              help="Request timeout in seconds (default: 10)")

    args = parser.parse_args()

    # Require at least one target
    if not any([args.username, args.name, args.email, args.phone, args.image]):
        print(f"{Colors.RED}[!] Error: Provide at least one target (--username, --name, --email, --phone, or --image){Colors.RESET}")
        parser.print_help()
        sys.exit(1)

    if args.no_color:
        Colors.disable()

    # Print legal disclaimer
    print(f"\n{Colors.YELLOW}{'='*65}")
    print(" ⚠  LEGAL DISCLAIMER")
    print("="*65)
    print(" This tool is for AUTHORIZED security research and educational")
    print(" purposes ONLY. Unauthorized use against individuals or systems")
    print(" you do not have explicit permission to investigate may violate")
    print(" computer crime laws (CFAA, GDPR, etc.).")
    print(f"{'='*65}{Colors.RESET}\n")

    # Build target profile from inputs
    target = {
        "username": args.username,
        "name": args.name,
        "email": args.email,
        "phone": args.phone,
        "image": args.image,
        "sex": args.sex,
        "country": args.country,
        "city": args.city,
        "age": args.age,
        "company": args.company,
    }

    results = {}

    # --- Username search across platforms ---
    if args.username and (args.all or args.social or not any([args.social, args.profile, args.img])):
        print_status("Starting username search across social platforms...", "info")
        searcher = UsernameSearcher(timeout=args.timeout, verbose=args.verbose)
        results["social_accounts"] = searcher.search(args.username)

    # --- Profile intelligence builder ---
    if args.name and (args.all or args.profile or not any([args.social, args.profile, args.img])):
        print_status("Building intelligence profile...", "info")
        builder = ProfileBuilder(verbose=args.verbose)
        results["profile"] = builder.build(target)

    # --- Email lookup ---
    if args.email:
        print_status(f"Investigating email: {args.email}", "info")
        builder = ProfileBuilder(verbose=args.verbose)
        results["email_info"] = builder.email_lookup(args.email)

    # --- Phone lookup ---
    if args.phone:
        print_status(f"Investigating phone: {args.phone}", "info")
        builder = ProfileBuilder(verbose=args.verbose)
        results["phone_info"] = builder.phone_lookup(args.phone)

    # --- Image analysis ---
    if (args.image or (args.username and args.all)) and (args.all or args.img or args.image):
        print_status("Searching for public image data...", "info")
        img_searcher = ImageSearcher(verbose=args.verbose)
        if args.image:
            results["image_analysis"] = img_searcher.analyze_local(args.image)
        if args.username and args.all:
            results["profile_images"] = img_searcher.search_by_username(args.username)

    # --- Generate report ---
    reporter = ReportGenerator(target, results)
    reporter.print_summary()

    if args.output:
        reporter.save(args.output)
        print_status(f"Report saved to: {args.output}", "success")

if __name__ == "__main__":
    main()
