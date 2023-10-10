#C:\Users\0737772\Documents\Python\Pong.py

#pip install graphics.py
from graphics import *
import msvcrt
win = GraphWin(width = 1000, height = 500) # create a window
win.setCoords(0, 0, 20, 10) # set the coordinates of the window; bottom left is (0, 0) and top right is (10, 10)
win.getMouse() # pause before closing

screenH = 50
screenW = 100

p1_score = 0
p2_score = 0
p1Y = 0.0
p2Y = 0.0

Ball_Veloc_X = 0.0
Ball_Veloc_Y = 0.0

# Puts ball in the center of the screen
Ball_Pos_X = screenW / 2
Ball_Pos_Y = screenH / 2

# Pong prototype
#def ai_turn():

# https://stackoverflow.com/questions/13207678/whats-the-simplest-way-of-detecting-keyboard-input-in-a-script-from-the-terminal
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

def clamp(Input, LB, UB):
    val = Input
    if (val > UB):
        val = UB
    elif (val < LB):
        val = LB
    return val

paddleH = 1
'''
def drawPaddle(playerNum):
    Ypos = 0.0
    if (playerNum == 1):
        Ypos = p1Y
    else:
        Xpos = p1X
    midpoint = screenH / 2
    offset = (midpoint - paddleH / 2)  * Ypos
    #mySquare = Rectangle(Point(1, midpoint + (paddleH/2) + offset), Point(1.3, midpoint + (paddleH/2) + offset)) # create a rectangle from (1, 1) to (9, 9)
    mySqaure = Rectangle(Point(1, 1), Point(1.3, 2))
    mySquare.draw(win) # draw it to the window
    #win.getMouse()
'''
#def renderBoard():

#drawPaddle(1)
mySquare = Rectangle(Point(1, 1), Point(2, 2))
mySquare.draw(win)
#win.getMouse() # pause before closing

Player1_Keys = ['w','s']
Player2_Keys = ['o','k']
while (not (p1_score > 9 or p2_score > 9)):
    #print("Test")
    if msvcrt.kbhit():
        key = chr(msvcrt.getch()[0])
        #print("Key pressed: %s" % msvcrt.getch())
        
        if (key == Player1_Keys[0]):
            p1Y = clamp(p1Y + .05, 0, 1)
            print(f"{key}")
        elif key == Player1_Keys[1]:
             p1Y = clamp(p1Y - .05, 0, 1)
             print(f"{key}")
