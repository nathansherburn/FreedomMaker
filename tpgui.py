#!/user/bin/python

from Tkinter import *
import tkMessageBox
from tkFileDialog import askopenfilename      

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

import ttk


# create a window
main_window = Tk()
main_window.wm_title("PDF to Web")
main_window.geometry('800x600')

# the original text file
text_file = ""
text_buffer = ""
text_current_line = ""

# initialize line to first
line_number = 1

# functions for buttons
def open_file():
	global text_file
	global text_buffer
	global line_number
	line_number = 1
	pdf_path = askopenfilename()
	text_file = convert_pdf_to_txt(pdf_path)
	text_file = text_file.replace("\n\n", "<double new line>")
	text_file = text_file.replace("\n", "")
	text_file = text_file.replace("<double new line>", "\n\n")
	#text_file = text_file.replace("! ", "fi")
	original_text.config(state=NORMAL)
	original_text.delete(0.0, END)
	original_text.insert(INSERT, text_file)
	original_text.config(state=DISABLED)
	new_text.config(state=NORMAL)
	new_text.delete(0.0, END)
	new_text.config(state=DISABLED)
	text_buffer = StringIO(text_file)
	fetch_line()

def do_nothing():
   pass

def convert_pdf_to_txt(path):
	rsrcmgr = PDFResourceManager()
	retstr = StringIO()
	codec = 'US-ASCII'
	laparams = LAParams()
	device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
	file_pointer = file(path, 'rb')
	interpreter = PDFPageInterpreter(rsrcmgr, device)
	password = ""
	maxpages = 0
	caching = True
	pagenos=set()
	for page in PDFPage.get_pages(file_pointer, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
		interpreter.process_page(page)
	file_pointer.close()
	device.close()
	str = retstr.getvalue()
	retstr.close()
	return str

# define functions for text parsing
def keep_text():
	new_text.config(state=NORMAL)
	new_text.insert(END, text_current_line)
	new_text.config(state=DISABLED)
	fetch_line()

def ignore_text():
	fetch_line()

def fetch_line():
	global text_buffer
	global line_number
	global text_current_line
	text_current_line = text_buffer.readline()
	original_text.tag_remove("highlight", "1.0", END)
	original_text.tag_add("highlight", str(line_number)+".0", str(line_number)+"."+str(len(text_current_line)))
	original_text.tag_config("highlight", background="yellow", foreground="black")
	line_number += 1

# define the menu at the window top
menubar = Menu(main_window)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=do_nothing)
filemenu.add_command(label="Open PDF", command=open_file)
filemenu.add_command(label="Save", command=do_nothing)
filemenu.add_command(label="Save as...", command=do_nothing)
filemenu.add_command(label="Close", command=do_nothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=main_window.quit)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=do_nothing)
editmenu.add_separator()
editmenu.add_command(label="Cut", command=do_nothing)
editmenu.add_command(label="Copy", command=do_nothing)
editmenu.add_command(label="Paste", command=do_nothing)
editmenu.add_command(label="Delete", command=do_nothing)
editmenu.add_command(label="Select All", command=do_nothing)
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=do_nothing)
helpmenu.add_command(label="About...", command=do_nothing)
menubar.add_cascade(label="Help", menu=helpmenu)

main_window.config(menu=menubar)


# button definitions
keep_btn = Button(main_window, width=12, text="Keep >", command=keep_text)
keep_btn.pack()

ignore_btn = Button(main_window, width=12, text="Ignore", command=ignore_text)
ignore_btn.pack()

create_btn = Button(main_window, width=12, text="Create Website", command=do_nothing)
create_btn.pack()


# define textboxes
original_text = Text(main_window)
original_text.insert(INSERT, "Click 'File' > 'Open PDF' to begin...")
original_text.pack()
original_text.place(anchor=SW, relheight=1.0, relwidth=0.4, relx=0.0, rely=1.0)

new_text = Text(main_window)
new_text.insert(INSERT, "This is where your good content will go...")
new_text.pack()
new_text.place(anchor=SE, relheight=1.0, relwidth=0.4, relx=1.0, rely=1.0, x=-12)


# define the scrollbars
original_text_scrollbar = Scrollbar(main_window)
original_text_scrollbar.config(command=original_text.yview)
original_text.config(yscrollcommand=original_text_scrollbar.set)
original_text_scrollbar.place(relheight=1.0, relx=0.4)
original_text.config(state=DISABLED)

new_text_scrollbar = Scrollbar(main_window)
new_text_scrollbar.config(command=new_text.yview)
new_text.config(yscrollcommand=new_text_scrollbar.set)
new_text_scrollbar.place(relheight=1.0, relx=1.0, x=-12)
new_text.config(state=DISABLED)

main_window.mainloop()
