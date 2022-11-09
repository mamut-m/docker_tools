#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
from pathlib import Path


def call(cmd_str: str) -> str:
    return subprocess.check_output(cmd_str, shell=True).decode("utf-8")


def call_script(shell_commands: list[str], level=1):
    outputs: list[tuple[str, str]] = []
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
    lines = file_path_p.read_text().splitlines()
    commented_lines = "\n# activate_autocompletion removed # ".join([""] + lines)
    file_path_p.write_text(commented_lines)


def main():
    script = """
    sudo apt-get update
    sudo apt-get install bash-completion 
    """
    commands = script.splitlines()
    print(commands)
    call_script(commands)


if __name__ == "__main__":
    main()
