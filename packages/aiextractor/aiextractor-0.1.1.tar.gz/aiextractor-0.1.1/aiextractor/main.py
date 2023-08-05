from tkinter import filedialog, simpledialog, Listbox
from tkinter import *
from aiextractor import Pipero

root = Tk()
root.filename = filedialog.askopenfiles(initialdir="/", title="Select files")


data = Pipero(root.filename)
headers = data.extract_headers()
listbox = Listbox(selectmode=MULTIPLE)
listbox.pack()
for i in headers:
    listbox.insert(END, str(i))
listbox.bind("<Double-Button-1>", True)


def close():
    global listbox, root, headers
    items = [headers[int(item)] for item in listbox.curselection()]
    data.extract_data(items)
    data.save_data()
    root.destroy()


b = Button(root, text="OK", command=close).pack()

root.mainloop()
