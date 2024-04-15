import pygame
from pygame.locals import *
import os
import random
import sys
import math

pygame.init()

W, H = 800, 447
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Side Scroller')

bg = pygame.image.load('bg.png').convert()
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()

class player(object):
    run = [pygame.image.load("8.png"),
           pygame.image.load("9.png"),
           pygame.image.load("10.png"),
           pygame.image.load("11.png"),
           pygame.image.load("12.png"),
           pygame.image.load("13.png"),
           pygame.image.load("14.png"),
           pygame.image.load("15.png")] 
    
    jump = [pygame.image.load("1.png"),
            pygame.image.load("2.png"),
            pygame.image.load("3.png"),
            pygame.image.load("4.png"),
            pygame.image.load("5.png"),
            pygame.image.load("6.png"),
            pygame.image.load("7.png")]
    
    slide = [pygame.image.load("S1.png"),
             pygame.image.load("S2.png"),
             pygame.image.load("S2.png"),
             pygame.image.load("S2.png"),
             pygame.image.load("S2.png"),
             pygame.image.load("S2.png"),
             pygame.image.load("S2.png"),
             pygame.image.load("S2.png"),
             pygame.image.load("S3.png"),
             pygame.image.load("S4.png"),
             pygame.image.load("S5.png")]
    
    jumpList =[1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,
               4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
               0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,
               -2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
    
    fall = pygame.image.load("0.png")
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False
        self.falling = False  # NEW - Khởi tạo thuộc tính falling

    def draw(self, win):
        if self.falling:  # NEW - Kiểm tra trạng thái rơi
            win.blit(self.fall, (self.x, self.y + 30))  # NEW - Hiển thị ảnh rơi
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.3
            win.blit(self.jump[self.jumpCount // 18], (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)  # NEW
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
                self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)  # NEW
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            # NEW ELIF STATEMENT
            elif self.slideCount > 20 and self.slideCount < 80:
                self.hitbox = (self.x, self.y + 3, self.width - 8, self.height - 35)  # NEW
            if self.slideCount >= 110:
                self.slideCount = 0
                self.runCount = 0
                self.slideUp = False
                self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)  # NEW
            win.blit(self.slide[self.slideCount // 10], (self.x, self.y))
            self.slideCount += 1
        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount // 6], (self.x, self.y))
            self.runCount += 1
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 13)  # NEW
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # NEW - Vẽ vùng va chạm (màu đỏ)

class saw(object):
    rotate = [pygame.image.load('SAW0.PNG'),pygame.image.load('SAW1.PNG'),pygame.image.load('SAW2.PNG'),pygame.image.load('SAW3.PNG')]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotateCount = 0
        self.vel = 1.4  # Tốc độ di chuyển

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self.height - 5)  # Vùng va chạm chính xác cho nhân vật
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # Vẽ vùng va chạm
        if self.rotateCount >= 8:
            self.rotateCount = 0
        win.blit(pygame.transform.scale(self.rotate[self.rotateCount // 2], (64, 64)), (self.x, self.y))
        self.rotateCount += 1

    def collide(self, runner):
        #Xác định xem hình chữ nhật va chạm có chồng lên nhau không
        if runner.hitbox[1] < self.hitbox[1] + self.hitbox[3] and runner.hitbox[1] + runner.hitbox[3] > self.hitbox[1]:
            if runner.hitbox[0] + runner.hitbox[2] > self.hitbox[0] and runner.hitbox[0] < self.hitbox[0] + self.hitbox[2]:
                return True
        return False

class saw2(object):
    rotate = [
        pygame.image.load('SAW0.PNG'),
        pygame.image.load('SAW1.PNG'),
        pygame.image.load('SAW2.PNG'),
        pygame.image.load('SAW3.PNG')
        ]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotateCount = 0
        self.vel = 1.4

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self.height - 5)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        if self.rotateCount >= 8:
            self.rotateCount = 0
        win.blit(pygame.transform.scale(self.rotate[self.rotateCount // 2], (64, 64)), (self.x, self.y))
        self.rotateCount += 1

    def collide(self, runner):
        if runner.hitbox[1] < self.hitbox[1] + self.hitbox[3] and runner.hitbox[1] + runner.hitbox[3] > self.hitbox[1]:
            if runner.hitbox[0] + runner.hitbox[2] > self.hitbox[0] and runner.hitbox[0] < self.hitbox[0] + self.hitbox[2]:
                return True
        return False

def redrawWindow():
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    runner.draw(win)
    for obj in objects:
        obj.draw(win)
    pygame.display.update()

def updateFile():
    #Ghi điểm vào file
    f = open('scores.txt','r')
    file = f.readlines()
    last = int(file[0])

    if last < int(score):
        f.close()
        file = open('scores.txt', 'w')
        file.write(str(score))
        file.close()

        return score
    return last

def endScreen():
    #Màn hình kết thúc game
    global pause, score, speed, objects
    pause = 0
    speed = 30
    objects = []

    #Text
    run = True
    while run:
        pygame.time.delay(100)
        win.blit(bg, (0,0))
        largeFont = pygame.font.SysFont('comicsans', 80)
        previousScore = largeFont.render('Best Score: ' + str(updateFile()),1,(255,255,255))
        win.blit(previousScore, (W/2 - previousScore.get_width()/2, 150))
        newScore = largeFont.render('Your Score: ' + str(score),1,(255,255,255))
        win.blit(newScore, (W/2 - newScore.get_width()/2, 240))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()



runner = player(200, 313, 64, 64)
objects = []
speed = 30
score = 0

# MAIN
run = True
pause = 0
fallSpeed = 0
while run:
    if pause > 0:
        pause += 1
        if pause > fallSpeed * 2:
            endScreen()

    score = speed // 10 - 3  # Điểm số dựa trên tốc độ

    for obj in objects:
        if obj.collide(runner):
            runner.falling = True
            if pause == 0:
                pause = 1
                fallSpeed = speed
        obj.x -= 1.4  # Điều chỉnh tốc độ chạy của vật thể
        if obj.x < obj.width * -1:  # Kiểm tra xem vật thể có ra khỏi màn hình không
            objects.pop(objects.index(obj))

    bgX -= 1.4
    bgX2 -= 1.4

    if bgX < bg.get_width() * -1:  # Lặp lại hình nền
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        if not (runner.jumping):
            runner.jumping = True

    if keys[pygame.K_DOWN]:
        if not (runner.sliding):
            runner.sliding = True

    clock.tick(speed)  # Cài đặt tốc độ khung hình

    # Tạo vật thể
    if len(objects) == 0:
        if random.randint(0, 2) == 0:
            objects.append(saw(810, 310, 64, 64))
        elif random.randint(0, 2) == 1:
            objects.append(saw2(810, 310, 64, 64))

    redrawWindow()

pygame.quit()