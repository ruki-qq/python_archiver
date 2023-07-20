import csv

import xlsxwriter
from attrs import define


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
         Content of table file being created
    """

    file_name: str
    data: list[list]

    def write_data_csv(self) -> None:
        """Write data to csv file."""

        with open(f'{self.file_name}.csv', mode='w') as csv_file:
            csv_writer = csv.writer(
                csv_file,
                delimiter=',',
                quotechar='"',
                quoting=csv.QUOTE_NONNUMERIC,
            )
            for row in self.data:
                csv_writer.writerow(row)

    def write_data_xlxs(self) -> None:
        """Write data to xlsx file."""

        workbook = xlsxwriter.Workbook(f'{self.file_name}.xlsx')
        worksheet = workbook.add_worksheet()

        row = 0
        for line in self.data:
            worksheet.write_row(row, 0, line)
            row += 1

        workbook.close()
