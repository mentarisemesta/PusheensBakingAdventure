#add_library('sound')
import os

path = os.getcwd()
print path

class Game:
    def __init__(self):
        self.w=1280
        self.h=720
        self.g=720-137
        self.stage = 1
        self.paused=False
        self.state = "menu"
        self.startImage=[]
         
    def createGame(self):
        self.platforms=[]
        self.bgImgs=[]
        self.x=0
        self.food=[]
        self.trash=[]
        self.score = 0
        self.cnt = 0
        self.time = 60
        for i in range(1):
            self.bgImgs.append(loadImage(path+'/superMarioRes/bgImg.png'))
            #self.bgImgs.append(loadImage(path+'/superMarioRes/layer_0'+str(i+1)+'.png'))
        
        #self.bgMusic=SoundFile(this, path+"/superMarioRes/backgroundMusic.mp3")
        #self.bgMusic.amp(0.5)
        #self.bgMusic.play()

        f = open(path+"/superMarioRes/stage"+str(self.stage)+".csv","r")
        for item in f:
            item = item.strip().split(",")
            if item[0] == "Mario":
                self.mario = Mario(int(item[1]),int(item[2]),int(item[3]),int(item[4]),item[5],int(item[6]))
            elif item[0] == "Butter":
                self.food.append(Butter(int(item[1]),int(item[2]),int(item[3]),int(item[4]),item[5],int(item[6])))
            elif item[0] == "Flour":
                self.food.append(Flour(int(item[1]),int(item[2]),int(item[3]),int(item[4]),item[5],int(item[6])))
            elif item[0] == "Sugar":
                self.food.append(Sugar(int(item[1]),int(item[2]),int(item[3]),int(item[4]),item[5],int(item[6])))
            elif item[0] == "Egg":
                self.food.append(Sugar(int(item[1]),int(item[2]),int(item[3]),int(item[4]),item[5],int(item[6])))
            elif item[0] == "Chocolate":
                self.food.append(Sugar(int(item[1]),int(item[2]),int(item[3]),int(item[4]),item[5],int(item[6])))
            elif item[0] == "Cherry":
                self.food.append(Sugar(int(item[1]),int(item[2]),int(item[3]),int(item[4]),item[5],int(item[6])))
            elif item[0] == "Yoghurt":
                self.food.append(Sugar(int(item[1]),int(item[2]),int(item[3]),int(item[4]),item[5],int(item[6])))
            elif item[0] == "Carrot":
                self.food.append(Sugar(int(item[1]),int(item[2]),int(item[3]),int(item[4]),item[5],int(item[6])))
            elif item[0] == "Cheese":
                self.food.append(Sugar(int(item[1]),int(item[2]),int(item[3]),int(item[4]),item[5],int(item[6])))
            elif item[0] == "Trash":
                self.trash.append(Trash(int(item[1]),int(item[2]),int(item[3]),int(item[4]),item[5],int(item[6])))
            elif item[0] == "Platform":
                self.platforms.append(Platform(int(item[1]),int(item[2]),int(item[3]),int(item[4]),item[5]))                                          
            elif item[0] == "End":
                self.stage_x_end = int(item[1])
        f.close()

    def display(self):
        self.cnt  = (self.cnt + 1)%60
        if self.cnt == 0:
            self.time-=1
        cnt = 0
        for img in self.bgImgs[::-1]:
            if cnt == 0:
                x = (self.x//10)%self.w
            elif cnt == 1:
                x = (self.x//5)%self.w
            elif cnt == 2:
                x = (self.x//3)%self.w
            elif cnt == 3:
                x = (self.x//2)%self.w
            else:
                x = (self.x)%self.w
                
            image(img,0,0,self.w-x,self.h,x,0,self.w,self.h)
            # image(img,self.w-x-1,0,x,self.h,0,0,x,self.h)
            cnt+=1
            
        #stroke(255)
        #line(0,self.g,self.w,self.g)
        
        for f in self.food:
            f.display()
            
        for t in self.trash:
            t.display()    
            
        for p in self.platforms:
            p.display()
            
        self.mario.display()
        fill(255)
        textSize(32)
        text(str(self.score), 10, 25)
        text(str(self.time), 10, 50)
        
        #if self.mario.x >= self.stage_x_end:
         #   self.stage += 1
          #  self.createGame()

class Creature:
    def __init__(self,x,y,r,g,imgName,F):
        self.x=x
        self.y=y
        self.r=r
        self.w=self.r*2
        self.h=self.r*2
        self.vx=0
        self.vy=0
        self.F=F # max number of frames
        self.f=0 # current frame
        self.g=g
        self.dir=1
        self.img = loadImage(imgName)
        self.jump = 0
        
    def gravity(self):
        if self.y+self.r < self.g:
            self.vy+=0.1
            
            if self.y+self.r+self.vy > self.g:
                self.vy = self.g-self.y-self.r
        else:
            self.vy=0
            self.jump=0
            #self.y = self.g-self.r
            
        # adjusting the character ground
        for p in game.platforms:
            if self.x+self.r >= p.x and self.x-self.r <= p.x+p.w and self.y+self.r <= p.y:
                self.g = p.y
                break
            else:
                self.g=game.g
    
    def update(self):
        self.gravity()
        self.x+=self.vx
        self.y+=self.vy    
        
    def display(self):
        self.update()
        
        if self.vx != 0:
            self.f = (self.f+0.1)%self.F
            
        noStroke()
        noFill()
        ellipse(self.x-game.x,self.y,self.r*2,self.r*2)
        noStroke()
        line(self.x-self.r-game.x,self.g,self.x+self.r-game.x,self.g)
        
        if self.dir > 0:
            image(self.img,self.x-self.r-game.x,self.y-self.r,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h)
        else:
            image(self.img,self.x-self.r-game.x,self.y-self.r,self.w,self.h,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h)
         
class Mario(Creature):
    def __init__(self,x,y,r,g,imgName,F):
        Creature.__init__(self,x,y,r,g,imgName,F)
        
        self.keyHandler={LEFT:False,RIGHT:False,UP:False,"P":False}
        #self.jumpSound = SoundFile (this, path+"/superMarioRes/jump.mp3") 
        #self.killSound = SoundFile (this, path+"/superMarioRes/kill.mp3")
    
    def update(self):
        self.gravity()
        
        if self.keyHandler[LEFT]:
            self.vx = -2
            self.dir = -1
        elif self.keyHandler[RIGHT]:
            self.vx = 2
            self.dir = 1
        else:
            self.vx = 0
            
        if self.keyHandler[UP] and self.jump < 2 and self.vy >= 0:
            self.vy = -6.5
            #self.jumpSound.play()
            self.jump+=1
        
        self.x+=self.vx
        self.y+=self.vy 
        
        if self.x >= game.w//2:
            game.x += self.vx
            
        #collision detection
        for f in game.food:
            if self.distance(f) < self.r+f.r:
                game.food.remove(f)
                del f
                game.score += 10
                
        for t in game.trash:
            if self.distance(t) < self.r+t.r:
                game.trash.remove(t)
                del t
                exit()

    def distance(self,other):
        return((self.x-other.x)**2+(self.y-other.y)**2)**0.5
    
class Platform:
    def __init__(self,x,y,w,h,img):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.img=loadImage(path+'/'+img)
    
    def display(self):
        image(self.img,self.x-game.x,self.y)

class Butter(Creature):
    def __init__(self,x,y,r,g,imgName,F):
        Creature.__init__(self,x,y,r,g,imgName,F)
        self.vx = 1
        self.x1=self.x-100
        self.x2=self.x+100
        
    def update(self):
        self.gravity()
        
        if self.x < self.x1:
            self.vx = 1
            self.dir = 1
        elif self.x > self.x2:
            self.vx=-1
            self.dir=-1
            
        self.x+=self.vx
        self.y+=self.vy

class Sugar(Creature):
    def __init__(self,x,y,r,g,imgName,F):
        Creature.__init__(self,x,y,r,g,imgName,F)
        self.vx = 1
        self.x1=self.x-100
        self.x2=self.x+100
        
    def update(self):
        self.gravity()
        
        if self.x < self.x1:
            self.vx = 1
            self.dir = 1
        elif self.x > self.x2:
            self.vx=-1
            self.dir=-1
            
        self.x+=self.vx
        self.y+=self.vy
        
class Egg(Creature):
    def __init__(self,x,y,r,g,imgName,F):
        Creature.__init__(self,x,y,r,g,imgName,F)
        self.vx = 1
        self.x1=self.x-100
        self.x2=self.x+100
        
    def update(self):
        self.gravity()
        
        if self.x < self.x1:
            self.vx = 1
            self.dir = 1
        elif self.x > self.x2:
            self.vx=-1
            self.dir=-1
            
        self.x+=self.vx
        self.y+=self.vy

class Chocolate(Creature):
    def __init__(self,x,y,r,g,imgName,F):
        Creature.__init__(self,x,y,r,g,imgName,F)
        self.vx = 1
        self.x1=self.x-100
        self.x2=self.x+100
        
    def update(self):
        self.gravity()
        
        if self.x < self.x1:
            self.vx = 1
            self.dir = 1
        elif self.x > self.x2:
            self.vx=-1
            self.dir=-1
            
        self.x+=self.vx
        self.y+=self.vy
        
class Sugar(Creature):
    def __init__(self,x,y,r,g,imgName,F):
        Creature.__init__(self,x,y,r,g,imgName,F)
        self.vx = 1
        self.x1=self.x-100
        self.x2=self.x+100
        
    def update(self):
        self.gravity()
        
        if self.x < self.x1:
            self.vx = 1
            self.dir = 1
        elif self.x > self.x2:
            self.vx=-1
            self.dir=-1
            
        self.x+=self.vx
        self.y+=self.vy
        
class Flour(Creature):
    def __init__(self,x,y,r,g,imgName,F):
        Creature.__init__(self,x,y,r,g,imgName,F)
        self.vx = 1
        self.x1=self.x-100
        self.x2=self.x+100
        
    def update(self):
        self.gravity()
        
        if self.x < self.x1:
            self.vx = 1
            self.dir = 1
        elif self.x > self.x2:
            self.vx=-1
            self.dir=-1
            
        self.x+=self.vx
        self.y+=self.vy

class Trash(Creature):
    def __init__(self,x,y,r,g,imgName,F):
        Creature.__init__(self,x,y,r,g,imgName,F)
        self.vx = 1
        self.x1=self.x-100
        self.x2=self.x+100
        
    def update(self):
        self.gravity()
        
        if self.x < self.x1:
            self.vx = 1
            self.dir = 1
        elif self.x > self.x2:
            self.vx=-1
            self.dir=-1
            
        self.x+=self.vx
        self.y+=self.vy
    
game = Game()

def setup():
    size(game.w,game.h)
    game.createGame()
    img = loadImage(path+"/superMarioRes/startImage.png")
    background(img)
    
def draw():
    if game.state=='menu':
        if game.state=="menu" and game.w//2-150<= mouseX <= game.w//2+160 and game.h//2-30 <= mouseY <= game.h//2+10:
            fill(0)
        else:
            fill(255)
        textSize(64)
        text("Play Game",game.w//2-150,game.h//2)
        noFill()
        stroke(255)
    elif game.state == 'play':
        if not game.paused:
            background("#ffd1dc")
            game.display()
        else:
            fill(255,0,0)
            textSize(32)
            text("Pause",game.w//2,game.h//2)
        
def keyPressed():
    print (keyCode)
    game.mario.keyHandler[keyCode]=True
    if keyCode == 80:
        game.paused = not game.paused

def keyReleased():
    game.mario.keyHandler[keyCode]=False
    
def mouseClicked():
    if game.state=="menu" and game.w//2 <= mouseX <= game.w//2+160 and game.h//2-30 <= mouseY <= game.h//2+10:
        game.state="play"
    
