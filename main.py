#C:\Users\0737772\Documents\Python\Pong.py

# https://mcsp.wartburg.edu/zelle/python/graphics/graphics/node3.html

# Basic key pressed detection
# if msvcrt.kbhit():
#        key = chr(msvcrt.getch()[0])
#        print("Key pressed: %s" % msvcrt.getch())
import socket
import keyboard
from playsound import playsound
from threading import Thread
import winsound
import keyboard  # using module keyboard
import time
import tkinter as tk
#pip install graphics.py
from graphics import *
import msvcrt

deltaTime = 1.0

class Window(GraphWin):
    def __init__(self, title="Graphics Window",
                 width=200, height=200, autoflush=True):
        super().__init__(title, width, height, autoflush)

class KeyRepeater(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current = {}
        self.functions = {}
        self.bind("<KeyPress>", self.keydown, add="+")
        self.bind("<KeyRelease>", self.keyup, add="+")
        self.key_loop()
    def key_loop(self):
        # list makes a copy to avoid changing arr size during loop
        for function in list(self.current.values()):
            if function:
                function()
        self.after(40, self.key_loop) # set repeat time here.
    def key_bind(self, key, function):
        self.functions[key]=function
    def keydown(self, event=None):
        if event.keysym in self.functions:
            self.current[event.keysym]=self.functions.get(event.keysym)
    def keyup(self, event=None):
        self.current.pop(event.keysym,None)


win = Window(width = 1000, height = 500) # create a window
#win.canvas.cords()
win.setBackground("white")
screenW = 100
screenH = 50
win.setCoords(0, 0, screenW, screenH) # set the coordinates of the window; bottom left is (0, 0) and top right is (10, 10)
win.checkMouse() 

# Variables for multiplayer
plyrNum = 0 # Multiplayer player num
UDP_IP = "127.0.0.1"
UDP_Init_Port = 5000
UDP_P1_PORT = 5005
UDP_P2_PORT = 5010
UDP_Output_Port = -1
UDP_Input_Port = -1
InSock = 0
OutSock = 0

PhysicsSpeed = 1 # Change this to account for differences in processor tick speed

p1Y = 0.0
p2Y = 0.0
p1_score = 0
p2_score = 0

Ball_Veloc_X = .08
Ball_Veloc_Y = 0

# Puts ball in the center of the screen
Ball_Pos_X = screenW / 2
Ball_Pos_Y = screenH / 2

# Pong prototype
#def ai_turn():

# https://stackoverflow.com/questions/13207678/whats-the-simplest-way-of-detecting-keyboard-input-in-a-script-from-the-terminal

class ThreadWithReturnValue(Thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

'''
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen. From http://code.activestate.com/recipes/134892/"""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            try:
                self.impl = _GetchMacCarbon()
            except(AttributeError, ImportError):
                self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys, termios # import termios now or else you'll get the Unix version on the Mac

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

class _GetchMacCarbon:
    """
    A function which returns the current ASCII key that is down;
    if no ASCII key is down, the null string is returned.  The
    page http://www.mactech.com/macintosh-c/chap02-1.html was
    very helpful in figuring out how to do this.
    """
    def __init__(self):
        import Carbon
        Carbon.Evt #see if it has this (in Unix, it doesn't)

    def __call__(self):
        import Carbon
        if Carbon.Evt.EventAvail(0x0008)[0]==0: # 0x0008 is the keyDownMask
            return ''
        else:
            #
            # The event contains the following info:
            # (what,msg,when,where,mod)=Carbon.Evt.GetNextEvent(0x0008)[1]
            #
            # The message (msg) contains the ASCII char which is
            # extracted with the 0x000000FF charCodeMask; this
            # number is converted to an ASCII character with chr() and
            # returned
            #
            (what,msg,when,where,mod)=Carbon.Evt.GetNextEvent(0x0008)[1]
            return chr(msg & 0x000000FF)


def getKey():
    inkey = _Getch()
    import sys
    for i in xrange(sys.maxint):
        k=inkey()
        if k<>'':break

    return k
'''


def clear(my_win):
    for item in win.items[:]:
        item.undraw()
    my_win.update()

def clamp(Input, LB, UB):
    val = Input
    if (val > UB):
        val = UB
    elif (val < LB):
        val = LB
    return val

def establishConnection():

    global plyrNum
    plyrNum = 0 # Multiplayer player num
    global UDP_IP
    UDP_IP = "127.0.0.1"
    global UDP_Init_Port
    UDP_Init_Port = 5000
    global UDP_P1_PORT
    UDP_P1_PORT = 5005
    global UDP_P2_PORT
    UDP_P2_PORT = 5010
    global UDP_Output_Port
    UDP_Output_Port = 5005
    global UDP_Input_Port
    UDP_Input_Port = 5010
    
    global InSock
    global OutSock

    try:
        InSock = socket.socket(socket.AF_INET, # Internet
                socket.SOCK_DGRAM) # UDP
        InSock.bind((UDP_IP, UDP_Input_Port))
        print("Success")
        plyrNum = 1
        print("1\n")
        UDP_Output_Port = 5005
        UDP_Input_Port = 5010
    except:
        plyrNum = 2
        print("2\n")
        UDP_Output_Port = 5010
        UDP_Input_Port = 5005

        InSock = socket.socket(socket.AF_INET, # Internet
                socket.SOCK_DGRAM) # UDP
        InSock.bind((UDP_IP, UDP_Input_Port))

    print(f"P{plyrNum} Client Listening")
    
    OutSock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
    InSock.settimeout(0) # Prevents program from hanging if no data is recieved

def getMultiplayerData():
    InSock.settimeout(0) # Prevents program from hanging if no data is recieved

    data = "No Connection"
    try:
        data = InSock.recv(1024)
        data = (data).decode('utf8') # Converts byte string to string
    except:
        print("No Connection")
    
    return data

def sendMultiplayerData(data):
    OutSock = socket.socket(socket.AF_INET, # Internet
                socket.SOCK_DGRAM) # UDP
    data = bytes(data, 'utf-8')
    OutSock.sendto(data, (UDP_IP, UDP_Output_Port))

# Handles sound so that it doesn't pause program
def playy():
    #print("A sound is supposed to play")
    playsound("PongSoundWAV.wav", block = True)

Texts = []
#Asks user if they want to play against AI
PVP_Text = Text(Point(screenW / 2, screenH / 2 + 7), "Player vs Player")
PVP_Text.setSize(30)
PVP_Text.draw(win)
AI_Text = Text(Point(screenW / 2, screenH / 2), "Player vs Computer")
AI_Text.setSize(30)
AI_Text.draw(win)
Mult_Text = Text(Point(screenW / 2, screenH / 2 - 7), "Multiplayer")
Mult_Text.setSize(30)
Mult_Text.draw(win)

for i in range(0,3):
    myBox = Rectangle(Point(screenW / 2 - 25, screenH / 2 + 7 - (i*7) + 3), Point(screenW / 2 + 25, screenH / 2 + 7 - (i*7) - 3))
    myBox.draw(win)

gamemode = 0 # 0 = PVP, 1 = PVC, 2: LAN Multiplayer
BufferBool = False
while BufferBool == False:
    if win.isOpen:
        clickPoint = win.getMouse()
        if clickPoint.getX() > screenW / 2 - 25 and clickPoint.getX() < screenW / 2 + 25:
            for i in range(0,3):
                if clickPoint.getY() < screenH / 2 + 7 - (i*7) + 3 and clickPoint.getY() > screenH / 2 + 7 - (i*7) - 3:
                    gamemode = i
                    BufferBool = True
                    clear(win)
                    break

paddleH = 1*(screenH/5)
paddleW = screenW*.02
offsetX = screenW*.05

def calc_AI_move():
    global Ball_Pos_X
    global Ball_Pos_Y
    global Ball_Veloc_X
    global Ball_Veloc_Y
    distance_From_Paddle_X = screenW - offsetX
    Y_at_X = Ball_Pos_Y - Ball_Veloc_Y * distance_From_Paddle_X
    new_Ypos = Y_at_X + PongBallRadius
    return new_Ypos


shapes = [0,0,0]

def drawPaddle(playerNum):
    global p1Y
    global p2Y
    Ypos = 0.0
    if (playerNum == 1):
        if shapes[0] != 0:
            shapes[0].undraw() # Undraws previously drawn shape
        Ypos = p1Y
    else:
        if shapes[1] != 0:
            shapes[1].undraw() # Undraws previously drawn shape
        Ypos = p2Y
    midpoint = screenH / 2
    offset = (midpoint - paddleH / 2) * Ypos
    #print("Y1", midpoint - (paddleH/2) + offset)
    #print("Y2", midpoint + (paddleH/2) + offset)
    X1 = 0.0
    X2 = 0.0
    if playerNum == 1:
        X1 = offsetX
        X2 = offsetX+paddleW
    else:
        X1 = screenW - offsetX-paddleW
        X2 = screenW - offsetX

    mySquare = Rectangle(Point(X1, midpoint - (paddleH/2) + offset), Point(X2, midpoint + (paddleH/2) + offset)) # create a rectangle from (1, 1) to (9, 9)

    if playerNum == 1:
        shapes[0] = mySquare
    else:
        shapes[1] = mySquare

    #mySqaure = Rectangle(Point(1, 1), Point(1.3, 2))
    mySquare.draw(win) # draw it to the window
    #win.getMouse()

def resetScene():
    global Ball_Veloc_X
    global Ball_Veloc_Y
    global Ball_Pos_X
    global Ball_Pos_Y
    global p1Y
    global p2Y
    Ball_Pos_X = screenW / 2
    Ball_Pos_Y = screenH/2
    shapes[2].undraw()
    myCircle = Circle(Point(Ball_Pos_X, Ball_Pos_Y), PongBallRadius)
    myCircle.draw(win) # draw it to the window
    shapes[2] = myCircle
    Ball_Veloc_X = .1
    Ball_Veloc_Y = 0
    p1Y = 0
    p2Y = 0
    drawPaddle(1)
    drawPaddle(2)
    
PongBallRadius = 1

buffer1 = False # Prevents it adding more score than it should due to double or triple hits
buffer2 = False
def drawPongBall():
    # clears old ball
    #if shapes[2] != 0:
        #shapes[2].undraw() # Undraws previously drawn shape
    
    global buffer1
    global buffer2
    global Ball_Veloc_X
    global Ball_Veloc_Y
    global Ball_Pos_X
    global Ball_Pos_Y
    global screenW
    global screenH
    global p1_score
    global p2_score
    midpoint = screenH / 2
    offset1 = (midpoint - paddleH / 2) * p1Y + midpoint - (paddleH / 2)
    offset2 = (midpoint - paddleH / 2) * p2Y + midpoint - (paddleH / 2)

    X = Ball_Pos_X
    Y = Ball_Pos_Y

    R = PongBallRadius
    # Checks for top border collision
    if (Y+R >= screenH or Y+R <= 0):
        if (Y+R >= screenH):
            Ball_Pos_Y = 1
        if (Y+R <= 0):
            Ball_Pos_Y = 0
        #Ball_Veloc_X *= -1
        Ball_Veloc_Y *= -1
        #Ball_Veloc_Y += 1
        buffer1 = True
    # Checks for side border collision
    # Left side hit
    if (X+R >= screenW):
        buffer1 = True
        p1_score += 1
        resetScene()
    # Right side hit
    if (X+R <= 0):
        buffer1 = True
        p2_score += 1
        resetScene()
    if buffer1 == True and not ((X+R >= screenW or X+R <= 0)):
        buffer1 = False
    # Checks for collision with paddle
    #print("X",X,"X1:",offsetX+paddleW,"Offset1:", offset1,"PaddleW:", paddleW)

    paddle1Hit = (Y-R <= offset1+paddleH and Y+R >= offset1 and X-R <= offsetX+paddleW and X+R >= offsetX)
    paddle2Hit = (Y-R <= offset2+paddleH and Y+R >= offset2 and X-R <= (screenW-offsetX)+paddleW and X+R >= (screenW-offsetX)-paddleW)
    ifBuffer = paddle1Hit or paddle2Hit

    diff = 0.0
    if paddle1Hit:
        #stop_threads = False
        playsound('PongSoundWAV.wav', False)
        T = Thread(target=playy) # create thread
        T.start() # Launch created thread
        
        diff = (Ball_Pos_Y + PongBallRadius) - (p1Y * (screenH/2) + midpoint)
    elif paddle2Hit:
        #stop_threads = False
        T = Thread(target=playy) # create thread
        T.start() # Launch created thread
    
        diff = (Ball_Pos_Y + PongBallRadius) - (p2Y * (screenH/2) + midpoint)

    #ifBuffer = Y-R <= offset1+paddleH and Y+R >= offset1 and X-R <= offsetX+paddleW and X+R >= offsetX
    #print((screenW-offsetX)+paddleW, (screenW-offsetX)-paddleW, X)
    if ifBuffer and buffer2 == False:
        #print(Ball_Pos_Y, (p2Y * (screenH/2))+midpoint)
        Ball_Veloc_X *= -1
        Ball_Veloc_Y *= -1
        Ball_Veloc_Y -= (diff / 100)
        Ball_Veloc_Y *= .3
        buffer2 = True
    elif buffer2 and ifBuffer == False:
        buffer2 = False

    # Clamps veloc so it that the ball can't become outragely fast
    Ball_Veloc_X = clamp(Ball_Veloc_X, -.015, .015)
    #print(Ball_Veloc_X)
    Ball_Veloc_Y = clamp(Ball_Veloc_Y, -.007, .007)
    # Moves ball
    if gamemode == 0:
        Ball_Pos_X += Ball_Veloc_X * deltaTime * 4000
        Ball_Pos_Y += Ball_Veloc_Y * deltaTime * 4000

    #print("X: ", Ball_Pos_X, "Y: ", Ball_Pos_Y)
    if shapes[2] == 0:
        myCircle = Circle(Point(Ball_Pos_X, Ball_Pos_Y), PongBallRadius)
        myCircle.draw(win) # draw it to the window
        shapes[2] = myCircle
        #print(myCircle.getP1().getX()) - how to getX of circle
        #print(myCircle.getP1().getY())
        #myCircle.move(.5,0)
    else:
        shapes[2].move(Ball_Veloc_X * deltaTime * 4000, Ball_Veloc_Y * deltaTime * 4000)

    Ball_Pos_X = shapes[2].getP1().getX()
    Ball_Pos_Y = shapes[2].getP1().getY()

#def renderBoard():
#mySquare = Rectangle(Point(1, 1), Point(2, 2))
#mySquare.draw(win)
#win.getMouse() # pause before closing

#drawPaddle(1)
#drawPaddle(2)

Player1_Keys = ['w','s']
Player2_Keys = ['o','k']

drawPaddle(1)
drawPaddle(2)

move_increment = 1

def moveP1_UP():
    global p1Y
    p1Y += move_increment * deltaTime
    drawPaddle(1)
def moveP1_Down():
    global p1Y
    p1Y -= move_increment * deltaTime
    drawPaddle(1)
def moveP2_UP():
    global p2Y
    p2Y += move_increment * deltaTime
    drawPaddle(2)
def moveP2_Down():
    global p2Y
    p2Y -= move_increment * deltaTime
    drawPaddle(2)

'''
if gamemode == 0: # Local
    inputWin.key_bind(Player1_Keys[0], moveP1_UP)
    inputWin.key_bind(Player1_Keys[1], moveP1_Down)
    inputWin.key_bind(Player2_Keys[0], moveP2_UP)
    inputWin.key_bind(Player2_Keys[1], moveP2_Down)
elif gamemode == 1:
    inputWin.key_bind(Player1_Keys[0], moveP1_UP)
    inputWin.key_bind(Player1_Keys[1], moveP1_Down)
elif gamemode == 2:
    establishConnection() # Initalizes Multiplayer Connection
    if plyrNum == 1:
        inputWin.key_bind(Player1_Keys[0], moveP1_UP)
        inputWin.key_bind(Player1_Keys[1], moveP1_Down)
    else:
        inputWin.key_bind(Player1_Keys[0], moveP2_Down)
        inputWin.key_bind(Player1_Keys[1], moveP2_UP)
'''
if (gamemode == 2):
    establishConnection() # Initalizes Multiplayer Connection
#inputWin.mainloop()
oldPC_Y = p2Y
old_P1_Score = -1
old_P2_Score = -1
oldTime = time.time()
count = 0
text_objects = [0,0]
while (not (p1_score > 9 or p2_score > 9)):
    if gamemode == 0: # Local
        if keyboard.is_pressed(Player1_Keys[0]):
            moveP1_UP()
        if keyboard.is_pressed(Player1_Keys[1]):
            moveP1_Down()
        if keyboard.is_pressed(Player2_Keys[0]):
            moveP2_UP()
        if keyboard.is_pressed(Player2_Keys[1]):
            moveP2_Down()
    elif gamemode == 1:
        if keyboard.is_pressed(Player1_Keys[0]):
            moveP1_UP()
        if keyboard.is_pressed(Player1_Keys[1]):
            moveP1_Down()
    elif gamemode == 2:
        establishConnection() # Initalizes Multiplayer Connection
        if plyrNum == 1:
            if keyboard.is_pressed(Player1_Keys[0]):
                moveP1_UP()
            if keyboard.is_pressed(Player1_Keys[1]):
                moveP1_Down()
        else:
            if keyboard.is_pressed(Player2_Keys[0]):
                moveP2_UP()
            if keyboard.is_pressed(Player2_Keys[1]):
                moveP2_Down()
    count += 1
    if count > 125:
        count = 0
    #if keyboard.is_pressed():  # if key 'q' is pressed 
        #print('You Pressed A Key!')
    pt = win.checkMouse() # Prevents the lagging circle of death
    if gamemode == 1 :
        if count == 75: # Do it at increments to avoid a flickering effect
            if oldPC_Y != p2Y: # Updates computers paddle
                drawPaddle(2)
            oldPC_Y = p2Y
            p2Y = clamp(calc_AI_move() / (screenH *.5) - 1,p2Y-(45*deltaTime),p2Y+(45*deltaTime))
    elif gamemode == 2 and count == 125:
        if plyrNum == 1:
            sendMultiplayerData(str(p1Y) + '\n' + str(p1_score) + '\n' + str(p2_score) + '\n' + str(Ball_Pos_X) + '\n' + str(Ball_Pos_Y) + '\n' + str(Ball_Veloc_X) + '\n' + str(Ball_Veloc_Y))
            t1 = ThreadWithReturnValue(target=getMultiplayerData)
            t1.start()
            data = t1.join()
            dataArr = [] # Stores Data: p1Y, p1_score, p2_score
            dataArr.clear()
            if data != "No Connection":
                bufferSTR = ""
                for i in range(0,len(data)):
                    if data[i] == '\n':
                        dataArr.append((bufferSTR))
                        bufferSTR = ""
                    bufferSTR += (data[i])
                dataArr.append(bufferSTR)
                p2Y = float((dataArr[0]))
                #p2_score = int(dataArr[1])
                drawPaddle(2)
            else:
                Ball_Pos_X = screenW/2
                Ball_Pos_Y = screenH/2
                Ball_Veloc_Y = 0
        else:
            sendMultiplayerData(str(p2Y))
            t1 = ThreadWithReturnValue(target=getMultiplayerData)
            t1.start()
            data = t1.join()
            dataArr = [] # Stores Data: p1Y, p1_score, p2_score
            dataArr.clear()
            if data != "No Connection":
                bufferSTR = ""
                for i in range(0,len(data)):
                    if data[i] == '\n':
                        dataArr.append((bufferSTR))
                        bufferSTR = ""
                    bufferSTR += (data[i])
                dataArr.append(bufferSTR)
                p1Y = float((dataArr[0]))
                p1_score = int(dataArr[1])
                p2_score = int(dataArr[2])
                Ball_Pos_X = float((dataArr[3]))
                Ball_Pos_X = float((dataArr[4]))
                Ball_Veloc_X = float((dataArr[5]))
                Ball_Veloc_Y = float((dataArr[6]))
                drawPaddle(1)
                drawPaddle(2)
            else:
                Ball_Pos_X = screenW/2
                Ball_Pos_Y = screenH/2
                Ball_Veloc_Y = 0
        


    # draws scores to screen
    if p1_score != old_P1_Score and count == 125:
        if text_objects[0] != 0:
            text_objects[0].undraw() # Removes old text
        P1_Text = Text(Point(screenW *.45, screenH * .95), p1_score)
        P1_Text.setSize(30)
        P1_Text.draw(win)
        text_objects[0] = (P1_Text)
        old_P1_Score = p1_score

    if p2_score != old_P2_Score and count == 125:
        if text_objects[1] != 0:
            text_objects[1].undraw() # Removes old text
        P2_Text = Text(Point(screenW *.55, screenH * .95), p2_score)
        P2_Text.setSize(30)
        P2_Text.draw(win)
        text_objects[1] = (P2_Text)
        old_P2_Score = p2_score
    if True:
        drawPongBall()

    deltaTime = time.time() - oldTime
    oldTime = time.time()
win.close()
