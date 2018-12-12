


def gui(schedule, courses, schedule_counter, bool):
    window = tk.Tk()
    window.geometry('650x300')
    window.configure(bg='white')
    # Add title to GUI
    window.title("GUI Safariteam")

    lbl = tk.Label(window, text="Hill climber: ").grid()

    Label(window, text="Iterations: ").grid(row=1)
    Label(window, text="Runs (n): ").grid(row=2)

    e1 = Entry(window)
    e2 = Entry(window)

    e1.grid(row=1, column=1)
    e2.grid(row=2, column=1)

    e1.insert(10,"10000")
    e2.insert(10,"5")

    e1.bind('<Return>', lambda _: printen(e1.get(), e2.get()))
    e2.bind('<Return>', lambda _: printen(e1.get(), e2.get()))

    def printen(ding, ding2):
        print(ding, ding2)
        print("Hahah lol kijk hoe leuk dit is ieee jaaaa lekker klikken")

    lbl = tk.Label(window, text="Press enter to run. ").grid()
    # def hill_climber():
    #     hillclimber.soft_constraints(schedule, courses, schedule_counter, True)
    # def magniet():
    #     print("MAG NIET hahaheheheheheeh gna gna gna")
    #
    #
    # # Add button
    # ttk.Button(window, text="Ja doe maar genetisch", command = printen, style = 'grey/silver.TLabel').grid()
    # ttk.Button(window, text="Hill climber", command = hill_climber, padding=6).grid(column = 1, row = 1)
    #
    # tk.Label(window, text="Ja en hoe vaak dan???!!").grid()
    # tk.Label(window, text="WIL JE PLOT!??!!!!!!!!!!").grid()
    # tk.Button(window, text="ja.", command = magniet).grid(column=0, row=8)
    # tk.Button(window, text="nee.", command = magniet).grid(column=0, row=8, columnspan = 2)

    # rad1 = tk.Radiobutton(window,text='Of misschien met radiobuttons', value=1)
    # rad2 = tk.Radiobutton(window,text='Algoritmes aaklikken', value=2)
    # rad3 = tk.Radiobutton(window,text='Enzo', value=3)
    # rad1.grid()
    # rad2.grid()
    # rad3.grid()
    #
    # style = ttk.Style()
    # style.layout("TMenubutton", [
    #    ("Menubutton.background", None),
    #    ("Menubutton.button", {"children":
    #        [("Menubutton.focus", {"children":
    #            [("Menubutton.padding", {"children":
    #                [("Menubutton.label", {"side": "left", "expand": 1})]
    #            })]
    #        })]
    #    }),
    # ])
    #
    # mbtn = ttk.Menubutton(text='Of even lekker een dropdown!?? nee he')
    # mbtn.grid()
    #
    # bar = Progressbar(window, length=400)
    # bar['value'] = 70
    # bar.grid(column =0,row =19)

    window.mainloop()
