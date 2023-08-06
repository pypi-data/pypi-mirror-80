#!/usr/bin/python3
# -*- coding: utf-8 -*-   vim: set fileencoding=utf-8 :

"""A Git repository on which we can run commands.

The Git class has a few specific commands, like git.hard_reset() or
git.current_branch(), defined below.

Any other method call 'git.<CMD>(…)' is converted to a system call
'git CMD …', e.g.
    from git_adapter.git import Git
    git = Git(sandbox=".")
    git.log()       ↦ git log
    git.ls_files()  ↦ git ls-files
    file="modified.txt"; git.add(file)
                    ↦ git add modified.txt
    git.commit(m="T'was brillig.", author="me")
                    ↦ git commit -m "T'was brillig." --author=me
    git.log(first_parent=True, max_count=20, author="me")
                    ↦ git log --first-parent --max-count=20 --author=me
    git.worktree.add(PATH, BRANCH)
                    ↦ git worktree add PATH BRANCH

Calling a git command returns a generator of `str` representing the lines of
output from the command:
    files = list(git.ls_files())

To retrieve just the first line of output, the generator has a method
first_line():
    head = git.rev_parse("HEAD").first_line()

Note that in the command name and in the kwargs, underscores are mapped to
hyphens, so there currently is no way to call 'git strange_command
--strange_option', because git_adapter would try to call 'git
strange-command --strange-option' instead.


Example usage:
    git = Git.clone_repo("git@git.host:test-repo")
    log_lines = git.log(first_parent=True, max_count=20, author="me")
    files = git.ls_files()

    with open("greeting.txt", "w") as fh:
        fh.write("Hello world\\n")
    git.commit("greeting.txt", m="Greet the world.", author="me")

    origin = git.remote().first_line()
    branch = git.current_branch()
    git.push(origin, branch)

    # Python reserved keywords have to be escaped with a trailing
    # underscore:
    git.grep("keyword", break_=True, heading=True)


The Git class is derived from the more general Command class that can be
used in a similar manner:
    ip = Command(["ip"])
    ip.address.show()             ↦ ip address show
    ip.address.show("dev", "lo")  ↦ ip address show dev lo
    ip.address.show.dev("lo")     ↦ ditto
    ip.address.show.dev.lo()      ↦ ditto

"""


import os
import re
import subprocess
import sys
import traceback

from typing import Dict, List, Iterator, Optional, Union


INFINITY = float("Inf")

# All(?) reserved words in Python, based on
# https://docs.python.org/3.8/reference/lexical_analysis.html#identifiers
PYTHON_RESERVED_WORDS = [
    "and",
    "as",
    "assert",
    "async",
    "await",
    "break",
    "class",
    "continue",
    "def",
    "del",
    "elif",
    "else",
    "except",
    "False",
    "finally",
    "for",
    "from",
    "global",
    "if",
    "import",
    "in",
    "is",
    "lambda",
    "None",
    "nonlocal",
    "not",
    "or",
    "pass",
    "raise",
    "return",
    "True",
    "try",
    "while",
    "with",
    "yield",
]


class Command:
    """A (shell) command that takes subcommands.

    Examples:
      Command(["ls"])("-l")              # run 'ls -l'
      Command(["ip"]).address.show()     # run 'ip address show'
      Command(["ip", "address"]).show()  # ditto
      Command(["git"]).log()             # run 'git log'

    """

    def __init__(
        self,
        cmd: List[str],
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        logger: Optional["Logger"] = None,
        verbose: bool = False,
    ) -> None:
        """Create a Command object.
        Arguments:
            cmd:
                The command to call, as list of words.
                E.g. ["ls"], ["git", "worktree", "add"].
            cwd:
                Directory where the command will be run.
            env:
                A dict for setting environment variables for the command's
                process.
                If not set, the environment is inherited from os.environ.
            logger:
                A Logger object to log actions and output.
                The default is to use a NullLogger that will only print
                output if an error occurs.
            verbose:
                If True, use a StdoutLogger as default logger.
        """
        self.cmd = cmd
        self.cwd = cwd
        if env is None:
            self.environ = dict(os.environ)
        else:
            self.environ = dict(env)
        if logger:
            self.logger = logger  # type: Logger
        else:
            if verbose:
                self.logger = StdoutLogger()
            else:
                self.logger = NullLogger()

    def update_env(self, env: Dict[str, str]) -> None:
        """Set/overwrite entries in the command's environment."""
        self.environ = {**self.environ, **env}

    def set_logger(self, logger: "Logger") -> None:
        """Set the logger for this Command object."""
        self.logger = logger

    def __call__(self, *args: str, **kwargs: str) -> "OutputGenerator":
        """
        Arguments:
            args:
                Handed on to the git command. E.g.
                   git.log("HEAD") ↦ got log HEAD
            kwargs:
                Keyword arguments that are mapped to command-line options
                for the git command. E.g.
                    self.commit(m="T'was brillig.", author="me")
                        ↦ git commit -m "T'was brillig." --author=me
        Returns:
            A string generator representing the lines of output from the
            git command.

        """
        adjusted_cmd = self._restore_names(self.cmd)
        git_cli_options = self._kwargs_to_options(kwargs)
        cmd_line = [*adjusted_cmd, *git_cli_options, *args]
        try:
            return run_cmd(
                cmd_line,
                env=self.environ,
                logger=self.logger,
                cwd=self.cwd,
            )
        except subprocess.CalledProcessError as e:
            raise CmdError(cmd_line, e.output, e.returncode)

    def __getattr__(self, attribute: str) -> "Command":
        """Map undefined attributes to commands."""
        return Command(
            cmd=self.cmd + [attribute], cwd=self.cwd, logger=self.logger
        )

    @staticmethod
    def _restore_names(cmd: List[str]) -> List[str]:
        """Revert underscores to hyphens."""
        return [part.replace("_", "-") for part in cmd]

    def _kwargs_to_options(self, kwargs: Dict[str, str]) -> List[str]:
        options = []
        for (opt, value) in kwargs.items():
            opt = self._reconstruct_option(opt)
            if len(opt) == 1:
                fmt = "-{}"
            else:
                fmt = "--{}"
            option = fmt.format(opt.replace("_", "-"))
            if isinstance(value, bool):
                if not value:
                    option = re.sub(r"^--", "--no-", option)
                options.append(option)
            else:
                options.append(option + "=" + str(value))
        return options

    @staticmethod
    def _reconstruct_option(parameter_name: str) -> str:
        """We cannot use Python keywords as parameter names.

        So we have appended an underscore to them that needs to be removed
        here.

        """
        if parameter_name[-1] != "_":
            return parameter_name
        keyword = parameter_name[:-1]
        if keyword in PYTHON_RESERVED_WORDS:
            return keyword
        else:
            raise Exception(
                "Unexpected escaped parameter:"
                " is {} really a reserved keyword in Python??".format(
                    keyword
                )
            )


class Git(Command):
    """Class to run git commands with."""

    def __init__(
        self,
        sandbox: str,
        env: Optional[Dict[str, str]] = None,
        logger: Optional["Logger"] = None,
        verbose: bool = False,
    ) -> None:
        """Create a Git object.

        Arguments:
            sandbox:
                Directory where the git commands will be applied.
            env:
                A dict for setting environment variables for the git
                process.
                If set, defines the complete environment.
                If not set, the environment is inherited from os.environ.
            logger:
                A Logger object to log actions and output.
                The default is to use a NullLogger that will only print
                output if an error occurs.
            verbose:
                If True, use a StdoutLogger as default logger.

        """
        super().__init__(["git"], sandbox, env, logger, verbose)
        self.sandbox = sandbox

    @staticmethod
    def clone_repo(
        url: str,
        sandbox: Optional[str] = None,
        origin: Optional[str] = None,
        reference: Optional[str] = None,
        logger: Optional["Logger"] = None,
        verbose: bool = False,
    ) -> "Git":
        """Clone a Git repository
            Arguments:
                url:
                    Check out a Git repository from that URL.
                sandbox:
                    Name of the directory to be checked out.
                origin:
                    Set the name of the remote.
                reference:
                    Use this Git repository as reference object store
                    (useful to minimize the volume of network traffic).
                logger:
                    A Logger object to log actions and output.
                    The default is to use a NullLogger that will only print
                    output if an error occurs.
                verbose:
                    If True, use a StdoutLogger as default logger.

            Returns:
                A Git object providing access to the clone.

        """
        args = []
        kwargs = {}
        args.append(url)
        if origin is not None:
            kwargs["origin"] = origin
        if sandbox is not None:
            args.append(sandbox)
        else:
            # Guess the default name for sandbox
            m = re.search(
                r".* : (?: .* /)? (?P<name> [^:/]*?) (?: \.git)? $",
                url,
                flags=re.VERBOSE,
            )
            if m:
                sandbox = m.group("name")
            else:
                raise CmdError(
                    None,
                    "Failed to guess sandbox name for url {}".format(url),
                )
        if reference is not None:
            kwargs["reference"] = reference

        Git(".", logger=logger, verbose=verbose).clone(*args, **kwargs)
        return Git(sandbox, logger=logger, verbose=verbose)

    def hard_reset(self) -> None:
        """Clean up and do a hard reset."""
        self.reset(".")
        self.checkout(".")
        self.clean("--force", "-d", "-x", "-q")
        self.reset("--hard")

    def current_branch(self) -> Optional[str]:
        """Return the current branch."""
        for line in self.branch():
            m = re.search(r"^\* +(?P<branch>\S+)$", line)
            if m:
                return m.group("branch")
        return None

    def __repr__(self) -> str:
        return "git_adapter.git.Git('{}')".format(self.sandbox)


class Logger:
    """A logging interface."""

    def log(
        self,
        msg: Union[str, List[str]] = "",
        indent: int = 0,
        separator: bool = False,
    ) -> None:
        """Log one or several lines.

        Arguments:
            msg:
                One string or a list of strings representing the line(s)
                to log.
            indent:
                Indent each line by this many space characters.
            separator:
                If True, print one empty separator line before msg.
        """
        raise Exception("Abstract method not implemented")

    def write(
        self,
        msg: Union[str, List[str]] = "",
        indent: int = 0,
        separator: bool = False,
    ) -> None:
        """Make sure to write one or several lines.

        Arguments are as for self.log().

        """
        raise Exception("Abstract method not implemented")

    def error(self) -> None:
        """An error has occurred: apply some wind-up procedure.

        """
        raise Exception("Abstract method not implemented")

    @staticmethod
    def _pack_as_list(msg: Union[str, List[str]]) -> List[str]:
        """Convert one string or a list of strings to a list of strings"""
        if isinstance(msg, str):
            return [msg]
        else:
            return msg


class FileLogger(Logger):
    """Log to file and stdout."""

    def __init__(
        self, log_dir: str, log_file: str, separator: int = 1
    ) -> None:
        """Create a FileLogger.

        Parameters:
            log_dir:
                Directory to write the log file to.
            log_file:
                The name of the log file.
            separator:
                Print that many empty lines to stdout.
        """
        if not os.path.isdir(log_dir):
            os.mkdir(log_dir)
        for i in range(separator):
            print()
        self.fh = open(os.path.join(log_dir, log_file), "w")
        self.empty = True

    def log(
        self,
        msg: Union[str, List[str]] = "",
        indent: int = 0,
        separator: bool = False,
    ) -> None:
        if separator and not self.empty:
            self._print()
        messages = Logger._pack_as_list(msg)
        for line in messages:
            self._log_one_line(line, indent=indent)
        self.fh.flush()

    def _log_one_line(self, line: str, indent: int = 0) -> None:
        line = line.rstrip()
        if line:
            prefix = " " * indent
            self._print(prefix + line)
        else:
            self._print()

    def _print(self, line: str = "") -> None:
        print(line)
        self.fh.write(line + "\n")
        self.empty = False

    def write(
        self,
        msg: Union[str, List[str]] = "",
        indent: int = 0,
        separator: bool = False,
    ) -> None:
        self.log(msg, indent=indent, separator=separator)

    def error(self) -> None:
        # Each line of output has already been printed
        pass


class StdoutLogger(Logger):
    """Log to stdout.

    This logger can be used before any directories for logging output are
    set up.

    """

    def log(
        self,
        msg: Union[str, List[str]] = "",
        indent: int = 0,
        separator: bool = False,
    ) -> None:
        if separator:
            print()
        messages = Logger._pack_as_list(msg)
        for line in messages:
            print(line)

    def write(
        self,
        msg: Union[str, List[str]] = "",
        indent: int = 0,
        separator: bool = False,
    ) -> None:
        self.log(msg, indent=indent, separator=separator)

    def error(self) -> None:
        # Each line of output has already been printed
        pass


class NullLogger(Logger):
    """Don't log unless we encounter errors.

    """

    def __init__(self) -> None:
        self.output = []  # type: List[str]

    def log(
        self,
        msg: Union[str, List[str]] = "",
        indent: int = 0,
        separator: bool = False,
    ) -> None:
        self.output.extend(Logger._pack_as_list(msg))

    def write(
        self,
        msg: Union[str, List[str]] = "",
        indent: int = 0,
        separator: bool = False,
    ) -> None:
        messages = Logger._pack_as_list(msg)
        for line in messages:
            print(line)

    def error(self) -> None:
        for line in self.output:
            print(line)


class CmdError(Exception):
    def __init__(
        self,
        cmd_line: Optional[List[str]],
        output_str: str,
        returncode: Optional[int] = None,
    ) -> None:
        self.returncode = returncode
        self.output_lines = []
        if cmd_line:
            self.output_lines += [
                "Command '{}' failed:".format(" ".join(cmd_line))
            ]
        self.output_lines += output_str.splitlines()


class OutputGenerator:
    """Represent lines of output as strings.

    """

    def __init__(self) -> None:
        self.lines = []  # type: List[str]
        self.index = 0

    def append(self, line: str) -> None:
        self.lines.append(line)

    def __iter__(self) -> Iterator[str]:
        for line in self.lines:
            yield line

    def first_line(self) -> str:
        if len(self.lines) >= 1:
            return self.lines[0]
        else:
            return ""


def run_cmd(
    cmd_line: List[str],
    env: Optional[Dict[str, str]] = None,
    logger: Optional[Logger] = None,
    verbose: bool = False,
    cwd: Optional[str] = None,
    raise_exception: bool = True,
) -> OutputGenerator:
    """Run a shell command.

    Parameters:
        cmd_line:
            The command [cmd, arg1, …] to run.
        env:
            A dict for setting environment variables for the process.
            If set, defines the complete environment.
            If not set, the environment is inherited from os.environ.
        logger:
            A Logger object that logs all output (interspersed stdout
            and stderr) from the shell command.
            The default is to use a NullLogger that will only print output
            if an error occurs.
        verbose:
            If True, use a StdoutLogger as default logger.
        cwd:
            Directory in which to execute the command. If None, use '.'.
        raise_exception:
            When the system command fails: If raise_exception=True, raise
            a CalledProcessError, if False, exit with status 1.
    Returns:
        A string generator representing the lines ouf output.
    Raises:
        CalledProcessError if the command failed and raise_exception is
        True.

    """
    if cwd is None:
        cwd = "."
    if logger:
        logger_ = logger
    else:
        if verbose:
            logger_ = StdoutLogger()
        else:
            logger_ = NullLogger()
    logger_.log("{}".format(_format_cmd_line(cmd_line)), separator=True)
    output_generator = OutputGenerator()
    try:
        with subprocess.Popen(
            # Use stdbuff to unbuffer stdout, in order to get
            # immediate output and correct interspersing of stdout and
            # stderr. Note that this will still not work for arbitrary
            # commands in cmd_line.
            # In particular, for a Python script that mixes print
            # statements and output from subprocess, when run with
            # Python 2.7, stdbuf works as expected, while the script
            # running with Python 3.8 still buffers the output (and
            # git_adapter accordingly gets the output in wrong order).
            ["stdbuf", "-o0"] + cmd_line,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=cwd,
            env=env,
            universal_newlines=True,
        ) as process:
            output = process.stdout
            assert output is not None  # appease mypy
            for raw_line in output:
                line = raw_line.rstrip()
                logger_.log(line, indent=2)
                output_generator.append(line)
            status = process.wait()
            if status != 0:
                if raise_exception:
                    raise subprocess.CalledProcessError(
                        status,
                        cmd_line,
                        output="\n".join(list(output_generator)),
                    )
                else:
                    logger_.error()
                    logger_.write(
                        "An error occurred when running the command"
                    )
                    logger_.write("  " + " ".join(cmd_line))
                    logger_.write("Aborting.")
                    logger_.write(traceback.format_exc().split("\n"))
                    sys.exit(1)
            return output_generator
    except OSError as e:
        raise subprocess.CalledProcessError(e.errno, cmd_line, str(e))


def _format_cmd_line(cmd_line: List[str]) -> str:
    """Format a shell command line.

    Try to use quotation marks where needed.
    No attempt is made to handle cases where both sorts of quotation marks
    would be needed in one argument.

    """
    line = []
    for part in cmd_line:
        if " " not in part:
            line.append(part)
            continue
        if "'" not in part:
            line.append("'{}'".format(part))
            continue
        line.append('"{}"'.format(part))
    return " ".join(line)


# Local Variables:
#   compile-command: (concat "mypy --ignore-missing-imports --strict \
#     " (file-name-nondirectory buffer-file-name))
# End:
