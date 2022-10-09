#DINO RUN FOR LINUX(Terminal version)

#SET UP
from random import randint,choices
import threading
from time import sleep
from os import system,path,popen
import tty
import sys
import termios

#CLASS
class Obstacle:
    def __init__(self):
        self.oy2=3
        self.ox=l-5
        self.ox2=self.ox+randint(2,-(self.ox-l))
        self.oy=b-choices(range(self.oy2,10),weights=(90,15,25,10,5,20,25),k=1)[0]
        self.lst=[]
    def render(self):
        self.lst=[]
        for i in range(self.oy2):
            self.lst.append(range(self.ox+i*d+self.oy*d,self.ox2+i*d+self.oy*d))
        for i in self.lst:
            gassign(i)

    def delete(self):
        for i in self.lst:
            gdelete(i)

    def move(self):
        self.delete()
        self.ox -= 1
        self.ox2 -= 1
        self.render()


#FUNCTIONS
def gassign(lst):
    for i in lst:
        if out[i] == " ":
            try:
                out[i]=gchr
            except:
                pass

def gdelete(lst):
    for i in lst:
        if out[i] == gchr:
            try:
                out[i]=" "
            except:
                pass

def assign(lst):
    for i in lst:
        if out[i] == " ":
            try:
                out[i]=pchr
            except:
                pass
def delete(lst):
    for i in lst:
        if out[i] == pchr:
            try:
                out[i]=" "
            except:
                pass


def moveObs():
    global score,gmag,pmag,spacing,minspace
    obstacles.append(Obstacle())
    # spacing=randint(40,l-1)
    while True:
        if not stopgame:
            try:
                for i in range(len(obstacles)):
                    if obstacles[i].ox<1:
                        obstacles[i].delete()
                        obstacles.pop(i)
                    if len(obstacles) == 0:
                            obstacles.append(Obstacle())
                    else:
                        if obstacles[-1].ox==l-spacing:
                            obstacles.append(Obstacle())
                            if randomspacing:
                                spacing=randint(minspace,80)
                    obstacles[i].move()
                score+=1
                if progressive:
                    if score in [500,1000,1500]:
                        pmag-=0.002
                        gmag-=0.002
                        minspace+=2
                        # spacing=30

                    elif score == 2500:
                        pmag-=0.001
                        gmag-=0.001
                        minspace+=2

                    elif score in [4000,8000,15000,30000,80000,150000]:
                        pmag-=0.0011
                        gmag-=0.0007
                        minspace+=2
            except:
                pass
            sleep(gmag)
            show()


def move(dir):
    global u,d
    if dir=="up":
        try:
            delete(range(pi+1+u*d,pi+3+u*d))
            delete(range(pi+d+u*d,pi+4+d+u*d))
            delete(range(pi+2*d+u*d,pi+4+2*d+u*d))
            assign(range(pi+1+int(u-1)*d,pi+3+int(u-1)*d))
            assign(range(pi+d+int(u-1)*d,pi+4+d+int(u-1)*d))
            assign(range(pi+2*d+int(u-1)*d,pi+4+2*d+int(u-1)*d))
            u-=1
        except:
            pass
    elif dir=="down":
        try:
            delete(range(pi+1+u*d,pi+3+u*d))
            delete(range(pi+d+u*d,pi+4+d+u*d))
            delete(range(pi+2*d+u*d,pi+4+2*d+u*d))
            assign(range(pi+1+int(u+1)*d,pi+3+int(u+1)*d))
            assign(range(pi+d+int(u+1)*d,pi+4+d+int(u+1)*d))
            assign(range(pi+2*d+int(u+1)*d,pi+4+2*d+int(u+1)*d))
            u+=1
        except:
            pass

def show():
    if not stopgame:
        system("clear")
        for i in out:
            if i == "\n":
                print()
            else:
                print(i,end="")
        for i in gout:
            print(i,end="")
        print()
        print("\t\t\tScore:",int(score//10))


def keyread():
    global key
    while True:
        if not stopgame:
            key=sys.stdin.read(1)[0]

def collision():
    for i in range(len(out)):
        try:
            if out[i]==pchr and (out[i+1]==gchr or out[i+l]==gchr):
                return True
            if jumping:
                if out[i]==pchr and out[i-l]==gchr:
                    return True
        except:
            pass
    return False


#VARIABLES
pchr="$"           #Player character
gchr="#"           #Ground/Obstacle character
l = int(popen("stty size","r").read().split()[-1]) - 1 #Length of Display
b = 25             #Breadth of Display
ul = b-3           #Player's initial y position 
pi = 15            #Player's initial x position
startslow=True     #Starts with slow speed
progressive=True   #Progressive increase in Speed
if startslow:
    pmag = 0.05    #Player y speed(jump speed)
    gmag = 0.01    #Player x Speed(ground move speed)
else:              #Speeds when not starting slow
    pmag = 0.004
    gmag = 0.015
jmag=3             #Jumping Force
gravity = 0.4      #Acceleration due to gravity
minspace = 35      #Minimum Space between Obstacles
randomspacing=True #Random spacing between obstacles
spacing=50         #Spacing if randomspacing is set to False

#INITIALIZATION
orig_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)
d = l+1
obstacles=[]
out = list((" "*l+"\n")*b)
gout = list((gchr*(l-2)+"\n")*2)
stopgame=False
u = ul
keyRead=threading.Thread(target=keyread)
groundMove=threading.Thread(target=moveObs)
assign(range(pi+1+u*d,pi+3+u*d))
assign(range(pi+d+u*d,pi+4+d+u*d))
assign(range(pi+2*d+u*d,pi+4+2*d+u*d))
ducking=False
jumping=False
ducked=0
keyRead.daemon=True
groundMove.daemon=True
keyRead.start()
groundMove.start()
key=0
score=0

#MAIN LOOP
while True:
    if u == ul:
        if key == " " or key == "w":
            jumping=True
            mag=jmag
            acc=gravity
            upcomplete,downcomplete=False,True
        if key == "s":
            ducking=True
            ducked=0
    key=0
    if ducking:
        delete(range(pi+1+u*d,pi+3+u*d))
        ducked+=1

    if ducked == 15:
        ducking=False
        assign(range(pi+1+u*d,pi+3+u*d))

    if jumping:
        if not upcomplete:
            for i in range(int(mag)):
                move("up")
            mag-=acc

        if mag <= 1:
            upcomplete=True
            downcomplete=False

        if not downcomplete:
            for i in range(int(mag)):
                move("down")
            mag+=acc

        if u==ul:
            downcomplete=True
            upcomplete=True
            jumping=False
    if collision():
        sleep(0.005)
        stopgame=True
        sleep(0.1)
        print("\n"+" "*(l//2-5)+"GAME OVER!")

        if not path.isfile("hs"):
            with open("hs","w") as f:
                pass

        with open("hs","r") as f:
            hs = f.read()
            if hs != "":
                hs = int(hs)
            else:
                hs=score

        if score//10>=hs//10:
            hs=score
            with open("hs","w") as f:
                f.write(str(hs))
            print(" "*(l//2-7)+"NEW HIGHSCORE!")
        print(" "*(l//2-7)+"Highscore:",hs//10)
        input(" "*(l//2-23)+"Press Enter 2 times to Restart, Ctrl+c to exit")
        u=ul
        obstacles=[]
        out = list((" "*l+"\n")*b)
        assign(range(pi+1+u*d,pi+3+u*d))
        assign(range(pi+d+u*d,pi+4+d+u*d))
        assign(range(pi+2*d+u*d,pi+4+2*d+u*d))
        jumping=False
        stopgame=False
        obstacles.append(Obstacle())
        score=0
        gmag=0.01
        pmag=0.05

    sleep(pmag)
