from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import tkinter.colorchooser as cc
from tkinter import ttk


from PIL import Image, ImageTk
import os

# Creating all the functions of all the buttons in the NotePad
def open_file():
    file = fd.askopenfilename(defaultextension='.txt', filetypes=[('All Files', '*.*'), ("Text File", "*.txt*"), ("Python File", "*.py")])

    if file:
        global current_file
        current_file = file

    text_area.delete(1.0, END)
    with open(file, "r") as file_:
        text_area.insert(1.0, file_.read())
        file_.close()


def new_file():
    text_area.delete(1.0, END)
    root.title("New File - Notepad")


def save_file():
    global current_file
    if current_file:
        with open(current_file, 'w') as file:
            file.write(text_area.get(1.0, END))
            file.close()
    else:
        save_as_file()


def save_as_file():
    global current_file
    file = fd.asksaveasfilename(initialfile='Untitled.txt', defaultextension='.txt', filetypes=[("Text File", "*.txt*"), ("Word Document", '*,docx*'), ("PDF", "*.pdf*")])
    if file:
        with open(file, 'w') as file_:
            file_.write(text_area.get(1.0, END))
            file_.close()
        current_file = file

        
def toggle_always_on_top():
    global always_on_top
    if always_on_top.get() == 0:
        root.attributes('-topmost', False)
    else:
        root.attributes('-topmost', True)
    root.focus_set()

def exit_application():
    root.destroy()


def copy_text():
    text_area.event_generate("<<Copy>>")


def cut_text():
    text_area.event_generate("<<Cut>>")


def paste_text():
    text_area.event_generate("<<Paste>>")


def select_all():
    text_area.event_generate("<<Control-Keypress-A>>")


def delete_last_char():
    text_area.event_generate("<<KP_Delete>>")


def undo_text():
    text_area.edit_undo()


def redo_text():
    text_area.edit_redo()


def about_notepad():
    mb.showinfo("About Notepad", "This is just another Notepad, but this is better than all others")


def about_commands():
    commands = """
Under the File Menu:
- 'New' clears the entire Text Area
- 'Open' clears text and opens another file
- 'Save' saves your current file 
- 'Save As' saves your file in another extension

Under the Edit Menu:
- 'Copy' copies the selected text to your clipboard
- 'Cut' cuts the selected text and removes it from the text area 
- 'Paste' pastes the copied/cut text
- 'Select All' selects the entire text
- 'Delete' deletes the last character  
"""

    mb.showinfo(title="All commands", message=commands, width=60, height=40)


def set_background_color():
    color = cc.askcolor(title="Choose Background Color")[1]
    text_area.config(bg=color)


def set_text_color():
    color = cc.askcolor(title="Choose Text Color")[1]
    text_area.config(fg=color)


def update_line_numbers(event=None):
    # Rensa befintliga radnummer
    line_numbers.delete('1.0', 'end')

    # Hämta antalet rader i textområdet
    total_lines = str(text_area.get('1.0', 'end')).count('\n')

    # Lägg till radnummer för varje rad
    for line in range(1, total_lines + 1):
        line_numbers.insert('end', str(line) + '\n')

# Händelsekoppling för att uppdatera radnumren när du börjar skriva
def on_text_change(event=None):
    update_line_numbers()


# Initializing the window
root = Tk()
root.title("Untitled - Notepad")
root.geometry('1000x600')
root.resizable(1, 1)

root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=1)

icon = ImageTk.PhotoImage(Image.open('Notepad.png'))
root.iconphoto(False, icon)
file = ''
# global variabel för att hålla reda på den aktuella filen som är öppen
current_file = ''

# Setting the basic components of the window
menu_bar = Menu(root)
root.config(menu=menu_bar)

line_numbers = Text(root, width=4, height=25, bg='#f0f0f0', relief='flat')
line_numbers.grid(row=0, column=0, sticky='ns')

separator = ttk.Separator(root, orient='vertical')
separator.grid(row=0, column=1, sticky='ns')

text_area = Text(root, width=97, height=25 ,font=("Monospace", 12), undo=True)
text_area.grid(row=0, column=2, sticky=NSEW)

scroller = Scrollbar(text_area, orient=VERTICAL)
scroller.pack(side=RIGHT, fill=Y)

scroller.config(command=text_area.yview)
text_area.config(yscrollcommand=scroller.set)

text_area.bind('<Key>', on_text_change)

# Adding the File Menu and its components
file_menu = Menu(menu_bar, tearoff=False, activebackground='DodgerBlue')

file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open File", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Close File", command=exit_application)

menu_bar.add_cascade(label="File", menu=file_menu)

# Adding the Edit Menu and its components
edit_menu = Menu(menu_bar, tearoff=False, activebackground='DodgerBlue')

edit_menu.add_command(label='Undo   '+'            Crtl+Z', command=undo_text)
edit_menu.add_command(label='Redo   '+'             Crtl+Y', command=redo_text)
edit_menu.add_command(label='Copy', command=copy_text)
edit_menu.add_command(label='Cut', command=cut_text)
edit_menu.add_command(label='Paste', command=paste_text)
edit_menu.add_separator()
edit_menu.add_command(label='Select All', command=select_all)
edit_menu.add_command(label='Delete', command=delete_last_char)

menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Adding the Setting Menu and its components
setting_menu = Menu(menu_bar, tearoff=False, activebackground='DodgerBlue')

setting_menu.add_command(label="Background color", command=set_background_color)
setting_menu.add_command(label="Text color", command=set_text_color)


menu_bar.add_cascade(label="Settings", menu=setting_menu)

# Adding the Help Menu and its components
help_menu = Menu(menu_bar, tearoff=False, activebackground='DodgerBlue')

help_menu.add_command(label='About Notepad', command=about_notepad)
help_menu.add_command(label='About Commands', command=about_commands)

menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)

# Adding the View Menu and its components
always_on_top = IntVar()
always_on_top_menu = Menu(menu_bar, tearoff=False, activebackground='DodgerBlue')
always_on_top_menu.add_checkbutton(label="Always On Top", variable=always_on_top, command=toggle_always_on_top)

menu_bar.add_cascade(label="View", menu=always_on_top_menu)


# Adding a label to the bottom that counts the number of characters in the text
# Label(root, text=f"{len(text_area.get(1.0, END))} characters", font=("Times New Roman", 12)).place(anchor=S, y=490)

# Finalizing the window
root.update()
root.mainloop()