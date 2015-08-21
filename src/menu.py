from tkinter import *
import config


class Menu:

    def __init__(self, root):
        self.root = root

        self.root.protocol('WM_DELETE_WINDOW', self.exit)

        buttons_frame_padx = "3m"
        buttons_frame_pady = "2m"
        buttons_frame_ipadx = "3m"
        buttons_frame_ipady = "1m"

        settings = Frame(root)
        settings.pack(side=TOP,
                      ipadx=buttons_frame_ipadx,
                      ipady=buttons_frame_ipady,
                      padx=buttons_frame_padx,
                      pady=buttons_frame_pady)

        controls = Frame(root)
        controls.pack(side=BOTTOM,
                      ipadx=buttons_frame_ipadx,
                      ipady=buttons_frame_ipady,
                      padx=buttons_frame_padx,
                      pady=buttons_frame_pady)

        fullscreen_label = Label(settings, text="Fullscreen:")
        fullscreen_label.grid(row=0, sticky=W)

        fullscreen = Checkbutton(settings)
        if config.fullscreen:
            fullscreen.select()
        else:
            fullscreen.deselect()
        fullscreen.grid(row=0, column=1, sticky=W)
        fullscreen.bind("<Button-1>", self.fullscreen_toggle)

        speed_label = Label(settings, text="Speed:")
        speed_label.grid(row=1, sticky=W)

        optionList = config.speed_value.keys()
        self.chosen_speed = StringVar()
        self.chosen_speed.set(config.speed)
        speed_menu = OptionMenu(settings, self.chosen_speed, *optionList)
        speed_menu.grid(row=1, column=1, sticky=W)

        play_button = Button(controls)
        play_button["text"] = "Play!"
        play_button.pack(side=LEFT)
        play_button.bind("<Button-1>", self.play_button_click)

        exit_button = Button(controls)
        exit_button["text"] = "Exit"
        exit_button.pack(side=RIGHT)
        exit_button.bind("<Button-1>", self.exit_button_click)

    def exit_button_click(self, event):
        self.exit()

    def exit(self):
        exit(0)

    def play_button_click(self, event):
        config.speed = self.chosen_speed.get()
        self.root.destroy()

    def fullscreen_toggle(self, event):
        config.fullscreen = not config.fullscreen


def _center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))


def show_menu():
    root = Tk()
    # root.overrideredirect(1)
    root.resizable(0, 0)
    _center(root)
    root.wm_title("Rats " + str(config.version) + " Settings")
    Menu(root)
    root.mainloop()
