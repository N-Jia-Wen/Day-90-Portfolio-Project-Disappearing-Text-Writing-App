from tkinter import Tk, Label, Text, Canvas, Button, END
from ctypes import windll
# import pyglet

# To fix blurry tkinter font AND blurry pop-up box when uploading img file. Taken from https://stackoverflow.com
# /questions/41315873/attempting-to-resolve-blurred-tkinter-text-scaling-on-windows-10-high-dpi-disp/43046744#43046744
windll.shcore.SetProcessDpiAwareness(1)


# Taken and modified from the TypingSpeedTracker class on Day 86:
class DangerWritingApp:

    def __init__(self):
        self.window = Tk()
        self.window.title("Typing Speed Tracker!")
        self.window.minsize(width=1500, height=1000)
        self.window.config(padx=20, pady=20)
        self.window.attributes("-fullscreen", True)

        self.toggle_button = Button(text="Toggle Fullscreen", command=self.toggle_fullscreen)
        self.toggle_button.place(x=0, y=0)

        self.title_label = Label(text="Welcome to the Disappearing Text Writing App!",
                                 font=("Calibri", 30, "bold"))
        self.title_label.config(pady=50)
        self.title_label.pack()

        self.subtitle_label = Label(text="Once you press the start button, the timer would begin counting down. "
                                         "When it reaches 0, all your text will be cleared after 5 seconds. "
                                         "Continue typing to keep refreshing the timer.",
                                    font=("Calibri", 20, "normal"), wraplength=2000)
        self.subtitle_label.config(pady=30)
        self.subtitle_label.pack()

        self.type_text = Text(self.window, wrap="word", height=21, width=125, font=("Calibri", 18, "normal"))
        self.type_text.bind("<KeyRelease>", self.refresh_timer) # Add function here
        self.type_text.config(state="disabled")
        self.type_text.pack()

        # Whitespace separator (empty Label widget)
        whitespace_1 = Label(self.window, height=2)
        whitespace_1.pack()

        self.canvas = Canvas(width=250, height=75, bg="black")
        self.timer_display = self.canvas.create_text(125, 37.5, text="0", fill="#4AA03F",
                                                     font=("Calibri", 30, "bold"), tags=["text"])
        self.canvas.pack()
        self.timer_functionality = None

        # Whitespace separator (empty Label widget)
        whitespace_2 = Label(self.window, height=1)
        whitespace_2.pack()

        self.start_button = Button(text="Start typing!", font=("Calibri", 16, "normal"), fg="white", bg="green",
                                   command=self.start_timer)
        self.start_button.pack()

        self.window.mainloop()

    def toggle_fullscreen(self):
        self.window.attributes('-fullscreen', not self.window.attributes('-fullscreen'))

    def count_down(self, count: int, is_timer_start):
        self.start_button.config(state="disabled", bg="white")

        # When timer is counting down (either upon start (green) or after start (red)):
        if count > 0:
            if is_timer_start is False:
                # Red colour:
                self.canvas.itemconfig(self.timer_display, fill="#E4080A")

            self.canvas.itemconfig(self.timer_display, text=count)
            # Timer ticks down every second
            self.timer_functionality = self.window.after(1000, self.count_down, count - 1, is_timer_start)

        # When count down reaches zero, displays "Go!" for 1 second
        elif count == 0 and is_timer_start is True:
            self.canvas.itemconfig(self.timer_display, text="Go!")
            # Allows user to start typing
            self.type_text.config(state="normal")
            self.type_text.focus()

            # count + 10 and False are passed as positional arguments to count_down method
            self.timer_functionality = self.window.after(1000, self.count_down, count + 10, False)

        # When timer reaches zero again, clears everything in text widget.
        elif count == 0 and is_timer_start is False:
            self.canvas.itemconfig(self.timer_display, text="Time's Up!", fill="#E4080A",
                                   font=("Calibri", 20, "normal"))
            self.type_text.config(state="disabled")
            self.window.after_cancel(self.timer_functionality)

            self.window.after(5000, self.clear_text)

    def refresh_timer(self, event):
        self.window.after_cancel(self.timer_functionality)
        self.count_down(10, False)

    def start_timer(self):
        self.count_down(3, True)

    def clear_text(self):
        self.type_text.config(state="normal")
        self.type_text.delete("1.0", END)
        self.type_text.config(state="disabled")

        self.canvas.itemconfig(self.timer_display, text="0", font=("Calibri", 30, "bold"), fill="#4AA03F")
        self.start_button.config(fg="white", bg="green", state="normal")


test = DangerWritingApp()
