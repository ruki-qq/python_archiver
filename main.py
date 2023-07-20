import typer
from modules.data_gen import DataGenerator
from modules.create_table import TableData
from modules.archiving import Archiver


def data_resolver() -> list[list] | str:
    should_generate: bool = (
        True if input('Do you want to generate data? (y/n)') == 'y' else False
    )
    if should_generate:
        data_gen = DataGenerator()
        rows = int(
            input(
                'How many rows do you want to generate? (in range(500000,'
                ' 2000000))'
            )
        )
        return data_gen.generate_table(rows)
    return input('Type text')


def data_saver(data: list[list] | str) -> None:
    if type(data) == str:
        pass
    else:
        file_name: str = input('Type file name for table: ')
        table = TableData(file_name, data)
        file_format: str = input('Type table file format(csv/xlxs): ')
        if file_format == 'csv':
            table.write_data_csv()
        else:
            table.write_data_xlxs()


def data_archiver(file_path: str):
    arch_name: str = input('Archive name: ')
    arch_type: str = input('Which archive type? (zip, 7z)')
    arch: Archiver = Archiver(arch_name, arch_type)
    arch.archive_data(file_path)


def main():
    data = data_resolver()
    data_saver(data)
    data_archiver('file3.csv')


if __name__ == '__main__':
    main()
