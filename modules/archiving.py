from io import BytesIO
from typing import Callable
from zipfile import ZipFile

from attr._make import Attribute
from attrs import define, field
from py7zr import SevenZipFile

SUPPORTED_ARCH_FORMATS: dict[str] = {'7z': SevenZipFile, 'zip': ZipFile}
ARCH_FOLDER: str = 'archived_data/'


@define
class Archiver:
    """Class to create archive files.

    Available table file formats can be looked up in
      SUPPORTED_ARCH_FORMATS constant.

    Parameters:
     ----------
     archive_format: str
         Archive file format
    """

    arch_name: str
    archive_format: str = field()
    file_path: str

    @archive_format.validator
    def check_if_supported(self, attribute: Attribute, value: str) -> None:
        if value not in SUPPORTED_ARCH_FORMATS:
            raise ValueError(
                'You must provide one of these formats:'
                f' {SUPPORTED_ARCH_FORMATS}'
            )

    def archive_file(self, buf_name: BytesIO = None) -> None:
        """Create archive file."""

        arch_file: Callable = SUPPORTED_ARCH_FORMATS[self.archive_format]

        name: str | BytesIO = (
            buf_name
            if buf_name
            else f'{ARCH_FOLDER}{self.arch_name}.{self.archive_format}'
        )
        with arch_file(name, 'w') as archive:
            archive.write(self.file_path)

    def archive_file_split(
            self,
            chunk_size: int,
    ) -> None:
        """Create split archive."""

        buf: BytesIO = BytesIO()

        self.archive_file(buf)

        buf.seek(0)
        num_chunks: int = (buf.getbuffer().nbytes + chunk_size - 1) // chunk_size

        bufs_list: list[BytesIO] = []

        for chunk_idx in range(num_chunks):
            start: int = chunk_idx * chunk_size
            end: int = start + chunk_size
            chunk_data: bytes = buf.getvalue()[start:end]
            bufs_list.append(BytesIO(chunk_data))

        self.write_res_arch(bufs_list)

    def write_res_arch(self, bufs_list: list[BytesIO]):
        """Creates an archive with split archive in it."""

        raise NotImplementedError('Method is not implemented.')


@define
class ArchiverZIP(Archiver):
    """Class to create ZIP archives."""

    def write_res_arch(self, bufs_list: list[BytesIO]) -> None:
        """Create ZIP archive with parted archive in it."""

        arch_file: Callable = SUPPORTED_ARCH_FORMATS[self.archive_format]

        with BytesIO() as res_arch_buf:
            with arch_file(res_arch_buf, 'w') as out_zip:
                for idx, chunk in enumerate(bufs_list):
                    out_zip.writestr(
                        f'{self.arch_name}.{self.archive_format}.{idx + 1:03d}',
                        chunk.getvalue(),
                    )
            with open(
                    f'{ARCH_FOLDER}{self.arch_name}.{self.archive_format}', 'wb'
            ) as output_file:
                output_file.write(res_arch_buf.getvalue())


@define
class Archiver7Z(Archiver):
    """Class to create 7Z archives."""

    def write_res_arch(self, bufs_list: list[BytesIO]) -> None:
        """Create 7Z archive with parted archive in it."""

        arch_file: Callable = SUPPORTED_ARCH_FORMATS[self.archive_format]

        with BytesIO() as res_arch_buf:
            with arch_file(res_arch_buf, 'w') as out_7z:
                for idx, chunk in enumerate(bufs_list):
                    out_7z.writestr(
                        chunk.getvalue(),
                        f'{self.arch_name}.{self.archive_format}.{idx + 1:03d}',
                    )
            with open(
                    f'{ARCH_FOLDER}{self.arch_name}.{self.archive_format}', 'wb'
            ) as output_file:
                output_file.write(res_arch_buf.getvalue())


def archive_data(
        arch_name: str,
        arch_format: str,
        file_path: str,
        must_split: bool = False,
        max_file_size: int = 0,
) -> None:
    """Create archive file with provided format and data."""

    arch_formats: dict[str, Callable] = {
        'zip': ArchiverZIP,
        '7z': Archiver7Z,
    }
    arch: Archiver = arch_formats[arch_format](arch_name, arch_format, file_path)
    if must_split:
        print(f'Creating parted {arch_format} archive')
        arch.archive_file_split(max_file_size)
        print(
            'Archive with parts created:'
            f' {ARCH_FOLDER}{arch_name}.{arch_format}'
        )
    else:
        print(f'Creating {arch_format} archive')
        arch.archive_file()
        print(
            'Archive created:'
            f' {ARCH_FOLDER}{arch_name}.{arch_format}'
        )
