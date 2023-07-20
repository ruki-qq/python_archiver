import csv

import xlsxwriter
from attrs import define


@define
class TableData:
    """Class to retrieve data and set it in table format."""

    filename: str
    data: list[list] | str

    def write_data_csv(self) -> None:
        """Writes data to csv file and prints status."""

        with open(f'{self.filename}.csv', mode='w') as csv_file:
            csv_writer = csv.writer(
                csv_file,
                delimiter=',',
                quotechar='"',
                quoting=csv.QUOTE_NONNUMERIC,
            )
            for row in self.data:
                csv_writer.writerow(row)

    def write_data_xlxs(self) -> None:
        """Writes data to xlsx file and prints status."""

        workbook = xlsxwriter.Workbook(f'{self.filename}.xlsx')
        worksheet = workbook.add_worksheet()

        row = 0

        for line in self.data:
            worksheet.write_row(row, 0, line)
            row += 1

        workbook.close()
