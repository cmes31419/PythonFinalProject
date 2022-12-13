import sys

import pygame
from pygame.locals import QUIT

import math
import random

FPS = 60
WHITE = (255, 255, 255)
WIDTH = 800
HEIGHT = 600

# 初始化
pygame.init()
# 建立視窗，大小為 800x600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# 設置視窗標題(遊戲名稱)
pygame.display.set_caption('ion')
clock = pygame.time.Clock()
screen.fill(WHITE)  # 清除畫面並填滿白色(顏色可查RGB配色表)

class Ion(pygame.sprite.Sprite):
    def __init__(self, width=100, height=100, random_x=0, random_y=0):
        super().__init__()
        random_x, random_y = random.randint(width, WIDTH-width), random.randint(height, HEIGHT-height)
        # 載入圖片
        self.raw_image = pygame.image.load('round1.png').convert_alpha()
        # 縮小圖片
        self.image = pygame.transform.scale(self.raw_image, (width, height))
        # 定位
        self.rect = self.image.get_rect()
        self.rect.center = (random_x, random_y)
        
        # 初速30，隨機方向，加速度為速度*(-0.03)
        self.direction = random.uniform(0, 2*math.pi)
        self.speedx = 30*math.cos(self.direction)
        self.speedy = 30*math.sin(self.direction)
        self.accelerationx = -self.speedx*0.03
        self.accelerationy = -self.speedy*0.03

        # 圖片長寬
        self.width = width
        self.height = height

    def update(self):
        # 若超出邊界則視為撞牆
        if self.rect.right >= WIDTH and self.speedx >= 0:
            self.speedx = -self.speedx
            self.accelerationx = -self.accelerationx
        if self.rect.left <= 0 and self.speedx <= 0:
            self.speedx = -self.speedx
            self.accelerationx = -self.accelerationx
        if self.rect.top <= 0 and self.speedy < 0:
            self.speedy = -self.speedy
            self.accelerationy = -self.accelerationy
        if self.rect.bottom >= HEIGHT and self.speedy > 0:
            self.speedy = -self.speedy
            self.accelerationy = -self.accelerationy
        
        # 存之前的速度
        pre_speedx = self.speedx
        pre_speedy = self.speedy

        # 更新改變位置與速度
        self.rect.x += self.speedx
        self.speedx += self.accelerationx
        self.rect.y += self.speedy
        self.speedy += self.accelerationy 

        # 判斷是否停下(速度歸零或變號)
        if self.speedx == 0 or pre_speedx/self.speedx < 0:
            self.speedx = 0
            self.accelerationx = 0
        if self.speedy == 0 or pre_speedy/self.speedy < 0:
            self.speedy = 0
            self.accelerationy = 0
        

all_sprites = pygame.sprite.Group()
ion = Ion()
all_sprites.add(ion)

# 更新畫面，等所有操作完成後一次更新
pygame.display.update()

# 事件處理
while True:
    clock.tick(FPS)  #一秒內最多執行FPS次
    for event in pygame.event.get():
        # 當使用者結束視窗，程式也結束
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:  # 按P遊戲畫面截圖
            pygame.image.save(screen, "ion.png")
    # 更新遊戲
    all_sprites.update()
    # 畫面顯示
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.update()