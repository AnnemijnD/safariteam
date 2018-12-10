from tkinter.ttk import Progressbar
import tkinter as tk
from tkinter import ttk


def gui():
    window = tk.Tk()
    window.geometry('650x300')
    window.configure(bg='white')
    # Add title to GUI
    window.title("Hier moet even een logische titel")

    ttk.Style().configure('grey/silver.TLabel', foreground='grey', background='silver', padding=6)
    ttk.Style().configure('test.TLabel', padding=6)

    lbl = tk.Label(window, text="Hier moet even een logische vraagstelling").grid()

    def printen():
        print("Hahah lol kijk hoe leuk dit is ieee jaaaa lekker klikken")
    def printen2():
        print("NU HEB JE WEL GENOEG GEKLIKT HE")
    def magniet():
        print("MAG NIET hahaheheheheheeh gna gna gna")


    # Add button
    ttk.Button(window, text="Ja doe maar genetisch", command = printen, style = 'grey/silver.TLabel').grid()
    ttk.Button(window, text="duizendmiljoen keer genetisch", command = printen, padding=6).grid(column = 1, row = 1)
    ttk.Button(window, text="Hmmm ja doe maar hill climber", command = printen2, style="test.TLabel").grid()
    ttk.Button(window, text="Oh nee toch niet doe maar simulated annealing", command = printen2).grid()

    tk.Label(window, text="Ja en hoe vaak dan???!!").grid()
    tk.Label(window, text="WIL JE PLOT!??!!!!!!!!!!").grid()
    tk.Button(window, text="ja.", command = magniet).grid(column=0, row=8)
    tk.Button(window, text="nee.", command = magniet).grid(column=0, row=8, columnspan = 2)

    rad1 = tk.Radiobutton(window,text='Of misschien met radiobuttons', value=1)
    rad2 = tk.Radiobutton(window,text='Algoritmes aaklikken', value=2)
    rad3 = tk.Radiobutton(window,text='Enzo', value=3)
    rad1.grid()
    rad2.grid()
    rad3.grid()

    style = ttk.Style()
    style.layout("TMenubutton", [
       ("Menubutton.background", None),
       ("Menubutton.button", {"children":
           [("Menubutton.focus", {"children":
               [("Menubutton.padding", {"children":
                   [("Menubutton.label", {"side": "left", "expand": 1})]
               })]
           })]
       }),
    ])

    mbtn = ttk.Menubutton(text='Of even lekker een dropdown!?? nee he')
    mbtn.grid()

    bar = Progressbar(window, length=400)
    bar['value'] = 70
    bar.grid(column =0,row =19)

    window.mainloop()
