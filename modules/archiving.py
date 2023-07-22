import zipfile
from io import BytesIO
from typing import Callable

import py7zr
from attr._make import Attribute
from attrs import define, field
from rich import print

SUPPORTED_ARCH_FORMATS: list[str] = ['7z', 'zip']
ARCH_FOLDER: str = 'archived_data/'


@define
class Archiver:
    """Class to create archive files.

    Available archive formats:
     7z, zip

    Parameters:
     ----------
     archive_format: str
         Archive file format
    """

    archive_format: str = field()

    @archive_format.validator
    def check_if_supported(self, attribute: Attribute, value: str) -> None:
        if value not in SUPPORTED_ARCH_FORMATS:
            raise ValueError(
                'You must provide one of these formats:'
                f' {SUPPORTED_ARCH_FORMATS}'
            )

    def archive_file_zip(
        self, arch_name: str | BytesIO, file_path: str
    ) -> None:
        """Create ZIP archive."""

        name: str | BytesIO = (
            arch_name
            if type(arch_name) == BytesIO
            else f'{ARCH_FOLDER}{arch_name}.{self.archive_format}'
        )
        with zipfile.ZipFile(name, 'w') as archive:
            archive.write(file_path)

    def archive_file_7z(
        self, arch_name: str | BytesIO, file_path: str
    ) -> None:
        """Create 7Z archive."""

        name = (
            arch_name
            if type(arch_name) == BytesIO
            else f'{ARCH_FOLDER}{arch_name}.{self.archive_format}'
        )
        with py7zr.SevenZipFile(name, 'w') as archive:
            archive.write(file_path)

    def archive_file_split(
        self,
        arch_name: str,
        arch_method: Callable,
        file_path: str,
        chunk_size: int,
    ) -> None:
        """Create splitted archive."""

        buf: BytesIO = BytesIO()

        arch_method(buf, file_path)

        buf.seek(0)
        num_chunks: int = (
            buf.getbuffer().nbytes + chunk_size - 1
        ) // chunk_size

        bufs_list: list[BytesIO] = []

        for chunk_idx in range(num_chunks):
            start: int = chunk_idx * chunk_size
            end: int = start + chunk_size
            chunk_data: bytes = buf.getvalue()[start:end]
            bufs_list.append(BytesIO(chunk_data))

        with BytesIO() as res_arch_buf:
            if self.archive_format == 'zip':
                with zipfile.ZipFile(res_arch_buf, 'w') as out_zip:
                    for idx, chunk in enumerate(bufs_list):
                        out_zip.writestr(
                            f'{arch_name}.{self.archive_format}.{idx+1:03d}',
                            chunk.getvalue(),
                        )
                with open(
                    f'{ARCH_FOLDER}{arch_name}.{self.archive_format}', 'wb'
                ) as output_file:
                    output_file.write(res_arch_buf.getvalue())
            elif self.archive_format == '7z':
                with py7zr.SevenZipFile(res_arch_buf, 'w') as out_7z:
                    for idx, chunk in enumerate(bufs_list):
                        out_7z.writestr(
                            chunk.getvalue(),
                            f'{arch_name}.{self.archive_format}.{idx+1:03d}',
                        )
                with open(
                    f'{ARCH_FOLDER}{arch_name}.{self.archive_format}', 'wb'
                ) as output_file:
                    output_file.write(res_arch_buf.getvalue())

    def archive_data(
        self,
        arch_name: str,
        file_path: str,
        must_split: bool = False,
        max_file_size: int = 0,
    ) -> None:
        """Create archive file with provided format and data."""

        arch_formats: dict[str, Callable] = {
            'zip': self.archive_file_zip,
            '7z': self.archive_file_7z,
        }
        if must_split:
            print(f'Creating parted {self.archive_format} archive')
            self.archive_file_split(
                arch_name,
                arch_formats[self.archive_format],
                file_path,
                max_file_size,
            )
            print(
                'Archive with parts created:'
                f' {ARCH_FOLDER}{arch_name}.{self.archive_format}'
            )
        else:
            print(f'Creating {self.archive_format} archive')
            arch_formats[self.archive_format](arch_name, file_path)
            print(
                'Archive created:'
                f' {ARCH_FOLDER}{arch_name}.{self.archive_format}'
            )
