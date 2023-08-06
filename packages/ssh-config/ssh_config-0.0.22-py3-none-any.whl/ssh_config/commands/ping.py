from .base import BaseCommand
from .utils import table_print, grep


class Ping(BaseCommand):
    """Ping hosts.

    usage: ping [options] [PATTERN]

    Options:
        -v --verbose            Verbose output
        -h --help               Show this screen
    """

    def execute(self):
        pattern = self.options.get("PATTERN", None)
        verbose = self.options.get("--verbose")

        printer = table_print(verbose)
        target = grep(pattern, printer)
        for host in self.config:
            target.send(host)
