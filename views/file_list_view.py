import tkinter as tk
from tkinter import Tk, Toplevel


class FileListView(tk.Listbox):
    """ A Tkinter listbox with drag & drop reordering of lines
        Source: https://stackoverflow.com/questions/14459993/tkinter-listbox-drag-and-drop-with-python
    """
    def __init__(self, master: Toplevel or Tk, **kw):
        kw['selectmode'] = tk.EXTENDED
        tk.Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.set_current)
        self.bind('<Control-1>', self.toggle_selection)
        self.bind('<B1-Motion>', self.shift_selection)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Enter>', self.on_enter)
        self.selection_clicked = False
        self.shifting = False
        self.left = False
        self.unlock_shifting()
        self.ctrl_clicked = False

    def order_changed_event_handler(self):
        pass

    def on_leave(self, _event):
        # prevents changing selection when dragging
        # already selected items beyond the edge of the listbox
        if self.selection_clicked:
            self.left = True
            return 'break'

    def on_enter(self, _event):
        #TODO
        self.left = False

    def set_current(self, event):
        self.ctrl_clicked = False
        i = self.nearest(event.y)
        self.selection_clicked = self.selection_includes(i)
        if self.selection_clicked:
            return 'break'

    def toggle_selection(self, event):
        self.ctrl_clicked = True

    def move_element(self, source, target):
        if not self.ctrl_clicked:
            element = self.get(source)
            self.delete(source)
            self.insert(target, element)

    def unlock_shifting(self):
        self.shifting = False

    def lock_shifting(self):
        # prevent moving processes from disturbing each other
        # and prevent scrolling too fast
        # when dragged to the top/bottom of visible area
        self.shifting = True

    def shift_selection(self, event):
        if self.ctrl_clicked:
            return
        selection = self.curselection()
        if not self.selection_clicked or len(selection) == 0:
            return

        selection_range = range(min(selection), max(selection))
        current_index = self.nearest(event.y)

        if self.shifting:
            return 'break'

        line_height = 15
        bottom_y = self.winfo_height()
        if event.y >= bottom_y - line_height:
            self.lock_shifting()
            self.see(self.nearest(bottom_y - line_height) + 1)
            self.master.after(500, self.unlock_shifting)
        if event.y <= line_height:
            self.lock_shifting()
            self.see(self.nearest(line_height) - 1)
            self.master.after(500, self.unlock_shifting)

        if current_index < min(selection):
            self.lock_shifting()
            not_in_selection_index = 0
            for i in selection_range[::-1]:
                if not self.selection_includes(i):
                    self.move_element(i, max(selection) - not_in_selection_index)
                    not_in_selection_index += 1
            current_index = min(selection)-1
            self.move_element(current_index, current_index + len(selection))
            self.order_changed_event_handler()
        elif current_index > max(selection):
            self.lock_shifting()
            not_in_selection_index = 0
            for i in selection_range:
                if not self.selection_includes(i):
                    self.move_element(i, min(selection) + not_in_selection_index)
                    not_in_selection_index += 1
            current_index = max(selection)+1
            self.move_element(current_index, current_index - len(selection))
            self.order_changed_event_handler()
        self.unlock_shifting()
        return 'break'
