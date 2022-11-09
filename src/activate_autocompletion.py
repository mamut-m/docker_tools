#!/usr/bin/env python3

import subprocess
from pathlib import Path
from typing import List, Tuple


def call(cmd_str: str) -> str:
    return subprocess.check_output(cmd_str, shell=True).decode("utf-8")


def call_script(shell_commands: List[str], level=1):
    outputs: List[Tuple[str, str]] = []
    for line_idx, line in enumerate(shell_commands):
        if line.strip() == "":
            continue
        try:
            print(f"calling {line!r} {'>'*5*level}")
            result = call(line)
            outputs.append((line, result))
            print(result)
        except subprocess.CalledProcessError as called_process_error:
            print(
                f"could not call line: {line_idx} in list of commands:\n{called_process_error}"
            )
            raise called_process_error
    return outputs


def comment_out_lines_in_file(file_path):
    file_path_p = Path(file_path)
    assert file_path_p.is_file()
    try:
        lines = file_path_p.read_text(encoding="utf8").splitlines()
        commented_lines = "\n# activate_autocompletion removed # ".join([""] + lines)
        file_path_p.write_text(commented_lines, encoding="utf8")
    except PermissionError as permission_error:
        print(
            f"ERROR: you dont have permission for {file_path}. maybe call with sudo?\n {permission_error}"
        )


ACTIVATE_AUTO_COMPLETE_STR = """
if ! shopt -oq posix; then
    if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
    elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
    fi
fi
"""


def add_autocomplete_to_bashrc():
    with Path("~/.bashrc").expanduser().open(mode="a", encoding="utf-8") as file:
        file.write(ACTIVATE_AUTO_COMPLETE_STR)


def activate_autocompletion():
    SCRIPT = """
    sudo apt-get update
    sudo apt-get install bash-completion 
    """
    commands = SCRIPT.splitlines()
    call_script(commands)
    comment_out_lines_in_file("/etc/apt/apt.conf.d/docker-clean")
    add_autocomplete_to_bashrc()


# enable bash completion in interactive shells
# if ! shopt -oq posix; then
#  if [ -f /usr/share/bash-completion/bash_completion ]; then
#    . /usr/share/bash-completion/bash_completion
#  elif [ -f /etc/bash_completion ]; then
#    . /etc/bash_completion
#  fi
# fi

if __name__ == "__main__":
    activate_autocompletion()
