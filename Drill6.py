from pico2d import *
from collections import deque

TUK_WIDTH,TUK_HEIGHT = 1280,1024

open_canvas(1280,1024)

back_ground = load_image('TUK_GROUND.png')

class Hand:
    def __init__(self,x,y):
        self.pos =[x,y]
        self.handImg = load_image('hand_arrow.png')
    def Render(self):
        self.handImg.draw(self.pos[0],self.pos[1])

class Boy:
    def __init__(self):
        self.pos = [TUK_WIDTH//2, TUK_HEIGHT//2]
        self.boyImg = load_image('animation_sheet.png')
        self.frame = 0
        self.targetDir = [1,1]
        self.dir = 1
        self.length = 0
        self.speed = 500
        self.handQueue = deque()
        self.target = 0
        self.animMap = {
            0 : self.run_right,
            1:  self.run_left
        }
    def run_right(self,frame):
        self.boyImg.clip_draw(frame * 100, 100, 100, 100, self.pos[0], self.pos[1]),
    def run_left(self,frame):
        self.boyImg.clip_draw(frame * 100, 0, 100, 100, self.pos[0], self.pos[1])
    def Update(self):
        if 0 >= self.length:
            return
        dx = self.targetDir[0] * self.speed * 0.02
        dy = self.targetDir[1] * self.speed * 0.02
        self.pos[0] += dx
        self.pos[1] += dy
        self.length -= math.sqrt(dx ** 2 + dy ** 2)
    def Render(self):
        for hand in self.handQueue:
            hand.Render()
        self.animMap[self.dir](self.frame)
        self.frame = (self.frame + 1) % 8
    def StartChase(self):
        self.target = self.handQueue[0]
        dx = self.target.pos[0] - self.pos[0]
        dy = self.target.pos[1] - self.pos[1]
        self.length = math.sqrt(dx ** 2 + dy ** 2)
        self.targetDir[0] = dx / self.length
        self.targetDir[1] = dy / self.length
        if self.targetDir[0] > 0:
            self.dir = 0
        else:
            self.dir = 1
        self.frame = 0
    def CheckArrive(self):
        if 0 >= self.length :
            if self.handQueue:
                self.handQueue.popleft()
            if self.handQueue:
                self.StartChase()
    def AddHand(self,x,y):
        self.handQueue.append(Hand(x,y))
        self.StartChase()


def handle_event():
    global boy
    global mainHand
    for eve in get_events():
        if eve.type == SDL_KEYDOWN:
            if eve.key == SDLK_ESCAPE:
                return False
        elif eve.type == SDL_MOUSEBUTTONDOWN:
            boy.AddHand(eve.x ,TUK_HEIGHT - eve.y )
        elif eve.type == SDL_MOUSEMOTION:
            mainHand.pos[0] = eve.x
            mainHand.pos[1] = TUK_HEIGHT - eve.y
    return True
boy = Boy()
mainHand = Hand(0,0)
hide_cursor()
while handle_event():
    back_ground.draw(TUK_WIDTH//2,TUK_HEIGHT//2)
    boy.Update()
    boy.Render()
    mainHand.Render()
    update_canvas()
    boy.CheckArrive()
    clear_canvas()
    delay(0.02)

close_canvas()