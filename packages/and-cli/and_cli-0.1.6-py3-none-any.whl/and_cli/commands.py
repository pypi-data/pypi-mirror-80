import click
import os
import subprocess
import time
import glob
from and_cli import NUM_COLS
from math import floor, ceil


@click.group()
def _and():
    pass


@_and.command()
@click.option(
    "--file",
    "-f",
    "filename",
    default="*.cpp",
    help="Name of C++ file to compile and run",
)
@click.option(
    "--input", "-i", "in_filename", default="in.txt", help="Input piped into program"
)
def run(filename, in_filename):
    """Compiles and runs a C++ program"""
    try:
        _compile(filename)
    except RuntimeError:
        click.echo(click.style("Something went wrong in compilation", fg="red"))
        return

    in_file = open(in_filename, "r") if in_filename in os.listdir() else None

    _print_title(f"[ Input | {in_filename if in_file else 'stdin'} ]")
    if in_file:
        click.echo(in_file.read())
        in_file.seek(0, 0)

    run_start = time.time()
    runner = subprocess.run(
        ["./out"], stdin=in_file, check=False, stdout=subprocess.PIPE, text=True
    )

    if runner.returncode != 0:
        click.echo(click.style("Something went wrong while running", fg="red"))
        return
    run_end = time.time()

    _print_title("[ Output | stdout ]")
    click.echo(runner.stdout.strip())

    _print_title(f"[ Time | {run_end - run_start:.4f}s ]")

    os.remove("out")

    if in_file:
        in_file.close()


@_and.command()
@click.option(
    "--file",
    "-f",
    "filename",
    default="*.cpp",
    help="Name of C++ file to compile and run",
)
def comp(filename):
    """Compiles a C++ program"""
    try:
        _compile(filename)
    except RuntimeError:
        click.echo(click.style("Something went wrong in compilation", fg="red"))
        return


def _compile(filename):
    compile_start = time.time()
    compiler = subprocess.run(["g++", *glob.glob(filename), "-o", "out"], check=False)
    if compiler.returncode != 0:
        raise RuntimeError

    compile_end = time.time()
    click.echo(
        click.style(
            f"Compiled successfully in {compile_end - compile_start:.4f} seconds",
            fg="green",
        )
    )


def _print_title(msg):
    """Prints a message surrounded by '-' to a width of NUM_COLS

    Args:
        msg (str): The message to format and print
    """
    click.echo(
        "-" * floor((NUM_COLS - len(msg)) / 2)
        + msg
        + "-" * ceil((NUM_COLS - len(msg)) / 2)
    )