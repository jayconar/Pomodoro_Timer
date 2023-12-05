from tkinter import Tk, Button, Label, PhotoImage, Canvas, mainloop
from pygame.mixer import init, music
from math import floor
from os import path

FONT = "Berlin Sans FB Demi Bold"
BGC = "#FFF9C9"
GREEN = "#1CCC28"

WORK = 25 * 60
SHORT_BREAK = 5 * 60
LONG_BREAK = 20 * 60
cycle = 1
count = ""
directory = path.dirname(path.abspath(__file__))
init()


def alarm():
    music.load(path.join(directory, "art", "next_level.mp3"))
    music.play()
    screen.after(2000)
    music.stop()


def reset():
    global cycle
    screen.after_cancel(count)
    canvas.itemconfig(temps, text="00:00")
    cycle = 1
    checkmark.config(text="")
    session.config(text="Timer")
    start_button.config(state="normal")


def start():
    global cycle
    if cycle % 2 != 0:
        session.config(text="Work")
        timer(WORK)
        cycle += 1
    elif cycle % 8 == 0:
        session.config(text="Rest")
        cycle = 1
        timer(LONG_BREAK)
    elif cycle % 2 == 0:
        session.config(text="Short Break")
        timer(SHORT_BREAK)
        cycle += 1
    start_button.config(state="disabled")


def timer(total_seconds):
    if total_seconds >= 0:
        minutes = floor(total_seconds/60)
        seconds = total_seconds % 60
        if seconds < 10:
            seconds = f"0{seconds}"
        canvas.itemconfig(temps, text=f"{minutes}:{seconds}")
        global count
        count = screen.after(1000, timer, total_seconds - 1)
    elif total_seconds < 0:
        overs = ""
        for i in range(floor(cycle/2)):
            overs += " ✔ "
        checkmark.config(text=overs)
        alarm()
        start()


screen = Tk()
screen.title("Pomodoro Timer")
screen.iconbitmap(path.join(directory, "art", "pomodoro.ico"))
screen.config(padx=100, pady=60, bg=BGC, highlightthickness=0, width=360, height=360)

canvas = Canvas(width=280, height=280, bg=BGC, highlightthickness=0)
image = PhotoImage(file=path.join(directory, "art", "pomodoro.png"))
canvas.create_image(140, 140, image=image)
temps = canvas.create_text(140, 170, text="00:00", font=(FONT, 36))
canvas.grid(column=1, row=1)

session = Label(text="Timer", bg=BGC, font=(FONT, 38, "bold"))
session.grid(column=1, row=0)
checkmark = Label(text="", fg=GREEN, bg=BGC, font=(FONT, 24, "bold"))
checkmark.grid(column=1, row=2)

reset_button = Button(text="Reset", command=reset, width=6, bg="black", fg="white", font=(FONT, 16),
                      highlightthickness=0)
reset_button.grid(column=2, row=2)
start_button = Button(text="Start", command=start, width=6, bg="black", fg="white", font=(FONT, 16),
                      highlightthickness=0)
start_button.grid(column=0, row=2)

mainloop()
