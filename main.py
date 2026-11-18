import customtkinter


class InputFrame(customtkinter.CTkFrame):
    """Entry and button for a new note. It does not know where notes are stored, it only calls on_add."""

    def __init__(self, master, on_add):
        super().__init__(master, fg_color="transparent")
        self.on_add = on_add
        self.grid_columnconfigure(0, weight=1)

        self.entry = customtkinter.CTkEntry(self, placeholder_text="New note")
        self.entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.entry.bind("<Return>", lambda event: self.add())
        self.button = customtkinter.CTkButton(self, text="Add", width=80, command=self.add)
        self.button.grid(row=0, column=1)

    def add(self):
        text = self.entry.get().strip()
        if text:
            self.on_add(text)
            self.entry.delete(0, "end")


class NoteListFrame(customtkinter.CTkScrollableFrame):
    """Shows the notes it gets from show(). A click on Delete calls on_delete with the index of the note."""

    def __init__(self, master, on_delete):
        super().__init__(master, label_text="Notes")
        self.on_delete = on_delete
        self.grid_columnconfigure(0, weight=1)
        self.rows = []
        self.delete_buttons = []

    def show(self, notes):
        for row in self.rows:
            row.destroy()
        self.rows = []
        self.delete_buttons = []

        for index, note in enumerate(notes):
            row = customtkinter.CTkFrame(self)
            row.grid(row=index, column=0, padx=5, pady=(5, 0), sticky="ew")
            row.grid_columnconfigure(0, weight=1)
            label = customtkinter.CTkLabel(row, text=note, anchor="w")
            label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
            button = customtkinter.CTkButton(row, text="Delete", width=60, fg_color="transparent", border_width=1,
                                             text_color=("gray10", "gray90"),
                                             command=lambda i=index: self.on_delete(i))
            button.grid(row=0, column=1, padx=5, pady=5)
            self.rows.append(row)
            self.delete_buttons.append(button)


class StatusBar(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0)
        self.grid_columnconfigure(0, weight=1)
        self.label = customtkinter.CTkLabel(self, text="", anchor="w")
        self.label.grid(row=0, column=0, padx=20, sticky="ew")

    def set(self, text):
        self.label.configure(text=text)


class App(customtkinter.CTk):
    """The main window owns the data (the list of notes) and connects the frames."""

    def __init__(self):
        super().__init__()

        self.title("Notes")
        self.geometry("400x420")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.notes = []

        self.input_frame = InputFrame(self, on_add=self.add_note)
        self.input_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.note_list = NoteListFrame(self, on_delete=self.delete_note)
        self.note_list.grid(row=1, column=0, padx=20, pady=0, sticky="nsew")
        self.status_bar = StatusBar(self)
        self.status_bar.grid(row=2, column=0, pady=(20, 0), sticky="ew")

        self.update_view()

    def add_note(self, text):
        self.notes.append(text)
        self.update_view()

    def delete_note(self, index):
        del self.notes[index]
        self.update_view()

    def update_view(self):
        self.note_list.show(self.notes)
        count = len(self.notes)
        self.status_bar.set(f"{count} note" if count == 1 else f"{count} notes")


app = App()
app.mainloop()