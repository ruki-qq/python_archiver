# python_archiver

This project is for archiving data from CLI.
It's currently supports 7z, zip archive formats.

## Usage/Examples

```bash
pip install -r requirements.txt
python main.py
# CLI interface is very informative by itself ;)
```

## Documentation

You can provide a file for archiving with 3 methods:\

1. Generate fake data in range of 500.000 to 2.000.000 rows and create a csv/xlsx file from that.\
2. Specify file path in CLI
3. Create TXT file with provided filename and content from CLI

After providing data you need to choose archive file format and choose if you want to split your archive into parts.\

All generated data, archives and logs will stash in corresponding folders.
