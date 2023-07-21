from pathlib import Path

import typer
from rich import print
from rich.prompt import Confirm, IntPrompt, Prompt

from modules.archiving import Archiver, SUPPORTED_FORMATS
from modules.create_table import TableData
from modules.data_gen import DataGenerator

app = typer.Typer()


def data_generation() -> str:
    while True:
        rows: int = IntPrompt.ask(
            (
                'Enter a number of rows between [b]500.000[/b] and'
                ' [b]1.000.000[/b]'
            ),
            default=500_000,
        )
        if rows >= 500_000 and rows <= 2_000_000:
            break
        print('[prompt.invalid]Number must be between 500.000 and 2.000.000')

    data_gen: DataGenerator = DataGenerator(rows)
    data: list[list] = data_gen.generate_table()
    return data_saver(data)


def data_saver(data: list[list]) -> str:
    file_name: str = Prompt.ask('Type file name for table')
    table = TableData(file_name, data)
    file_format: str = Prompt.ask(
        'Type table file format', choices=['csv', 'xlsx']
    )
    if file_format == 'csv':
        return table.write_data_csv()
    return table.write_data_xlsx()


def data_path() -> str:
    while True:
        path: str = Prompt.ask('Path to your data')
        if Path(path).is_file():
            break
        print('[prompt.invalid]File does not exist, provide correct path')
    return path


def data_typing() -> str:
    file_name: str = Prompt.ask('TXT file name')
    with open(f'{file_name}.txt', mode='w') as txt_file:
        data: str = Prompt.ask('TXT file content')
        txt_file.write(data)
    return f'{file_name}.txt'


def data_resolver() -> str:
    actions: dict = {
        'generate data': data_generation,
        'specify path': data_path,
        'type text': data_typing,
    }
    action: str = Prompt.ask(
        'What data do you want to archive?',
        choices=actions,
        default='generate data',
    )
    file_path: str = actions[action]()
    return file_path


def data_archiver(file_path: str):
    arch_name: str = Prompt.ask('Archive name')
    arch_type: str = Prompt.ask(
        'Choose archive format', choices=SUPPORTED_FORMATS
    )
    arch: Archiver = Archiver(arch_type)
    arch.archive_data(arch_name, file_path)


def main():
    file_path: str = data_resolver()
    data_archiver(file_path)


@app.command()
def run():
    main()


@app.command()
def generate_list(rows: int):
    data_gen = DataGenerator(rows)
    data: list[list] = data_gen.generate_table()
    file_name: str = Prompt.ask('Type file name for table')
    table = TableData(file_name, data)
    file_format: str = Prompt.ask(
        'Type table file format',
        choices=['csv', 'xlsx'],
    )
    if file_format == 'csv':
        return table.write_data_csv()
    return table.write_data_xlsx()


if __name__ == '__main__':
    app()
