import logging
from pathlib import Path

import typer
from rich import print
from rich.prompt import Confirm, IntPrompt, Prompt

from modules.archiving import ARCH_FOLDER, SUPPORTED_ARCH_FORMATS, Archiver
from modules.create_table import FILE_FOLDER, TableData
from modules.data_gen import DataGenerator

logging.basicConfig(
    format='%(levelname)s - %(module)s - %(asctime)s - %(message)s',
    level=logging.INFO,
    filename='logs/app.log',
)


def data_generation() -> str:
    """Generate random data."""
    logging.info('Generating data for table file')
    while True:
        rows: int = IntPrompt.ask(
            'Enter a number of rows between [b]500.000[/b] and'
            ' [b]2.000.000[/b]',
            default=500_000,
        )
        if rows >= 500_000 and rows <= 2_000_000:
            break
        print('[prompt.invalid]Number must be between 500.000 and 2.000.000')

    data_gen: DataGenerator = DataGenerator(rows)
    logging.info('Starting generation process')
    data: list[list] = data_gen.generate_table()
    return data_saver(data)


def data_saver(data: list[list]) -> str:
    """Save data to table file and return it's path."""
    logging.info('Saving generated data to table file')
    file_name: str = input('Type file name for table: ')
    file_format: str = Prompt.ask(
        'Type table file format', choices=['csv', 'xlsx'], default='csv'
    )
    table = TableData(file_name, file_format, data)
    logging.info(
        f'Starting file creation at {FILE_FOLDER}{file_name}.{file_format}'
    )
    return table.write_data()


def data_path() -> str:
    """Get file path from user and return it."""
    logging.info('Asking user to specify data file path')
    while True:
        path: str = Prompt.ask('Path to your data')
        if Path(path).is_file():
            break
        print('[prompt.invalid]File does not exist, provide correct path')
    logging.info(f'User specified path: {path}')
    return path


def data_typing() -> str:
    """Create TXT file with data from user and return it's path."""
    logging.info('Asking user to provide data in terminal')
    file_name: str = Prompt.ask('TXT file name')
    with open(f'user_data/{file_name}.txt', mode='w') as txt_file:
        data: str = Prompt.ask('TXT file content')
        txt_file.write(data)
    print(f'Saved prompt to TXT file: user_data/{file_name}.txt')
    logging.info(f'Writing user data to TXT file: user_data/{file_name}.txt')
    return f'user_data/{file_name}.txt'


def data_resolver() -> str:
    """Resolve data file and return path to file."""
    logging.info('Asking user for data to archive')
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


def data_archiver(file_path: str) -> None:
    """Archive user file."""
    logging.info('Archiving provided data')
    arch_name: str = Prompt.ask('Archive name')
    arch_type: str = Prompt.ask(
        'Choose archive format',
        choices=SUPPORTED_ARCH_FORMATS,
        default=SUPPORTED_ARCH_FORMATS[0],
    )
    must_split: bool = Confirm.ask(
        'Do you want to split archive file?', default=False
    )
    arch: Archiver = Archiver(arch_type)
    if must_split:
        logging.info(
            f'Starting archiving data into parted {arch_type} archive'
        )
        max_file_size: int = IntPrompt.ask(
            'Specify max file size in bytes', default=1_000_000
        )
        arch.archive_data(arch_name, file_path, must_split, max_file_size)
        logging.info(
            f'Archive created: {ARCH_FOLDER}{arch_name}.{arch_type}[PARTS]'
        )
    else:
        logging.info(f'Starting archiving data into {arch_type} archive')
        arch.archive_data(arch_name, file_path)
        logging.info(f'Archive created: {ARCH_FOLDER}{arch_name}.{arch_type}')


def main():
    """Main function."""
    logging.info('Starting app')
    file_path: str = data_resolver()
    data_archiver(file_path)
    logging.info('Finished')


if __name__ == '__main__':
    typer.run(main)
