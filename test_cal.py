from tkinter import *
from datetime import datetime
from bs4 import BeautifulSoup
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
import datetime
from PIL import Image, ImageTk


def print_sel():
    print(cal.selection_get())
    print(type(cal.selection_get()))
    cal.see(datetime.date(year=2016, month=2, day=5))

def example1():
    top = Toplevel(window)

    import datetime
    today = datetime.date.today()

    mindate = datetime.date(year=1958, month=1, day=1)
    maxdate = today
    print(mindate, maxdate)

    cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                   mindate=mindate, maxdate=maxdate, disabledforeground='red',
                   cursor="hand1", year=2018, month=2, day=5)
    cal.pack(fill="both", expand=True)
    Button(top, text="ok", command=print_sel).pack()


def example2():
    top = Toplevel(window)

    cal = Calendar(top, selectmode='none')
    date = cal.datetime.today() + cal.timedelta(days=2)
    cal.calevent_create(date, 'Hello World', 'message')
    cal.calevent_create(date, 'Reminder 2', 'reminder')
    cal.calevent_create(date + cal.timedelta(days=-2), 'Reminder 1', 'reminder')
    cal.calevent_create(date + cal.timedelta(days=3), 'Message', 'message')

    cal.tag_config('reminder', background='red', foreground='yellow')

    cal.pack(fill="both", expand=True)
    Label(top, text="Hover over the events.").pack()


def example3():
    top = Toplevel(window)

    Label(top, text='Choose date').pack(padx=10, pady=10)

    cal = DateEntry(top, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=2010)
    cal.pack(padx=10, pady=10)


window = Tk()
window.title("Widget Examples")
width = int(600*1.2)
height = int(408*1.2)
window.geometry(f"{width}x{height}+{int((1920-width)/2)}+{int((1080-height)/2)}")
window.resizable(False, False)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)



canvas = Canvas(width=width, height=height)
canvas.place(x=0, y=0)

img = Image.open("spotify.jpg")
img = img.resize((width,height), Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(img)
canvas.create_image(width/2, height/2, image=img)

today = datetime.date.today()
mindate = datetime.date(year=1958, month=1, day=1)
maxdate = today
print(mindate, maxdate)

cal = Calendar(mindate=mindate, maxdate=maxdate, selectmode='day', font="Arial 16",
               background="black", disabledbackground="black",
               bordercolor="#088a5c", headersbackground="#088a5c", normalbackground="#4cf5ca", foreground='white',
               normalforeground='#088a5c', headersforeground='white', date_pattern="yyyy-mm-dd")
cal.grid(row=0, column=0)

# ENTRY
select_label = Label(text="Select date and Enter Playlist Name", foreground="#088a5c", font=("Arial", 17, "bold"))
select_label.grid(row=1, column=0)
name_entry = Entry(width=30, font=("Arial", 17), highlightthickness=3, foreground="#2a5447", background="#4cf5ca",
                   highlightbackground="#062c1b", highlightcolor="#062c1b")
name_entry.grid(row=2, column=0)
name_entry.focus()

# BUTTONS
add_button = Button(text="Create Playlist", background="#088a5c", foreground="white", font=("Arial", 15, "bold"), command=print_sel)
add_button.grid(row=3, column=0, pady=10, sticky=E, padx=160)
# Button(window, text='Calendar', command=example1).pack(padx=10, pady=10)
# Button(window, text='Calendar with events', command=example2).pack(padx=10, pady=10)
# Button(window, text='DateEntry', command=example3).pack(padx=10, pady=10)

window.mainloop()
