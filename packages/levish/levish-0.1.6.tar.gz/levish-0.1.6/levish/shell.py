import os
from inspect import getfullargspec

from pyfiglet import figlet_format


# TODO add system command functionality
# TODO add some more basic commands (ls, cd, mkdir, rm, etc)



#* ------------------------
#* --- Main Shell class ---
#* ------------------------

class Shell:
    """Creates a new Shell object
    
    Args:
        name (str): Name of the shell.
        show_cwd (bool, optional): Add current working directory to prefix, defaults to "False"
        prefix (str, optional): Shell prefix, defaults to "[>]"
        figlet (bool, optional): Enable figlet print on first start, defaults to "False"
        figlet_font (str, optional): Change figlet font, defaults to "standard"
    """
    def __init__(self, name, show_cwd=False, prefix="[>] ", figlet=False, figlet_font="standard"):
        self._name = name
        self._show_cwd = show_cwd
        self._prefix = prefix
        self._commands = {}
        self._help = ""
        self._figlet = figlet
        self._figlet_font = figlet_font
        self._looping = True



    #* ---------------------
    #* --- loop function ---
    #* ---------------------

    def _loop(self):
        """Main loop waiting for input and executing functions.

        Loop can be exited by calling "_break_loop()"
        """
        while self._looping:
            if self._show_cwd:
                inp = input(f"{self._name}@{os.getcwd()} {self._prefix}")
            else:
                inp = input(self._prefix)

            # test if input is longer than 0 else continue loop
            if (len(inp)) > 0:
                # split input into cmd (first words) and args (every other word as list)
                # keep in mind that the input function always returns a string, so the args also will be strings
                # use int() to convert them into an integer
                cmd, args = inp.split()[0], inp.split()[1:]
                # test if cmd is in commands dict
                if cmd in self._commands:
                    # execute function with given args
                    self._commands[cmd]["func"](args)
                else:
                    # print not found error
                    print(f"Command '{cmd}' does not exist. Try 'help'")
                print("")
            else:
                # continue loop if inp == 0
                continue



    #* ----------------------------
    #* --- add command function ---
    #* ----------------------------

    def add_command(self, cmd: "str", function: "func", description: "str"="no description"):
        """Add a new command to the Shell

        Args:
            cmd (str): command that executes the function
            function (function): functions that is executed when command is typed
            description (str, optional): Defaults to "no description".

        Raises:
            CommandAlreadyExistError: Raised when a command is added that already exist in command dict.
            MissingArgsInFunctionError: Raised when added command function has no parameter called args.
            FunctionNotCallableError: Raised when added command function is not actually a function.
        """
        # check if passed in function is really a function
        if callable(function):
            # check if function takes 1 argument called args
            if "args" in getfullargspec(function).args:
                if not cmd in self._commands:
                    self._commands[cmd] = {
                        "func": function,
                        "desc": description
                    }
                else:
                    raise CommandAlreadyExistError(cmd)
            else:
                raise MissingArgsInFunctionError(cmd)
        else:
            raise FunctionNotCallableError(cmd)


    def command(self, function: "function"):
        """add_command but as decorator
        """
        self.add_command(function.__name__, function, f"{function.__doc__.strip()}")



    #* --------------------------------------
    #* --- other internal functions start ---
    #* --------------------------------------

    def _break_loop(self):
        """Break out of _loop by setting self._looping to False."""
        self._looping = False

    def _build_help(self):
        """Builds the help string that is displayed when the 'help' command is executed."""
        self._help = "------------------------\nCOMMAND: DESCRIPTION"
        for cmd in self._commands:
            self._help += f"\n{cmd}: {self._commands[cmd]['desc']}"
        self._help += "\n------------------------"



    #* ----------------------
    #* --- basic commands ---
    #* ----------------------

    def _cmd_help(self, args):
        if len(args) > 0:
            if args[0] in self._commands:
                print(self._commands[args[0]]["desc"])
            else:
                print(f"Command '{args[0]}' not found")
        else:
            print(self._help)

    def _cmd_cls(self, args):
        os.system("cls")
    
    def _cmd_clear(self, args):
        os.system("clear")

    def _cmd_exit(self, args):
        self._break_loop()




    #* -----------------------------------
    #* --- add basic commands function ---
    #* -----------------------------------

    def add_basic_commands(self):
        """This adds basic commands like 'cls/clear' & 'exit' to the shell"""
        self.add_command("cls", self._cmd_cls, "Clears the screen (windows)")
        self.add_command("clear", self._cmd_clear, "Clears the screen (unix)")
        self.add_command("exit", self._cmd_exit, "Exit the shell")



    #* --------------------
    #* --- run function ---
    #* --------------------

    def run(self):
        """Initialize the Shell and run self._loop"""
        self.add_command("help", self._cmd_help, "Shows help")
        # create help string
        self._build_help()
        # splash
        if self._figlet:
            print(figlet_format(self._name, self._figlet_font))
        # start main loop
        self._loop()



    #* -------------------------
    #* --- custom exceptions ---
    #* -------------------------

class CommandAlreadyExistError(Exception):
    def __init__(self, cmd):
        self.message = f"'{cmd}': This command already exists."

    def __str__(self):
        return self.message

class MissingArgsInFunctionError(Exception):
    def __init__(self, cmd):
        self.message = f"'{cmd}': Function must take 1 argument called args."

    def __str__(self):
        return self.message

class FunctionNotCallableError(Exception):
    def __init__(self, cmd):
        self.message = f"'{cmd}': The passed in function is not a callable object."

    def __str__(self):
        return self.message