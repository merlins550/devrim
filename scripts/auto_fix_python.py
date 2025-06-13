import subprocess
import sys


COMMANDS = [
    [
        "autoflake",
        "--in-place",
        "--remove-unused-variables",
        "--remove-all-unused-imports",
        "-r",
        ".",
    ],
    ["isort", "."],
    ["black", "."],
]


def run(cmd):
    """Run a command and stream output."""

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.returncode != 0 and result.stderr:
        print(result.stderr, file=sys.stderr)


def main():
    for cmd in COMMANDS:
        run(cmd)


if __name__ == '__main__':
    main()
