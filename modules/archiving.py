import zipfile

import py7zr
from attrs import define, field


@define
class Archiver:
    archive_name: str
    archive_type: str = field()

    @archive_type.validator
    def check(self, attribute, value: str) -> None:
        while value not in ['7z', 'zip']:
            print(attribute)
            value = input('Please, provide one of these formats: zip, 7z')

    def archive_file_zip(self, file_path: str) -> None:
        with zipfile.ZipFile(
            f'archived_data/{self.archive_name}.zip', mode='w'
        ) as archive:
            archive.write(file_path)

    def archive_file_7z(self, file_path: str) -> None:
        with py7zr.SevenZipFile(
            'archived_data/{self.archive_name}.7z', 'w'
        ) as archive:
            archive.write(file_path)

    ARCH_TYPES: dict = {
        'zip': archive_file_zip,
        '7z': archive_file_7z,
    }

    def archive_data(self, file_path: str) -> None:
        self.archive_file_zip(file_path)
