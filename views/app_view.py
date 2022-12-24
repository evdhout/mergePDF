import tkinter as tk
import webbrowser
from tkinter import Tk, ttk, filedialog

from models.options import Options
from views.file_list_view import FileListView
from views.message_box import MessageBox
from controllers.merge_controller import MergeController, TooFewFilesException, NoFileNameException


class AppView(Tk):
    def __init__(self, options: Options):
        super().__init__()
        self.options: Options = options
        self.merge_controller: MergeController = MergeController(options=self.options)

        self.title(Options.APPLICATION_NAME)
        self.geometry("800x600")

        style = ttk.Style()
        if options.is_windows():
            style.theme_use('classic')

        # create the menus
        app_menu = tk.Menu(self)
        self.config(menu=app_menu)

        file_menu = tk.Menu(app_menu)
        app_menu.add_cascade(label="Bestand", menu=file_menu)
        file_menu.add_command(label="Selecteer PDF bestanden", command=self.select_pdf_files)
        file_menu.add_command(label="Afsluiten", command=self.quit)

        info_menu = tk.Menu(app_menu)
        app_menu.add_cascade(label="Info", menu=info_menu)
        info_menu.add_command(label=f"Over {Options.APPLICATION_NAME}", command=self.show_program_info)

        # set up default padding
        frame_pad_x = (5, 5)
        frame_pad_y = (5, 5)

        # set up main window
        self.app_frame = ttk.Frame(self)
        self.app_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True,
                            padx=frame_pad_x, pady=frame_pad_y)

        # user input fields (filename and pdf files)
        frame_file_selection: ttk.Frame = ttk.Frame(master=self.app_frame)
        frame_file_selection.pack(side=tk.TOP, fill=tk.BOTH, padx=frame_pad_x, pady=frame_pad_y)
        label_filename: ttk.Label = ttk.Label(master=frame_file_selection, text="Naam van samengevoegde PDF")
        label_filename.pack(side=tk.LEFT)
        self.filename: tk.StringVar = tk.StringVar()
        input_filename: ttk.Entry = ttk.Entry(master=frame_file_selection, textvariable=self.filename)
        input_filename.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=frame_pad_x, pady=frame_pad_y)
        button_select_files: ttk.Button = ttk.Button(master=frame_file_selection, text="Selecteer PDF bestanden",
                                                     command=self.select_pdf_files)
        button_select_files.pack(side=tk.TOP, fill=tk.X, padx=frame_pad_x, pady=frame_pad_y)

        # create the listbox to hold the file list
        frame_file_list: ttk.Frame = ttk.Frame(master=self.app_frame)
        frame_file_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=frame_pad_x, pady=frame_pad_y)
        self.file_list_view = FileListView(master=frame_file_list)
        self.file_list_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        frame_list_buttons: ttk.Frame = ttk.Frame(master=frame_file_list)
        frame_list_buttons.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=frame_pad_x, pady=frame_pad_y)
        button_clear_list: ttk.Button = ttk.Button(master=frame_list_buttons, text="Maak lijst leeg",
                                                   command=self.clear_file_list)
        button_clear_list.pack(side=tk.TOP, fill=tk.X, expand=False, padx=frame_pad_x, pady=frame_pad_y)
        button_remove_selection: ttk.Button = ttk.Button(master=frame_list_buttons, text="Verwijder selectie",
                                                         command=self.remove_selection)
        button_remove_selection.pack(side=tk.TOP, fill=tk.X, expand=False, padx=frame_pad_x, pady=frame_pad_y)

        button_merge_files: ttk.Button = ttk.Button(master=self.app_frame, text="PDF bestanden samenvoegen",
                                                    command=self.merge_pdf_files)
        button_merge_files.pack(side=tk.TOP, fill=tk.X, padx=frame_pad_x, pady=frame_pad_y)

    def _fake_command(self):
        pass

    def remove_selection(self):
        for selection in reversed([s for s in self.file_list_view.curselection()]):
            self.options.message(message=f'Deleting selection {selection}')
            self.file_list_view.delete(selection)

    def clear_file_list(self):
        self.file_list_view.delete(first=0, last=tk.END)

    def merge_pdf_files(self, force_overwrite: bool = False):
        pdf_list = self.file_list_view.get(first=0, last=tk.END)
        pdf_filename = self.filename.get()

        try:
            self.merge_controller.merge(pdf_files=pdf_list, file_name=pdf_filename, force_overwrite=force_overwrite)
        except NoFileNameException:
            MessageBox.show_error(message='Geef eerst de naam op van het samengevoegde bestand')
        except TooFewFilesException:
            MessageBox.show_error(message='Selecteer tenminste twee bestanden.',
                                  title='Te weinig bestanden')
        except FileExistsError:
            force_overwrite = MessageBox.ask_ok_cancel(message='Weet je zeker dat je het bestand wilt overschrijven?',
                                                       detail=f'{pdf_filename}')
        except FileNotFoundError as e:
            print('File not found exception')
            print(str(e))
            MessageBox.show_error(message=str(e), title='Bestand bestaat niet')
            return

        if force_overwrite:
            self.merge_pdf_files(force_overwrite=True)

    def select_pdf_files(self):
        filenames = filedialog.askopenfilenames(initialdir=self.options.path,
                                                title="Selecteer PDF bestanden",
                                                filetypes=[('PDF', '.pdf'), ('Alle bestanden', '*.*')])
        self.options.message(filenames)

        for f in filenames:
            self.file_list_view.insert(tk.END, f)

    def show_program_info(self):
        about_view = tk.Toplevel(master=self.master)
        about_view.geometry("300x100")
        about_view.configure(background="white")
        about_view.title(f"Over {Options.APPLICATION_NAME}")

        ttk.Label(about_view,
                  text=f"{Options.APPLICATION_NAME} ({Options.APPLICATION_VERSION}) door {Options.APPLICATION_AUTHOR}",
                  background="white").pack(pady=10)
        github_source = ttk.Label(about_view, text=Options.APPLICATION_SOURCE_URL, background="white")
        github_source.bind("<Button-1>", lambda e: webbrowser.open_new(Options.APPLICATION_SOURCE_URL))
        github_source.pack(pady=10)

        about_view.mainloop()
