from . import Cmd
from . import powerShell
class System:
    def __init__(self):
        self.cmd = Cmd.cmd()
        self.powershell = powerShell.PowerShell()

