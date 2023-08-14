import _csv
import csv
from typing import Callable

from attr._make import Attribute
from attrs import define, field
from progress.bar import IncrementalBar
from rich import print
from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet

SUPPORTED_TABLE_FILE_FORMATS: list[str] = ['csv', 'xlsx']
FILE_FOLDER: str = 'generated_files/'


@define
class TableData:
    """Class to retrieve data and set it in table format.

    Available table file formats can be looked up in
      SUPPORTED_TABLE_FILE_FORMATS constant.

    Parameters:
     ----------
     file_name: str
         Name to create table file
     file_format: str
         Format of table file
     data: list[list[str | int]]
         Content of table file
    """

    file_name: str
    file_format: str = field()
    data: list[list[str | int]]

    @file_format.validator
    def check_if_supported(self, attribute: Attribute, value: str) -> None:
        if value not in SUPPORTED_TABLE_FILE_FORMATS:
            raise ValueError(
                'You must provide one of these formats:'
                f' {SUPPORTED_TABLE_FILE_FORMATS}'
            )

    def write_data(self, **kwargs) -> str:
        """Write data to file and return path to it."""

        raise NotImplementedError('Method is not implemented.')


@define
class TableCSV(TableData):
    """Class to write data to CSV file."""

    def write_data(self, delimiter: str = ',', quotechar: str = '"') -> str:
        """Write data to csv file and return path to it."""

        with open(f'{FILE_FOLDER}{self.file_name}.csv', mode='w') as csv_file:
            csv_writer: _csv._writer = csv.writer(
                csv_file,
                delimiter=delimiter,
                quotechar=quotechar,
                quoting=csv.QUOTE_NONNUMERIC,
            )
            with IncrementalBar(
                    'Creating file', max=len(self.data), suffix='%(elapsed)d s.'
            ) as bar:
                for row in self.data:
                    csv_writer.writerow(row)
                    bar.next()

        print(f'File created: {FILE_FOLDER}{self.file_name}.csv')
        return f'{FILE_FOLDER}{self.file_name}.csv'


@define
class TableXLSX(TableData):
    """Class to write data to XLSX file."""

    def write_data(self) -> str:
        """Write data to xlsx file and return path to it."""

        max_sheet_rows: int = 1_048_576
        workbook: Workbook = Workbook(f'{FILE_FOLDER}{self.file_name}.xlsx')
        num_sheets: int = (
                                  len(self.data) + max_sheet_rows - 1
                          ) // max_sheet_rows
        for sheet_idx in range(num_sheets):
            worksheet: Worksheet = workbook.add_worksheet()
            row: int = 0
            start: int = sheet_idx * max_sheet_rows
            end: int = start + max_sheet_rows
            with IncrementalBar(
                    f'Creating file (sheet #{sheet_idx + 1})',
                    max=len(self.data[start:end]),
                    suffix='%(elapsed)d s.',
            ) as bar:
                for line in self.data[start:end]:
                    worksheet.write_row(row, 0, line)
                    row += 1
                    bar.next()
        workbook.close()
        print(f'File created: {FILE_FOLDER}{self.file_name}.xlsx')
        return f'{FILE_FOLDER}{self.file_name}.xlsx'


def save_table(file_name: str, file_format: str, data: list[list[str | int]]) -> str:
    """Save table file with provided format and data."""
    arch_types: dict[str, Callable] = {
        'csv': TableCSV,
        'xlsx': TableXLSX,
    }
    return arch_types[file_format](file_name, file_format, data).write_data()
