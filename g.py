import tkinter as tkr
from tkinter import messagebox as mb
import random as rd
import requests as rq
import sys

GREAD = 10
HEIGHT = 350
WIDTH = 500

all_right = True
jratva = 0
bonus = 0
score_count = 0
global_count = 0

score = 0
timer = 0
eat = False


def inet():
    def send_data():
        wind.destroy()
        rq.get('https://nikitapetrov1997.000webhostapp.com', params={'name': name.get(), 'score':score_count})
        req_score()
     
    name = tkr.StringVar()
     
    message_entry = tkr.Entry(textvariable=name)
    message_entry.place(relx=.5, rely=.1, anchor="c")
     
    message_button = tkr.Button(text="Click Me", command=send_data)
    message_button.place(relx=.5, rely=.5, anchor="c")
    
    #name = input("Enter your name: ")
    #rq.get('https://nikitapetrov1997.000webhostapp.com', params={'name': name, 'score':score_count})
    #req_score()
        

def req_score():
    r = [i.split(',') for i in rq.get('https://nikitapetrov1997.000webhostapp.com/hello.txt').text.rstrip().split('\n')]
    for i in r:
        i[1] = int(i[1])
    p = sorted(r, key=lambda x: x[1], reverse=True)[0:10]
    s = ""
    for i in range(len(p)):
        s += str(i+1) + ". " + p[i][0] + " | " + str(p[i][1]) + "\n"
    #[print(i+1, "Name", p[i][0], "Score", p[i][1]) for i in range(len(p))]
    #mb.showinfo("Leaderboard", s)
    scr_wind = tkr.Tk()
    scr_wind.title("Leaderboard")
    scr_lbl = tkr.Label(scr_wind, text=s, font="Arial 15")
    scr_lbl.pack(side="top", fill="both", expand=True, padx=40, pady=60)

def eating(object, score_encr):
    global global_count
    global score_count
    global bonus
    canv.delete(object)
    panel.delete(score)
    global_count += 1
    score_count += score_encr
    d.new_cusok()


def generate():
    global jratva
    jratva = canv.create_text(
        GREAD * rd.randint(1, WIDTH/GREAD), GREAD * rd.randint(1, HEIGHT/GREAD), text='$', font='Arial 12')


def generate_bonus():
    global bonus
    bonus = canv.create_text(
        GREAD * rd.randint(1, WIDTH / GREAD), GREAD * rd.randint(1, HEIGHT / GREAD), text='X', font='Arial 15 bold')


#New SCORE widow        
def show_score(sc):
    global score
    score = panel.create_text(5, (HEIGHT)/30, text='Score: ' + str(sc), font='Arial 15', anchor='w')
 

def play():
    global all_right
    global jratva
    global bonus
    global score
    global timer
    global eat

    if all_right:
        if d.idet != tuple(_ * -1 for _ in d.new_dir): #Allows not to lay the snake head on the tail
            d.idet = d.new_dir                         #in case of fast key switching
        d.move()
        x, y = canv.coords(d.cusoks[-1].fig)
        
        if x > WIDTH or x < 0:
            canv.coords(d.cusoks[-1].fig, abs(x - WIDTH) - GREAD, y) #Now segments are teleported in right place
        if y > HEIGHT or y < 0:                                      #without any offset
            canv.coords(d.cusoks[-1].fig, x, abs(y - HEIGHT) - GREAD)
            
        if canv.coords(d.cusoks[-1].fig) in [canv.coords(d.cusoks[i].fig) for i in range(len(d.cusoks) - 1)]:
            all_right = False
        if canv.coords(jratva) == canv.coords(d.cusoks[-1].fig) or canv.coords(jratva) == canv.coords(d.cusoks[-2].fig):
            eat = True
            eating(jratva, 5)
            generate()
            show_score(score_count)
        if global_count % 2 == 0 and global_count != 0 and bonus == 0 and eat:
            timer = 0
            generate_bonus()
        elif bonus != 0:
            timer += 1
        if timer == 40:
            canv.delete(bonus)
            bonus = 0
            eat = False
        if canv.coords(bonus) == canv.coords(d.cusoks[-1].fig) or canv.coords(bonus) == canv.coords(d.cusoks[-2].fig):
            eating(bonus, 5)
            bonus = 0
            show_score(score_count)
        wind.after(50, play)
    else:
        canv.create_text(250, 175, text='Good boy\n' + 'Score: ' + str(score_count), font='Arial 20')
        wind.after(100, inet)
        
        
        
class cusok():
    def __init__(self, x, y):
        self.fig = canv.create_text(x, y, text='+', font='Arial 20')


class dermo():
    def __init__(self, cusoks):
        self.cusoks = cusoks
        self.napr = dict(zip(['Up', 'Down', 'Left', 'Right'], [(0, -1), (0, 1), (-1, 0), (1, 0)]))
        self.idet = self.napr['Right']
        self.new_dir = self.idet

    def move(self):
        for i in range(len(self.cusoks) - 1):
            x, y = canv.coords(self.cusoks[i + 1].fig)
            canv.coords(self.cusoks[i].fig, x, y)
        x1, y1 = canv.coords(self.cusoks[-1].fig)
        canv.coords(self.cusoks[-1].fig, x1 + self.idet[0]*GREAD, y1 + self.idet[1]*GREAD)

    def povorot(self, event):
        self.new_dir = self.napr.get(event.keysym, self.idet)
        #if self.idet != tuple(_ * -1 for _ in tmp):
        #    self.idet = tmp

    def new_cusok(self):
        x, y = canv.coords(self.cusoks[-1].fig)
        self.cusoks.append(cusok(x + GREAD * self.idet[0], y + GREAD * self.idet[1]))
  
  
plate = tkr.Tk()
plate.geometry('300x100')
ss_butt = tkr.Button(text='Show score', command=req_score)
pg_butt = tkr.Button(text='play game', command=plate.destroy)
qq_butt = tkr.Button(text='quit', command=sys.exit)  
ss_butt.pack(expand=False, side="top", fill="both")
pg_butt.pack(expand=False, side="top", fill="both")
qq_butt.pack(expand=False, side="top", fill="both")
plate.protocol("WM_DELETE_WINDOW", sys.exit)
plate.mainloop()


wind = tkr.Tk()
wind.title('Govno')
canv = tkr.Canvas(wind, width=WIDTH, height=HEIGHT, bg='#ffff55')
canv.grid()
canv.focus_force()
panel = tkr.Canvas(wind, width=WIDTH, height=(HEIGHT/15), bg='#aaaaaa')
panel.grid()

init_length = 5
cuski = [cusok(GREAD * i, GREAD) for i in range(1, init_length + 1)]
d = dermo(cuski)

canv.bind("<KeyPress>", d.povorot)
generate()

show_score(0)

play()
wind.mainloop()
