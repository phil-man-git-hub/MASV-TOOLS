#!/usr/bin/env python3

# python/masv_portal/src/masv_portal/cli/__init__.py

"""Command registration and interfaces for the CLI."""

from abc import ABC, abstractmethod
from argparse import ArgumentParser, _SubParsersAction
from typing import List

class Command(ABC):
    """Base class for all CLI commands."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the command."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """The description of the command."""
        pass
    
    @abstractmethod
    def register_subparser(self, subparsers: _SubParsersAction) -> ArgumentParser:
        """Register this command's subparser and return it."""
        pass
    
    @abstractmethod
    def execute(self, args: ArgumentParser) -> int:
        """Execute the command with the parsed arguments."""
        pass

def get_portal_commands() -> List[Command]:
    """Get all available portal commands."""
    from .list import ListCommand
    from .create import CreateCommand
    from .delete import DeleteCommand
    
    return [
        ListCommand(),
        CreateCommand(),
        DeleteCommand()
    ]
