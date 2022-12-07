import tkinter as tk
from tkinter import filedialog as filedialog
from tkinter import messagebox
from tja2osu import convertio as convertio

file_path = ""
def tja_select():
  global file_path
  idir = 'C:\\python_test'
  filetype = [("tjaFile","*.tja")]
  file_path = filedialog.askopenfilename(title="Select the tja file", filetypes = filetype, initialdir = idir)
  if file_path != "":
    input_box.delete(0,tk.END)
    input_box.insert(tk.END, file_path)
    file_path = ""

def osu_select():
  idir = 'C:\\python_test'
  file_out = filedialog.askdirectory(title="Select the path to save osu", initialdir = idir)
  if file_out != "":
    file_in = input_box.get()
    artist = input_box1.get()
    creator = input_box2.get()
    convertio(file_in, artist, creator, file_out)
    input_box.delete(0,tk.END)
    input_box.insert(tk.END, file_path)
    messagebox.showinfo('Success!', 'The file has successfully converted!')
    file_out = ""
  
root = tk.Tk()
root.title("TJA2OSU GUI")
root.geometry("360x240")

input_box = tk.Entry(width=40)
input_box.place(x=10, y=150)

input_label = tk.Label(text="tja File")
input_label.place(x=10, y=120)

button = tk.Button(text="Open",command=tja_select)
button.place(x=300, y=145)

input_box1 = tk.Entry(width=40)
input_box1.place(x=10, y=50)
input_label1 = tk.Label(text="Artist")
input_label1.place(x=10, y=20)

input_box2 = tk.Entry(width=40)
input_box2.place(x=10, y=100)
input_label2 = tk.Label(text="Creator")
input_label2.place(x=10, y=70)

button = tk.Button(text="Convert",command=osu_select, width=45, justify=tk.CENTER)
button.place(x=20, y=200)

root.mainloop()
