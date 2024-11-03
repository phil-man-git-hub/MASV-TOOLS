#!/usr/bin/env python3

# python/masv_portal/src/masv_portal/cli/commands/list.py

"""List command implementation for MASV portals."""

from argparse import ArgumentParser, _SubParsersAction
from typing import List, Optional

from masv_portal.api.client import request
from masv_portal.config import get_team, die
# from masv_portal.cli.commands import Command
from masv_portal.cli import Command

def get_tag(portal: dict) -> str:
    """Get the tag name from a Portal object.
    
    Args:
        portal: A Portal from the MASV server response.
        
    Returns:
        The tag name if present, empty string otherwise.
    """
    return portal.get('tag', {}).get('name', '')

def list_portal(portal: dict) -> None:
    """Output information about one Portal.
    
    Keeps the format simple: uses a single space to separate each column
    so that it's easy to parse this output with other command line tools.
    
    Args:
        portal: A Portal from the MASV server response.
    """
    print(f"{portal['id']} {portal['created_at']} \"{get_tag(portal)}\" {portal['subdomain']}")

class ListCommand(Command):
    @property
    def name(self) -> str:
        return "ls"
    
    @property
    def description(self) -> str:
        return "List the ID, creation date, tag, and subdomain of the specified portals"
    
    def register_subparser(self, subparsers: _SubParsersAction) -> ArgumentParser:
        parser = subparsers.add_parser(self.name, description=self.description)
        parser.add_argument(
            '-t', '--team',
            help='Team ID. Default: MASV_TEAM environment variable'
        )
        parser.add_argument(
            'ids_or_subdomains',
            nargs='*',
            metavar='IDsOrSubdomains',
            help='IDs or subdomains of Portals to list'
        )
        parser.set_defaults(func=self.execute)
        return parser
    
    def execute(self, args) -> int:
        """Execute the list command.
        
        Args:
            args: Parsed command line arguments.
            
        Returns:
            Exit code (0 for success, non-zero for failure).
        """
        team = args.team or get_team()
        
        try:
            portals = request(
                f"/v1/teams/{team}/portals",
                method='GET',
                verbose=args.verbose
            )
            
            if not args.ids_or_subdomains:
                for portal in portals:
                    list_portal(portal)
            else:
                for id_or_subdomain in args.ids_or_subdomains:
                    portal = next(
                        (p for p in portals 
                         if p['id'] == id_or_subdomain or p['subdomain'] == id_or_subdomain),
                        None
                    )
                    if portal:
                        list_portal(portal)
                    else:
                        die(f"No such portal {id_or_subdomain}")
            return 0
            
        except Exception as e:
            die(str(e))
            return 1