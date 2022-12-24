#!python3
from controllers.options_controller import OptionsController, Options
from views.app_view import AppView

from PyPDF2 import PdfMerger

if __name__ == '__main__':
    app_view: AppView = AppView(options=OptionsController().options)
    app_view.mainloop()

