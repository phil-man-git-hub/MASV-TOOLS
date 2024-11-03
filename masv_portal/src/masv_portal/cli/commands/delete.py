#!/usr/bin/env python3

# python/masv_portal/src/masv_portal/cli/commands/delete.py

"""Delete command implementation for MASV portals."""

from argparse import ArgumentParser, _SubParsersAction
from typing import List

from masv_portal.api.client import request
from masv_portal.config import die
# from masv_portal.cli.commands import Command
from masv_portal.cli import Command

class DeleteCommand(Command):
    @property
    def name(self) -> str:
        return "rm"
    
    @property
    def description(self) -> str:
        return "Delete existing Portals"
    
    def register_subparser(self, subparsers: _SubParsersAction) -> ArgumentParser:
        parser = subparsers.add_parser(self.name, description=self.description)
        parser.add_argument(
            'ids',
            nargs='+',
            metavar='IDs',
            help='IDs of Portals to delete'
        )
        parser.set_defaults(func=self.execute)
        return parser
    
    def execute(self, args) -> int:
        """Execute the delete command."""
        for portal_id in args.ids:
            try:
                request(
                    f"/v1/portals/{portal_id}",
                    method='DELETE',
                    verbose=args.verbose
                )
            except Exception as e:
                die(str(e))
                return 1
        return 0