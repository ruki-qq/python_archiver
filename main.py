import typer

from modules.rich_cli import CliInterface

if __name__ == '__main__':
    interface = CliInterface()
    typer.run(interface.main_flow)
