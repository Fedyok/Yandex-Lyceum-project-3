#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import os


PLATFORM_COLOR = "#FF6262"

ICON_DIR = os.path.dirname(__file__)  # полный путь к каталогу с файлами

class Platform(sprite.Sprite):  #класс боковых стенок
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((32, 32))
        self.image.fill(Color("green"))
        self.image = image.load("%s/data/wall.png" % ICON_DIR)
        self.rect = Rect(x, y, 32, 32)
        

class Finish(Platform):  #класс платформ, по которым мы прыгаем
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((57, 15))
        self.image.fill(Color("#FF6262"))
        self.image = image.load("%s/data/platform1.png" % ICON_DIR)
        self.rect = Rect(x, y, 57, 15)



class Stop(Platform):  # класс финиша
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("%s/data/finish-flag.png" % ICON_DIR)


class Dimonster(sprite.Sprite):  # класс движущегося монстра
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((32, 32))
        self.image.fill(Color("#FF6262"))
        self.rect = Rect(x, y, 32, 32)
        self.image = image.load("%s/data/mmm.png" % ICON_DIR)
        self.xvel = 1    # скорость перемещения.
        self.startX = x  # начальная позиция Х
        self.startY = y
        self.max_len = 20

    def update(self):

        self.rect.x += self.xvel
        if abs(self.startX - self.rect.x) > self.max_len:
            self.xvel = -self.xvel



class Arrow(sprite.Sprite):  # класс пули персонажа
    def __init__(self, x, y):

        sprite.Sprite.__init__(self)
        self.image = Surface((32, 32))
        self.image.fill(Color("#FF6262"))
        self.rect = Rect(x, y, 32, 32)
        self.image = image.load("%s/data/arrow.png" % ICON_DIR)
        self.startX = -10  # начальная позиция Х
        self.startY = -10
        self.max_len = 300  # максимальное расстояние, на которое она может лететь
        self.push = False

    def update(self, starthero, platforms):
        self.rect.y -= 5
        a = 1
        a = self.collide(platforms)
        if abs(starthero - self.rect.y) > self.max_len:
            self.yvel = self.startY
            self.xvel = self.startX
            self.push = False
        return a
    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if isinstance(p, Dimonster):
                    self.push = False
                    return 0  # при столкновении с монстром возвращает 0
                else:
                    return 1  # иначе 1
