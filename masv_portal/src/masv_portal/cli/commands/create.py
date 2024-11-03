#!/usr/bin/env python3

# python/masv_portal/src/masv_portal/cli/commands/create.py

"""Create command implementation for MASV portals."""

from argparse import ArgumentParser, _SubParsersAction
import json
from typing import List, Optional

from masv_portal.api.client import request
from masv_portal.config import get_team, die
# from masv_portal.cli.commands import Command
from masv_portal.cli import Command

class CreateCommand(Command):
    @property
    def name(self) -> str:
        return "new"
    
    @property
    def description(self) -> str:
        return "Create new Portal"
    
    def register_subparser(self, subparsers: _SubParsersAction) -> ArgumentParser:
        parser = subparsers.add_parser(self.name, description=self.description)
        
        # Required arguments
        parser.add_argument(
            '--subdomain',
            required=True,
            help='Subdomain of the Portal to create'
        )
        parser.add_argument(
            '--name',
            required=True,
            help='Name of the Portal to create'
        )
        parser.add_argument(
            '--message',
            required=True,
            help='Message displayed on the Portal upload page'
        )
        parser.add_argument(
            '--recipients',
            required=True,
            nargs='+',
            help='Email address(es) that will receive notification of uploads'
        )
        
        # Optional arguments
        parser.add_argument(
            '-t', '--team',
            help='Team ID. Default: MASV_TEAM environment variable'
        )
        parser.add_argument(
            '--access_code',
            help='Password to upload packages to this Portal'
        )
        parser.add_argument(
            '--download_password',
            help='Password for downloading packages from this Portal'
        )
        parser.add_argument(
            '--tag',
            help='Name of tag to associate with all packages from this Portal'
        )
        
        parser.set_defaults(func=self.execute)
        return parser
    
    def execute(self, args) -> int:
        """Execute the create command."""
        team = args.team or get_team()
        
        portal_spec = {
            'name': args.name,
            'subdomain': args.subdomain,
            'message': args.message,
            'recipients': args.recipients,
            'access_code': args.access_code,
            'download_password': args.download_password,
            'tag': {
                'name': args.tag
            } if args.tag else None
        }
        
        # Remove None values
        portal_spec = {k: v for k, v in portal_spec.items() if v is not None}
        
        try:
            data = request(
                f"/v1/teams/{team}/portals",
                method='POST',
                headers={'Content-Type': 'application/json'},
                body=json.dumps(portal_spec),
                verbose=args.verbose
            )
            
            print(f"{data['id']} https://{data['subdomain']}.portal.massive.io/")
            return 0
            
        except Exception as e:
            die(str(e))
            return 1