import csv

import _csv
from attrs import define
from progress.bar import IncrementalBar
from rich import print
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet


@define
class TableData:
    """Class to retrieve data and set it in table format.

    Available table file formats:
     csv, xlsx

    Parameters:
     ----------
     file_name: str
         Name to create table file
     data: list[list]
         Content of table file
    """

    file_name: str
    data: list[list]

    def write_data_csv(self) -> str:
        """Write data to csv file."""

        with open(f'{self.file_name}.csv', mode='w') as csv_file:
            csv_writer: _csv._writer = csv.writer(
                csv_file,
                delimiter=',',
                quotechar='"',
                quoting=csv.QUOTE_NONNUMERIC,
            )
            with IncrementalBar(
                'Creating file', max=len(self.data), suffix='%(elapsed)d s.'
            ) as bar:
                for row in self.data:
                    csv_writer.writerow(row)
                    bar.next()

        print(f'File created: {self.file_name}.csv')
        return f'{self.file_name}.csv'

    def write_data_xlsx(self) -> str:
        """Write data to xlsx file."""

        workbook: Workbook = Workbook(f'{self.file_name}.xlsx')
        worksheet: Worksheet = workbook.add_worksheet()
        row: int = 0
        with IncrementalBar(
            'Creating file', max=len(self.data), suffix='%(elapsed)d s.'
        ) as bar:
            if len(self.data) > 1_048_576:
                for line in self.data[:1_048_576]:
                    worksheet.write_row(row, 0, line)
                    row += 1
                    bar.next()
                worksheet = workbook.add_worksheet()
                row = 0
                for line in self.data[1_048_576:]:
                    worksheet.write_row(row, 0, line)
                    row += 1
                    bar.next()
            else:
                for line in self.data:
                    worksheet.write_row(row, 0, line)
                    row += 1
                    bar.next()
        workbook.close()

        print(f'File created: {self.file_name}.xlsx')
        return f'{self.file_name}.xlsx'
