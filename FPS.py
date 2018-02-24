###############################################################################
# Name:
#  _____              _      _   _  __     _       _                   _    _ 
# |  __ \            (_)    | | | |/ /    | |     | |                 | |  (_)
# | |  | | __ _ _ __  _  ___| | | ' /_   _| | __ _| | _____  _   _ ___| | ___ 
# | |  | |/ _` | '_ \| |/ _ \ | |  <| | | | |/ _` | |/ / _ \| | | / __| |/ / |
# | |__| | (_| | | | | |  __/ | | . \ |_| | | (_| |   < (_) | |_| \__ \   <| |
# |_____/ \__,_|_| |_|_|\___|_| |_|\_\__,_|_|\__,_|_|\_\___/ \__,_|___/_|\_\_|
# Due Date: January 25, 2016
# Description: 3D First Person Shooter Game
###############################################################################

import pygame
import math
from random import randint

pygame.font.init()
pygame.init
WIDTH = 900
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

crosshair = pygame.image.load("crosshair.png")
crosshair = crosshair.convert_alpha()
crosshair = pygame.transform.scale(crosshair, (25,25))

startScreen = pygame.image.load("startScreen.png")
startScreen = startScreen.convert_alpha()
startScreen = pygame.transform.scale(startScreen, (WIDTH,HEIGHT))

ak = pygame.image.load("ak.png")
ak = ak.convert_alpha()
ak = pygame.transform.scale(ak, (450,250))

bulletImpact = pygame.image.load("bullethole.png")
bulletImpact = bulletImpact.convert_alpha()
bulletImpact = pygame.transform.scale(bulletImpact, (10,10))

bottomStrip = pygame.image.load("bottomStrip.png")
bottomStrip = bottomStrip.convert_alpha()
bottomStrip = pygame.transform.scale(bottomStrip,(WIDTH,50))

target = pygame.image.load("bullseye.png")
target = target.convert_alpha()
targetW = 100
targetH = 100
target = pygame.transform.scale(target, (targetW,targetH))

bulletsCountFont = pygame.font.SysFont("Arial Black",20)
magazineCountFont = pygame.font.SysFont("Arial Black",15)

currentFrame = 1
frameCount = 0
reload = []

bullets  = 30
magazine = 90

for i in range(1,44):
    reload.append(pygame.image.load("frame"+str(i)+".png"))
    reload[i-1] = reload[i-1].convert_alpha()
    reload[i-1] = pygame.transform.scale(reload[i-1],(800,400))

bullet = []
bulletVisible = []

pygame.mouse.set_pos((WIDTH/2,HEIGHT/2))

forward = False
backward = False
left = False
right = False
crouch = False

distx = 0
disty = 0

distancex = 0
distancey = 0

start = False

cursorX = WIDTH/2
cursorY = HEIGHT/2

frontRectW = 300
frontRectH = 150
frontRectX = (WIDTH)+frontRectW/2
frontRectY = (HEIGHT)+frontRectH/2

topLeftStartX = -100
topLeftStartY = -100
topLeftEndX = frontRectX
topLeftEndY = frontRectY

topRightStartX = WIDTH
topRightStartY = -100
topRightEndX = frontRectX+frontRectW
topRightEndY = frontRectY

bottomRightStartX = WIDTH
bottomRightStartY = HEIGHT
bottomRightEndX = frontRectX+frontRectW
bottomRightEndY = frontRectY+frontRectH

bottomLeftStartX = -100
bottomLeftStartY = HEIGHT
bottomLeftEndX = frontRectX
bottomLeftEndY = frontRectY+frontRectH

shoot = False

reloading = False

topR = 255
topG = 255
topB = 255

startText = "Press Enter to Begin"
startColour = 255

shootCursorX = []
shootCursorY = []

change = 5
startFont = pygame.font.SysFont("Arial Black",30)

backwards = 205

def startScreennnnnn():
    global startColour
    global change
    
    screen.blit(startScreen,(0,0))
    startTextBlit = startFont.render(str(startText),1,(startColour,startColour,startColour))
    screen.blit(startTextBlit, (300,500))
    startColour -=change
    if(startColour<=0):
        change = -5
    elif(startColour>=255):
        change = 5

    pygame.mouse.set_visible(False)
    

class Bullet(object):
    def __init__(self,bulletX,bulletY):
        self.bulletX = bulletX
        self.bulletY = bulletY

    def draw(self,screen,bulletX,bulletY):
        screen.blit(bulletImpact,(bulletX,bulletY))

def redrawScreen():
    global currentFrame
    global reloading
    global bullets
    global magazine
    global newCoordinates
    global targetX
    global targetY

    screen.fill((255,255,255))

    frontRectX = -cursorX+distx
    frontRectY = -cursorY+disty
    topLeftEndX = -cursorX+distx
    topLeftEndY = -cursorY+disty
    topRightEndX = -cursorX+distx+frontRectW
    topRightEndY = -cursorY+disty
    bottomRightEndX = -cursorX+distx+frontRectW
    bottomRightEndY = -cursorY+disty+frontRectH
    bottomLeftEndX = -cursorX+distx
    bottomLeftEndY = -cursorY+disty+frontRectH

    #targetX = randint(frontRectX,frontRectX+frontRectW)
    #targetY = randint(frontRectY,frontRectY+frontRectH)
##    if newCoordinates:
##        targetX = randint(frontRectX,frontRectX+frontRectW)
##        targetY = randint(frontRectY,frontRectY+frontRectH)
##        print("7")
##        newCoordinates = False

    targetX = frontRectX+10
    targetY = frontRectY+10

##    print(targetX)
##    print(newCursorX)
    for i in range(0,len(bullet)):
        pass
        #bullet[i].draw(screen,shootCursorX[i],shootCursorY[i])
    
    for i in range(0,len(shootCursorX)):
        shootCursorX[i] -=cursorX
        shootCursorY[i] -=cursorY
        #print(shootCursorX,shootCursorY)

    for i in range(int(bottomLeftEndY),bottomLeftStartY):
            shadow = (255,0,0)
            pygame.draw.line(screen, shadow, (bottomLeftStartX+((bottomLeftEndX-bottomLeftStartX)*(i/(bottomLeftEndY))),i), (bottomRightStartX-(bottomRightStartX-bottomRightEndX)*(i/(bottomRightEndY)),i), 1)

    for i in range(topLeftStartY,int(topLeftEndY)):
        shadowR = 255-(i*0.1)
        if(shadowR<=0):
            shadow = (0,0,0)
        else:
            shadow = (shadowR,255-(i*0.1),255-(i*0.1))
        
        pygame.draw.line(screen, shadow, (topLeftStartX+((topLeftEndX-topLeftStartX)*(i/(topLeftEndY))),i), (topRightStartX-(topRightStartX-topRightEndX)*(i/(topRightEndY)),i), 1)

    pygame.draw.line(screen, (0,0,0), (topLeftStartX, topLeftStartY) , (topLeftEndX, topLeftEndY), 1)

    
    pygame.draw.line(screen, (0,0,0), (topRightStartX, topRightStartY) , (topRightEndX, topRightEndY), 1)
    
    
    pygame.draw.line(screen, (0,0,0), (bottomRightStartX, bottomRightStartY) , (bottomRightEndX, bottomRightEndY), 1)
    
    
    pygame.draw.line(screen, (0,0,0), (bottomLeftStartX, bottomLeftStartY) , (bottomLeftEndX, bottomLeftEndY), 1)

    
    pygame.draw.rect(screen, (0,0,0), (frontRectX, frontRectY, frontRectW, frontRectH), 1)

##    target1 = pygame.image.load("bullseye.png")
##    target1 = pygame.transform.scale(target1, (targetW,targetH))
##    screen.blit(target1, (frontRectX, frontRectY))
##
##    target2 = pygame.image.load("bullseye.png")
##    target2 = pygame.transform.scale(target2, (targetW,targetH))
##    screen.blit(target2, (frontRectX+frontRectW-targetW, frontRectY))

##    target1 = pygame.image.load("bullseye.png")
##    target1 = pygame.transform.scale(target1, (targetW,targetH))
##    screen.blit(target1, (targetX, targetY))

    pygame.draw.circle(screen, (255,0,0),(int(targetX),int(targetY)),10,0)

    screen.blit(crosshair,((WIDTH/2)-(25/2),(HEIGHT/2)-(25/2)))
    #screen.blit(ak,(800-(706/2),600-(444/2)))
    if(reloading==False):
        screen.blit(reload[0],(100,200))
    elif(reloading==True and magazine>0 and bullets<30):
        screen.blit(reload[currentFrame],(100,200))
        if(frameCount%2==0):
            currentFrame+=1
        if(currentFrame>=43):
            currentFrame = 1
            reloading = False
            if(magazine>=30):
                addBullets = 30-bullets
                bullets+=addBullets
                magazine-=addBullets
            else:
                bullets+=magazine
                magazine = 0
    else:
        reloading = False

##    for i in range(HEIGHT-50,HEIGHT):
##        shadeR = 255-(i*0.1)
##        if(shadeR<=0):
##            shade = (0,0,0)
##        else:
##            shade = (shadeR,255-(i*0.1),255-(i*0.1))
##        pygame.draw.line(screen, shade, (0,i), (WIDTH,i), 1)
    #screen.blit(bottomStrip,(0,550))

    bulletCount = bulletsCountFont.render(str(bullets),1,(0,0,0))
    screen.blit(bulletCount,(WIDTH-85,HEIGHT-35))
    magazineCount = magazineCountFont.render("/ "+str(magazine),1,(0,0,0))
    screen.blit(magazineCount,(WIDTH-50,HEIGHT-30))
    
    pygame.display.update()

inPlay = True

while inPlay:

    backwards = 5
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False
            if event.key == pygame.K_UP or event.key==pygame.K_w:
                forward = True
            elif event.key == pygame.K_DOWN or event.key==pygame.K_s:
                backward = True
            elif event.key == pygame.K_LEFT or event.key==pygame.K_a:
                left = True
            elif event.key == pygame.K_RIGHT or event.key==pygame.K_d:
                right = True
            elif event.key == pygame.K_LSHIFT or event.key==pygame.K_RSHIFT:
                pass
##                crouch = True
##                disty-=30
##                topLeftStartY-=30
##                topRightStartY-=30
##                bottomLeftStartY-=30
##                bottomRightStartY-=30
            elif event.key == pygame.K_r and bullets<30:
                reloading = True
            elif event.key == pygame.K_RETURN and start==False:
                start = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key==pygame.K_w:
                forward = False
            elif event.key == pygame.K_DOWN or event.key==pygame.K_s:
                backward = False
            elif event.key == pygame.K_LEFT or event.key==pygame.K_a:
                left = False
            elif event.key == pygame.K_RIGHT or event.key==pygame.K_d:
                right = False
            elif event.key == pygame.K_LSHIFT or event.key==pygame.K_RSHIFT:
                pass
##                crouch = False
##                disty+=30
##                topLeftStartY+=30
##                topRightStartY+=30
##                bottomLeftStartY+=30
##                bottomRightStartY+=30

        if event.type == pygame.MOUSEBUTTONDOWN and reloading==False:
            shoot = True
        elif event.type == pygame.MOUSEBUTTONUP:
            shoot = False
            if(bullets<=0):
                reloading = True

    (newCursorX,newCursorY)=pygame.mouse.get_pos()
        
    cursorX -= WIDTH/2-newCursorX
    cursorY -= HEIGHT/2-newCursorY
    pygame.mouse.set_pos((WIDTH/2,HEIGHT/2))

    if forward:
        frontRectW+=5
        frontRectH+=2.5
        distx-=2.5
        disty-=1.25
        targetW+=2
        targetH+=2

    if backward and frontRectW>100:
    #if backward:
##        frontRectW-=5
##        frontRectH-=2.5
##        distx+=2.5
##        disty+=1.25
##        targetW-=2
##        targetH-=2
        frontRectW-=backwards
        frontRectH-=backwards/2
        distx+=backwards/2
        disty+=backwards/4
        targetW-=backwards/2
        targetH-=backwards/2

    if left:
        distx+=5
        topLeftStartX+=5
        topRightStartX+=5
        bottomLeftStartX+=5
        bottomRightStartX+=5

    if right:
        distx-=5
        topLeftStartX-=5
        topRightStartX-=5
        bottomLeftStartX-=5
        bottomRightStartX-=5

    if shoot:
##        target1 = pygame.image.load("bullseye.png")
##        target1 = pygame.transform.scale(target1, (targetW,targetH))
##        screen.blit(target1, (frontRectX, frontRectY))
##
##        target2 = pygame.image.load("bullseye.png")
##        target2 = pygame.transform.scale(target2, (targetW,targetH))
##        screen.blit(target2, (frontRectX+frontRectW-targetW, frontRectY))
        
        #if(bullets>0):
        print(newCursorX,frontRectX)
        if(frontRectX>newCursorX):
            #if((newCursorX >= targetX+5 and newCursorX <= targetX-5) and (newCursorY >= targetY+5 and newCursorY <= targetY-5)):
            print("hit")
##            print("7")
        bullets-=1
        #else:
            #pass
        
##        (newCursorX,newCursorY)=pygame.mouse.get_pos()
##        distancex = 445
##        distancey = 295
##
##        shootCursorX.append(distancex)
##        shootCursorY.append(distancey)
        #print(shootCursorX,shootCursorY)
##        bullet.append(Bullet(shootCursorX[len(shootCursorX)-1],shootCursorY[len(shootCursorY)-1]))
        
        #(newCursorX,newCursorY)=pygame.mouse.get_pos()
##        shootCursorX.append(-newCursorX)
##        shootCursorY.append(-newCursorY)
##        distx = frontRectX-newCursorX
##        disty = frontRectY-newCursorY
##        
##        shootCursorX.append(frontRectX-newCursorX)
##        shootCursorY.append(frontRectY-newCursorY)
##
##        bulletVisible[len(bulletVisible)-1] = True
##
##        print(shootCursorX,shootCursorY)
##        bullet.append(Bullet(shootCursorX[len(shootCursorX)-1],shootCursorY[len(shootCursorY)-1]))

    pygame.display.update()
    
    frameCount+=1
        
    if(start==True):
        redrawScreen()
    else:
        startScreennnnnn()
pygame.quit()
