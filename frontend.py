from Tkinter import *
from backend import *
import tkinter.messagebox


class GUI:
    movies_list = {}

    def __init__(self, root):
        """
        This method init the GUI of part A
        :param root: the main instance of gui class
        """
        init()
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
        self.text_Genre = Label(root, text="Genre:")
        self.entry_Genre = Entry(root)
        self.text_Genre.grid(row=0, column=2)
        self.entry_Genre.grid(row=0, column=3)

        self.button_View = Button(text="View all", fg='black', height=1, width=13, command=lambda: self.view_all())
        self.button_Search = Button(text="Search entry", fg='black', height=1, width=13,
                                    command=lambda: self.search_movie())
        self.button_Add = Button(text="Add entry", fg='black', height=1, width=13, command=lambda: self.add_movie())
        self.button_Update = Button(text="Update selected", fg='black', height=1, width=13,
                                    command=lambda: self.update_movie())
        self.button_Delete = Button(text="Delete selected", fg='black',  height=1, width=13,
                                    command=lambda: self.delete_movie())
        self.button_Close = Button(text="Close", fg='black', height=1, width=13, command=lambda: self.close())

        self.button_View.grid(row=2, column=3)
        self.button_Search.grid(row=3, column=3)
        self.button_Add.grid(row=4, column=3)
        self.button_Update.grid(row=5, column=3)
        self.button_Delete.grid(row=6, column=3)
        self.button_Close.grid(row=7, column=3)
        # scrollbar
        self.scrollbar = Scrollbar(root)
        self.scrollbar.grid(row=4, column=2, rowspan=2)
        # listBox
        self.movies_List_Entry = Listbox(root, width=25, height=8, yscrollcommand = self.scrollbar.set)
        self.movies_List_Entry.grid(row=3, column=0, rowspan=5, columnspan=2)

    def view_all(self):
        """
        This method show all movies details
        """
        self.movies_List_Entry.delete(0, END)
        for row in viewall():
            self.movies_List_Entry.insert(END, row)

    def search_movie(self):
        """
        This method show details of searcher movie
        """
        if self.entry_Title.get() == '' and self.entry_Id.get() == '' and self.entry_Genre.get() == '':
            tkinter.messagebox.showerror("Error", "Please fill one entry")
        else:
            self.movies_List_Entry.delete(0, END)
            for row in search_entry(self.entry_Id.get(), self.entry_Title.get(), self.entry_Genre.get()):
                self.movies_List_Entry.insert(END, row)

    def add_movie(self):
        """
        This method add movie to db and show it in GUI
        """
        if self.entry_Title.get() == '' or self.entry_Id.get() == '' or self.entry_Genre.get() == '':
            tkinter.messagebox.showerror("Error", "Please fill all entries")
        else:
            title_movie = self.entry_Title.get()
            id_movie = self.entry_Id.get()
            genre_movie = self.entry_Genre.get()
            insert(id_movie, title_movie, genre_movie)
            self.view_all()

    def update_movie(self):
        """
        This method update movie to db and show it in GUI
        """
        if self.movies_List_Entry.get(ACTIVE) == '':
            tkinter.messagebox.showerror("Error", "Please choose one from the movies to update")
        elif self.entry_Title.get() == '' and self.entry_Id.get() == '' and self.entry_Genre.get() == '':
            tkinter.messagebox.showerror("Error", "Please fill one from the entries")
        else:
            value = str((self.movies_List_Entry.get(ACTIVE)))
            split_value = value[1:len(value) - 1]
            final_splited_value = split_value.split(', ')
            new_id = self.entry_Id.get()
            new_title = self.entry_Title.get()
            new_genre = self.entry_Genre.get()
            del_id = final_splited_value[0].replace('\'', '')
            del_title = final_splited_value[1].replace('\'', '')
            del_genre = final_splited_value[2].replace('\'', '')
            if new_id != '':
                if new_genre != '' and new_title != '':
                    self.add_movie()
                    delete(del_id, del_title, del_genre)
                elif new_genre != '' and new_title == '':
                    self.entry_Title.insert(0, del_title)
                    self.add_movie()
                    delete(del_id, del_title, del_genre)
                elif new_genre == '' and new_title != '':
                    self.entry_Genre.insert(0, del_genre)
                    self.add_movie()
                    delete(del_id, del_title, del_genre)
                else:
                    self.entry_Title.insert(0, del_title)
                    self.entry_Genre.insert(0, del_genre)
                    self.add_movie()
                    delete(del_id, del_title, del_genre)
            else:
                if new_genre != '' and new_title != '':
                    update(del_id, new_title, new_genre)
                elif new_genre != '' and new_title == '':
                    update(del_id, del_title, new_genre)
                else:
                    update(del_id, new_title, del_genre)
        self.view_all()

    def delete_movie(self):
        """
        This method delete movie from db and show it in GUI
        """
        if self.movies_List_Entry.get(ACTIVE) == '':
            tkinter.messagebox.showerror("Error", "Please choose one from the movies to delete")
        else:
            value = str((self.movies_List_Entry.get(ACTIVE)))
            split_value = value[1:len(value) - 1]
            final_splited_value = split_value.split(', ')
            del_id = final_splited_value[0].replace('\'', '')
            del_title = final_splited_value[1].replace('\'', '')
            del_genre = final_splited_value[2].replace('\'', '')
            print value
            delete(del_id, del_title, del_genre)
            self.view_all()

    @staticmethod
    def close():
        """
        This method close the GUI
        """
        root.destroy()


if __name__ == '__main__':
    print('START!')

    root = Tk()
    g = GUI(root)
    root.mainloop()
    print('CLOSED!')
