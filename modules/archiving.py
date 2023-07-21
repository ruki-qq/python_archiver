import zipfile

import py7zr
from attrs import define, field
from split_file_writer import SplitFileWriter

SUPPORTED_FORMATS: list[str] = ['7z', 'zip']


@define
class Archiver:
    """Class to create archive files.

    Available archive formats:
     7z, zip

    Parameters:
     ----------
     archive_type: str
         Archive file format
    """

    archive_type: str = field()

    @archive_type.validator
    def check_if_supported(self, attribute, value: str) -> None:
        if value not in SUPPORTED_FORMATS:
            raise ValueError(
                f'You must provide one of these formats: {SUPPORTED_FORMATS}'
            )
            # print(attribute)
            # value = input(
            #     'Please, provide one of these formats:'
            #     f' {self.SUPPORTED_FORMATS}'
            # )

    def archive_file_zip(
        self, arch_name: str | SplitFileWriter, file_path: str
    ) -> None:
        """Create ZIP archive."""

        name = (
            arch_name
            if type(arch_name) == SplitFileWriter
            else f'archived_data/{arch_name}.zip'
        )
        with zipfile.ZipFile(name, mode='w') as archive:
            archive.write(file_path)

    def archive_file_7z(
        self, arch_name: str | SplitFileWriter, file_path: str
    ) -> None:
        """Create 7Z archive."""

        name = (
            arch_name
            if type(arch_name) == SplitFileWriter
            else f'archived_data/{arch_name}.7z'
        )
        with py7zr.SevenZipFile(name, 'w') as archive:
            archive.write(file_path)

    def archive_file_split(
        self, arch_name: str, file_path: str, max_file_size: int
    ) -> None:
        """Create splitted archive."""

        arch_types: dict = {
            'zip': self.archive_file_zip,
            '7z': self.archive_file_7z,
        }
        with SplitFileWriter(
            f'archived_data/{arch_name}.zip.', max_file_size
        ) as sfw:
            arch_types[self.archive_type](sfw, file_path)

    def archive_data(self, arch_name: str, file_path: str) -> None:
        """Create archive file with provided format and data."""

        arch_types: dict = {
            'zip': self.archive_file_zip,
            '7z': self.archive_file_7z,
        }
        arch_types[self.archive_type](file_path)
