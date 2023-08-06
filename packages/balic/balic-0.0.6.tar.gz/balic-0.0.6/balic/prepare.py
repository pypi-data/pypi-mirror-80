import os
import logging

from cliff.command import Command
from balic import Balic


class Prepare(Command):

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        """Prepare linux container
        """
        self.balic = Balic(parsed_args.name)
        self.balic.prepare(
            parsed_args.directory,
            parsed_args.environment,
        )

    def get_description(self):
        return "prepare linux container"

    def get_parser(self, prog_name):
        parser = super(Prepare, self).get_parser(prog_name)
        parser = Balic.get_parser(parser)
        parser.add_argument("-d", "--directory", required=True)
        parser.add_argument("-e", "--environment", default="")
        return parser
