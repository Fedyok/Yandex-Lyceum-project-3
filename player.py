#!/usr/bin/env python
# -*- coding: utf-8 -*-

# импорт всего нужного
from pygame import *
import pyganim
import os
import blocks
import doodle
import pygame


COLOR =  "#888888"

ICON_DIR = os.path.dirname(__file__)

ANIMATION_RIGHT = [('%s/data/doodle1.png' % ICON_DIR)]
ANIMATION_LEFT = [('%s/data/doodle.png' % ICON_DIR)]
ANIMATION_JUMP_LEFT = [('%s/data/jj.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP_RIGHT = [('%s/data/jj.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP = [('%s/data/jj.png' % ICON_DIR, 0.1)]
ANIMATION_STAY = [('%s/data/doodle.png' % ICON_DIR, 0.1)]


class Player(sprite.Sprite):  # класс игрока(персонажа)
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.winner = False
        self.life = 3
        self.die = False
        self.points = 0
        self.speed = 0.0000000000005
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.yvel = 0
        self.onGround = False
        self.image = Surface((32, 32))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, 32, 32)
        self.image.set_colorkey(Color(COLOR))
#        Анимация движения вправо
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, 0.1))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
#        Анимация движения влево        
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, 0.1))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        
        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))  # По-умолчанию, стоим
        
        self.boltAnimJumpLeft= pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()
        
        self.boltAnimJumpRight= pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()
        
        self.boltAnimJump= pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()

    def update(self, left, right, up, shoot, platforms):

        if up:
            if self.onGround:
                self.yvel = -10
            self.image.fill(Color(COLOR))
            self.boltAnimJump.blit(self.image, (0, 0))

        if left:
            self.xvel = -7  # Лево
            self.image.fill(Color(COLOR))
            if up:
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))

        if right:
            self.xvel = 7  # Право = x + n
            self.image.fill(Color(COLOR))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))

        if not(left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
            if not up:
                self.image.fill(Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))

        if not self.onGround:
            self.yvel +=  0.35

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p): # если есть пересечение платформы с игроком

                if xvel > 0:                      # если движется вправо
                    self.rect.right = p.rect.left

                if xvel < 0:                      # если движется влево
                    self.rect.left = p.rect.right

                if yvel > 0:                      # если падает вниз
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0

                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
                    
                if isinstance(p, blocks.Stop):
                    try:
                        self.winner = True
                        self.life += 1
                        self.retry()
                    except Exception as e:
                        print(e)

                    
                if isinstance(p, blocks.Dimonster):
                    self.die = True
       
    def retry(self):
        time.wait(500)
        self.rect.x = self.startX
        self.rect.y = self.startY
        self.life -= 1
