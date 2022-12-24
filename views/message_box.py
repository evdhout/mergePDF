from tkinter import messagebox


class MessageBox:
    def __init__(self):
        pass

    @staticmethod
    def show_error(message: str, title: str = 'Foutmelding', detail: str or None = None):
        messagebox.showerror(message=message, title=title, icon="error", detail=detail)

    @staticmethod
    def ask_ok_cancel(message: str, title: str = 'Bevestiging', detail: str or None = None) -> bool:
        return messagebox.askokcancel(message=message, title=title, icon="warning", detail=detail)

    @staticmethod
    def show_message(message: str, title: str = 'Melding', detail: str or None = None):
        messagebox.showerror(message=message, title=title, icon="info", detail=detail)
