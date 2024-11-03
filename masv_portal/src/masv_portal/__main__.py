#!/usr/bin/env python3

# python/masv_portal/src/masv_portal/__main__.py

"""
Entry point for masv_portal.
"""

import sys
import argparse
from typing import NoReturn

from masv_portal.config import TOOL_NAME
# from masv_portal.cli.commands import get_portal_commands
from masv_portal.cli import get_portal_commands

def main() -> NoReturn:
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(
        prog=TOOL_NAME,
        description='A command line tool to list, create, and delete MASV Portals'
    )
    
    # Add global options
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Log activity to standard error'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='1.0.0'
    )

    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest='command')
    
    # Register all portal commands
    for command in get_portal_commands():
        command.register_subparser(subparsers)

    # Parse arguments and execute
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
        
    try:
        sys.exit(args.func(args))
    except Exception as e:
        if args.verbose:
            raise
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()