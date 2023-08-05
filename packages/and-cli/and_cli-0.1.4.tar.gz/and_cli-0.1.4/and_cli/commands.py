import click
import os
import subprocess
import time
import glob


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

    run_start = time.time()
    runner = subprocess.run(
        ["./out"], stdin=in_file, check=False, stdout=subprocess.PIPE, text=True
    )

    if runner.returncode != 0:
        click.echo(click.style("Something went wrong while running", fg="red"))
        return
    run_end = time.time()

    click.echo(
        click.style(
            f"Ran successfully in {run_end - run_start:.4f} seconds", fg="green"
        )
    )
    in_file.seek(0, 0)
    click.echo("=" * 35 + "INPUT" + "=" * 36)
    click.echo(in_file.read())
    click.echo("=" * 35 + "OUTPUT" + "=" * 36)
    click.echo(runner.stdout.strip())
    click.echo("=" * 76)

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