import logging
from pathlib import Path
from typing import Callable

from attrs import define
from rich import print
from rich.prompt import Confirm, IntPrompt, Prompt

from modules.archiving import ARCH_FOLDER, SUPPORTED_ARCH_FORMATS, archive_data
from modules.constants import DEF_ARCH_PART_SIZE, MAX_GEN_ROWS, MIN_GEN_ROWS
from modules.create_table import FILE_FOLDER, SUPPORTED_TABLE_FILE_FORMATS, save_table
from modules.data_gen import DataGenerator

logging.basicConfig(
    format='%(levelname)s - %(module)s - %(asctime)s - %(message)s',
    level=logging.INFO,
    filename='logs/app.log',
)


@define
class CliInterface:
    """Command line interface class.

    Using typer and rich.
    """

    @staticmethod
    def data_saver(data: list[list[str | int]]) -> str:
        """Save data to table file and return it's path."""

        logging.info('Saving generated data to table file')
        file_name: str = Prompt.ask('Type file name for table')
        file_format: str = Prompt.ask(
            'Type table file format', choices=SUPPORTED_TABLE_FILE_FORMATS, default=SUPPORTED_TABLE_FILE_FORMATS[0]
        )
        logging.info(f'Starting file creation at {FILE_FOLDER}{file_name}.{file_format}')
        return save_table(file_name, file_format, data)

    def data_generation(self) -> str:
        """Generate random data."""

        logging.info('Generating data for table file')
        while True:
            rows: int = IntPrompt.ask(
                f'Enter a number of rows between [b]{MIN_GEN_ROWS:,}[/b] and'
                f' [b]{MAX_GEN_ROWS:,}[/b]',
                default=MAX_GEN_ROWS // 2,
            )
            if MIN_GEN_ROWS <= rows <= MAX_GEN_ROWS:
                break
            print(f'[prompt.invalid]Number must be between {MIN_GEN_ROWS:,} and {MAX_GEN_ROWS:,}')
        logging.info('Starting generation process')
        data: list[list[str | int]] = DataGenerator(rows).generate_table()
        return self.data_saver(data)

    @staticmethod
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

    @staticmethod
    def data_typing() -> str:
        """Create TXT file with data from user and return its path."""

        logging.info('Asking user to provide data in terminal')
        file_name: str = Prompt.ask('TXT file name')
        with open(f'user_data/{file_name}.txt', mode='w') as txt_file:
            data: str = Prompt.ask('TXT file content')
            txt_file.write(data)
        print(f'Saved prompt to TXT file: user_data/{file_name}.txt')
        logging.info(f'Writing user data to TXT file: user_data/{file_name}.txt')
        return f'user_data/{file_name}.txt'

    @staticmethod
    def data_archiver(file_path: str) -> None:
        """Archive user file."""

        logging.info('Archiving provided data')
        arch_name: str = Prompt.ask('Archive name')
        choices = list(SUPPORTED_ARCH_FORMATS)
        arch_format: str = Prompt.ask(
            'Choose archive format',
            choices=choices,
            default=choices[0],
        )
        must_split: bool = Confirm.ask(
            'Do you want to split archive file?', default=False
        )
        if must_split:
            logging.info(f'Starting archiving data into parted {arch_format} archive')
            max_file_size: int = IntPrompt.ask(
                'Specify max file size in bytes', default=DEF_ARCH_PART_SIZE
            )
            archive_data(arch_name, arch_format, file_path, must_split, max_file_size)
            logging.info(f'Archive with parts created: {ARCH_FOLDER}{arch_name}.{arch_format}')
        else:
            logging.info(f'Starting archiving data into {arch_format} archive')
            archive_data(arch_name, arch_format, file_path)
            logging.info(f'Archive created: {ARCH_FOLDER}{arch_name}.{arch_format}')

    def data_choice(self) -> str:
        """Resolve data file and return path to file."""

        logging.info('Asking user for data to archive')
        actions: dict[str, Callable] = {
            'generate data': self.data_generation,
            'specify path': self.data_path,
            'type text': self.data_typing,
        }
        choices = list(actions)
        action: str = Prompt.ask(
            'What data do you want to archive?',
            choices=choices,
            default='generate data',
        )
        file_path: str = actions[action]()
        return file_path

    def main_flow(self) -> None:
        """Main method."""

        logging.info('Starting app')
        file_path: str = self.data_choice()
        self.data_archiver(file_path)
        logging.info('Finished')
