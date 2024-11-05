from argparse import RawTextHelpFormatter, ArgumentParser
from ansimarkup import AnsiMarkup
from rich.console import Console

from os import system
system('cls')


class CustomHelpFormatter(RawTextHelpFormatter):
    def _format_action(self, action):
        # Call the default formatter to get the formatted action
        result = super()._format_action(action)
        # Add an extra newline after each option
        return result + "\n"


class Parser(ArgumentParser):
    def __init__(self):
        self.mk = markup
        super().__init__(
            formatter_class=CustomHelpFormatter,
            # description=AnsiMarkup().parse("<green><bold>ADB wrapper to manage Android connections through WiFi.</bold></green>\nRequires androidSDK or atleast adb-platform tools to be available in the ENV"),
            description=f'{self.mk.boldWrap("ADB wrapper to manage Android connections through WiFi", 'green')}\n\nRequires androidSDK or atleast adb-platform tools to be available in the ENV',
            epilog= "rules:\n"
                    "  - flags : [-p | -c | -l | -rm] are mutually exclusive\n"
                    "  - all   : -a used with [-c, -rm] only\n"
                    "  - yes   : -y used with [-rm -a] only\n"
                    "  - params:\n"
                    "     * -p : This can have 0 or 1[IPAddress:Port] or 2[Code] additional params\n"
                    "            Usage: -p | -p 192.168.0.0:8888 | -p 192.168.0.0:8888 123456\n\n"
                    "     * -c : This can have 0 or 1[Index or IPAddress] or 2[Port] additional params\n"
                    "            Usage: -c | -c 1 | -c 192.168.0.0 | -c 1 8888 | -c 192.168.0.0 8888 | -c -a\n\n"
                    "     * -rm: This can have 0 or 1[Index or IPAddress] additional params\n"
                    "            Usage: -rm | -rm 1 | -rm 192.168.0.0 | -rm -a | -rm -a -y\n\n"
                    "     * -l : This can have 0 additional params\n"
                    "            Usage: -l\n\n"
                    "     * -a : This is a combination flag and can only be used along side supported flags\n"
                    "            Usage: -c -a | -rm -a\n\n"
                    "     * -y : This is a combination flag and can only be used along side supported flags\n"
                    "            Usage: -rm -a -y\n"
                    " "
        )
        group = self.add_mutually_exclusive_group()

        group.add_argument('-p', '--pair', nargs='*', metavar=('ip:port', 'code'), help='pair a new device')
        group.add_argument('-c', '--connect', nargs='*', metavar=('index/ip', 'port'), help='connect to a paired device')
        group.add_argument('-l', '--list', action='store_true', help='list all paired devices with index & status')
        group.add_argument('-rm', '--remove', nargs='*', metavar='index/ip', help='remove a paired device')
        self.add_argument('-a', '--all', action='store_true', help='perform action on all paired devices.\nused with in combination with [-c, -rm]')
        self.add_argument('-y','--yes', action='store_true', help='perform action without user prompt\nused in combination with [-rm -a]')


class MarkUp(AnsiMarkup):
    def __init__(self):
        super().__init__()
        self.txt = None

    def wrap(self, txt, color=None, bgcolor=None, bold=False, parse=True):
        self.txt =  txt
        if color:   self.txt = self.tagWrap(color)
        if bgcolor: self.txt = self.tagWrap(f'bg {bgcolor}')
        if bold:    self.txt = self.tagWrap('bold')
        return self.parse(self.txt) if parse else self.txt

    tagWrap = lambda self, tag: f"<{tag}>{self.txt}</{tag}>"
    boldWrap = lambda self, txt, color=None, bgcolor=None: self.wrap(txt, color, bgcolor, bold=True)
    green = lambda self, txt: self.wrap(txt, 'green')


class Logger(Console):
    def info(self, *txt, blankline=False):
        self.print('[[bold blue]INFO[/]]',end=' ')
        print(*txt)
        if blankline: self.info()

    def warning(self, *txt):
        self.print('[[bold yellow]WARN[/]]',end=' ')
        print(*txt)

    def error(self, *txt):
        self.print('[[bold red]ERROR[/]]',end=' ')
        print(*txt)

    def critical(self, *txt):
        self.print('[[white on red]FATAL[/]]',end=' ')
        print(*txt)


# instances
markup = MarkUp()
log = Logger()
_success = markup.wrap('Success','green')
_failed = markup.wrap('Failed','red')