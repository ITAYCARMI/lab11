from Tkinter import *
from backend import *

class GUI:
    movies_list = {}

    def __init__(self, root):
        self.topFrame = Frame(root)
        window_width = 400
        window_height = 400
        position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(root.winfo_screenheight() / 2 - window_height / 2)
        root.title("MovieDB")
        root.geometry("300x260+{}+{}".format(position_right, position_down))
        root.resizable(0, 0)
        self.text_Title = Label(root, text="Title:")
        self.entry_Title = Entry(root)
        self.text_Title.grid(row=0)
        self.entry_Title.grid(row=0, column=1)
        self.text_Id = Label(root, text="ID:")
        self.entry_Id = Entry(root)
        self.text_Id.grid(row=1)
        self.entry_Id.grid(row=1, column=1)
        self.text_Year = Label(root, text="Year:")
        self.entry_Year = Entry(root)
        self.text_Year.grid(row=0,column=2)
        self.entry_Year.grid(row=0, column=3)

        self.button_View = Button(text="View all", fg='black', height = 1, width = 13,command=lambda: self.view_all())
        self.button_Search = Button(text="Search entry", fg='black', height = 1, width = 13,command=lambda: self.search_movie())
        self.button_Add = Button(text="Add entry", fg='black', height = 1, width = 13, command=lambda: self.add_movie())
        self.button_Update = Button(text="Update selected", fg='black', height = 1, width = 13, command=lambda: self.update_movie())
        self.button_Delete = Button(text="Delete selected", fg='black',  height = 1, width = 13,command=lambda: self.delete_movie())
        self.button_Close = Button(text="Close", fg='black',height = 1, width = 13, command=lambda: self.close())

        self.button_View.grid(row=2, column=3)
        self.button_Search.grid(row=3, column=3)
        self.button_Add.grid(row=4, column=3)
        self.button_Update.grid(row=5, column=3)
        self.button_Delete.grid(row=6, column=3)
        self.button_Close.grid(row=7, column=3)
        # scrollbar
        self.scrollbar = Scrollbar(root)
        self.scrollbar.grid(row=4,column=2, rowspan=2)
        # listBox
        self.movies_List_Entry = Listbox(root, width=25, height=8, yscrollcommand = self.scrollbar.set)
        self.movies_List_Entry.grid(row=3, column=0, rowspan=5, columnspan=2)


    def view_all(self):
        self.movies_List_Entry.delete(0, END)
        for row in viewall():
            self.movies_List_Entry.insert(END, row)

    def search_movie(self):
        if self.entry_Title.get() == '' or self.entry_Id.get() == '' or self.entry_Year.get() == '':
            tkinter.messagebox.showerror("Error", "Please fill one entry")
        else:
            title = self.entry_Title
            id = self.entry_Id
            year = self.entry_Year

    def add_movie(self):
        if self.entry_Title.get() == '' or self.entry_Id.get() == '' or self.entry_Year.get() == '':
            tkinter.messagebox.showerror("Error", "Please fill all entries")
        else:
            title_movie = self.entry_Title.get()
            id_movie = self.entry_Id.get()
            year_movie = self.entry_Year.get()
            self.movies_list[self.entry_Id] = {'title': title_movie, 'id': id_movie, 'year': year_movie}
            self.movies_List_Entry.delete(0, END)
            for movie in self.movies_list:
                self.movies_List_Entry.insert(END, self.movies_list[movie].title)

    def update_movie(self):
        pass

    def delete_movie(self):
        pass

    def close(self):
        pass


if __name__ == '__main__':
    print('START!')

    root = Tk()
    g = GUI(root)
    root.mainloop()
