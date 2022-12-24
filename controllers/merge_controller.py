from pathlib import Path
from PyPDF2 import PdfWriter

from controllers.options_controller import Options
from views.message_box import MessageBox


class NoFileNameException(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message


class TooFewFilesException(Exception):
    def __init__(self, message: str, file_list):
        super().__init__()
        self.message = message
        self.file_list = file_list


class MergeController:
    def __init__(self, options: Options):
        self.options: Options = options

    def merge(self, pdf_files: [str], file_name: str, force_overwrite: bool = False):
        if len(pdf_files) < 2:
            raise TooFewFilesException()

        if not file_name:
            raise NoFileNameException()

        save_file: Path = self.options.path / file_name
        if save_file.suffix.lower() != '.pdf':
            save_file = save_file.with_suffix(save_file.suffix + '.pdf')

        self.options.message(f'Filename: {save_file}')
        if not force_overwrite and save_file.exists():
            raise FileExistsError(f'Bestand {save_file} bestaat')

        pdf_file: Path
        merger: PdfWriter = PdfWriter()
        for pdf_file in [Path(f) for f in pdf_files]:
            self.options.message(f'Adding {pdf_file} to merge list')
            if pdf_file.is_file():
                merger.append(pdf_file)
            else:
                raise FileNotFoundError(f'PDF bestand {pdf_file} bestaat niet')
        merger.write(save_file)
        merger.close()

        MessageBox.show_message(message=f'Bestanden samengevoegd in {save_file}.',
                                title='Succes!')
